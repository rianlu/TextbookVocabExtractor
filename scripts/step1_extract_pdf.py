import fitz
import re
import os
import json
import glob
from typing import List, Dict

LIGATURE_MAP = {
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "ﬀ": "ff",
    "ﬅ": "ft",
    "ﬆ": "st",
}


def normalize_ligatures(text: str) -> str:
    for src, dst in LIGATURE_MAP.items():
        text = text.replace(src, dst)
    return text


def load_config(file_path):
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", file_path)
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

BOOK_CONFIGS = load_config("book_configs.json")
MANUAL_RANGES = BOOK_CONFIGS.get("manual_ranges", {})


class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.vocab_pages = []
        # 保存书名（不含路径和扩展名），用于分书音标处理
        self.book_name = os.path.basename(pdf_path).replace('.pdf', '')

    def set_manual_range(self, start_idx: int, end_idx: int):
        """Set a manual page range (0-indexed)."""
        self.vocab_pages = list(range(start_idx, end_idx))
        print(f"  Manual Range Set: Index {start_idx} to {end_idx}")

    def detect_vocab_sections(self) -> List[int]:
        # Keep this for books not in the manual list
        if self.vocab_pages:
            return self.vocab_pages
            
        total_pages = len(self.doc)
        start_marker_pages = []
        end_marker_pages = []
        
        search_range = range(max(0, total_pages - 80), total_pages)
        for i in search_range:
            text = self.doc[i].get_text("text")
            clean_text = re.sub(r'\s+', '', text).lower()
            if 'wordsandexpressions' in clean_text:
                start_marker_pages.append(i)
            if 'propernouns' in clean_text or 'propernames' in clean_text:
                end_marker_pages.append(i)
        
        final_start = -1
        final_end = -1
        if end_marker_pages:
            final_end = end_marker_pages[-1]
            for s in reversed(start_marker_pages):
                if s < final_end:
                    final_start = s
                    break
        
        if final_start != -1:
            self.vocab_pages = list(range(final_start, final_end))
        return self.vocab_pages

    def extract_words(self) -> Dict[str, List[str]]:
        if not self.vocab_pages:
            self.detect_vocab_sections()
            
        unit_mapping = {}
        current_unit = "General"
        pending_broken_phonetic = False
        
        for p in self.vocab_pages:
            page = self.doc[p]
            mid_x = page.rect.width / 2
            
            blocks = page.get_text("blocks")
            text_blocks = [b for b in blocks if b[6] == 0]
            
            # Sort columns
            left_col = sorted([b for b in text_blocks if b[0] < mid_x], key=lambda b: b[1])
            right_col = sorted([b for b in text_blocks if b[0] >= mid_x], key=lambda b: b[1])
            ordered_blocks = left_col + right_col
            
            for b in ordered_blocks:
                block_text = b[4]
                lines = block_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line: continue

                    # Normalize curly apostrophes to keep phrases like sb's intact.
                    line = line.replace('’', "'").replace('‘', "'").replace('‛', "'")
                    # Normalize common PDF ligatures, e.g. surﬁng -> surfing.
                    line = normalize_ligatures(line)
                    
                    # 移除所有不可见控制字符，但保留 PUA 字符（U+E000-U+F8FF）
                    line = "".join(ch for ch in line if ch.isprintable() or 0xE000 <= ord(ch) <= 0xF8FF)
                    line = line.strip()
                    if not line: continue
                    
                    clean_line_flat = re.sub(r'\s+', '', line).upper()
                    
                    # Skip navigation headers
                    if any(hn in clean_line_flat for hn in ["WORDSANDEXPRESSIONS", "PROPERNOUNS", "PROPERNAMES"]):
                        if len(clean_line_flat) < 35:
                            continue

                    # Handle broken phonetic lines, e.g.:
                    #   November /n...
                    #   vemb.../ n. 11月
                    # The second line is a phonetic tail, not a standalone word.
                    open_phonetic_line = re.match(r"^\s*([A-Za-z][A-Za-z\s'’\.\-]*)\s*/[^/]*$", line)
                    if open_phonetic_line:
                        word = open_phonetic_line.group(1).strip()
                        if word:
                            self._add_word_to_mapping(word, current_unit, unit_mapping)
                        pending_broken_phonetic = True
                        continue

                    if pending_broken_phonetic:
                        tail_line = re.match(r"^\s*[A-Za-z][A-Za-z'’\.\-]*[^/]*\/\s*(?:[a-z]{1,6}\.)", line, re.I)
                        pending_broken_phonetic = False
                        if tail_line:
                            continue

                    # Robust Unit Detection
                    is_unit = False
                    # 识别 Unit, Module, Starter
                    if clean_line_flat.startswith('UNIT') or clean_line_flat.startswith('MODULE'):
                        is_unit = True
                    elif clean_line_flat.startswith('REVISIONMODULE'):
                        is_unit = True
                    elif clean_line_flat == 'STARTER':
                        is_unit = True
                    elif re.match(r'^(STARTER|UNIT|MODULE|REVISIONMODULE)\s*[A-Z\d]+', line, re.I):
                        is_unit = True

                    if is_unit:
                        clean_unit = re.sub(r'\s+', ' ', line).strip().title()
                        # 特殊处理 Revision Module A -> Revision Module A (不缩减空格)
                        if "Revision" in clean_unit:
                            clean_unit = re.sub(r'Revision\s*Module\s*([A-Z])', r'Revision Module \1', clean_unit, flags=re.I)
                        elif len(clean_unit) > 1 and clean_unit[1] == ' ':
                            clean_unit = re.sub(r'\s+', '', clean_unit).title()
                        
                        if any(kw in clean_unit for kw in ["Unit", "Module", "Starter", "Revision"]):
                            # Always follow document order; the PDF vocabulary list is already
                            # arranged by unit sequence, and revision modules can appear between
                            # regular modules (e.g. Module 5 -> Revision Module A -> Module 6).
                            current_unit = clean_unit
                            continue
                    
                    # Word and phonetic boundary detection
                    # 允许行首有星号、点、圆点或其他标记，以及空白字符
                    # 1. Try to match word + phonetic pattern (we ignore phonetic content)
                    wp_match = re.search(r'^\s*[\*\•\.]?\s*([a-zA-Z\s\-\'\.]+?)\s*[\/\[]([^\/\]]+)[\/\]](.*)', line)
                    if wp_match:
                        word = wp_match.group(1).strip()
                        # PIVOT: Discard PDF phonetics due to unreliability.
                        remaining = wp_match.group(3).strip()
                        
                        # 特殊逻辑：支持同一行中有后续短语（如 lot /lɒt/ a lot of）
                        # 尝试在剩余部分中寻找纯单词或短语
                        if remaining:
                            # 过滤掉常见的页码（如括号里的数字 (14)）
                            clean_remaining = re.sub(r'\(?\d+\)?', '', remaining).strip()
                            if clean_remaining and len(clean_remaining) > 1:
                                # 将该行视为两个词条处理（递归调用或手动添加）
                                # 为了保持简单，我们先添加主词条，再添加剩余部分作为无音标词条
                                self._add_word_to_mapping(word, current_unit, unit_mapping)
                                word = clean_remaining
                    else:
                        # 2. Fallback to just word detection (support for indented phrases)
                        # 增加限制：如果紧跟中文，可能不是单词而是释义行（如 "v. 微笑"）
                        # 检查是否以词性缩写开头且后面跟着非英文内容
                        pos_with_trans = re.match(r'^\s*([a-z]{1,6}\.)\s*([^\x00-\x7F]+)', line)
                        if pos_with_trans:
                            continue

                        word_match = re.search(r'^\s*[\*\•\.]?\s*([a-zA-Z\s\-\'\.]+)', line)
                        if word_match:
                            word = word_match.group(1).strip()
                        else:
                            continue # Not a word line
                    if word:
                        self._add_word_to_mapping(word, current_unit, unit_mapping)
                                
        self.doc.close()
        return unit_mapping

    def _add_word_to_mapping(self, word: str, current_unit: str, unit_mapping: dict):
        # 移除末尾可能的页码标记（如 any (14)）
        word = re.sub(r'\s+\(?\d+\)?$', '', word).strip()
        if not word: return

        # 过滤逻辑
        # 移除末尾的点号，以便匹配 blacklist（如 "v." -> "v"）
        w_lower = word.lower().rstrip('.')
        # 1. 词性缩写黑名单 (仅保留纯粹的词性简称)
        blacklist = {
            'adj', 'adv', 'pron', 'num', 'v', 'n', 'prep', 'art', 'conj', 'interj'
        }
        if w_lower in blacklist:
            return
            
        # 2. 只有大写字母且长度较长的通常是页眉（如 WORDS AND EXPRESSIONS）
        if word.isupper() and len(word) > 10:
            return

        if len(word) > 1 or word.lower() in ['a', 'i']:
            if current_unit not in unit_mapping:
                unit_mapping[current_unit] = []
            if word not in unit_mapping[current_unit]:
                unit_mapping[current_unit].append(word)

def main():
    input_dir = "textbook"
    inter_dir = "intermediate"
    os.makedirs(inter_dir, exist_ok=True)
    
    # MANUAL CONFIGURATION (Loaded from book_configs.json)
    
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

    all_unit_mappings = {}
    global_words = set()
    
    for pdf_path in pdf_files:
        book_name = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"Processing: {book_name}")
        extractor = PDFExtractor(pdf_path)
        
        if book_name in MANUAL_RANGES:
            start, end = MANUAL_RANGES[book_name]
            extractor.set_manual_range(start, end)

        
        mapping = extractor.extract_words()
        all_unit_mappings[book_name] = mapping
        
        for words in mapping.values():
            global_words.update(words)
            
        # Per book output dir
        book_output_dir = os.path.join("output", "教材分类", book_name)
        os.makedirs(book_output_dir, exist_ok=True)
        
    # Save Unit Mappings
    with open(os.path.join(inter_dir, "unit_mapping.json"), "w", encoding="utf-8") as f:
        json.dump(all_unit_mappings, f, ensure_ascii=False, indent=2)
        
    # Save Unit Mappings by Book
    book_units_dir = os.path.join(inter_dir, "book_units")
    os.makedirs(book_units_dir, exist_ok=True)
    for book_name, mapping in all_unit_mappings.items():
        with open(os.path.join(book_units_dir, f"{book_name}.json"), "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)

    # Save Words by Book (txt) - MAINTAIN ORDER
    book_words_dir = os.path.join(inter_dir, "book_words")
    os.makedirs(book_words_dir, exist_ok=True)
    for book_name, mapping in all_unit_mappings.items():
        book_words = []
        seen = set()
        for words in mapping.values():
            for w in words:
                if w not in seen:
                    book_words.append(w)
                    seen.add(w)
        
        # Save to intermediate (for internal pipeline)
        with open(os.path.join(book_words_dir, f"{book_name}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(book_words))
            
        # Save to output folder (for user) - Categorization
        book_output_dir = os.path.join("output", "教材分类", book_name)
        os.makedirs(book_output_dir, exist_ok=True)
        with open(os.path.join(book_output_dir, "unique_words.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(book_words))
        
        # Also save the unit mapping for this book in its output folder
        with open(os.path.join(book_output_dir, "unit_mapping.json"), "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        
    # Save Unique Word List (Global)
    sorted_words = sorted(list(global_words))
    with open(os.path.join(inter_dir, "unique_words.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted_words))
        
    print(f"\nFinished Step 1. Extracted units for {len(pdf_files)} books.")
    print(f"Global unique words: {len(sorted_words)}")
    print(f"Outputs saved in {inter_dir}/")

if __name__ == "__main__":
    main()
