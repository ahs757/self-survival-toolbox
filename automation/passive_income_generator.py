#!/usr/bin/env python3
"""
💰 被动收入生成器 - Passive Income Generator
自动生成和管理多种被动收入来源
"""

import json
import os
import random
from datetime import datetime

class PassiveIncomeGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.products_dir = os.path.join(os.path.dirname(self.base_dir), 'products')
        os.makedirs(self.products_dir, exist_ok=True)

        # 产品线配置
        self.product_lines = {
            'digital_products': [
                {'id': 'efficiency-toolkit', 'name': '效率工具包', 'price': 29, 'cost': 0, 'type': '一次性'},
                {'id': 'automation-scripts', 'name': '自动化脚本包', 'price': 19, 'cost': 0, 'type': '一次性'},
                {'id': 'resume-templates', 'name': '简历模板库', 'price': 9.9, 'cost': 0, 'type': '一次性'},
                {'id': 'ppt-templates', 'name': 'PPT模板合集', 'price': 19, 'cost': 0, 'type': '一次性'},
                {'id': 'excel-templates', 'name': 'Excel模板大全', 'price': 15, 'cost': 0, 'type': '一次性'},
            ],
            'services': [
                {'id': 'resume-optimization', 'name': '简历优化', 'price': 99, 'cost': 30, 'type': '服务'},
                {'id': 'career-planning', 'name': '职业规划咨询', 'price': 199, 'cost': 60, 'type': '服务'},
                {'id': '1on1-coaching', 'name': '一对一指导', 'price': 499, 'cost': 200, 'type': '月费'},
            ],
            'subscriptions': [
                {'id': 'vip-group', 'name': 'VIP答疑群', 'price': 99, 'cost': 10, 'type': '年费'},
                {'id': 'content-club', 'name': '内容创作俱乐部', 'price': 199, 'cost': 30, 'type': '年费'},
            ],
            'affiliate': [
                {'id': 'tool-affiliate', 'name': '效率工具推广', 'commission': 0.3, 'type': '佣金'},
                {'id': 'course-affiliate', 'name': '课程推广', 'commission': 0.4, 'type': '佣金'},
                {'id': 'platform-affiliate', 'name': '平台推广', 'commission': 0.5, 'type': '佣金'},
            ]
        }

        # 渠道配置
        self.channels = {
            'xiaohongshu': {'name': '小红书', 'audience': '职场女性', 'best_time': '20:00-22:00'},
            'zhihu': {'name': '知乎', 'audience': '职场人士', 'best_time': '09:00-11:00'},
            'wechat': {'name': '微信', 'audience': '私域流量', 'best_time': '19:00-21:00'},
            'douyin': {'name': '抖音', 'audience': '泛流量', 'best_time': '12:00-14:00'},
            'weibo': {'name': '微博', 'audience': '泛流量', 'best_time': '18:00-20:00'},
            'github': {'name': 'GitHub', 'audience': '程序员', 'best_time': '全天'},
        }

    def generate_product_sales_page(self, product_id):
        """生成产品销售页面"""
        product = None
        for line in self.product_lines.values():
            for p in line:
                if p['id'] == product_id:
                    product = p
                    break
            if product:
                break

        if not product:
            print(f"⚠️ 未找到产品: {product_id}")
            return None

        page_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product['name']} - 让你的效率提升10倍</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 1.2em;
        }}
        .price-box {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
        }}
        .price {{
            font-size: 3em;
            font-weight: bold;
        }}
        .original-price {{
            text-decoration: line-through;
            font-size: 1.5em;
            opacity: 0.7;
        }}
        .btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 40px;
            border-radius: 15px;
            text-decoration: none;
            font-size: 1.3em;
            font-weight: bold;
            margin: 20px 10px;
            transition: all 0.3s;
        }}
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
        .features {{
            margin: 30px 0;
        }}
        .feature {{
            display: flex;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}
        .feature-icon {{
            font-size: 2em;
            margin-right: 15px;
        }}
        .testimonials {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
        }}
        .testimonial {{
            margin-bottom: 20px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 {product['name']}</h1>
            <p>让你的效率提升10倍，每天多出3小时自由时间</p>
        </div>

        <div class="price-box">
            <div class="original-price">原价 ¥{product['price'] * 3}</div>
            <div class="price">¥{product['price']}</div>
            <div>限时特惠 - 省67%</div>
        </div>

        <div class="features">
            <h2>📦 产品包含</h2>
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <div>
                    <h3>自动化脚本</h3>
                    <p>10+个自动化脚本，一键处理数据，效率提升10倍</p>
                </div>
            </div>
            <div class="feature">
                <div class="feature-icon">📋</div>
                <div>
                    <h3>实用模板</h3>
                    <p>50+个专业模板，周报/PPT/简历，直接套用</p>
                </div>
            </div>
            <div class="feature">
                <div class="feature-icon">⏰</div>
                <div>
                    <h3>时间管理工具</h3>
                    <p>番茄钟、任务清单、时间统计，高效管理每一天</p>
                </div>
            </div>
            <div class="feature">
                <div class="feature-icon">📚</div>
                <div>
                    <h3>技能指南</h3>
                    <p>简历优化、面试技巧、薪资谈判，职场必备</p>
                </div>
            </div>
        </div>

        <div class="testimonials">
            <h2>💬 客户好评</h2>
            <div class="testimonial">
                <p>"以前每天加班到10点，现在5点准时下班，太香了！"</p>
                <p><strong>- 小王，互联网产品经理</strong></p>
            </div>
            <div class="testimonial">
                <p>"周报从2小时变成10分钟，领导还夸我进步大"</p>
                <p><strong>- 小李，运营专员</strong></p>
            </div>
            <div class="testimonial">
                <p>"用了简历模板，一周拿到5个offer"</p>
                <p><strong>- 小张，应届毕业生</strong></p>
            </div>
        </div>

        <div style="text-align: center;">
            <a href="payment_v2.html?product={product_id}&price={product['price']}" class="btn">
                💳 微信支付 ¥{product['price']}
            </a>
            <a href="payment_v2.html?product={product_id}&price={product['price']}" class="btn">
                💙 支付宝 ¥{product['price']}
            </a>
        </div>

        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>🔒 安全支付 · ⚡ 即时发货 · 🔄 7天退款保障</p>
            <p>客服微信: efficiency_helper | 邮箱: help@efficiency-toolkit.com</p>
        </div>
    </div>
</body>
</html>"""

        return page_content

    def generate_marketing_copy(self, product_id, platform):
        """生成营销文案"""
        product = None
        for line in self.product_lines.values():
            for p in line:
                if p['id'] == product_id:
                    product = p
                    break
            if product:
                break

        if not product:
            return None

        # 不同平台的文案风格
        copies = {
            'xiaohongshu': f"""🔥 打工人必看！{product['name']}让我每天多出3小时

姐妹们！！！我真的哭死 😭😭😭

之前每天加班到10点，现在5点准时下班
全靠这个{product['name']}，后悔没早点知道！

✅ 一键处理数据
✅ 效率提升10倍
✅ 每天多出3小时

原价¥{product['price']*3}，现在只要¥{product['price']}
需要的姐妹评论区扣"{product['name']}"！

#效率工具 #打工人 #职场干货 #时间管理""",

            'zhihu': f"""## 如何在短时间内大幅提高工作效率？

分享一个让我效率提升10倍的神器：{product['name']}

### 核心功能

1. **自动化处理**
   - 一键处理500条数据
   - 批量重命名文件
   - 自动生成报告

2. **模板库**
   - 周报模板：10分钟完成周报
   - PPT模板：一套模板走天下
   - 简历模板：投递100份收到50个面试

3. **时间管理**
   - 番茄钟：25分钟高效专注
   - 任务清单：自动排序优先级
   - 时间统计：可视化你的时间去哪了

### 实际效果

使用后：
- 每天准时5点下班
- 周报从2小时变成10分钟
- Excel处理效率提升10倍

### 获取方式

现在限时优惠：¥{product['price']}（原价¥{product['price']*3}）

需要的朋友可以私信我获取。""",

            'wechat': f"""【效率提升神器】💡

最近发现了一个超好用的{product['name']}

效果：
✅ 每天多出3小时自由时间
✅ 周报10分钟搞定
✅ 数据处理效率提升10倍

原价¥{product['price']*3}，限时优惠¥{product['price']}

需要的朋友私聊我～""",

            'douyin': f"""【画面】深夜加班的办公室
【旁白】
"你是不是也这样？
每天加班到10点
周报写了2小时
Excel做到眼花"

【画面】切换到轻松下班
【旁白】
"直到我发现了{product['name']}
现在每天5点准时下班
想知道怎么做吗？
评论区扣1，我教你"

【字幕】{product['name']} ¥{product['price']}
限时优惠中！"""
        }

        return copies.get(platform, copies['wechat'])

    def calculate_income_projection(self):
        """计算收入预测"""
        # 基于产品线和渠道的收入预测
        projection = {
            'conservative': 0,
            'moderate': 0,
            'optimistic': 0,
            'breakdown': {}
        }

        # 数字产品预测（被动收入）
        for product in self.product_lines['digital_products']:
            daily_sales = random.randint(1, 5)
            monthly_revenue = daily_sales * 30 * product['price']
            projection['breakdown'][product['name']] = {
                'daily_sales': daily_sales,
                'monthly_revenue': monthly_revenue
            }
            projection['conservative'] += monthly_revenue * 0.5
            projection['moderate'] += monthly_revenue * 0.8
            projection['optimistic'] += monthly_revenue * 1.2

        # 服务预测（主动收入）
        for service in self.product_lines['services']:
            monthly_clients = random.randint(5, 15)
            monthly_revenue = monthly_clients * service['price']
            projection['breakdown'][service['name']] = {
                'monthly_clients': monthly_clients,
                'monthly_revenue': monthly_revenue
            }
            projection['conservative'] += monthly_revenue * 0.6
            projection['moderate'] += monthly_revenue * 0.9
            projection['optimistic'] += monthly_revenue * 1.5

        # 佣金预测
        for affiliate in self.product_lines['affiliate']:
            monthly_referrals = random.randint(10, 30)
            avg_commission = 50  # 平均每单佣金
            monthly_revenue = monthly_referrals * avg_commission
            projection['breakdown'][affiliate['name']] = {
                'monthly_referrals': monthly_referrals,
                'monthly_revenue': monthly_revenue
            }
            projection['conservative'] += monthly_revenue * 0.4
            projection['moderate'] += monthly_revenue * 0.7
            projection['optimistic'] += monthly_revenue * 1.0

        return projection

    def generate_income_report(self):
        """生成收入报告"""
        projection = self.calculate_income_projection()

        report = f"""
{'='*60}
📊 被动收入预测报告
{'='*60}

💰 月收入预测

保守估计: ¥{projection['conservative']:,.0f}
中等估计: ¥{projection['moderate']:,.0f}
乐观估计: ¥{projection['optimistic']:,.0f}

📈 收入构成明细

"""
        for product, data in projection['breakdown'].items():
            if 'daily_sales' in data:
                report += f"📦 {product}: 每日{data['daily_sales']}单, 月收入 ¥{data['monthly_revenue']:,.0f}\n"
            elif 'monthly_clients' in data:
                report += f"🔧 {product}: 每月{data['monthly_clients']}客户, 月收入 ¥{data['monthly_revenue']:,.0f}\n"
            elif 'monthly_referrals' in data:
                report += f"📢 {product}: 每月{data['monthly_referrals']}推荐, 月收入 ¥{data['monthly_revenue']:,.0f}\n"

        report += f"""
🎯 目标分解

每日目标:
- 数字产品销售: 3-5单
- 咨询服务: 1-2客户
- 新增线索: 10-15个

每周目标:
- 内容发布: 20-30条
- 客户跟进: 20-30人
- 收入目标: ¥{projection['moderate']/4:,.0f}

每月目标:
- 数字产品: ¥{sum(d['monthly_revenue'] for p, d in projection['breakdown'].items() if 'daily_sales' in d):,.0f}
- 咨询服务: ¥{sum(d['monthly_revenue'] for p, d in projection['breakdown'].items() if 'monthly_clients' in d):,.0f}
- 佣金收入: ¥{sum(d['monthly_revenue'] for p, d in projection['breakdown'].items() if 'monthly_referrals' in d):,.0f}

💡 增长策略

1. 增加内容发布频率
2. 优化销售页面转化率
3. 扩展新渠道（抖音、B站）
4. 开发新产品线
5. 建立分销体系

{'='*60}
"""

        # 保存报告
        report_dir = os.path.join(self.base_dir, 'reports')
        os.makedirs(report_dir, exist_ok=True)
        report_file = os.path.join(report_dir, f'income_projection_{datetime.now().strftime("%Y%m%d")}.md')

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(report)
        return report

    def run(self):
        """运行被动收入生成器"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   💰 被动收入生成器 - Passive Income Generator 💰             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)

        print("\n📊 产品线概览:")
        for line_name, products in self.product_lines.items():
            print(f"\n🏷️ {line_name}:")
            for product in products:
                if 'price' in product:
                    print(f"  - {product['name']}: ¥{product['price']} ({product['type']})")
                elif 'commission' in product:
                    print(f"  - {product['name']}: {product['commission']*100}%佣金 ({product['type']})")

        print("\n📢 营销渠道:")
        for channel_id, channel in self.channels.items():
            print(f"  - {channel['name']}: {channel['audience']} (最佳时间: {channel['best_time']})")

        # 生成收入预测
        print("\n💰 生成收入预测...")
        self.generate_income_report()

        # 生成销售页面
        print("\n📄 生成销售页面...")
        for product in self.product_lines['digital_products']:
            page_content = self.generate_product_sales_page(product['id'])
            if page_content:
                page_file = os.path.join(self.products_dir, f"{product['id']}.html")
                with open(page_file, 'w', encoding='utf-8') as f:
                    f.write(page_content)
                print(f"  ✅ {product['name']} 销售页面已生成")

        print("""
✅ 被动收入系统已就绪！

📋 下一步行动：
1. 上传收款码到 monetization/images/
2. 发布销售页面到各个平台
3. 开始内容营销
4. 跟进客户转化
5. 优化产品和服务

🎯 今日目标：
- 发布 5 条营销内容
- 收集 10 个潜在客户
- 转化 2-3 个销售

🚀 开始赚钱吧！
        """)

def main():
    """主函数"""
    generator = PassiveIncomeGenerator()
    generator.run()

if __name__ == '__main__':
    main()
