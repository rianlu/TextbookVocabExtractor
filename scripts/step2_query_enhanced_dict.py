import csv
import json
import os
import re

class EnhancedLookup:
    def __init__(self, ecdict_path, word_csv_path, trans_csv_path):
        self.ecdict_path = ecdict_path
        self.word_csv_path = word_csv_path
        self.trans_csv_path = trans_csv_path
        self.data = {}
        self.incomplete_words = []

    def load_ecdict(self):
        print(f"Loading ECDICT from {self.ecdict_path}...")
        try:
            with open(self.ecdict_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    word = row['word'].lower()
                    raw_trans = row.get('translation', '')
                    meanings = self.parse_translation(raw_trans)
                    
                    self.data[word] = {
                        "phonetic": row.get('phonetic', ''),
                        "pos_str": row.get('pos', ''), # ECDICT's pos summary
                        "meanings": meanings,
                        "tag": row.get('tag', ''),
                        "phonetic_uk": "",
                        "phonetic_us": ""
                    }
        except Exception as e:
            print(f"Error loading ECDICT: {e}")

    def parse_translation(self, text):
        if not text: return []
        lines = re.split(r'\\n|\n', text)
        meanings = []
        seen = set()
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Match common POS markers at the start
            match = re.match(r'^([a-z]+\.?)\s*(.*)', line)
            if match:
                pos = match.group(1)
                trans = match.group(2).strip()
            elif line.startswith('[') and ']' in line:
                end_idx = line.find(']')
                pos = line[1:end_idx]
                trans = line[end_idx+1:].strip()
            else:
                pos = ""
                trans = line
            
            # Basic cleanup: remove POS markers from trans if they were missed by regex
            # e.g. "n.脑" -> "脑"
            trans = re.sub(r'^[a-z]+\.\s*', '', trans).strip()
            
            if trans:
                key = (pos, trans)
                if key not in seen:
                    meanings.append({
                        "pos": pos,
                        "translation": trans
                    })
                    seen.add(key)
        return meanings

    def load_word_translations(self):
        print(f"Loading Word Translations from {self.trans_csv_path}...")
        try:
            with open(self.trans_csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    word = row['word'].lower()
                    trans = row['translation']
                    if word in self.data:
                        new_meanings = self.parse_translation(trans)
                        existing_keys = set((m["pos"], m["translation"]) for m in self.data[word]["meanings"])
                        for nm in new_meanings:
                            key = (nm["pos"], nm["translation"])
                            if key not in existing_keys:
                                self.data[word]["meanings"].append(nm)
                                existing_keys.add(key)
                    else:
                        self.data[word] = {
                            "pos_str": "", "meanings": self.parse_translation(trans), "tag": ""
                        }
        except Exception as e:
            print(f"Error loading Translations: {e}")

    def query_all(self, words):
        result = {}
        for word in words:
            w_lower = word.lower()
            entry = self.data.get(w_lower, {})
            
            # Check for incomplete data
            reasons = []
            if not entry.get("meanings"):
                reasons.append("Missing meanings")
            
            all_pos = set()
            if entry.get("pos_str"):
                # ECDICT pos_str like "n/v"
                for p in entry["pos_str"].split('/'):
                    if p: all_pos.add(p + ".")
            
            for m in entry.get("meanings", []):
                if m.get("pos"):
                    all_pos.add(m["pos"])
            
            if not all_pos:
                reasons.append("Missing POS")
            
            if reasons:
                self.incomplete_words.append(f"{word}: {', '.join(reasons)}")

            result[word] = {
                "meanings": entry.get("meanings", []),
                "all_pos": sorted(list(all_pos)),
                "tag": entry.get("tag", "")
            }
        return result

def main():
    inter_dir = "intermediate"
    word_list_path = os.path.join(inter_dir, "unique_words.txt")
    log_path = os.path.join(inter_dir, "incomplete_data.log")
    
    ecdict_csv = "DICT/ECDICT/stardict.csv"
    dict_word_csv = "DICT/DictionaryData/word.csv"
    dict_trans_csv = "DICT/DictionaryData/word_translation.csv"
    
    if not os.path.exists(word_list_path):
        print("Error: unique_words.txt not found.")
        return
        
    with open(word_list_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
        
    lookup = EnhancedLookup(ecdict_csv, dict_word_csv, dict_trans_csv)
    lookup.load_ecdict()
    lookup.load_word_translations()
    
    print(f"Querying enhanced data for {len(words)} words...")
    final_data = lookup.query_all(words)
    
    # Save log
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lookup.incomplete_words))
    print(f"Found {len(lookup.incomplete_words)} words with incomplete data. Log saved to {log_path}")

    # Save Global data
    output_path = os.path.join(inter_dir, "ecdict_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f"Global enhanced data saved to {output_path}")

    # Save Per-Book data for user categorization
    unit_mapping_path = os.path.join(inter_dir, "unit_mapping.json")
    if os.path.exists(unit_mapping_path):
        print(f"Categorizing data by book...")
        with open(unit_mapping_path, "r", encoding="utf-8") as f:
            unit_mappings = json.load(f)
        
        for book_name, units in unit_mappings.items():
            book_vocab = set()
            for words in units.values():
                book_vocab.update(words)
            
            book_dict_data = {w: final_data[w] for w in book_vocab if w in final_data}
            
            book_output_dir = os.path.join("output", "教材分类", book_name)
            os.makedirs(book_output_dir, exist_ok=True)
            
            path = os.path.join(book_output_dir, "dictionary_data.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(book_dict_data, f, ensure_ascii=False, indent=2)
            # print(f"  Exported dictionary data for {book_name}")
        
    print(f"Finished. Enhanced data exported to 'output/教材分类/'.")

if __name__ == "__main__":
    main()
