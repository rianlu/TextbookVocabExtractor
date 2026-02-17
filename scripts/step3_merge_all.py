import json
import os
import re
from collections import Counter

POS_PRIORITY = {
    "v.": 1,
    "vt.": 2,
    "vi.": 3,
    "n.": 4,
    "adj.": 5,
    "adv.": 6,
    "prep.": 7,
    "pron.": 8,
    "conj.": 9,
    "interj.": 10,
    "aux.": 11,
    "num.": 12,
    "art.": 13,
    "pl.": 14,
    "vbl.": 15,
}
MAX_MEANING_ITEMS = 3
MAX_TRANSLATION_CHUNKS = 3

def parse_filename_info(filename: str):
    grade_map = {"七": 7, "八": 8, "九": 9}
    semester_map = {"上": 1, "下": 2}
    grade = 7
    semester = 1
    for k, v in grade_map.items():
        if k in filename: grade = v
    for k, v in semester_map.items():
        if k in filename: semester = v
    return grade, semester

def get_target_filename(grade, semester):
    grade_str = {7: "七", 8: "八", 9: "九"}[grade]
    semester_str = {1: "上", 2: "下"}[semester]
    return f"外研版初中英语{grade_str}年级{semester_str}册.json"

def is_noisy_pdf_phonetic(phonetic):
    if not phonetic:
        return False
    # 典型的乱码包括 =$# 等，但不再将数字视为绝对噪音，因为某些映射后可能仍保留数字或已处理。
    # 同时也排除掉 PUA 字符的误判。
    return bool(re.search(r"[=\$\#\u0400-\u04FF]", phonetic))


def normalize_pdf_phonetic(phonetic):
    if not phonetic:
        return ""
    p = phonetic.strip()
    # Some textbooks extract "ɒ" as "=" (e.g. on /=n/).
    p = p.replace("=", "ɒ")
    return p

def select_best_pdf_phonetic(book_phonetic, global_phonetic):
    b = normalize_pdf_phonetic(book_phonetic)
    g = normalize_pdf_phonetic(global_phonetic)
    if not b and not g:
        return ""
    if b and g:
        b_noisy = is_noisy_pdf_phonetic(b)
        g_noisy = is_noisy_pdf_phonetic(g)
        if b_noisy and not g_noisy:
            return g
        if g_noisy and not b_noisy:
            return b
        # Both clean or both noisy: keep book-level to preserve textbook consistency.
        return b
    return b or g

def format_phonetic(word, book_pdf_phonetics, global_pdf_phonetics):
    phonetic = select_best_pdf_phonetic(
        book_pdf_phonetics.get(word, ""),
        global_pdf_phonetics.get(word, "")
    )
    if phonetic:
        return f"[{phonetic}]"
    return ""

def clean_meaning_text(text):
    if not text: return ""
    # Remove any letters followed by a dot (like n., v., adj.) at the beginning
    text = re.sub(r'^[a-z]+\.\s?', '', text)
    # Remove numeric weights like ":100" or "/v:75"
    text = re.sub(r'\/?[a-z]+:\d+', '', text)
    # Remove remaining slashes and multiple spaces
    text = text.replace('/', ' ').strip()
    return re.sub(r'\s+', ' ', text)

def normalize_pos(pos):
    if not pos:
        return ""
    p = pos.strip().lower().replace(" ", "")
    p = p.rstrip(".")
    mapping = {
        "a": "adj.",
        "adj": "adj.",
        "n": "n.",
        "v": "v.",
        "vt": "vt.",
        "vi": "vi.",
        "adv": "adv.",
        "prep": "prep.",
        "pron": "pron.",
        "conj": "conj.",
        "interj": "interj.",
        "int": "interj.",
        "aux": "aux.",
        "num": "num.",
        "art": "art.",
        "pl": "pl.",
        "vbl": "vbl.",
        "na": "na.",
    }
    if p in mapping:
        return mapping[p]
    return ""

def normalize_translation(raw_text):
    if not raw_text:
        return ""
    text = raw_text.strip()
    # Remove leading domain tags like [计], [法], [网络]
    text = re.sub(r'^(?:\[[^\]]+\]\s*)+', '', text)
    text = clean_meaning_text(text)
    return text.strip("；;，, ")

def shorten_translation(text):
    if not text:
        return ""
    chunks = [c.strip() for c in re.split(r'[，,、；;]', text) if c.strip()]
    if not chunks:
        return text

    selected = []
    for c in chunks:
        if c not in selected:
            selected.append(c)
        if len(selected) >= MAX_TRANSLATION_CHUNKS:
            break
    return "、".join(selected)

def is_plausible_english_term(word):
    if not word:
        return False
    if not re.fullmatch(r"[A-Za-z][A-Za-z\s\-\.'’]*", word):
        return False

    tokens = [t.strip(".'").lower() for t in word.split() if t.strip(".'")]
    if not tokens:
        return False

    pos_like = {
        'adj', 'adv', 'pron', 'num', 'v', 'n', 'prep', 'art', 'conj', 'interj',
        'vt', 'vi', 'aux', 'int', 'pl', 'vbl', 'na', 'sb', 'sth'
    }
    if all(t in pos_like for t in tokens):
        return False

    return True

def format_merged_meaning(ed):
    meanings = ed.get("meanings", [])
    if not meanings:
        return ""

    pos_to_trans = {}
    no_pos_trans = []

    for m in meanings:
        pos = normalize_pos(m.get("pos", ""))
        trans = shorten_translation(normalize_translation(m.get("translation", "")))
        if not trans:
            continue

        if pos:
            if pos not in pos_to_trans:
                pos_to_trans[pos] = []
            if trans not in pos_to_trans[pos]:
                pos_to_trans[pos].append(trans)
        else:
            if trans not in no_pos_trans:
                no_pos_trans.append(trans)

    parts = []
    ordered_pos = sorted(pos_to_trans.keys(), key=lambda p: (POS_PRIORITY.get(p, 99), p))
    for p in ordered_pos:
        parts.append(f"{p} {pos_to_trans[p][0]}")
    parts.extend(no_pos_trans)

    if not parts:
        return ""
    # Keep concise but preserve multi-POS information.
    return "；".join(parts[:MAX_MEANING_ITEMS])

def merge():
    inter_dir = "intermediate"
    unit_mapping_path = os.path.join(inter_dir, "unit_mapping.json")
    ecdict_data_path = os.path.join(inter_dir, "ecdict_data.json")
    ai_data_path = os.path.join(inter_dir, "ai_data.json")
    phonetics_path = os.path.join(inter_dir, "word_phonetics.json")
    
    if not os.path.exists(unit_mapping_path) or not os.path.exists(ecdict_data_path):
        print("Error: Missing intermediate files.")
        return
        
    with open(unit_mapping_path, "r", encoding="utf-8") as f:
        unit_mappings = json.load(f)
    with open(ecdict_data_path, "r", encoding="utf-8") as f:
        ecdict_data = json.load(f)
    with open(phonetics_path, "r", encoding="utf-8") as f:
        global_pdf_phonetics = json.load(f)
        
    ai_data = {}
    if os.path.exists(ai_data_path):
        with open(ai_data_path, "r", encoding="utf-8") as f:
            ai_data = json.load(f)

    report = {
        "books": {},
        "global": {
            "total_words": 0,
            "output_words": 0,
            "skipped_words": 0,
            "missing_meaning_count": 0,
            "missing_phonetic_count": 0,
            "missing_sentence_count": 0
        }
    }

    for book_name, units in unit_mappings.items():
        print(f"Merging: {book_name}")
        grade, semester = parse_filename_info(book_name)
        book_counter = Counter()
        skipped_samples = []
        book_phonetics = {}
        book_phonetics_path = os.path.join("output", "教材分类", book_name, "word_phonetics.json")
        if os.path.exists(book_phonetics_path):
            with open(book_phonetics_path, "r", encoding="utf-8") as f:
                book_phonetics = json.load(f)
        
        final_book_data = []
        for unit_name, words in units.items():
            unit_entry = {"grade": grade, "semester": semester, "unit": unit_name, "data": []}
            for word in words:
                book_counter["total_words"] += 1
                ed = ecdict_data.get(word, {})
                ad = ai_data.get(word, {})
                
                meaning = format_merged_meaning(ed)
                phonetic = format_phonetic(
                    word,
                    book_phonetics,
                    global_pdf_phonetics
                )
                
                app_sentences = ad.get("app_sentences", [{"en": f"Example sentence for {word}.", "cn": "暂无例句。"}])
                word_entry = {
                    "text": word,
                    "phonetic": phonetic,
                    "meaning": meaning,
                    "app_sentences": app_sentences
                }

                if not meaning:
                    book_counter["missing_meaning_count"] += 1
                if not phonetic:
                    book_counter["missing_phonetic_count"] += 1
                if not app_sentences:
                    book_counter["missing_sentence_count"] += 1

                # 安全兜底过滤：只有当释义完全为空，且 PDF 中也没提到音标时，才视为噪音
                if not word_entry["meaning"] and not word_entry["phonetic"]:
                    if is_plausible_english_term(word):
                        word_entry["meaning"] = "暂无释义"
                    else:
                        book_counter["skipped_words"] += 1
                        if len(skipped_samples) < 80:
                            skipped_samples.append(word)
                        continue

                book_counter["output_words"] += 1
                unit_entry["data"].append(word_entry)
            
            if unit_entry["data"]:
                final_book_data.append(unit_entry)
            
        # Save to output/合并成果 directory (no categorization subfolders here)
        merged_output_dir = os.path.join("output", "合并成果")
        os.makedirs(merged_output_dir, exist_ok=True)
        
        target_filename = os.path.join(merged_output_dir, f"{book_name}.json")
        print(f"  Saving to {target_filename}")
        
        with open(target_filename, "w", encoding="utf-8") as f:
            json.dump(final_book_data, f, ensure_ascii=False, indent=2)

        report["books"][book_name] = {
            "total_words": book_counter["total_words"],
            "output_words": book_counter["output_words"],
            "skipped_words": book_counter["skipped_words"],
            "missing_meaning_count": book_counter["missing_meaning_count"],
            "missing_phonetic_count": book_counter["missing_phonetic_count"],
            "missing_sentence_count": book_counter["missing_sentence_count"],
            "skipped_samples": skipped_samples
        }
        for k in report["global"]:
            report["global"][k] += report["books"][book_name][k]

    report_json_path = os.path.join(inter_dir, "pairing_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    lines = [
        "=== Pairing Report ===",
        f"Total words: {report['global']['total_words']}",
        f"Output words: {report['global']['output_words']}",
        f"Skipped words: {report['global']['skipped_words']}",
        f"Missing meaning: {report['global']['missing_meaning_count']}",
        f"Missing phonetic: {report['global']['missing_phonetic_count']}",
        f"Missing sentence: {report['global']['missing_sentence_count']}",
        "",
        "Per book:"
    ]
    for book_name, stats in report["books"].items():
        lines.append(
            f"- {book_name}: total={stats['total_words']}, output={stats['output_words']}, "
            f"skipped={stats['skipped_words']}, missing_meaning={stats['missing_meaning_count']}, "
            f"missing_phonetic={stats['missing_phonetic_count']}, missing_sentence={stats['missing_sentence_count']}"
        )
    report_txt_path = os.path.join(inter_dir, "pairing_report.txt")
    with open(report_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nMerge complete. Final results organized in 'output/合并成果/'.")
    print(f"Pairing report saved to: {report_json_path}")
    print(f"Pairing report summary saved to: {report_txt_path}")

if __name__ == "__main__":
    merge()
