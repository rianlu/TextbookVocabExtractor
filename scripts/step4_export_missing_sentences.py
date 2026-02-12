import glob
import json
import os


def is_placeholder_sentence(word, sent):
    en = (sent.get("en") or "").strip()
    cn = (sent.get("cn") or "").strip()
    return en == f"Example sentence for {word}." or cn == "暂无例句。"


def export_missing_sentence_words():
    merged_files = sorted(glob.glob(os.path.join("output", "合并成果", "*.json")))
    if not merged_files:
        print("No merged files found in output/合并成果.")
        return

    summary_lines = ["=== Missing Sentence Words By Book ==="]
    total_books = 0
    total_missing_words = 0
    generated_files = 0

    for path in merged_files:
        book_name = os.path.splitext(os.path.basename(path))[0]
        with open(path, "r", encoding="utf-8") as f:
            book_data = json.load(f)

        missing_words = set()
        for unit in book_data:
            for item in unit.get("data", []):
                word = (item.get("text") or "").strip()
                if not word:
                    continue

                sents = item.get("app_sentences") or []
                if not sents:
                    missing_words.add(word)
                    continue

                has_real_sentence = False
                for sent in sents:
                    en = (sent.get("en") or "").strip()
                    cn = (sent.get("cn") or "").strip()
                    if not en and not cn:
                        continue
                    if is_placeholder_sentence(word, sent):
                        continue
                    has_real_sentence = True
                    break

                if not has_real_sentence:
                    missing_words.add(word)

        total_books += 1
        total_missing_words += len(missing_words)
        summary_lines.append(f"{book_name}: {len(missing_words)}")

        book_dir = os.path.join("output", "教材分类", book_name)
        os.makedirs(book_dir, exist_ok=True)
        out_path = os.path.join(book_dir, "missing_sentence_words.txt")

        if missing_words:
            with open(out_path, "w", encoding="utf-8") as f:
                for word in sorted(missing_words, key=lambda x: x.lower()):
                    f.write(word + "\n")
            generated_files += 1
        elif os.path.exists(out_path):
            os.remove(out_path)

    summary_lines.append("")
    summary_lines.append(f"Books: {total_books}")
    summary_lines.append(f"Total missing words (sum by book): {total_missing_words}")
    summary_lines.append(f"Generated files: {generated_files}")

    summary_path = os.path.join("output", "教材分类", "missing_sentence_words_summary.txt")
    if total_missing_words > 0:
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("\n".join(summary_lines))
    elif os.path.exists(summary_path):
        os.remove(summary_path)

    print("Exported missing sentence words under output/教材分类/<book>/missing_sentence_words.txt")
    if total_missing_words > 0:
        print(f"Summary saved to: {summary_path}")
    else:
        print("No missing words found. No missing file generated.")


if __name__ == "__main__":
    export_missing_sentence_words()
