#!/usr/bin/env python3
"""
⏰ 任务调度器
定时执行各种赚钱任务
"""

import json
import os
import time
from datetime import datetime, timedelta

class TaskScheduler:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.tasks_file = os.path.join(self.base_dir, 'scheduled_tasks.json')
        self.load_tasks()

    def load_tasks(self):
        """加载任务"""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = {
                'daily': [
                    {'time': '08:00', 'task': 'check_yesterday_data', 'name': '检查昨日数据', 'enabled': True},
                    {'time': '08:30', 'task': 'publish_xiaohongshu', 'name': '发布小红书', 'enabled': True},
                    {'time': '09:00', 'task': 'publish_zhihu', 'name': '发布知乎', 'enabled': True},
                    {'time': '09:30', 'task': 'update_wechat_moments', 'name': '更新朋友圈', 'enabled': True},
                    {'time': '12:00', 'task': 'lunch_content', 'name': '午间内容', 'enabled': True},
                    {'time': '14:00', 'task': 'follow_up_leads', 'name': '跟进客户', 'enabled': True},
                    {'time': '16:00', 'task': 'create_video', 'name': '制作视频', 'enabled': True},
                    {'time': '18:00', 'task': 'publish_douyin', 'name': '发布抖音', 'enabled': True},
                    {'time': '20:00', 'task': 'wechat_group_activity', 'name': '微信群互动', 'enabled': True},
                    {'time': '21:00', 'task': 'daily_report', 'name': '生成日报', 'enabled': True},
                    {'time': '22:00', 'task': 'prepare_tomorrow', 'name': '准备明日', 'enabled': True}
                ],
                'weekly': [
                    {'day': 'Monday', 'task': 'weekly_plan', 'name': '制定周计划', 'enabled': True},
                    {'day': 'Friday', 'task': 'weekly_review', 'name': '周复盘', 'enabled': True},
                    {'day': 'Sunday', 'task': 'content_batch', 'name': '批量生成内容', 'enabled': True}
                ],
                'monthly': [
                    {'day': 1, 'task': 'monthly_report', 'name': '月度报告', 'enabled': True},
                    {'day': 15, 'task': 'mid_month_review', 'name': '月中复盘', 'enabled': True}
                ],
                'history': []
            }
            self.save_tasks()

    def save_tasks(self):
        """保存任务"""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def get_current_time(self):
        """获取当前时间"""
        return datetime.now()

    def get_today_tasks(self):
        """获取今日任务"""
        now = self.get_current_time()
        weekday = now.strftime('%A')
        day = now.day

        tasks = []

        # 日常任务
        for task in self.tasks['daily']:
            if task['enabled']:
                tasks.append({
                    'time': task['time'],
                    'name': task['name'],
                    'task': task['task'],
                    'type': 'daily',
                    'status': 'pending'
                })

        # 周任务
        for task in self.tasks['weekly']:
            if task['enabled'] and task['day'] == weekday:
                tasks.append({
                    'time': '10:00',
                    'name': task['name'],
                    'task': task['task'],
                    'type': 'weekly',
                    'status': 'pending'
                })

        # 月任务
        for task in self.tasks['monthly']:
            if task['enabled'] and task['day'] == day:
                tasks.append({
                    'time': '09:00',
                    'name': task['name'],
                    'task': task['task'],
                    'type': 'monthly',
                    'status': 'pending'
                })

        # 按时间排序
        tasks.sort(key=lambda x: x['time'])

        return tasks

    def display_today_schedule(self):
        """显示今日安排"""
        now = self.get_current_time()
        tasks = self.get_today_tasks()

        print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📅 今日任务安排 - {now.strftime('%Y-%m-%d %A')}              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

⏰ 当前时间: {now.strftime('%H:%M:%S')}
📋 待执行任务: {len(tasks)}个

""")

        current_time = now.strftime('%H:%M')

        for i, task in enumerate(tasks, 1):
            time_status = "✅" if task['time'] <= current_time else "⏳"
            type_icon = {"daily": "🔄", "weekly": "📅", "monthly": "📆"}.get(task['type'], "📌")

            print(f"  {time_status} {task['time']} - {type_icon} {task['name']}")
            if task['time'] <= current_time:
                print(f"      → 应该已执行")

        return tasks

    def mark_task_done(self, task_name):
        """标记任务完成"""
        now = self.get_current_time()

        record = {
            'task': task_name,
            'completed_at': now.isoformat(),
            'date': now.strftime('%Y-%m-%d')
        }

        self.tasks['history'].append(record)
        self.save_tasks()

        print(f"✅ 任务已完成: {task_name}")

    def get_task_stats(self):
        """获取任务统计"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_history = [h for h in self.tasks['history'] if h['date'] == today]

        tasks = self.get_today_tasks()
        completed = len(today_history)
        total = len(tasks)

        print(f"""
📊 今日任务统计

✅ 已完成: {completed}/{total}
⏳ 待完成: {total - completed}
📈 完成率: {(completed/total*100) if total > 0 else 0:.1f}%

已完成任务:
""")
        for record in today_history:
            time = datetime.fromisoformat(record['completed_at']).strftime('%H:%M')
            print(f"  ✅ {time} - {record['task']}")

    def generate_task_reminders(self):
        """生成任务提醒"""
        now = self.get_current_time()
        current_time = now.strftime('%H:%M')
        tasks = self.get_today_tasks()

        upcoming = []
        for task in tasks:
            if task['time'] > current_time:
                # 计算还有多久
                task_time = datetime.strptime(task['time'], '%H:%M').time()
                current = now.time()

                # 简单计算分钟差
                task_minutes = task_time.hour * 60 + task_time.minute
                current_minutes = current.hour * 60 + current.minute
                diff = task_minutes - current_minutes

                if diff <= 60:  # 1小时内的任务
                    upcoming.append({
                        'task': task,
                        'minutes_until': diff
                    })

        if upcoming:
            print("\n⏰ 即将到来的任务:")
            for item in upcoming:
                mins = item['minutes_until']
                if mins <= 5:
                    urgency = "🔥"
                elif mins <= 15:
                    urgency = "⚡"
                else:
                    urgency = "📌"

                print(f"  {urgency} {item['task']['time']} - {item['task']['name']} (还有{mins}分钟)")
        else:
            print("\n✅ 暂无即将到期的任务")

def main():
    """主函数"""
    scheduler = TaskScheduler()

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ⏰ 任务调度器 ⏰                                              ║
║                                                               ║
║   功能菜单:                                                    ║
║   1. 查看今日安排                                              ║
║   2. 标记任务完成                                              ║
║   3. 查看任务统计                                              ║
║   4. 查看即将到期任务                                          ║
║   5. 管理任务列表                                              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    choice = input("请选择功能 (1-5): ")

    if choice == '1':
        scheduler.display_today_schedule()
    elif choice == '2':
        task_name = input("完成的任务名称: ")
        scheduler.mark_task_done(task_name)
    elif choice == '3':
        scheduler.get_task_stats()
    elif choice == '4':
        scheduler.generate_task_reminders()
    elif choice == '5':
        print("\n📋 当前任务列表:")
        print("\n🔄 日常任务:")
        for task in scheduler.tasks['daily']:
            status = "✅" if task['enabled'] else "❌"
            print(f"  {status} {task['time']} - {task['name']}")

        print("\n📅 周任务:")
        for task in scheduler.tasks['weekly']:
            status = "✅" if task['enabled'] else "❌"
            print(f"  {status} {task['day']} - {task['name']}")

        print("\n📆 月任务:")
        for task in scheduler.tasks['monthly']:
            status = "✅" if task['enabled'] else "❌"
            print(f"  {status} 每月{task['day']}日 - {task['name']}")

if __name__ == '__main__':
    main()
