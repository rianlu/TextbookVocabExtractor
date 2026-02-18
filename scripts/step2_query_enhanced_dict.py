import csv
import json
import os
import re


class EnhancedLookup:
    def __init__(self, ecdict_path, ecdict5_path, trans_csv_path):
        self.ecdict_path = ecdict_path
        self.ecdict5_path = ecdict5_path
        self.trans_csv_path = trans_csv_path

        self.ecdict_data = {}
        self.ecdict5_data = {}
        self.trans_data = {}
        self.incomplete_words = []

    def parse_translation(self, text):
        if not text:
            return []

        lines = re.split(r"\\n|\n", text)
        meanings = []
        seen = set()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = re.match(r"^([a-z]+\.?)\s*(.*)", line)
            if match:
                pos = match.group(1)
                trans = match.group(2).strip()
            elif line.startswith("[") and "]" in line:
                end_idx = line.find("]")
                pos = line[1:end_idx]
                trans = line[end_idx + 1 :].strip()
            else:
                pos = ""
                trans = line

            trans = re.sub(r"^[a-z]+\.\s*", "", trans).strip()
            if not trans:
                continue

            key = (pos, trans)
            if key in seen:
                continue
            seen.add(key)
            meanings.append({"pos": pos, "translation": trans})

        return meanings

    def _load_stardict(self, csv_path, target):
        if not os.path.exists(csv_path):
            print(f"Skip missing stardict: {csv_path}")
            return

        print(f"Loading stardict from {csv_path}...")
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = (row.get("word") or "").strip().lower()
                if not word:
                    continue
                target[word] = {
                    "phonetic": row.get("phonetic", ""),
                    "pos_str": row.get("pos", ""),
                    "meanings": self.parse_translation(row.get("translation", "")),
                    "tag": row.get("tag", ""),
                }

    def load_ecdict(self):
        self._load_stardict(self.ecdict_path, self.ecdict_data)

    def load_ecdict5(self):
        self._load_stardict(self.ecdict5_path, self.ecdict5_data)

    def load_word_translations(self):
        print(f"Loading Word Translations from {self.trans_csv_path}...")
        if not os.path.exists(self.trans_csv_path):
            print(f"Skip missing translation dict: {self.trans_csv_path}")
            return

        with open(self.trans_csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = (row.get("word") or "").strip().lower()
                if not word:
                    continue
                meanings = self.parse_translation(row.get("translation", ""))
                if meanings:
                    self.trans_data[word] = meanings

    def _collect_pos(self, entry):
        all_pos = set()
        if entry.get("pos_str"):
            for p in entry["pos_str"].split("/"):
                p = p.strip()
                if p:
                    all_pos.add(p + ".")
        for m in entry.get("meanings", []):
            p = (m.get("pos") or "").strip()
            if p:
                all_pos.add(p)
        return all_pos

    def query_all(self, words):
        """
        Priority for meanings:
        1) DictionaryData word_translation.csv
        2) ECDICT
        3) ECDICT-5
        """
        result = {}
        for word in words:
            w_lower = word.lower()
            e = self.ecdict_data.get(w_lower, {})
            e5 = self.ecdict5_data.get(w_lower, {})
            trans_meanings = self.trans_data.get(w_lower, [])

            meanings = trans_meanings or e.get("meanings", []) or e5.get("meanings", [])
            phonetic = e.get("phonetic", "") or e5.get("phonetic", "")
            tag = e.get("tag", "") or e5.get("tag", "")

            all_pos = set()
            if trans_meanings:
                for m in trans_meanings:
                    p = (m.get("pos") or "").strip()
                    if p:
                        all_pos.add(p)
            else:
                all_pos |= self._collect_pos(e)
                if not all_pos:
                    all_pos |= self._collect_pos(e5)

            reasons = []
            if not meanings:
                reasons.append("Missing meanings")
            if not all_pos:
                reasons.append("Missing POS")
            if reasons:
                self.incomplete_words.append(f"{word}: {', '.join(reasons)}")

            result[word] = {
                "phonetic": phonetic,
                "meanings": meanings,
                "all_pos": sorted(list(all_pos)),
                "tag": tag,
            }

        return result


def main():
    inter_dir = "intermediate"
    word_list_path = os.path.join(inter_dir, "unique_words.txt")
    log_path = os.path.join(inter_dir, "incomplete_data.log")

    ecdict_csv = "DICT/ECDICT/stardict.csv"
    ecdict5_csv = "DICT/ECDICT-5/stardict.csv"
    dict_trans_csv = "DICT/DictionaryData/word_translation.csv"

    if not os.path.exists(word_list_path):
        print("Error: unique_words.txt not found.")
        return

    with open(word_list_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    lookup = EnhancedLookup(ecdict_csv, ecdict5_csv, dict_trans_csv)
    lookup.load_ecdict()
    lookup.load_ecdict5()
    lookup.load_word_translations()

    print(f"Querying enhanced data for {len(words)} words...")
    final_data = lookup.query_all(words)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lookup.incomplete_words))
    print(f"Found {len(lookup.incomplete_words)} words with incomplete data. Log saved to {log_path}")

    output_path = os.path.join(inter_dir, "ecdict_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(f"Global enhanced data saved to {output_path}")

    unit_mapping_path = os.path.join(inter_dir, "unit_mapping.json")
    if os.path.exists(unit_mapping_path):
        print("Categorizing data by book...")
        with open(unit_mapping_path, "r", encoding="utf-8") as f:
            unit_mappings = json.load(f)

        for book_name, units in unit_mappings.items():
            book_vocab = set()
            for book_words in units.values():
                book_vocab.update(book_words)

            book_dict_data = {w: final_data[w] for w in book_vocab if w in final_data}
            book_output_dir = os.path.join("output", "教材分类", book_name)
            os.makedirs(book_output_dir, exist_ok=True)
            path = os.path.join(book_output_dir, "dictionary_data.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(book_dict_data, f, ensure_ascii=False, indent=2)

    print("Finished. Enhanced data exported to 'output/教材分类/'.")


if __name__ == "__main__":
    main()
