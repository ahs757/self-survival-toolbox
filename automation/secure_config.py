#!/usr/bin/env python3
"""
安全配置管理器
用于安全管理所有平台账号和API密钥
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional

class SecureConfig:
    """安全管理配置和敏感信息"""

    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or os.path.dirname(os.path.abspath(__file__))
        self.env_file = os.path.join(self.config_dir, '.env')
        self.config_cache = {}

    def load_env(self) -> Dict[str, str]:
        """从.env文件加载环境变量"""
        env_vars = {}

        if os.path.exists(self.env_file):
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()

        # 也加载系统环境变量（优先级更高）
        for key in env_vars.keys():
            system_value = os.environ.get(key)
            if system_value:
                env_vars[key] = system_value

        return env_vars

    def get(self, key: str, default: str = None) -> Optional[str]:
        """获取配置值"""
        # 先检查环境变量
        value = os.environ.get(key)
        if value:
            return value

        # 再检查.env文件
        if not self.config_cache:
            self.config_cache = self.load_env()

        return self.config_cache.get(key, default)

    def get_github_config(self) -> Dict[str, str]:
        """获取GitHub配置"""
        return {
            'username': self.get('GITHUB_USERNAME', 'ahs757'),
            'token': self.get('GITHUB_TOKEN'),
            'repo': self.get('GITHUB_REPO', 'self-survival-toolbox')
        }

    def get_zhihu_config(self) -> Dict[str, str]:
        """获取知乎配置"""
        return {
            'phone': self.get('ZHIHU_PHONE', '18291161026'),
            'password': self.get('ZHIHU_PASSWORD')
        }

    def get_xiaohongshu_config(self) -> Dict[str, str]:
        """获取小红书配置"""
        return {
            'phone': self.get('XIAOHONGSHU_PHONE', '18291161026'),
            'password': self.get('XIAOHONGSHU_PASSWORD')
        }

    def get_a2hmarket_config(self) -> Dict[str, str]:
        """获取a2hmarket.ai配置"""
        return {
            'agent_id': self.get('A2HMARKET_AGENT_ID', 'ag_YCljze8QtDgxE9Zq'),
            'api_key': self.get('A2HMARKET_API_KEY')
        }

    def get_wechat_config(self) -> Dict[str, str]:
        """获取微信配置"""
        return {
            'app_id': self.get('WECHAT_APP_ID'),
            'app_secret': self.get('WECHAT_APP_SECRET'),
            'payment_mch_id': self.get('WECHAT_MCH_ID'),
            'payment_key': self.get('WECHAT_PAYMENT_KEY')
        }

    def get_openai_config(self) -> Dict[str, str]:
        """获取OpenAI配置（用于内容生成）"""
        return {
            'api_key': self.get('OPENAI_API_KEY'),
            'model': self.get('OPENAI_MODEL', 'gpt-4')
        }

    def get_email_config(self) -> Dict[str, str]:
        """获取邮件营销配置"""
        return {
            'smtp_host': self.get('SMTP_HOST'),
            'smtp_port': self.get('SMTP_PORT', '587'),
            'smtp_user': self.get('SMTP_USER'),
            'smtp_password': self.get('SMTP_PASSWORD'),
            'list_id': self.get('EMAIL_LIST_ID')
        }

    def get_all_platforms(self) -> Dict[str, Dict]:
        """获取所有平台配置摘要（不包含敏感信息）"""
        return {
            'github': {
                'username': self.get('GITHUB_USERNAME', 'ahs757'),
                'configured': bool(self.get('GITHUB_TOKEN'))
            },
            'zhihu': {
                'phone': self.get('ZHIHU_PHONE', '18291161026'),
                'configured': bool(self.get('ZHIHU_PASSWORD'))
            },
            'xiaohongshu': {
                'phone': self.get('XIAOHONGSHU_PHONE', '18291161026'),
                'configured': bool(self.get('XIAOHONGSHU_PASSWORD'))
            },
            'a2hmarket': {
                'agent_id': self.get('A2HMARKET_AGENT_ID', 'ag_YCljze8QtDgxE9Zq'),
                'configured': bool(self.get('A2HMARKET_API_KEY'))
            },
            'wechat': {
                'configured': bool(self.get('WECHAT_APP_ID'))
            },
            'openai': {
                'configured': bool(self.get('OPENAI_API_KEY'))
            },
            'email': {
                'configured': bool(self.get('SMTP_HOST'))
            }
        }

    def validate_config(self) -> Dict[str, list]:
        """验证配置完整性"""
        missing = []
        warnings = []

        # 检查必需配置
        if not self.get('GITHUB_TOKEN'):
            missing.append('GITHUB_TOKEN')

        if not self.get('ZHIHU_PASSWORD'):
            warnings.append('ZHIHU_PASSWORD - 知乎发布功能不可用')

        if not self.get('XIAOHONGSHU_PASSWORD'):
            warnings.append('XIAOHONGSHU_PASSWORD - 小红书发布功能不可用')

        if not self.get('OPENAI_API_KEY'):
            warnings.append('OPENAI_API_KEY - AI内容生成功能不可用')

        return {
            'missing': missing,
            'warnings': warnings,
            'valid': len(missing) == 0
        }


# 创建全局配置实例
config = SecureConfig()

# 导出常用函数
def get_config(key: str, default: str = None) -> Optional[str]:
    return config.get(key, default)

def get_platform_config(platform: str) -> Dict[str, str]:
    method_name = f'get_{platform}_config'
    if hasattr(config, method_name):
        return getattr(config, method_name)()
    return {}


if __name__ == '__main__':
    # 测试配置管理器
    print("🔧 配置状态检查")
    print("=" * 40)

    platforms = config.get_all_platforms()
    for platform, info in platforms.items():
        status = "✅ 已配置" if info.get('configured') else "❌ 未配置"
        print(f"{platform}: {status}")

    print("\n📋 配置验证结果")
    print("=" * 40)

    validation = config.validate_config()
    if validation['valid']:
        print("✅ 所有必需配置已就绪")
    else:
        print("❌ 缺少以下必需配置:")
        for item in validation['missing']:
            print(f"   - {item}")

    if validation['warnings']:
        print("\n⚠️ 警告:")
        for warning in validation['warnings']:
            print(f"   - {warning}")