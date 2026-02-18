# TextbookVocabExtractor

从教材 PDF 提取词汇表，补充词典释义和 AI 例句，导出供背单词 App 使用的 JSON 数据。

## 词典数据准备（需手动下载）
本项目**不会**将词典数据上传到 GitHub，请在本地自行下载并放置。

请下载以下数据，并放到 `DICT/` 对应目录：

1. `ECDICT`  
Link: https://github.com/skywind3000/ECDICT  
放置路径：`DICT/ECDICT/stardict.csv`

2. `ECDICT-5`  
Link: https://github.com/H1DDENADM1N/ECCEDICT  
放置路径：`DICT/ECDICT-5/stardict.csv`

3. `DictionaryData`  
Link: https://github.com/LinXueyuanStdio/DictionaryData/tree/master  
放置路径：
- `DICT/DictionaryData/word.csv`
- `DICT/DictionaryData/word_translation.csv`

## 本地目录说明
- `textbook/`：教材 PDF（仅本地使用）
- `sentence/`：AI 例句 JSON 输入
- `output/`：最终导出结果

## 运行方式
```bash
./venv/bin/python main.py
```

流水线步骤：
1. 从 PDF 提取单词和单元（不再使用 PDF 音标）
2. 合并 AI 例句文件
3. 查询词典释义
4. 从本地词典构建全局音标库
5. 合并为最终 JSON
6. 按教材导出“未匹配例句单词”文件
7. 清理中间文件

词典优先级：
- 音标：`DictionaryData(word.csv: uk/us)` → `ECDICT-5` → `ECDICT`
- 释义：`DictionaryData(word_translation.csv)` → `ECDICT` → `ECDICT-5`

## GitHub 同步说明
- 词典数据已在 `.gitignore` 中忽略，应只保留在本地。
- `textbook/` 和 `output/` 当前不忽略，便于协作成员直接使用样例数据。
- 如果你之前已经误提交了大文件，需要先取消跟踪：

```bash
git rm -r --cached DICT/ECDICT DICT/ECDICT-5 DICT/DictionaryData intermediate venv
git commit -m "chore: ignore local datasets and generated artifacts"
```

## 免责声明
- 本项目为学习与技术研究用途，项目本身不内置第三方词典数据与教材版权内容。
- 使用者需自行确认并遵守教材、词典及其他第三方数据的授权条款与适用法律法规。
- 项目与任何教材出版社、词典数据提供方无官方合作或隶属关系。
- 因使用本项目造成的任何版权、数据合规或商业风险，由使用者自行承担。

## 许可证
本项目采用 MIT License，详见 `LICENSE` 文件。
