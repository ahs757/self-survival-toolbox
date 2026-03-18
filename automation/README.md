# 🔐 账号密码安全配置指南

## ✅ 已有账号

| 平台 | 用途 | 状态 |
|------|------|------|
| **GitHub** | 代码托管、自动化部署 | ✅ 用户名: ahs757 |
| **知乎** | 内容发布、SEO引流 | ✅ 手机: 18291161026 |
| **小红书** | 社交媒体营销 | ✅ 手机: 18291161026 |
| **a2hmarket.ai** | AI赚钱、自动化营销 | ✅ Agent ID: ag_YCljze8QtDgxE9Zq |
| **微信收款码** | 收款 | ✅ 已有 |

## 🔑 需要补充的API密钥

以下密钥需要从对应平台获取，用于解锁完整功能：

### 必需配置

1. **GitHub Personal Access Token**
   - 访问: https://github.com/settings/tokens
   - 创建token时勾选: `repo`, `workflow`, `write:packages`
   - 环境变量: `GITHUB_TOKEN`

### 推荐配置

2. **OpenAI API Key** (AI内容生成)
   - 访问: https://platform.openai.com/api-keys
   - 环境变量: `OPENAI_API_KEY`
   - 用途: 自动生成SEO文章、内容优化

3. **微信公众号 AppID & AppSecret** (微信发布)
   - 访问: https://mp.weixin.qq.com
   - 环境变量: `WECHAT_APP_ID`, `WECHAT_APP_SECRET`

## 🚀 快速配置

### 方法1: 使用配置向导 (推荐)
```bash
cd automation
python setup_wizard.py
```

### 方法2: 手动配置
1. 复制 `.env.template` 为 `.env`
2. 填入你的API密钥和密码
3. 运行 `python secure_config.py` 验证配置

## 📁 文件说明

```
automation/
├── secure_config.py      # 安全配置管理器
├── setup_wizard.py       # 配置向导
├── content_publisher.py  # 内容发布器
├── .env.template         # 环境变量模板
└── .env                  # 实际配置 (自动生成，勿提交Git)
```

## ⚠️ 安全提醒

1. **永远不要** 将 `.env` 文件提交到Git
2. **永远不要** 在代码中硬编码密码
3. **定期更换** API密钥和密码
4. **使用强密码** 和双因素认证

## 🔧 当前配置状态

运行以下命令查看当前配置状态:
```bash
python secure_config.py
```

## 📞 需要帮助?

如有问题，请查看各平台的API文档:
- GitHub: https://docs.github.com/en/rest
- 知乎: 无官方API，使用模拟登录
- 小红书: 无官方API，使用模拟登录
- OpenAI: https://platform.openai.com/docs