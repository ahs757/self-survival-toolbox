#!/usr/bin/env python3
"""
测试调度器初始化
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scheduler import TaskScheduler

print("✅ 调度器模块导入成功")

scheduler = TaskScheduler()
print("✅ 调度器初始化成功")

print("\n📋 配置的智能体:")
for name, bot in scheduler.bots.items():
    print(f"  - {name}: {type(bot).__name__}")

print("\n⏰ 调度配置:")
for key, value in scheduler.config.items():
    print(f"  - {key}: {value.get('interval_hours', 'N/A')}小时")

print("\n🎯 系统已就绪，可以开始运行！")
