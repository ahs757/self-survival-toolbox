# 🛠️ 工具使用指南

## 文件整理神器 (file_organizer.py)

### 功能介绍
自动将文件按类型或日期分类整理，支持预览模式。

### 使用方法

```bash
# 按类型整理（预览模式）
python file_organizer.py ~/Downloads

# 按类型整理（执行移动）
python file_organizer.py ~/Downloads --mode type --execute

# 按日期整理
python file_organizer.py ~/Downloads --mode date --execute

# 自定义规则
python file_organizer.py ~/Downloads --rules rules.json
```

### 支持的文件类型
- 文档: PDF, DOC, DOCX, TXT, XLS, XLSX, PPT, PPTX
- 图片: JPG, PNG, GIF, SVG, WEBP
- 视频: MP4, AVI, MKV, MOV
- 音乐: MP3, WAV, FLAC, AAC
- 压缩包: ZIP, RAR, 7Z, TAR, GZ
- 代码: PY, JS, HTML, CSS, JAVA, CPP

---

## 批量重命名 (batch_rename.py)

### 功能介绍
支持多种模式的批量文件重命名。

### 使用方法

```bash
# 序号模式: file_001.txt, file_002.txt
python batch_rename.py ./photos --pattern seq --prefix "photo_"

# 日期模式: 2026-03-18_oldname.txt
python batch_rename.py ./docs --pattern date

# 前缀模式: report_oldname.txt
python batch_rename.py ./files --pattern prefix --prefix "report_"

# 后缀模式: oldname_v1.txt
python batch_rename.py ./files --pattern suffix --suffix "_v1"

# 正则替换: 将空格替换为下划线
python batch_rename.py ./files --pattern regex --find " " --replace "_"
```

---

## 文本统计 (text_stats.py)

### 功能介绍
分析文本内容，统计字数、词频等信息。

### 使用方法

```bash
# 分析文件
python text_stats.py article.txt

# 分析直接输入的文本
python text_stats.py "这是一段测试文本 hello world"

# 分析剪贴板内容（Windows）
python text_stats.py --clipboard
```

### 输出内容
- 总字符数、单词数
- 中英文分别统计
- 句子数、段落数
- 预估阅读时间
- 词频统计 TOP 10

---

## Markdown转HTML (md2html.py)

### 功能介绍
将Markdown文件转换为精美的HTML页面。

### 使用方法

```bash
# 基本转换
python md2html.py article.md

# 指定输出文件
python md2html.py article.md -o output.html

# 使用自定义模板
python md2html.py article.md --template custom.html

# 内联CSS样式
python md2html.py article.md --inline-css
```
