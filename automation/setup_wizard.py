#!/usr/bin/env python3
"""
环境配置向导
帮助用户安全地设置所有平台账号和API密钥
"""

import os
import sys
import getpass
from pathlib import Path

def print_header(text):
    """打印标题"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def print_step(step, text):
    """打印步骤"""
    print(f"\n📌 步骤 {step}: {text}")

def get_input(prompt, default=None, sensitive=False):
    """获取用户输入"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    if sensitive:
        value = getpass.getpass(prompt)
    else:
        value = input(prompt)

    return value if value else default

def save_env_file(config):
    """保存配置到.env文件"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')

    with open(env_path, 'w', encoding='utf-8') as f:
        f.write("# 自动生成的配置文件 - 请勿手动编辑\n")
        f.write("# 生成时间: " + __import__('datetime').datetime.now().isoformat() + "\n\n")

        for key, value in config.items():
            if value:
                f.write(f"{key}={value}\n")

    print(f"\n✅ 配置已保存到: {env_path}")
    print("⚠️  警告: 此文件包含敏感信息，请勿提交到Git或分享给他人！")

def main():
    print_header("🛠️ 自我生存工具箱 - 环境配置向导")
    print("此向导将帮助您配置所有平台账号和API密钥")
    print("所有敏感信息将安全存储在本地 .env 文件中")

    config = {}

    # GitHub配置
    print_step(1, "配置 GitHub")
    print("   用途: 代码托管、自动化部署")
    config['GITHUB_USERNAME'] = get_input("GitHub 用户名", "ahs757")
    config['GITHUB_TOKEN'] = get_input("GitHub Personal Access Token", sensitive=True)
    config['GITHUB_REPO'] = get_input("GitHub 仓库名", "self-survival-toolbox")

    # 知乎配置
    print_step(2, "配置 知乎")
    print("   用途: 内容发布、SEO引流")
    config['ZHIHU_PHONE'] = get_input("知乎手机号", "18291161026")
    config['ZHIHU_PASSWORD'] = get_input("知乎密码", sensitive=True)

    # 小红书配置
    print_step(3, "配置 小红书")
    print("   用途: 内容发布、社交媒体营销")
    config['XIAOHONGSHU_PHONE'] = get_input("小红书手机号", "18291161026")
    config['XIAOHONGSHU_PASSWORD'] = get_input("小红书密码", sensitive=True)

    # a2hmarket.ai配置
    print_step(4, "配置 a2hmarket.ai")
    print("   用途: AI赚钱、自动化营销")
    config['A2HMARKET_AGENT_ID'] = get_input("a2hmarket Agent ID", "ag_YCljze8QtDgxE9Zq")
    config['A2HMARKET_API_KEY'] = get_input("a2hmarket API Key", sensitive=True)

    # OpenAI配置
    print_step(5, "配置 OpenAI (可选)")
    print("   用途: AI内容生成、自动化写作")
    config['OPENAI_API_KEY'] = get_input("OpenAI API Key (可跳过)", sensitive=True)
    if config['OPENAI_API_KEY']:
        config['OPENAI_MODEL'] = get_input("OpenAI 模型", "gpt-4")

    # 邮件配置
    print_step(6, "配置 邮件营销 (可选)")
    print("   用途: 邮件列表、订阅者管理")
    use_email = get_input("是否配置邮件营销? (y/n)", "n")
    if use_email.lower() == 'y':
        config['SMTP_HOST'] = get_input("SMTP 服务器", "smtp.gmail.com")
        config['SMTP_PORT'] = get_input("SMTP 端口", "587")
        config['SMTP_USER'] = get_input("SMTP 用户名")
        config['SMTP_PASSWORD'] = get_input("SMTP 密码", sensitive=True)

    # 应用密钥
    print_step(7, "生成应用密钥")
    import secrets
    config['APP_SECRET_KEY'] = secrets.token_hex(32)
    print(f"   已生成随机密钥: {config['APP_SECRET_KEY'][:16]}...")

    # 保存配置
    print_header("💾 保存配置")
    save_env_file(config)

    # 验证配置
    print_header("🔍 配置验证")
    from secure_config import SecureConfig
    validator = SecureConfig()
    result = validator.validate_config()

    if result['valid']:
        print("✅ 所有必需配置已完成！")
    else:
        print("⚠️ 以下配置仍需补充:")
        for item in result['missing']:
            print(f"   - {item}")

    print("\n📝 后续步骤:")
    print("   1. 运行 'python secure_config.py' 检查配置状态")
    print("   2. 运行 'python content_publisher.py --mode scan' 扫描内容")
    print("   3. 运行 'python content_publisher.py --mode publish' 发布内容")

if __name__ == '__main__':
    main()