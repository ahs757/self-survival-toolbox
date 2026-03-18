#!/usr/bin/env python3
"""
启动所有智能体 - 主入口点
"""

import sys
import os
import time
import threading
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(__file__))

from scheduler import TaskScheduler
from content_bot import ContentMarketingBot
from customer_bot import CustomerFollowUpBot
from analytics_bot import DataAnalyticsBot
from affiliate_bot import AffiliateMarketingBot
from knowledge_bot import KnowledgeMonetizationBot

def run_content_agent():
    """运行内容营销智能体"""
    bot = ContentMarketingBot()
    print(f"[{datetime.now()}] 内容营销智能体启动")
    while True:
        try:
            bot.run_daily_content()
            time.sleep(6 * 3600)  # 每6小时运行一次
        except Exception as e:
            print(f"内容营销智能体错误: {e}")
            time.sleep(300)

def run_customer_agent():
    """运行客户跟进智能体"""
    bot = CustomerFollowUpBot()
    print(f"[{datetime.now()}] 客户跟进智能体启动")
    while True:
        try:
            bot.check_for_follow_ups()
            time.sleep(12 * 3600)  # 每12小时运行一次
        except Exception as e:
            print(f"客户跟进智能体错误: {e}")
            time.sleep(300)

def run_analytics_agent():
    """运行数据分析智能体"""
    bot = DataAnalyticsBot()
    print(f"[{datetime.now()}] 数据分析智能体启动")
    while True:
        try:
            # 这里需要实际数据
            time.sleep(24 * 3600)  # 每24小时运行一次
        except Exception as e:
            print(f"数据分析智能体错误: {e}")
            time.sleep(300)

def run_affiliate_agent():
    """运行联盟营销智能体"""
    bot = AffiliateMarketingBot()
    print(f"[{datetime.now()}] 联盟营销智能体启动")
    while True:
        try:
            bot.process_payouts()
            time.sleep(24 * 3600)  # 每24小时运行一次
        except Exception as e:
            print(f"联盟营销智能体错误: {e}")
            time.sleep(300)

def run_knowledge_agent():
    """运行知识付费智能体"""
    bot = KnowledgeMonetizationBot()
    print(f"[{datetime.now()}] 知识付费智能体启动")
    while True:
        try:
            bot.create_all_products()
            time.sleep(7 * 24 * 3600)  # 每周运行一次
        except Exception as e:
            print(f"知识付费智能体错误: {e}")
            time.sleep(300)

def main():
    """主函数"""
    print("=" * 60)
    print("LobsterAI 自动赚钱系统启动")
    print("=" * 60)
    print(f"启动时间: {datetime.now()}")
    print("系统将24/7持续运行，按 Ctrl+C 停止")
    print("-" * 60)

    # 创建所有智能体线程
    threads = [
        threading.Thread(target=run_content_agent, daemon=True),
        threading.Thread(target=run_customer_agent, daemon=True),
        threading.Thread(target=run_analytics_agent, daemon=True),
        threading.Thread(target=run_affiliate_agent, daemon=True),
        threading.Thread(target=run_knowledge_agent, daemon=True)
    ]

    # 启动所有线程
    for thread in threads:
        thread.start()
        time.sleep(1)  # 错开启动时间

    print("所有智能体已启动！")
    print("-" * 60)
    print("运行中的智能体:")
    print("1. 内容营销机器人 - 自动生成营销内容")
    print("2. 客户跟进系统 - 自动管理客户关系")
    print("3. 数据分析智能体 - 分析销售数据")
    print("4. 联盟营销系统 - 管理分销商")
    print("5. 知识付费平台 - 管理在线课程")
    print("-" * 60)

    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n接收到停止信号，正在关闭所有智能体...")
        print("感谢使用 LobsterAI 自动赚钱系统！")

if __name__ == "__main__":
    main()