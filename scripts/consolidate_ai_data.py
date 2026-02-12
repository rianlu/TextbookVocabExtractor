import json
import os
import glob

def consolidate():
    sentence_dir = "sentence"
    output_file = "intermediate/ai_data.json"
    reference_file = "外研版初中英语七年级上册.json"
    
    ai_data = {}
    
    # Try to load existing syllables from reference file
    syllables_cache = {}
    if os.path.exists(reference_file):
        try:
            with open(reference_file, "r", encoding="utf-8") as f:
                ref_data = json.load(f)
                for module in ref_data:
                    for word_entry in module.get("data", []):
                        word = word_entry.get("text")
                        syls = word_entry.get("syllables")
                        if word and syls:
                            syllables_cache[word] = syls
            print(f"Loaded {len(syllables_cache)} words with syllables from {reference_file}")
        except Exception as e:
            print(f"Could not load syllables from {reference_file}: {e}")

    # Process all sentence files
    sentence_files = glob.glob(os.path.join(sentence_dir, "*.json"))
    for sf in sentence_files:
        print(f"Loading sentences from {sf}")
        try:
            with open(sf, "r", encoding="utf-8") as f:
                data = json.load(f)
                for word, entry in data.items():
                    if word not in ai_data:
                        ai_data[word] = {
                            "syllables": syllables_cache.get(word, [word]),
                            "app_sentences": []
                        }
                    
                    # Support legacy compact list format:
                    # ["syllables or tokens", "english sentence", "chinese sentence"]
                    if isinstance(entry, list):
                        if len(entry) >= 3 and isinstance(entry[1], str) and isinstance(entry[2], str):
                            existing_ens = [asent["en"] for asent in ai_data[word]["app_sentences"]]
                            if entry[1] not in existing_ens:
                                ai_data[word]["app_sentences"].append({
                                    "en": entry[1],
                                    "cn": entry[2]
                                })
                        continue

                    # Check if it has 'sentence' key (as seen in the files)
                    if "sentence" in entry:
                        s = entry["sentence"]
                        if isinstance(s, list) and len(s) >= 2:
                            # Avoid duplicates
                            existing_ens = [asent["en"] for asent in ai_data[word]["app_sentences"]]
                            if s[0] not in existing_ens:
                                ai_data[word]["app_sentences"].append({
                                    "en": s[0],
                                    "cn": s[1]
                                })
                    elif "app_sentences" in entry:
                         for s in entry["app_sentences"]:
                            existing_ens = [asent["en"] for asent in ai_data[word]["app_sentences"]]
                            if s.get("en") not in existing_ens:
                                ai_data[word]["app_sentences"].append(s)
        except Exception as e:
            print(f"Error reading {sf}: {e}")

    # Ensure intermediate directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(ai_data, f, ensure_ascii=False, indent=2)
    print(f"Successfully consolidated AI data to {output_file}")

if __name__ == "__main__":
    consolidate()
