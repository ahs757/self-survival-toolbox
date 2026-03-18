# 🚀 效率工具包 - 安装和使用指南

## 📦 产品内容

```
效率工具包/
├── tools/                  # 文件管理工具
│   ├── file_organizer.py   # 智能文件整理器
│   ├── batch_rename.py     # 批量重命名工具
│   ├── text_stats.py       # 文本统计分析
│   └── md2html.py          # Markdown转HTML
│
├── automation/             # 自动化脚本
│   ├── system_monitor.py   # 系统监控工具
│   ├── backup_tool.py      # 备份工具
│   └── daily_report.py     # 每日报告生成器
│
├── templates/              # 模板资源
│   └── blog-template.html  # 博客HTML模板
│
└── docs/                   # 文档
    ├── INSTALL.md          # 安装指南
    ├── USAGE.md            # 使用手册
    └── FAQ.md              # 常见问题
```

## 🛠️ 系统要求

### 基础环境
- **操作系统**: Windows 10/11, macOS 10.15+, Linux
- **Python**: 3.7 或更高版本
- **内存**: 至少 4GB RAM
- **磁盘空间**: 至少 100MB 可用空间

### Python依赖包
```bash
# 自动安装所有依赖
pip install -r requirements.txt

# 或手动安装
pip install psutil  # 系统监控
pip install pathlib # 文件路径处理
```

## 📥 安装步骤

### 1. 解压产品包
```bash
# Windows
右键点击效率工具包.zip -> 解压到当前文件夹

# macOS/Linux
unzip 效率工具包.zip -d 效率工具包
```

### 2. 安装Python依赖
```bash
cd 效率工具包
pip install -r requirements.txt
```

### 3. 验证安装
```bash
# 测试文件整理器
python tools/file_organizer.py --help

# 测试系统监控
python automation/system_monitor.py --mode once
```

## 🚀 快速开始

### 文件整理器
```bash
# 按类型整理下载文件夹
python tools/file_organizer.py ~/Downloads ~/Organized --mode type

# 按日期整理
python tools/file_organizer.py ~/Documents ~/Organized --mode date

# 预览模式（不实际移动）
python tools/file_organizer.py ~/Desktop ~/Organized --dry-run
```

### 批量重命名
```bash
# 添加前缀
python tools/batch_rename.py ./photos --mode prefix_suffix --prefix "vacation_"

# 顺序编号
python tools/batch_rename.py ./documents --mode sequential --pattern "doc_{:03d}"

# 替换文本
python tools/batch_rename.py ./files --mode replace --old-text "draft" --new-text "final"

# 改变大小写
python tools/batch_rename.py ./files --mode case --case-type lower

# 添加日期
python tools/batch_rename.py ./files --mode date --date-format "%Y%m%d"
```

### 文本分析
```bash
# 分析单个文件
python tools/text_stats.py document.txt

# 生成JSON报告
python tools/text_stats.py document.txt --format json -o report.json

# 分析Markdown文件
python tools/text_stats.py article.md -o analysis.txt
```

### Markdown转HTML
```bash
# 基本转换
python tools/md2html.py article.md

# 指定输出文件
python tools/md2html.py article.md -o output.html

# 使用自定义标题
python tools/md2html.py article.md --title "我的文章"
```

### 系统监控
```bash
# 单次监控
python automation/system_monitor.py --mode once

# 持续监控（每5秒）
python automation/system_monitor.py --mode continuous --interval 5

# 生成JSON报告
python automation/system_monitor.py --mode once --format json -o system_report.json
```

### 备份工具
```bash
# 完整备份
python automation/backup_tool.py --mode full --source ~/Documents --name "my_backup"

# 增量备份
python automation/backup_tool.py --mode incremental --source ~/Documents --last-backup ./backups/last_backup

# 列出备份
python automation/backup_tool.py --mode list

# 清理旧备份
python automation/backup_tool.py --mode cleanup
```

### 每日报告
```bash
# 生成今日报告
python automation/daily_report.py

# 生成指定日期报告
python automation/daily_report.py --date 2026-03-18

# 生成Markdown格式报告
python automation/daily_report.py --format markdown -o daily_report.md
```

## ⚙️ 配置选项

### 配置文件
创建 `config.json` 文件来自定义设置：

```json
{
  "backup_dir": "./my_backups",
  "compression_level": 9,
  "exclude_patterns": ["*.tmp", "*.log", "__pycache__"],
  "include_hidden": false,
  "max_backup_age": 30
}
```

### 使用配置文件
```bash
python automation/backup_tool.py --config my_config.json --mode full --source ~/Documents
```

## 🔧 高级用法

### 定时任务设置

#### Windows（任务计划程序）
1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天、每周等）
4. 操作：启动程序
5. 程序：`python`
6. 参数：`automation/system_monitor.py --mode once`

#### macOS/Linux（cron）
```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天凌晨2点备份）
0 2 * * * cd /path/to/效率工具包 && python automation/backup_tool.py --mode full --source ~/Documents

# 每小时监控系统
0 * * * * cd /path/to/效率工具包 && python automation/system_monitor.py --mode once
```

### 集成到现有工作流

#### 在Python脚本中使用
```python
from tools.file_organizer import FileOrganizer

# 创建整理器实例
organizer = FileOrganizer()

# 执行文件整理
organizer.organize_by_type('~/Downloads', '~/Organized')
```

#### 在Shell脚本中使用
```bash
#!/bin/bash
# 每日自动化脚本

cd /path/to/效率工具包

# 备份重要文件
python automation/backup_tool.py --mode full --source ~/Documents --name "daily_backup"

# 生成系统报告
python automation/system_monitor.py --mode once -o "reports/system_$(date +%Y%m%d).txt"

# 整理下载文件夹
python tools/file_organizer.py ~/Downloads ~/Organized --mode type
```

## 📞 技术支持

### 常见问题
1. **Q: 提示"找不到模块"**
   A: 确保已安装Python依赖：`pip install -r requirements.txt`

2. **Q: 备份工具无法访问某些文件**
   A: 检查文件权限，可能需要管理员/root权限

3. **Q: 系统监控显示不完整**
   A: 某些系统信息需要管理员权限才能获取

### 联系方式
- **手机号**: 18291161026
- **微信**: [待添加]
- **邮箱**: [待添加]

### 更新和升级
- 购买后终身免费更新
- 更新时下载最新版本替换即可
- 配置文件会自动保留

## 🎯 使用技巧

### 1. 文件整理最佳实践
- 先使用 `--dry-run` 预览操作结果
- 定期整理下载文件夹，避免文件堆积
- 为不同项目创建单独的整理规则

### 2. 备份策略建议
- **完整备份**: 每周一次
- **增量备份**: 每天一次
- **重要文件**: 实时同步到云盘

### 3. 效率提升技巧
- 将常用命令添加到系统PATH
- 创建批处理脚本自动化重复任务
- 定期检查系统性能报告

## 📄 许可证

本产品为商业软件，购买后获得个人使用许可。

**禁止行为**:
- 转售或分发本产品
- 反编译或修改源代码
- 用于非法用途

**允许行为**:
- 个人和商业使用
- 在多台设备上安装
- 根据需要修改配置

---

**感谢购买效率工具包！**

如有任何问题，请随时联系技术支持。