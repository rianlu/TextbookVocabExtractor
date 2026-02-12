import json
import os

def get_missing_words(txt_path, json_path):
    if not os.path.exists(txt_path):
        return []
    with open(txt_path, 'r', encoding='utf-8') as f:
        txt_words = [line.strip() for line in f if line.strip()]
    
    if not os.path.exists(json_path):
        return txt_words
    
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    missing = [w for w in txt_words if w not in json_data]
    return missing

base_dir = 'output/教材分类/'
sentence_dir = 'sentence/'
all_missing = {}

for item in os.listdir(base_dir):
    dir_path = os.path.join(base_dir, item)
    if os.path.isdir(dir_path):
        txt_path = os.path.join(dir_path, 'missing_sentence_words.txt')
        if os.path.exists(txt_path):
            json_path = os.path.join(sentence_dir, item + '.json')
            missing = get_missing_words(txt_path, json_path)
            if missing:
                all_missing[item] = missing

with open('final_missing_report.json', 'w', encoding='utf-8') as f:
    json.dump(all_missing, f, ensure_ascii=False, indent=4)

if not all_missing:
    print("SUCCESS: All textbooks are complete!")
else:
    print(f"FAILED: Found missing words in {len(all_missing)} textbooks.")
    for book, words in all_missing.items():
        print(f"  - {book}: {len(words)} missing")
