# 🤖 自动化脚本包 - 安装和使用指南

## 📦 产品内容

```
自动化脚本包/
├── scripts/                # 自动化脚本
│   ├── email_automation.py # 邮件自动化
│   ├── social_media_auto.py # 社交媒体自动化
│   ├── data_monitor.py     # 数据监控自动化
│   └── life_automation.py  # 生活自动化
│
├── templates/              # 模板文件
│   ├── email_templates.json
│   ├── social_templates.json
│   └── report_templates.json
│
├── config/                 # 配置文件
│   ├── email_config.json
│   ├── social_config.json
│   └── monitor_config.json
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
- **内存**: 至少 2GB RAM
- **磁盘空间**: 至少 50MB 可用空间

### Python依赖包
```bash
# 自动安装所有依赖
pip install -r requirements.txt

# 或手动安装
pip install schedule  # 定时任务
pip install requests  # HTTP请求
pip install beautifulsoup4  # HTML解析
pip install pandas  # 数据分析
```

## 📥 安装步骤

### 1. 解压产品包
```bash
# Windows
右键点击自动化脚本包.zip -> 解压到当前文件夹

# macOS/Linux
unzip 自动化脚本包.zip -d 自动化脚本包
```

### 2. 安装Python依赖
```bash
cd 自动化脚本包
pip install -r requirements.txt
```

### 3. 配置文件设置
```bash
# 复制配置模板
cp config/email_config.example.json config/email_config.json
cp config/social_config.example.json config/social_config.json

# 编辑配置文件，填入你的API密钥
```

### 4. 验证安装
```bash
# 测试邮件自动化
python scripts/email_automation.py --mode test

# 测试社交媒体自动化
python scripts/social_media_auto.py --mode report
```

## 🚀 快速开始

### 邮件自动化
```bash
# 处理未读邮件
python scripts/email_automation.py --mode process

# 生成邮件报告
python scripts/email_automation.py --mode report

# 使用自定义配置
python scripts/email_automation.py --config my_email_config.json --mode process
```

### 社交媒体自动化
```bash
# 发布内容到所有平台
python scripts/social_media_auto.py --mode post --content "效率工具推荐"

# 发布到指定平台
python scripts/social_media_auto.py --mode post --platform weibo --content "分享一个好工具"

# 设置定时发布
python scripts/social_media_auto.py --mode schedule --platform weibo --content "定时发布测试" --schedule-time "2026-03-19 09:00:00"

# 批量定时发布
python scripts/social_media_auto.py --mode batch

# 运行自动化
python scripts/social_media_auto.py --mode auto
```

### 数据监控自动化
```bash
# 监控网站
python scripts/data_monitor.py --mode website --url https://example.com

# 监控价格
python scripts/data_monitor.py --mode price --url https://product-url.com --target-price 100

# 生成监控报告
python scripts/data_monitor.py --mode report
```

## ⚙️ 配置说明

### 邮件配置 (email_config.json)
```json
{
    "imap_server": "imap.gmail.com",
    "imap_port": 993,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "your-email@gmail.com",
    "password": "your-app-password",
    "use_ssl": true,
    "auto_reply": true,
    "auto_forward": false,
    "forward_to": "forward-email@example.com"
}
```

### 社交媒体配置 (social_config.json)
```json
{
    "platforms": {
        "weibo": {
            "enabled": true,
            "api_key": "your-weibo-api-key",
            "api_secret": "your-weibo-api-secret"
        },
        "wechat": {
            "enabled": true,
            "app_id": "your-wechat-app-id",
            "app_secret": "your-wechat-app-secret"
        }
    }
}
```

## 🔧 高级用法

### 定时任务设置

#### Windows（任务计划程序）
1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每天、每周等）
4. 操作：启动程序
5. 程序：`python`
6. 参数：`scripts/email_automation.py --mode process`

#### macOS/Linux（cron）
```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天早上9点处理邮件）
0 9 * * * cd /path/to/自动化脚本包 && python scripts/email_automation.py --mode process

# 每天中午12点发布社交媒体
0 12 * * * cd /path/to/自动化脚本包 && python scripts/social_media_auto.py --mode post --content "每日分享"
```

### 集成到现有工作流

#### 在Python脚本中使用
```python
from scripts.email_automation import EmailAutomation
from scripts.social_media_auto import SocialMediaAutomation

# 创建实例
email_auto = EmailAutomation('config/email_config.json')
social_auto = SocialMediaAutomation('config/social_config.json')

# 处理邮件
email_auto.process_emails()

# 发布社交媒体
social_auto.auto_post_all_platforms("效率工具推荐")
```

#### 在Shell脚本中使用
```bash
#!/bin/bash
# 每日自动化脚本

cd /path/to/自动化脚本包

# 处理邮件
python scripts/email_automation.py --mode process

# 发布社交媒体
python scripts/social_media_auto.py --mode post --content "每日分享"

# 生成报告
python scripts/email_automation.py --mode report > reports/email_$(date +%Y%m%d).txt
python scripts/social_media_auto.py --mode report > reports/social_$(date +%Y%m%d).txt
```

## 📞 技术支持

### 常见问题
1. **Q: 提示"找不到模块"**
   A: 确保已安装Python依赖：`pip install -r requirements.txt`

2. **Q: 邮件连接失败**
   A: 检查邮箱设置，确保开启了IMAP/SMTP服务，使用应用专用密码

3. **Q: 社交媒体发布失败**
   A: 检查API密钥是否正确，确保有发布权限

### 联系方式
- **手机号**: 18291161026
- **微信**: [待添加]
- **邮箱**: [待添加]

### 更新和升级
- 购买后终身免费更新
- 更新时下载最新版本替换即可
- 配置文件会自动保留

## 🎯 使用技巧

### 1. 邮件自动化最佳实践
- 设置合理的自动回复模板
- 定期清理垃圾邮件
- 备份重要邮件

### 2. 社交媒体自动化技巧
- 选择合适的时间发布
- 使用热门话题标签
- 定期分析发布效果

### 3. 数据监控建议
- 设置合理的监控频率
- 及时响应异常情况
- 定期备份监控数据

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

**感谢购买自动化脚本包！**

如有任何问题，请随时联系技术支持。