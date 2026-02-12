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

g7_up_txt = 'output/教材分类/【外研版】七年级上册英语电子课本/missing_sentence_words.txt'
g7_up_json = 'sentence/【外研版】七年级上册英语电子课本.json'
g7_up_missing = get_missing_words(g7_up_txt, g7_up_json)

g7_down_txt = 'output/教材分类/【外研版】七年级下册英语电子课本/missing_sentence_words.txt'
g7_down_json = 'sentence/【外研版】七年级下册英语电子课本.json'
g7_down_missing = get_missing_words(g7_down_txt, g7_down_json)

report = {
    "g7_up_missing": g7_up_missing,
    "g7_down_missing": g7_down_missing
}
with open('missing_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=4)
print("Report saved to missing_report.json")
