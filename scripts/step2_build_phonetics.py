import csv
import json
import os


def normalize_word(word: str) -> str:
    return (word or "").strip().lower()


def normalize_phonetic(phonetic: str) -> str:
    if not phonetic:
        return ""
    p = phonetic.strip()
    if not p:
        return ""

    if p.startswith("/") and p.endswith("/") and len(p) > 2:
        p = p[1:-1].strip()
    if not p:
        return ""
    if not p.startswith("["):
        p = f"[{p}]"
    return p


def load_uk_overrides(config_path="config/uk_phonetics.json"):
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {normalize_word(k): normalize_phonetic(v) for k, v in data.items()}
    return {}


def load_stardict(csv_path):
    data = {}
    if not os.path.exists(csv_path):
        print(f"Skip missing dictionary: {csv_path}")
        return data

    print(f"Loading stardict: {csv_path}")
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = normalize_word(row.get("word", ""))
            if not word:
                continue
            phonetic = normalize_phonetic(row.get("phonetic", ""))
            if phonetic:
                data[word] = phonetic

    print(f"Loaded {len(data)} phonetics from {csv_path}")
    return data


def load_dictionarydata_word(csv_path):
    """
    DictionaryData/word.csv uses '>' as delimiter in a single-column CSV.
    Format:
      vc_id>vc_vocabulary>vc_phonetic_uk>vc_phonetic_us>...
    """
    data = {}
    if not os.path.exists(csv_path):
        print(f"Skip missing dictionary: {csv_path}")
        return data

    print(f"Loading DictionaryData word list: {csv_path}")
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            return data

        for row in reader:
            if not row:
                continue
            raw = row[0]
            parts = raw.split(">")
            if len(parts) < 4:
                continue

            word = normalize_word(parts[1])
            uk = normalize_phonetic(parts[2])
            us = normalize_phonetic(parts[3])

            if not word:
                continue
            if uk:
                data[word] = uk
            elif us:
                data[word] = us

    print(f"Loaded {len(data)} phonetics from {csv_path}")
    return data


def main():
    inter_dir = "intermediate"
    os.makedirs(inter_dir, exist_ok=True)

    unit_mapping_path = os.path.join(inter_dir, "unit_mapping.json")
    if not os.path.exists(unit_mapping_path):
        print("Error: intermediate/unit_mapping.json not found.")
        return

    with open(unit_mapping_path, "r", encoding="utf-8") as f:
        unit_mappings = json.load(f)

    # Priority: manual overrides > ECDICT > ECDICT-5 > DictionaryData
    uk_overrides = load_uk_overrides("config/uk_phonetics.json")
    ecdict = load_stardict("DICT/ECDICT/stardict.csv")
    ecdict5 = load_stardict("DICT/ECDICT-5/stardict.csv")
    dict_word = load_dictionarydata_word("DICT/DictionaryData/word.csv")

    unique_words = set()
    for book_data in unit_mappings.values():
        for unit_words in book_data.values():
            unique_words.update(unit_words)

    print(f"Building phonetics for {len(unique_words)} unique words...")
    all_word_phonetics = {}
    missing_words = []

    for word in sorted(unique_words, key=str.lower):
        key = normalize_word(word)
        phonetic = (
            uk_overrides.get(key)
            or ecdict.get(key)
            or ecdict5.get(key)
            or dict_word.get(key)
            or ""
        )

        if phonetic:
            all_word_phonetics[word] = phonetic
        else:
            missing_words.append(word)

    output_path = os.path.join(inter_dir, "word_phonetics.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_word_phonetics, f, ensure_ascii=False, indent=2)

    missing_path = os.path.join(inter_dir, "missing_phonetics.txt")
    if missing_words:
        with open(missing_path, "w", encoding="utf-8") as f:
            f.write("\n".join(missing_words))
    elif os.path.exists(missing_path):
        os.remove(missing_path)

    print(f"Saved phonetics: {len(all_word_phonetics)} -> {output_path}")
    print(f"Missing phonetics: {len(missing_words)}")


if __name__ == "__main__":
    main()
