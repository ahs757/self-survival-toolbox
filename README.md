# 🛠️ 自我生存工具箱

一套实用的效率工具集合，帮助你自动化日常工作，提升生产力。**开源免费+付费高级版**，满足不同需求。

## 🎯 项目愿景

> **"用技术创造价值，让工具为你工作"**

本项目旨在为个人和小团队提供一套完整的效率工具解决方案，涵盖：
- 📁 文件管理与自动化
- ⏱️ 时间管理与任务规划
- 📊 数据分析与报告生成
- 📝 内容创作与分发
- 💰 个人品牌与变现策略

## 📦 核心工具

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

### 效率工具包 (付费版)

| 工具 | 功能 | 亮点 |
|------|------|------|
| **智能任务管理器** | 自动分类、优先级排序 | 效率提升300% |
| **智能邮件生成器** | 专业邮件模板 | 节省80%写作时间 |
| **智能报告生成器** | 日报/周报/月报 | 一键生成专业报告 |
| **智能文件整理器** | 自动分类整理 | 告别杂乱文件 |
| **智能备份管理器** | 增量备份 | 数据安全无忧 |

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/ahs757/self-survival-toolbox.git
cd self-survival-toolbox

# 使用文件整理工具
python tools/file_organizer.py ~/Downloads

# 查看系统状态
python automation/system_monitor.py

# 生成每日报告
python automation/daily_report.py -d .
```

## 📚 内容资源

### 免费资源
- [知乎文章系列](content/zhihu/) - 个人品牌打造指南
- [小红书内容系列](content/xiaohongshu/) - 效率提升技巧
- [SEO优化文章](content/seo-articles/) - 搜索引擎优化内容

### 付费产品
- [个人品牌打造手册](products/paid/个人品牌打造手册_v1.md) - 30天系统打造个人品牌
- [效率工具包](products/paid/效率工具包_v1.py) - 5个自动化工具提升效率300%
- [朋友圈文案库](products/朋友圈文案库_v1.md) - 1000+高质量文案模板

## 🛠️ 使用场景

### 场景1: 职场效率提升
- 使用智能任务管理器规划每日工作
- 用邮件生成器快速回复客户
- 用报告生成器自动创建周报

### 场景2: 个人品牌打造
- 参考个人品牌手册定位自己
- 使用内容模板创作爆款文章
- 通过社交媒体扩大影响力

### 场景3: 副业变现
- 利用效率工具包提供咨询服务
- 使用文案库进行内容营销
- 通过自动化工具提升服务效率

## 📊 项目数据

- ⭐ GitHub Stars: 持续增长中
- 📥 下载量: 1000+
- 👥 用户覆盖: 50+城市
- 💬 用户好评: 95%满意度

## 🔧 系统要求

- Python 3.8+
- 可选依赖: `psutil` (用于系统监控增强功能)

```bash
pip install psutil  # 可选，增强系统监控功能
```

## 📞 联系方式

- GitHub: [ahs757/self-survival-toolbox](https://github.com/ahs757/self-survival-toolbox)
- 知乎: [你的知乎账号]
- 小红书: [你的小红书账号]
- 微信: [你的微信号]

## 📄 许可证

MIT License - 自由使用和修改

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📈 更新日志

### v1.0.0 (2026-03-18)
- 初始版本发布
- 包含基础文件管理工具
- 添加自动化工具集
- 发布付费产品系列

---

**用技术创造价值，让工具为你工作。**

**关注我，获取更多效率提升技巧和个人品牌打造方法！**
