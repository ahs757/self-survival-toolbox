# ⚡ 自动化配置指南

## 系统监控 (system_monitor.py)

### 功能
- 实时监控CPU、内存、磁盘使用
- 支持持续监控模式
- 可输出JSON格式用于其他程序集成

### 使用方法

```bash
# 单次查看系统状态
python system_monitor.py

# 持续监控（每5秒刷新）
python system_monitor.py -w 5

# 输出JSON格式
python system_monitor.py -f json

# 保存报告到文件
python system_monitor.py -o system_report.txt
```

### 集成示例

```python
# 在其他程序中使用
from system_monitor import get_cpu_usage, get_memory_info

cpu = get_cpu_usage()
memory = get_memory_info()
print(f"CPU: {cpu}%, 内存: {memory['percent']}%")
```

---

## 文件备份 (backup_tool.py)

### 功能
- 增量备份：只备份新增或修改的文件
- 完整备份：备份所有文件
- 支持压缩备份
- 自动记录文件清单

### 使用方法

```bash
# 增量备份
python backup_tool.py ./source ./backup -m incremental

# 完整备份
python backup_tool.py ./source ./backup -m full

# 压缩完整备份
python backup_tool.py ./source ./backup -m full -z

# 排除特定文件
python backup_tool.py ./source ./backup -e ".tmp" ".log" "node_modules"
```

### 自动化备份脚本

创建 `auto_backup.bat` (Windows) 或 `auto_backup.sh` (Linux/Mac):

```bash
#!/bin/bash
# 每日自动备份
python backup_tool.py /path/to/source /path/to/backup -m incremental
```

---

## 每日报告 (daily_report.py)

### 功能
- 生成项目状态摘要
- 统计文件变化
- 追踪最近修改的文件

### 使用方法

```bash
# 生成当前目录报告
python daily_report.py

# 指定项目目录
python daily_report.py -d /path/to/project

# 输出到文件
python daily_report.py -d . -o daily_report.txt

# JSON格式输出
python daily_report.py -f json -o report.json
```

---

## 定时任务配置

### Windows 任务计划

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天/每周等）
4. 操作：启动程序
5. 程序：`python`
6. 参数：`C:\path\to\script.py`

### Linux/Mac Cron

```bash
# 编辑crontab
crontab -e

# 每天凌晨2点执行备份
0 2 * * * /usr/bin/python3 /path/to/backup_tool.py /source /backup -m incremental

# 每小时生成报告
0 * * * * /usr/bin/python3 /path/to/daily_report.py -d /project -o /reports/hourly.txt
```

---

## 常见问题

### Q: 没有psutil模块怎么办？
A: 所有工具都有内置的备选方法，不依赖psutil也能正常工作。但安装psutil会提供更好的性能和更多功能：

```bash
pip install psutil
```

### Q: 如何设置邮件通知？
A: 可以结合邮件模块，在监控到异常时发送邮件通知（高级功能，可自行扩展）。

### Q: 备份占用空间太大？
A: 使用增量备份模式，只备份变化的文件。也可以配合压缩选项使用。
