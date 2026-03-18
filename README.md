# 🛠️ 自我生存工具箱

一套实用的效率工具集合，帮助你自动化日常工作，提升生产力。

## 📦 工具列表

### 文件管理工具 (`tools/`)

| 工具 | 功能 | 使用方法 |
|------|------|----------|
| **file_organizer.py** | 文件自动整理 | `python file_organizer.py <目录> --mode type` |
| **batch_rename.py** | 批量重命名 | `python batch_rename.py <目录> --pattern seq` |
| **text_stats.py** | 文本统计分析 | `python text_stats.py <文件或文本>` |
| **md2html.py** | Markdown转HTML | `python md2html.py <文件> -o output.html` |

### 自动化工具 (`automation/`)

| 工具 | 功能 | 使用方法 |
|------|------|----------|
| **system_monitor.py** | 系统监控 | `python system_monitor.py -w 5` |
| **backup_tool.py** | 文件备份 | `python backup_tool.py <源> <目标> -m incremental` |
| **daily_report.py** | 每日报告 | `python daily_report.py -d <目录> -o report.txt` |

## 🚀 快速开始

```bash
# 克隆项目
git clone <repo-url>
cd 自我生存

# 使用文件整理工具
python tools/file_organizer.py ~/Downloads

# 查看系统状态
python automation/system_monitor.py

# 生成每日报告
python automation/daily_report.py -d .
```

## 📚 详细文档

- [工具使用指南](docs/tools-guide.md)
- [自动化配置说明](docs/automation-guide.md)
- [内容创作模板](content/)

## 📝 内容资源

- [博客模板](content/blog-template.html)
- [效率工具推荐](content/posts/2026-03-18-效率工具推荐.md)
- [自动化办公指南](content/posts/2026-03-18-自动化办公指南.md)

## 🔧 系统要求

- Python 3.8+
- 可选依赖: `psutil` (用于系统监控增强功能)

```bash
pip install psutil  # 可选，增强系统监控功能
```

## 📄 许可证

MIT License - 自由使用和修改

---

**用技术创造价值，让工具为你工作。**
