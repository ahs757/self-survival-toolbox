#!/usr/bin/env python3
"""
被动收入自动化系统
实现多渠道内容分发、客户管理、自动回复等功能
"""

import json
import os
import time
from datetime import datetime, timedelta
import random

class PassiveIncomeSystem:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.base_dir, 'passive_income_data.json')
        self.load_data()

    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'customers': [],
                'orders': [],
                'content_queue': [],
                'promotions': [],
                'stats': {
                    'total_income': 0,
                    'total_customers': 0,
                    'conversion_rate': 0
                }
            }
            self.save_data()

    def save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_customer(self, name, source, contact, interest=None):
        """添加客户"""
        customer = {
            'id': len(self.data['customers']) + 1,
            'name': name,
            'source': source,  # xiaohongshu/zhihu/wechat/douyin
            'contact': contact,
            'interest': interest or [],
            'status': 'new',  # new/contacted/interested/purchased
            'created_at': datetime.now().isoformat(),
            'last_contact': None,
            'notes': []
        }
        self.data['customers'].append(customer)
        self.save_data()
        print(f"✅ 新客户已添加: {name} (来源: {source})")
        return customer

    def add_order(self, customer_id, product, price, payment_method):
        """添加订单"""
        order = {
            'id': len(self.data['orders']) + 1,
            'customer_id': customer_id,
            'product': product,
            'price': price,
            'payment_method': payment_method,
            'status': 'pending',  # pending/paid/delivered/completed
            'created_at': datetime.now().isoformat(),
            'paid_at': None,
            'delivered_at': None
        }
        self.data['orders'].append(order)

        # 更新统计
        self.data['stats']['total_income'] += price
        self.save_data()
        print(f"✅ 新订单已创建: {product} - ¥{price}")
        return order

    def generate_daily_content(self):
        """生成每日内容计划"""
        content_types = [
            {
                'platform': 'xiaohongshu',
                'topic': '效率工具推荐',
                'title': f'打工人必备！{random.choice(["5个", "7个", "10个"])}让你效率翻倍的神器',
                'tags': ['#效率工具', '#打工人', '#职场干货'],
                'schedule': '09:00'
            },
            {
                'platform': 'zhihu',
                'topic': '职场技能',
                'title': f'如何在{random.choice(["1年", "2年", "3年"])}内实现薪资翻倍？',
                'tags': ['职场发展', '薪资谈判', '技能提升'],
                'schedule': '12:00'
            },
            {
                'platform': 'wechat',
                'topic': '朋友圈营销',
                'title': '今日份干货分享',
                'content_type': 'story',
                'schedule': '20:00'
            },
            {
                'platform': 'douyin',
                'topic': '短视频脚本',
                'title': f'{random.choice(["加班到10点", "周报写了2小时"])}的我，发现了这个秘密',
                'duration': '30s',
                'schedule': '18:00'
            }
        ]

        today = datetime.now().strftime('%Y-%m-%d')
        self.data['content_queue'].append({
            'date': today,
            'contents': content_types,
            'status': 'pending'
        })
        self.save_data()

        print(f"\n📅 {today} 内容计划已生成:")
        for content in content_types:
            print(f"  - [{content['schedule']}] {content['platform']}: {content['title']}")

        return content_types

    def generate_promotion_plan(self):
        """生成推广计划"""
        promotions = [
            {
                'type': 'discount',
                'name': '新人首单优惠',
                'description': '首次购买享8折优惠',
                'code': 'NEWUSER20',
                'discount': 0.2,
                'valid_days': 7
            },
            {
                'type': 'bundle',
                'name': '全能套餐',
                'description': '购买所有产品享5折',
                'original_price': 257,
                'bundle_price': 129,
                'savings': 128
            },
            {
                'type': 'referral',
                'name': '邀请有礼',
                'description': '邀请好友购买返现',
                'referrer_reward': 10,
                'referee_discount': 0.1
            },
            {
                'type': 'limited',
                'name': '限时特惠',
                'description': '每日前10名享特价',
                'daily_limit': 10,
                'special_price': 19
            }
        ]

        self.data['promotions'] = promotions
        self.save_data()

        print("\n🎁 推广活动已设置:")
        for promo in promotions:
            print(f"  - {promo['name']}: {promo['description']}")

        return promotions

    def auto_reply_template(self, platform, message_type):
        """自动回复模板"""
        templates = {
            'xiaohongshu': {
                'comment': [
                    "感谢关注！私信你啦～",
                    "已私信，请查收！",
                    "谢谢支持！详情已私信～"
                ],
                'dm': [
                    "你好！感谢对效率工具包的关注～\n\n包含：\n✅ 自动化脚本（10+个）\n✅ 实用模板（50+个）\n✅ 时间管理工具\n\n限时特惠：¥29（原价99）\n需要的话我发你购买链接？",
                    "你好！看到你对效率工具感兴趣～\n\n我这边有完整的工具包\n可以帮你每天省2-3小时\n\n要不要了解一下具体内容？"
                ]
            },
            'zhihu': {
                'comment': [
                    "感谢赞同！有问题随时交流～",
                    "谢谢支持！私信已发～"
                ],
                'dm': [
                    "你好！感谢对我的回答感兴趣～\n\n我把这些工具都整理成了工具包\n包含自动化脚本、模板库等\n\n需要的话可以看看：[链接]"
                ]
            },
            'wechat': {
                'friend_request': "你好！我是效率工具分享者，感谢添加～",
                'group_join': "大家好！专注效率工具和职场技能分享，多多交流～",
                'inquiry': "你好！看到你对效率工具感兴趣～\n\n我这边有：\n1. 自动化脚本包 ¥19\n2. 效率工具包 ¥29\n3. 个人品牌手册 ¥39\n4. 全能套餐 ¥129\n\n需要了解哪个？我发你详细介绍～"
            }
        }

        if platform in templates and message_type in templates[platform]:
            return random.choice(templates[platform][message_type])
        return "感谢您的关注！稍后回复您～"

    def calculate_conversion_rate(self):
        """计算转化率"""
        total_inquiries = len([c for c in self.data['customers'] if c['status'] in ['contacted', 'interested']])
        total_purchases = len([c for c in self.data['customers'] if c['status'] == 'purchased'])

        if total_inquiries > 0:
            rate = (total_purchases / total_inquiries) * 100
        else:
            rate = 0

        self.data['stats']['conversion_rate'] = round(rate, 2)
        self.data['stats']['total_customers'] = len(self.data['customers'])
        self.save_data()

        return rate

    def generate_daily_report(self):
        """生成每日报告"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_orders = [o for o in self.data['orders']
                       if o['created_at'].startswith(today)]

        today_income = sum(o['price'] for o in today_orders if o['status'] == 'paid')
        today_customers = len([c for c in self.data['customers']
                              if c['created_at'].startswith(today)])

        report = f"""
{'='*50}
📊 每日收入报告 - {today}
{'='*50}

💰 收入统计
- 今日收入: ¥{today_income}
- 总收入: ¥{self.data['stats']['total_income']}
- 今日订单: {len(today_orders)}
- 总订单数: {len(self.data['orders'])}

👥 客户统计
- 今日新增: {today_customers}
- 总客户数: {len(self.data['customers'])}
- 转化率: {self.calculate_conversion_rate()}%

📈 来源分析
"""
        # 统计来源
        sources = {}
        for customer in self.data['customers']:
            source = customer['source']
            sources[source] = sources.get(source, 0) + 1

        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            report += f"- {source}: {count}人\n"

        report += f"""
🎯 明日计划
- 发布3条小红书笔记
- 发布1篇知乎回答
- 发布2条朋友圈
- 跟进{len([c for c in self.data['customers'] if c['status'] == 'interested'])}个意向客户

💡 优化建议
"""
        # 根据数据给出建议
        if self.data['stats']['conversion_rate'] < 5:
            report += "- 转化率偏低，建议优化话术和跟进策略\n"
        if today_income == 0:
            report += "- 今日无收入，建议加大推广力度\n"
        if today_customers < 3:
            report += "- 新增客户较少，建议增加内容发布频率\n"

        report += f"\n{'='*50}\n"

        # 保存报告
        report_dir = os.path.join(self.base_dir, 'reports')
        os.makedirs(report_dir, exist_ok=True)
        report_file = os.path.join(report_dir, f'daily_report_{today}.md')

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(report)
        return report

    def run_daily_tasks(self):
        """运行每日任务"""
        print(f"\n🚀 开始执行每日任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)

        # 1. 生成内容计划
        print("\n📝 生成内容计划...")
        self.generate_daily_content()

        # 2. 设置推广活动
        print("\n🎁 设置推广活动...")
        self.generate_promotion_plan()

        # 3. 生成报告
        print("\n📊 生成每日报告...")
        self.generate_daily_report()

        print("\n✅ 所有任务完成！")

def main():
    """主函数"""
    system = PassiveIncomeSystem()

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   💰 被动收入自动化系统 💰                                      ║
║                                                               ║
║   功能菜单:                                                    ║
║   1. 运行每日任务                                              ║
║   2. 添加客户                                                  ║
║   3. 创建订单                                                  ║
║   4. 查看统计                                                  ║
║   5. 生成报告                                                  ║
║   6. 获取自动回复模板                                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    choice = input("请选择功能 (1-6): ")

    if choice == '1':
        system.run_daily_tasks()
    elif choice == '2':
        name = input("客户名称: ")
        source = input("来源 (xiaohongshu/zhihu/wechat/douyin): ")
        contact = input("联系方式: ")
        system.add_customer(name, source, contact)
    elif choice == '3':
        customer_id = int(input("客户ID: "))
        product = input("产品名称: ")
        price = float(input("价格: "))
        payment = input("支付方式 (wechat/alipay): ")
        system.add_order(customer_id, product, price, payment)
    elif choice == '4':
        rate = system.calculate_conversion_rate()
        print(f"\n📊 统计信息:")
        print(f"  总客户数: {len(system.data['customers'])}")
        print(f"  总订单数: {len(system.data['orders'])}")
        print(f"  总收入: ¥{system.data['stats']['total_income']}")
        print(f"  转化率: {rate}%")
    elif choice == '5':
        system.generate_daily_report()
    elif choice == '6':
        platform = input("平台 (xiaohongshu/zhihu/wechat): ")
        msg_type = input("消息类型 (comment/dm/inquiry): ")
        reply = system.auto_reply_template(platform, msg_type)
        print(f"\n自动回复模板:\n{reply}")

if __name__ == '__main__':
    main()
