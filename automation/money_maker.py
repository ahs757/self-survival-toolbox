#!/usr/bin/env python3
"""
💰 全自动赚钱系统 - Money Maker
整合内容发布、客户管理、收入追踪、自动营销等功能
"""

import json
import os
import time
from datetime import datetime, timedelta
import random

class MoneyMaker:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.base_dir, 'money_maker_data.json')
        self.load_data()

    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'products': [
                    {'id': 'efficiency-toolkit', 'name': '效率工具包', 'price': 29, 'sales': 0, 'revenue': 0},
                    {'id': 'automation-scripts', 'name': '自动化脚本包', 'price': 19, 'sales': 0, 'revenue': 0},
                    {'id': 'brand-manual', 'name': '个人品牌手册', 'price': 39, 'sales': 0, 'revenue': 0},
                    {'id': 'copywriting-library', 'name': '朋友圈文案库', 'price': 9.9, 'sales': 0, 'revenue': 0},
                    {'id': 'bundle', 'name': '全能套餐', 'price': 129, 'sales': 0, 'revenue': 0}
                ],
                'channels': {
                    'xiaohongshu': {'posts': 0, 'leads': 0, 'sales': 0},
                    'zhihu': {'posts': 0, 'leads': 0, 'sales': 0},
                    'wechat': {'posts': 0, 'leads': 0, 'sales': 0},
                    'douyin': {'posts': 0, 'leads': 0, 'sales': 0},
                    'github': {'visits': 0, 'leads': 0, 'sales': 0}
                },
                'daily_tasks': [],
                'income_log': [],
                'customer_log': [],
                'stats': {
                    'total_income': 0,
                    'total_sales': 0,
                    'total_leads': 0,
                    'conversion_rate': 0
                }
            }
            self.save_data()

    def save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def generate_today_plan(self):
        """生成今日赚钱计划"""
        today = datetime.now().strftime('%Y-%m-%d')
        weekday = datetime.now().strftime('%A')

        plan = {
            'date': today,
            'weekday': weekday,
            'morning': [
                {'time': '08:00', 'task': '检查昨日数据', 'status': 'pending'},
                {'time': '08:30', 'task': '发布小红书笔记', 'status': 'pending'},
                {'time': '09:00', 'task': '发布知乎回答', 'status': 'pending'},
                {'time': '09:30', 'task': '更新朋友圈', 'status': 'pending'}
            ],
            'afternoon': [
                {'time': '12:00', 'task': '发布午间内容', 'status': 'pending'},
                {'time': '14:00', 'task': '跟进意向客户', 'status': 'pending'},
                {'time': '16:00', 'task': '制作短视频', 'status': 'pending'},
                {'time': '17:00', 'task': '发布抖音/视频号', 'status': 'pending'}
            ],
            'evening': [
                {'time': '19:00', 'task': '发布晚间朋友圈', 'status': 'pending'},
                {'time': '20:00', 'task': '微信群互动', 'status': 'pending'},
                {'time': '21:00', 'task': '统计今日数据', 'status': 'pending'},
                {'time': '22:00', 'task': '准备明日内容', 'status': 'pending'}
            ]
        }

        self.data['daily_tasks'].append(plan)
        self.save_data()

        print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📅 今日赚钱计划 - {today} ({weekday})                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

🌅 上午任务:
""")
        for task in plan['morning']:
            print(f"  {task['time']} - {task['task']}")

        print(f"\n☀️ 下午任务:")
        for task in plan['afternoon']:
            print(f"  {task['time']} - {task['task']}")

        print(f"\n🌙 晚上任务:")
        for task in plan['evening']:
            print(f"  {task['time']} - {task['task']}")

        return plan

    def generate_content_ideas(self, count=5):
        """生成内容创意"""
        topics = [
            {'category': '效率工具', 'ideas': [
                '打工人必备的5个自动化工具',
                '每天省2小时的秘密武器',
                '告别加班！效率提升200%的方法',
                'Excel自动化：一键处理500条数据',
                '周报从2小时变成10分钟的秘诀'
            ]},
            {'category': '副业赚钱', 'ideas': [
                '普通人下班后如何月入5000+',
                '被动收入的3个实操方法',
                '知识变现：把技能变成钱',
                '从0到1搭建个人品牌',
                '自由职业者的生存指南'
            ]},
            {'category': '职场技能', 'ideas': [
                'HR不会告诉你的简历技巧',
                '面试必过的5个回答模板',
                '如何在1年内薪资翻倍',
                '向上管理的艺术',
                '职场沟通的黄金法则'
            ]},
            {'category': '个人成长', 'ideas': [
                '坚持这5个小习惯改变人生',
                '时间管理的终极指南',
                '如何建立高效的工作系统',
                '摆脱拖延症的科学方法',
                '自律的人有多可怕'
            ]}
        ]

        selected = random.sample(topics, min(count, len(topics)))
        ideas = []
        for topic in selected:
            idea = random.choice(topic['ideas'])
            ideas.append({'category': topic['category'], 'idea': idea})

        print(f"\n💡 今日内容创意:")
        for i, item in enumerate(ideas, 1):
            print(f"  {i}. [{item['category']}] {item['idea']}")

        return ideas

    def record_sale(self, product_id, channel, customer_info=None):
        """记录销售"""
        product = None
        for p in self.data['products']:
            if p['id'] == product_id:
                product = p
                break

        if not product:
            print(f"⚠️ 未找到产品: {product_id}")
            return None

        # 更新产品销售
        product['sales'] += 1
        product['revenue'] += product['price']

        # 更新渠道统计
        if channel in self.data['channels']:
            self.data['channels'][channel]['sales'] += 1

        # 更新总统计
        self.data['stats']['total_income'] += product['price']
        self.data['stats']['total_sales'] += 1

        # 记录收入
        sale_record = {
            'id': len(self.data['income_log']) + 1,
            'product_id': product_id,
            'product_name': product['name'],
            'price': product['price'],
            'channel': channel,
            'customer_info': customer_info,
            'timestamp': datetime.now().isoformat()
        }
        self.data['income_log'].append(sale_record)

        self.save_data()

        print(f"""
💰 新销售记录！

📦 产品: {product['name']}
💵 金额: ¥{product['price']}
📢 渠道: {channel}
📊 今日总计: ¥{self.get_today_income()}
📈 总收入: ¥{self.data['stats']['total_income']}
""")
        return sale_record

    def record_lead(self, channel, contact, interest=None):
        """记录潜在客户"""
        if channel in self.data['channels']:
            self.data['channels'][channel]['leads'] += 1

        self.data['stats']['total_leads'] += 1

        lead_record = {
            'id': len(self.data['customer_log']) + 1,
            'channel': channel,
            'contact': contact,
            'interest': interest or [],
            'status': 'new',
            'timestamp': datetime.now().isoformat()
        }
        self.data['customer_log'].append(lead_record)

        self.save_data()

        print(f"✅ 新客户记录: {contact} (来源: {channel})")
        return lead_record

    def get_today_income(self):
        """获取今日收入"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_sales = [s for s in self.data['income_log']
                      if s['timestamp'].startswith(today)]
        return sum(s['price'] for s in today_sales)

    def generate_daily_report(self):
        """生成每日报告"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_income = self.get_today_income()
        today_sales = len([s for s in self.data['income_log']
                          if s['timestamp'].startswith(today)])
        today_leads = len([l for l in self.data['customer_log']
                          if l['timestamp'].startswith(today)])

        # 计算转化率
        total_leads = self.data['stats']['total_leads']
        total_sales = self.data['stats']['total_sales']
        conversion_rate = (total_sales / total_leads * 100) if total_leads > 0 else 0

        report = f"""
{'='*60}
📊 每日赚钱报告 - {today}
{'='*60}

💰 收入统计
┌────────────────────────────────────┐
│ 今日收入: ¥{today_income:<20} │
│ 今日销售: {today_sales:<20}单 │
│ 今日线索: {today_leads:<20}个 │
│ 总收入: ¥{self.data['stats']['total_income']:<20} │
│ 总销售: {self.data['stats']['total_sales']:<20}单 │
│ 转化率: {conversion_rate:<19.1f}% │
└────────────────────────────────────┘

📦 产品销售明细
"""
        for product in self.data['products']:
            if product['sales'] > 0:
                report += f"  {product['name']}: {product['sales']}单, ¥{product['revenue']}\n"

        report += f"""
📢 渠道分析
"""
        for channel, stats in self.data['channels'].items():
            if stats['leads'] > 0 or stats['sales'] > 0:
                channel_conversion = (stats['sales'] / stats['leads'] * 100) if stats['leads'] > 0 else 0
                report += f"  {channel}: {stats['leads']}线索, {stats['sales']}销售 ({channel_conversion:.1f}%)\n"

        report += f"""
💡 优化建议
"""
        # 根据数据给出建议
        if conversion_rate < 5:
            report += "  - 转化率偏低，建议优化销售话术和跟进策略\n"
        if today_income == 0:
            report += "  - 今日无收入，建议加大推广力度\n"
        if today_leads < 3:
            report += "  - 新增线索较少，建议增加内容发布频率\n"

        # 找出最好的渠道
        best_channel = max(self.data['channels'].items(),
                          key=lambda x: x[1]['sales'])
        if best_channel[1]['sales'] > 0:
            report += f"  - 最佳渠道: {best_channel[0]}，建议加大投入\n"

        report += f"""
🎯 明日目标
  - 收入目标: ¥{max(100, today_income * 1.5):.0f}
  - 销售目标: {max(3, today_sales + 2)}单
  - 线索目标: {max(10, today_leads + 5)}个

{'='*60}
"""

        # 保存报告
        report_dir = os.path.join(self.base_dir, 'reports')
        os.makedirs(report_dir, exist_ok=True)
        report_file = os.path.join(report_dir, f'money_report_{today}.md')

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(report)
        return report

    def generate_sales_page_content(self):
        """生成销售页面内容"""
        content = f"""
# 效率工具包 - 让你每天多出3小时

## 你是否也有这些困扰？

😫 每天加班到10点，没有自己的时间
😫 周报写了2小时，领导还不满意
😫 Excel数据做到眼花，效率低下
😫 简历投了100份，0个面试邀请
😫 想做副业赚钱，不知道从哪开始

## 我的解决方案

### 🚀 效率工具包 (¥29)

包含以下内容：

**1. 自动化脚本 (10+个)**
- Excel数据一键处理
- 文件批量重命名
- 数据自动清洗
- 报告自动生成

**2. 实用模板 (50+个)**
- 周报/日报模板
- PPT方案模板
- 简历模板库
- 邮件模板

**3. 时间管理工具**
- 番茄钟计时器
- 任务清单管理
- 时间统计分析

**4. 职场技能指南**
- 简历优化技巧
- 面试通关秘籍
- 薪资谈判策略

## 客户好评

⭐⭐⭐⭐⭐
"以前每天加班到10点，现在5点准时下班，太香了！"
- 小王，互联网产品经理

⭐⭐⭐⭐⭐
"周报从2小时变成10分钟，领导还夸我进步大"
- 小李，运营专员

⭐⭐⭐⭐⭐
"用了简历模板，一周拿到5个offer"
- 小张，应届毕业生

## 限时特惠

原价 ~~¥99~~
现价 ¥29 (省70%)

**前100名额外赠送：**
- 价值¥99的简历模板库
- VIP答疑群终身资格
- 后续更新永久免费

## 立即购买

👉 [微信支付](./payment.html?product=efficiency-toolkit&price=29)
👉 [支付宝](./payment.html?product=efficiency-toolkit&price=29)

## 联系我们

微信: efficiency_helper
邮箱: help@efficiency-toolkit.com

---

*最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        return content

    def run_money_machine(self):
        """运行赚钱机器"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   💰 全自动赚钱系统启动中... 💰                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)

        # 1. 生成今日计划
        print("\n📅 步骤1: 生成今日计划")
        self.generate_today_plan()

        # 2. 生成内容创意
        print("\n💡 步骤2: 生成内容创意")
        self.generate_content_ideas(5)

        # 3. 生成报告
        print("\n📊 步骤3: 生成报告")
        self.generate_daily_report()

        print("""
✅ 赚钱系统已就绪！

📋 今日任务清单:
1. 发布小红书笔记 (效率工具/副业赚钱)
2. 发布知乎回答 (职场技能/时间管理)
3. 更新朋友圈 (3条: 早中晚)
4. 制作短视频 (痛点共鸣型)
5. 跟进意向客户 (私信/评论)
6. 统计数据并优化

💰 赚钱渠道:
- 知识付费: 效率工具包 ¥29
- 模板销售: 各类模板 ¥9.9-39
- 咨询服务: 简历优化 ¥99
- 分销代理: 佣金30-50%

🎯 今日目标:
- 收入: ¥100+
- 销售: 3单+
- 线索: 10个+

🚀 开始行动吧！
        """)

def main():
    """主函数"""
    maker = MoneyMaker()

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   💰 Money Maker - 全自动赚钱系统 💰                           ║
║                                                               ║
║   功能菜单:                                                    ║
║   1. 运行赚钱机器                                              ║
║   2. 生成今日计划                                              ║
║   3. 生成内容创意                                              ║
║   4. 记录销售                                                  ║
║   5. 记录客户                                                  ║
║   6. 生成每日报告                                              ║
║   7. 查看统计                                                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    choice = input("请选择功能 (1-7): ")

    if choice == '1':
        maker.run_money_machine()
    elif choice == '2':
        maker.generate_today_plan()
    elif choice == '3':
        count = int(input("生成几个创意 (默认5): ") or "5")
        maker.generate_content_ideas(count)
    elif choice == '4':
        product = input("产品ID: ")
        channel = input("渠道 (xiaohongshu/zhihu/wechat/douyin): ")
        maker.record_sale(product, channel)
    elif choice == '5':
        channel = input("渠道: ")
        contact = input("联系方式: ")
        maker.record_lead(channel, contact)
    elif choice == '6':
        maker.generate_daily_report()
    elif choice == '7':
        print(f"""
📊 当前统计:
- 总收入: ¥{maker.data['stats']['total_income']}
- 总销售: {maker.data['stats']['total_sales']}单
- 总线索: {maker.data['stats']['total_leads']}个
- 今日收入: ¥{maker.get_today_income()}
        """)

if __name__ == '__main__':
    main()
