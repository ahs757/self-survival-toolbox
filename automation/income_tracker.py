#!/usr/bin/env python3
"""
📊 收入追踪器 - Income Tracker
实时追踪和统计多渠道收入
"""

import json
import os
from datetime import datetime, timedelta

class IncomeTracker:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.base_dir, 'income_data.json')
        self.load_data()

    def load_data(self):
        """加载数据"""
        default_data = {
            'transactions': [],
            'daily_stats': {},
            'channel_stats': {},
            'product_stats': {},
            'goals': {
                'daily': 100,
                'weekly': 500,
                'monthly': 2000
            }
        }

        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                # 确保所有必需的键都存在
                for key, default_value in default_data.items():
                    if key not in loaded_data:
                        loaded_data[key] = default_value
                self.data = loaded_data
        else:
            self.data = default_data
            self.save_data()

    def save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_transaction(self, product_id, product_name, amount, channel, customer_info=None):
        """添加交易记录"""
        transaction = {
            'id': len(self.data['transactions']) + 1,
            'product_id': product_id,
            'product_name': product_name,
            'amount': amount,
            'channel': channel,
            'customer_info': customer_info,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'completed'
        }

        self.data['transactions'].append(transaction)

        # 更新每日统计
        date = transaction['date']
        if date not in self.data['daily_stats']:
            self.data['daily_stats'][date] = {'income': 0, 'transactions': 0, 'products': {}}
        self.data['daily_stats'][date]['income'] += amount
        self.data['daily_stats'][date]['transactions'] += 1

        # 更新渠道统计
        if channel not in self.data['channel_stats']:
            self.data['channel_stats'][channel] = {'income': 0, 'transactions': 0, 'products': {}}
        self.data['channel_stats'][channel]['income'] += amount
        self.data['channel_stats'][channel]['transactions'] += 1

        # 更新产品统计
        if product_id not in self.data['product_stats']:
            self.data['product_stats'][product_id] = {'name': product_name, 'income': 0, 'transactions': 0}
        self.data['product_stats'][product_id]['income'] += amount
        self.data['product_stats'][product_id]['transactions'] += 1

        self.save_data()

        print(f"""
💰 新交易记录！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 产品: {product_name}
💵 金额: ¥{amount}
📢 渠道: {channel}
📅 日期: {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
今日总计: ¥{self.get_today_income()}
本周总计: ¥{self.get_week_income()}
本月总计: ¥{self.get_month_income()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

        return transaction

    def get_today_income(self):
        """获取今日收入"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.data['daily_stats'].get(today, {}).get('income', 0)

    def get_week_income(self):
        """获取本周收入"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_income = 0

        for i in range(7):
            date = (week_start + timedelta(days=i)).strftime('%Y-%m-%d')
            week_income += self.data['daily_stats'].get(date, {}).get('income', 0)

        return week_income

    def get_month_income(self):
        """获取本月收入"""
        today = datetime.now()
        month_start = today.replace(day=1)
        month_income = 0

        for date_str, stats in self.data['daily_stats'].items():
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if date >= month_start:
                month_income += stats['income']

        return month_income

    def get_total_income(self):
        """获取总收入"""
        return sum(t['amount'] for t in self.data['transactions'])

    def generate_dashboard(self):
        """生成仪表板"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_income = self.get_today_income()
        week_income = self.get_week_income()
        month_income = self.get_month_income()
        total_income = self.get_total_income()

        # 计算目标完成度
        daily_goal = self.data['goals']['daily']
        weekly_goal = self.data['goals']['weekly']
        monthly_goal = self.data['goals']['monthly']

        daily_progress = (today_income / daily_goal * 100) if daily_goal > 0 else 0
        weekly_progress = (week_income / weekly_goal * 100) if weekly_goal > 0 else 0
        monthly_progress = (month_income / monthly_goal * 100) if monthly_goal > 0 else 0

        dashboard = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📊 收入仪表板 - {today}                                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

💰 收入概览
┌────────────────────────────────────────────────────────────┐
│ 今日收入: ¥{today_income:<10} 目标: ¥{daily_goal:<10} 完成: {daily_progress:.1f}%      │
│ 本周收入: ¥{week_income:<10} 目标: ¥{weekly_goal:<10} 完成: {weekly_progress:.1f}%      │
│ 本月收入: ¥{month_income:<10} 目标: ¥{monthly_goal:<10} 完成: {monthly_progress:.1f}%      │
│ 总收入:   ¥{total_income:<10}                                        │
└────────────────────────────────────────────────────────────┘

📢 渠道分析
"""
        for channel, stats in sorted(self.data['channel_stats'].items(), key=lambda x: x[1]['income'], reverse=True):
            dashboard += f"  {channel}: ¥{stats['income']} ({stats['transactions']}单)\n"

        dashboard += f"""
📦 产品分析
"""
        for product_id, stats in sorted(self.data['product_stats'].items(), key=lambda x: x[1]['income'], reverse=True):
            dashboard += f"  {stats['name']}: ¥{stats['income']} ({stats['transactions']}单)\n"

        # 最近交易
        recent_transactions = sorted(self.data['transactions'], key=lambda x: x['timestamp'], reverse=True)[:5]
        if recent_transactions:
            dashboard += f"""
📝 最近交易
"""
            for t in recent_transactions:
                dashboard += f"  {t['date']} {t['product_name']} ¥{t['amount']} ({t['channel']})\n"

        dashboard += f"""
🎯 目标进度

今日: {'█' * int(daily_progress/10)}{'░' * (10-int(daily_progress/10))} {daily_progress:.1f}%
本周: {'█' * int(weekly_progress/10)}{'░' * (10-int(weekly_progress/10))} {weekly_progress:.1f}%
本月: {'█' * int(monthly_progress/10)}{'░' * (10-int(monthly_progress/10))} {monthly_progress:.1f}%

💡 建议
"""
        if today_income < daily_goal:
            dashboard += "  - 今日收入未达标，建议加大推广力度\n"
        if week_income < weekly_goal * 0.5:
            dashboard += "  - 本周进度偏慢，建议增加内容发布\n"
        if len(self.data['channel_stats']) < 3:
            dashboard += "  - 渠道较少，建议扩展新渠道\n"

        return dashboard

    def run_demo(self):
        """运行演示"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📊 收入追踪器演示                                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)

        # 模拟一些交易
        demo_transactions = [
            ('efficiency-toolkit', '效率工具包', 29, 'xiaohongshu', '小王'),
            ('automation-scripts', '自动化脚本包', 19, 'zhihu', '小李'),
            ('resume-optimization', '简历优化', 99, 'wechat', '小张'),
            ('efficiency-toolkit', '效率工具包', 29, 'douyin', '小赵'),
            ('vip-group', 'VIP答疑群', 99, 'wechat', '小钱'),
        ]

        print("\n📝 模拟交易记录...")
        for product_id, product_name, amount, channel, customer in demo_transactions:
            self.add_transaction(product_id, product_name, amount, channel, customer)

        # 显示仪表板
        print(self.generate_dashboard())

def main():
    """主函数"""
    tracker = IncomeTracker()

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📊 Income Tracker - 收入追踪器                              ║
║                                                               ║
║   功能菜单:                                                    ║
║   1. 查看仪表板                                                ║
║   2. 添加交易                                                  ║
║   3. 查看统计                                                  ║
║   4. 运行演示                                                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    choice = input("请选择功能 (1-4): ")

    if choice == '1':
        print(tracker.generate_dashboard())
    elif choice == '2':
        product_id = input("产品ID: ")
        product_name = input("产品名称: ")
        amount = float(input("金额: "))
        channel = input("渠道: ")
        customer = input("客户信息(可选): ") or None
        tracker.add_transaction(product_id, product_name, amount, channel, customer)
    elif choice == '3':
        print(f"""
📊 统计信息:
- 总收入: ¥{tracker.get_total_income()}
- 今日收入: ¥{tracker.get_today_income()}
- 本周收入: ¥{tracker.get_week_income()}
- 本月收入: ¥{tracker.get_month_income()}
- 总交易数: {len(tracker.data['transactions'])}
        """)
    elif choice == '4':
        tracker.run_demo()

if __name__ == '__main__':
    main()
