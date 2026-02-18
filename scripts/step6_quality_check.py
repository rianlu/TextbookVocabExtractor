import glob
import json
import os
import re


PLACEHOLDER_CN = "暂无例句。"
PHONETIC_RE = re.compile(r"^\[[^\[\]]+\]$|^/[^/]+/$")
WORD_RE = re.compile(r"^[A-Za-z][A-Za-z'\-\.]*$")
TOKEN_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
ENABLE_SUSPICIOUS_FRAGMENT_CHECK = False
ISSUE_LABELS_ZH = {
    "empty_text": "词条文本为空",
    "empty_meaning": "释义为空",
    "missing_phonetic": "单词缺少音标",
    "phonetic_format": "音标格式异常",
    "missing_sentence": "缺少例句",
    "bad_sentence_item": "例句结构异常",
    "empty_sentence_item": "例句中英都为空",
    "placeholder_sentence": "仅有占位例句",
    "sentence_length": "例句长度不在推荐范围",
    "suspicious_fragment": "疑似截断词",
}


def is_placeholder_sentence(word, sent):
    en = (sent.get("en") or "").strip()
    cn = (sent.get("cn") or "").strip()
    return en == f"Example sentence for {word}." or cn == PLACEHOLDER_CN


def sentence_word_count(text):
    return len(TOKEN_RE.findall(text or ""))


def build_word_forms(word):
    w = word.lower()
    forms = {w}

    def is_cvc(base):
        if len(base) < 3:
            return False
        vowels = "aeiou"
        c1, v, c2 = base[-3], base[-2], base[-1]
        return (
            c1 not in vowels
            and v in vowels
            and c2 not in vowels
            and c2 not in "wxy"
        )

    if w.endswith("y") and len(w) > 2 and w[-2] not in "aeiou":
        stem = w[:-1]
        forms.update({stem + "ies", stem + "ied", stem + "ying"})
    else:
        forms.update({w + "s", w + "ed", w + "ing"})

    if w.endswith("e") and len(w) > 2:
        forms.add(w[:-1] + "ing")
        forms.add(w[:-1] + "ed")

    # Handle consonant doubling in common CVC verbs/adjectives: nod -> nodded/nodding
    if is_cvc(w):
        forms.add(w + w[-1] + "ed")
        forms.add(w + w[-1] + "ing")
        forms.add(w + w[-1] + "er")
        forms.add(w + w[-1] + "est")

    if w.endswith(("s", "x", "z", "ch", "sh")):
        forms.add(w + "es")

    forms.update({w + "er", w + "est"})
    return forms


def add_issue(container, issue_type, word, unit, detail):
    container.append(
        {
            "type": issue_type,
            "type_zh": ISSUE_LABELS_ZH.get(issue_type, issue_type),
            "word": word,
            "unit": unit,
            "detail": detail,
        }
    )


def detect_suspicious_fragments(words, word_meta):
    suspicious = []
    uniq = sorted(set(words), key=str.lower)
    for w in uniq:
        wl = w.lower()
        if " " in wl or len(wl) < 3:
            continue
        meta = word_meta.get(wl, {})
        if meta.get("has_meaning") and meta.get("has_phonetic"):
            continue
        for other in uniq:
            ol = other.lower()
            if wl == ol or " " in ol:
                continue
            other_meta = word_meta.get(ol, {})
            if not other_meta.get("has_meaning"):
                continue
            if ol.startswith(wl) and len(ol) - len(wl) <= 4:
                suspicious.append((w, other))
                break
    return suspicious


def run_quality_check():
    merged_files = sorted(glob.glob(os.path.join("output", "合并成果", "*.json")))
    if not merged_files:
        print("No merged files found in output/合并成果.")
        return

    report = {
        "summary": {
            "books": 0,
            "total_entries": 0,
            "error_count": 0,
            "warning_count": 0,
        },
        "books": {},
    }

    for path in merged_files:
        book_name = os.path.splitext(os.path.basename(path))[0]
        with open(path, "r", encoding="utf-8") as f:
            book_data = json.load(f)

        errors = []
        warnings = []
        book_words = []
        word_meta = {}
        entry_count = 0

        for unit in book_data:
            unit_name = unit.get("unit", "")
            for item in unit.get("data", []):
                entry_count += 1
                text = (item.get("text") or "").strip()
                phonetic = (item.get("phonetic") or "").strip()
                meaning = (item.get("meaning") or "").strip()
                sentences = item.get("app_sentences")
                book_words.append(text)
                word_meta[text.lower()] = {
                    "has_meaning": bool(meaning),
                    "has_phonetic": bool(phonetic),
                }

                if not text:
                    add_issue(errors, "empty_text", text, unit_name, "词条缺少 text 字段。")
                    continue

                if not meaning:
                    add_issue(warnings, "empty_meaning", text, unit_name, "释义为空。")

                if not phonetic:
                    if WORD_RE.fullmatch(text):
                        add_issue(errors, "missing_phonetic", text, unit_name, "单个单词缺少音标。")
                elif not PHONETIC_RE.fullmatch(phonetic):
                    add_issue(warnings, "phonetic_format", text, unit_name, f"音标格式不符合预期: {phonetic}")

                if not isinstance(sentences, list) or not sentences:
                    add_issue(errors, "missing_sentence", text, unit_name, "没有 app_sentences。")
                    continue

                valid_sentences = []
                for sent in sentences:
                    if not isinstance(sent, dict):
                        add_issue(errors, "bad_sentence_item", text, unit_name, "例句项不是对象结构。")
                        continue
                    en = (sent.get("en") or "").strip()
                    cn = (sent.get("cn") or "").strip()
                    if not en and not cn:
                        add_issue(errors, "empty_sentence_item", text, unit_name, "例句的英文和中文都为空。")
                        continue
                    if is_placeholder_sentence(text, sent):
                        continue
                    valid_sentences.append((en, cn))

                if not valid_sentences:
                    add_issue(errors, "placeholder_sentence", text, unit_name, "只有占位或空白例句。")
                    continue

                has_length_ok = False
                for en, _ in valid_sentences:
                    wc = sentence_word_count(en)
                    if 8 <= wc <= 15:
                        has_length_ok = True

                if not has_length_ok:
                    lengths = [sentence_word_count(en) for en, _ in valid_sentences]
                    add_issue(
                        warnings,
                        "sentence_length",
                        text,
                        unit_name,
                        f"所有有效例句长度都不在 8-15 词范围内: {lengths}",
                    )

        if ENABLE_SUSPICIOUS_FRAGMENT_CHECK:
            for frag, full in detect_suspicious_fragments(book_words, word_meta):
                add_issue(
                    warnings,
                    "suspicious_fragment",
                    frag,
                    "",
                    f"疑似被截断，可能来自词条 '{full}'。",
                )

        report["books"][book_name] = {
            "entries": entry_count,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "errors": errors,
            "warnings": warnings,
        }

        report["summary"]["books"] += 1
        report["summary"]["total_entries"] += entry_count
        report["summary"]["error_count"] += len(errors)
        report["summary"]["warning_count"] += len(warnings)

    out_dir = os.path.join("output", "质检报告")
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, "quality_report.json")
    md_path = os.path.join(out_dir, "quality_report.md")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    md_lines = [
        "# 质量检查报告",
        "",
        f"- 教材数量: {report['summary']['books']}",
        f"- 词条总数: {report['summary']['total_entries']}",
        f"- 错误总数: {report['summary']['error_count']}",
        f"- 警告总数: {report['summary']['warning_count']}",
        "",
        "## 各教材统计",
    ]
    for book_name, data in report["books"].items():
        md_lines.append(
            f"- {book_name}: entries={data['entries']}, errors={data['error_count']}, warnings={data['warning_count']}"
        )

    md_lines.append("")
    md_lines.append("## 错误样例（每本最多10条）")
    for book_name, data in report["books"].items():
        if not data["errors"]:
            continue
        md_lines.append(f"### {book_name}")
        for issue in data["errors"][:10]:
            md_lines.append(
                f"- [{issue['type_zh']}] {issue['word']} ({issue['unit']}): {issue['detail']}"
            )

    md_lines.append("")
    md_lines.append("## 警告样例（每本最多10条）")
    for book_name, data in report["books"].items():
        if not data["warnings"]:
            continue
        md_lines.append(f"### {book_name}")
        for issue in data["warnings"][:10]:
            md_lines.append(
                f"- [{issue['type_zh']}] {issue['word']} ({issue['unit']}): {issue['detail']}"
            )

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print("Quality check complete.")
    print(f"Report JSON: {json_path}")
    print(f"Report Markdown: {md_path}")
    print(
        "Summary: "
        f"books={report['summary']['books']}, "
        f"entries={report['summary']['total_entries']}, "
        f"errors={report['summary']['error_count']}, "
        f"warnings={report['summary']['warning_count']}"
    )


if __name__ == "__main__":
    run_quality_check()
