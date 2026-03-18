#!/usr/bin/env python3
"""
启动所有智能体 - 修复版
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scheduler import TaskScheduler
from datetime import datetime

def main():
    """主函数"""
    print("=" * 60)
    print("LobsterAI 自动赚钱系统启动")
    print("=" * 60)
    print(f"启动时间: {datetime.now()}")
    print("系统将24/7持续运行，按 Ctrl+C 停止")
    print("-" * 60)

    # 创建调度器
    scheduler = TaskScheduler()

    print("所有智能体已初始化！")
    print("-" * 60)
    print("运行中的智能体:")
    print("1. 内容营销机器人 - 每6小时自动生成营销内容")
    print("2. 客户跟进系统 - 每12小时自动管理客户关系")
    print("3. 数据分析智能体 - 每24小时分析销售数据")
    print("4. 联盟营销系统 - 每24小时管理分销商提现")
    print("5. 知识付费平台 - 每周更新在线课程")
    print("-" * 60)

    # 运行调度器
    scheduler.run_scheduler()

if __name__ == "__main__":
    main()
