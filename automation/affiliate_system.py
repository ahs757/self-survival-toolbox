#!/usr/bin/env python3
"""
联盟营销系统
实现分销、返佣、推广链接追踪等功能
"""

import json
import os
import hashlib
import uuid
from datetime import datetime

class AffiliateSystem:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.base_dir, 'affiliate_data.json')
        self.load_data()

    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'affiliates': [],
                'referrals': [],
                'commissions': [],
                'products': [
                    {'id': 'efficiency-toolkit', 'name': '效率工具包', 'price': 29, 'commission_rate': 0.3},
                    {'id': 'automation-scripts', 'name': '自动化脚本包', 'price': 19, 'commission_rate': 0.4},
                    {'id': 'brand-manual', 'name': '个人品牌手册', 'price': 39, 'commission_rate': 0.35},
                    {'id': 'bundle', 'name': '全能套餐', 'price': 129, 'commission_rate': 0.25}
                ],
                'payouts': []
            }
            self.save_data()

    def save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def generate_affiliate_code(self, name):
        """生成推广码"""
        # 使用名字和UUID生成唯一推广码
        raw = f"{name}_{uuid.uuid4().hex[:8]}"
        code = hashlib.md5(raw.encode()).hexdigest()[:8].upper()
        return f"REF_{code}"

    def register_affiliate(self, name, contact, bank_info=None):
        """注册推广员"""
        # 检查是否已注册
        for aff in self.data['affiliates']:
            if aff['contact'] == contact:
                print(f"⚠️ 该联系方式已注册: {contact}")
                return None

        code = self.generate_affiliate_code(name)

        affiliate = {
            'id': len(self.data['affiliates']) + 1,
            'name': name,
            'contact': contact,
            'code': code,
            'bank_info': bank_info,
            'status': 'active',  # active/suspended/banned
            'total_referrals': 0,
            'total_commission': 0,
            'pending_commission': 0,
            'paid_commission': 0,
            'registered_at': datetime.now().isoformat(),
            'tier': 'bronze'  # bronze/silver/gold/diamond
        }

        self.data['affiliates'].append(affiliate)
        self.save_data()

        print(f"""
✅ 推广员注册成功！

👤 姓名: {name}
🔑 推广码: {code}
📊 等级: 铜牌推广员

📝 你的专属推广链接:
https://ahs757.github.io/self-survival-toolbox/?ref={code}

💰 佣金比例:
- 效率工具包: 30% (¥8.7/单)
- 自动化脚本: 40% (¥7.6/单)
- 个人品牌: 35% (¥13.65/单)
- 全能套餐: 25% (¥32.25/单)

分享链接，有人购买你就能赚佣金！
""")
        return affiliate

    def track_referral(self, affiliate_code, product_id, order_amount):
        """追踪推荐"""
        # 查找推广员
        affiliate = None
        for aff in self.data['affiliates']:
            if aff['code'] == affiliate_code:
                affiliate = aff
                break

        if not affiliate:
            print(f"⚠️ 未找到推广码: {affiliate_code}")
            return None

        # 查找产品
        product = None
        for prod in self.data['products']:
            if prod['id'] == product_id:
                product = prod
                break

        if not product:
            print(f"⚠️ 未找到产品: {product_id}")
            return None

        # 计算佣金
        commission_rate = product['commission_rate']
        commission_amount = round(order_amount * commission_rate, 2)

        # 记录推荐
        referral = {
            'id': len(self.data['referrals']) + 1,
            'affiliate_id': affiliate['id'],
            'affiliate_code': affiliate_code,
            'product_id': product_id,
            'product_name': product['name'],
            'order_amount': order_amount,
            'commission_rate': commission_rate,
            'commission_amount': commission_amount,
            'status': 'pending',  # pending/confirmed/paid
            'created_at': datetime.now().isoformat()
        }

        self.data['referrals'].append(referral)

        # 更新推广员统计
        affiliate['total_referrals'] += 1
        affiliate['pending_commission'] += commission_amount
        affiliate['total_commission'] += commission_amount

        # 升级等级
        self.check_tier_upgrade(affiliate)

        self.save_data()

        print(f"""
✅ 推荐记录已创建！

👤 推广员: {affiliate['name']}
📦 产品: {product['name']}
💵 订单金额: ¥{order_amount}
💰 佣金: ¥{commission_amount} ({commission_rate*100}%)
📊 状态: 待确认

推广员当前统计:
- 总推荐数: {affiliate['total_referrals']}
- 待结算佣金: ¥{affiliate['pending_commission']}
- 总佣金: ¥{affiliate['total_commission']}
""")
        return referral

    def check_tier_upgrade(self, affiliate):
        """检查等级升级"""
        total = affiliate['total_commission']

        if total >= 5000:
            new_tier = 'diamond'
            new_rate_bonus = 0.1
        elif total >= 2000:
            new_tier = 'gold'
            new_rate_bonus = 0.05
        elif total >= 500:
            new_tier = 'silver'
            new_rate_bonus = 0.02
        else:
            new_tier = 'bronze'
            new_rate_bonus = 0

        if new_tier != affiliate['tier']:
            old_tier = affiliate['tier']
            affiliate['tier'] = new_tier
            print(f"""
🎉 等级升级！

{affiliate['name']} 从 {old_tier} 升级到 {new_tier}！
佣金比例提升 +{new_rate_bonus*100}%
""")
            return True
        return False

    def confirm_referral(self, referral_id):
        """确认推荐（订单完成）"""
        for ref in self.data['referrals']:
            if ref['id'] == referral_id:
                ref['status'] = 'confirmed'
                ref['confirmed_at'] = datetime.now().isoformat()
                self.save_data()
                print(f"✅ 推荐 #{referral_id} 已确认")
                return ref

        print(f"⚠️ 未找到推荐 #{referral_id}")
        return None

    def payout_commission(self, affiliate_id, amount):
        """结算佣金"""
        affiliate = None
        for aff in self.data['affiliates']:
            if aff['id'] == affiliate_id:
                affiliate = aff
                break

        if not affiliate:
            print(f"⚠️ 未找到推广员 #{affiliate_id}")
            return None

        if amount > affiliate['pending_commission']:
            print(f"⚠️ 结算金额超过待结算佣金 (¥{affiliate['pending_commission']})")
            return None

        payout = {
            'id': len(self.data['payouts']) + 1,
            'affiliate_id': affiliate_id,
            'affiliate_name': affiliate['name'],
            'amount': amount,
            'status': 'completed',
            'created_at': datetime.now().isoformat()
        }

        self.data['payouts'].append(payout)

        # 更新推广员统计
        affiliate['pending_commission'] -= amount
        affiliate['paid_commission'] += amount

        self.save_data()

        print(f"""
💰 佣金结算完成！

👤 推广员: {affiliate['name']}
💵 结算金额: ¥{amount}
📊 待结算余额: ¥{affiliate['pending_commission']}
""")
        return payout

    def get_affiliate_stats(self, affiliate_code):
        """获取推广员统计"""
        affiliate = None
        for aff in self.data['affiliates']:
            if aff['code'] == affiliate_code:
                affiliate = aff
                break

        if not affiliate:
            print(f"⚠️ 未找到推广码: {affiliate_code}")
            return None

        # 统计推荐
        referrals = [r for r in self.data['referrals'] if r['affiliate_code'] == affiliate_code]

        # 按产品统计
        product_stats = {}
        for ref in referrals:
            pid = ref['product_id']
            if pid not in product_stats:
                product_stats[pid] = {'count': 0, 'amount': 0, 'commission': 0}
            product_stats[pid]['count'] += 1
            product_stats[pid]['amount'] += ref['order_amount']
            product_stats[pid]['commission'] += ref['commission_amount']

        print(f"""
📊 推广员统计 - {affiliate['name']}

🔑 推广码: {affiliate['code']}
📈 等级: {affiliate['tier']}

💰 佣金统计:
- 总佣金: ¥{affiliate['total_commission']}
- 待结算: ¥{affiliate['pending_commission']}
- 已结算: ¥{affiliate['paid_commission']}

📦 推荐统计:
- 总推荐数: {affiliate['total_referrals']}
- 成功转化: {len([r for r in referrals if r['status'] == 'confirmed'])}

📋 产品明细:
""")

        for pid, stats in product_stats.items():
            product_name = next((p['name'] for p in self.data['products'] if p['id'] == pid), pid)
            print(f"  {product_name}: {stats['count']}单, ¥{stats['amount']}, 佣金¥{stats['commission']}")

        return affiliate

    def generate_promotion_materials(self, affiliate_code):
        """生成推广素材"""
        affiliate = None
        for aff in self.data['affiliates']:
            if aff['code'] == affiliate_code:
                affiliate = aff
                break

        if not affiliate:
            print(f"⚠️ 未找到推广码: {affiliate_code}")
            return None

        link = f"https://ahs757.github.io/self-survival-toolbox/?ref={affiliate_code}"

        materials = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📢 推广素材包 - {affiliate['name']:^20}                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

🔗 你的专属推广链接:
{link}

📝 朋友圈文案模板:

【模板1 - 干货分享】
分享一个我最近在用的效率工具包
里面有10+自动化脚本，每天省2-3小时
以前加班到10点，现在5点准时下班
需要的朋友点链接了解一下～
👉 {link}

【模板2 - 效果展示】
太香了！用了这个效率工具包
周报从2小时变成10分钟
Excel数据一键处理
简历投出去面试邀约不断
链接放这了，自取～
👉 {link}

【模板3 - 限时优惠】
效率工具包限时特惠！
原价99，现在只要29
包含：自动化脚本+模板库+时间管理工具
需要的抓紧，活动随时结束～
👉 {link}

💬 私聊话术:

你好！看到你对效率提升感兴趣
我这边有个工具包挺不错的
里面有自动化脚本、模板库等
帮你每天省2-3小时
要不要了解一下？
👉 {link}

📱 短视频文案:

【标题】加班到10点的我，发现了这个秘密
【内容】
你是不是也每天加班？
周报写2小时？
Excel做到眼花？
直到我发现了这个方法
现在每天准时下班
想知道怎么做吗？
评论区扣1，链接发你
👉 {link}

📊 产品介绍:

1️⃣ 效率工具包 ¥29 (佣金30%)
- 10+自动化脚本
- 50+实用模板
- 时间管理工具
- 简历优化指南

2️⃣ 自动化脚本包 ¥19 (佣金40%)
- Excel自动化
- 文件批量处理
- 数据分析脚本

3️⃣ 个人品牌手册 ¥39 (佣金35%)
- IP定位方法论
- 内容创作指南
- 变现路径规划

4️⃣ 全能套餐 ¥129 (佣金25%)
- 包含以上所有产品
- 赠送VIP答疑群
- 终身更新

💡 推广技巧:

1. 选择目标人群：打工人、应届生、职场新人
2. 突出痛点：加班、效率低、求职难
3. 展示效果：用数据说话
4. 制造紧迫：限时优惠、限量名额
5. 提供价值：先分享干货，再推荐产品

"""

        # 保存素材
        materials_dir = os.path.join(self.base_dir, 'affiliate_materials')
        os.makedirs(materials_dir, exist_ok=True)
        materials_file = os.path.join(materials_dir, f'materials_{affiliate_code}.txt')

        with open(materials_file, 'w', encoding='utf-8') as f:
            f.write(materials)

        print(materials)
        print(f"\n✅ 推广素材已保存到: {materials_file}")
        return materials

def main():
    """主函数"""
    system = AffiliateSystem()

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🤝 联盟营销系统 🤝                                           ║
║                                                               ║
║   功能菜单:                                                    ║
║   1. 注册推广员                                                ║
║   2. 记录推荐                                                  ║
║   3. 查看推广员统计                                            ║
║   4. 结算佣金                                                  ║
║   5. 生成推广素材                                              ║
║   6. 查看所有推广员                                            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    choice = input("请选择功能 (1-6): ")

    if choice == '1':
        name = input("推广员姓名: ")
        contact = input("联系方式 (微信/手机): ")
        system.register_affiliate(name, contact)

    elif choice == '2':
        code = input("推广码: ")
        product = input("产品ID (efficiency-toolkit/automation-scripts/brand-manual/bundle): ")
        amount = float(input("订单金额: "))
        system.track_referral(code, product, amount)

    elif choice == '3':
        code = input("推广码: ")
        system.get_affiliate_stats(code)

    elif choice == '4':
        affiliate_id = int(input("推广员ID: "))
        amount = float(input("结算金额: "))
        system.payout_commission(affiliate_id, amount)

    elif choice == '5':
        code = input("推广码: ")
        system.generate_promotion_materials(code)

    elif choice == '6':
        print("\n📋 所有推广员列表:")
        for aff in system.data['affiliates']:
            print(f"  [{aff['id']}] {aff['name']} - {aff['code']} - {aff['tier']} - ¥{aff['total_commission']}")

if __name__ == '__main__':
    main()
