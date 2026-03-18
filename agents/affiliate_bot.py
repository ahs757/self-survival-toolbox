#!/usr/bin/env python3
"""
智能体4：联盟营销系统
管理分销商、跟踪佣金、生成推广链接
"""

import json
import os
import hashlib
from datetime import datetime

class AffiliateMarketingBot:
    def __init__(self, config_path="config/affiliate.json"):
        self.config = self.load_config(config_path)
        self.affiliates = self.load_affiliates()
        self.commissions = []

    def load_config(self, path):
        """加载联盟营销配置"""
        default_config = {
            "commission_rates": {
                "copper": 0.3,
                "silver": 0.35,
                "gold": 0.4,
                "diamond": 0.5
            },
            "tier_thresholds": {
                "copper": 0,
                "silver": 1000,
                "gold": 5000,
                "diamond": 20000
            },
            "min_payout": 100,
            "cookie_duration": 30
        }
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default_config

    def load_affiliates(self):
        """加载分销商数据"""
        path = "data/affiliates.json"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"affiliates": [], "commissions": []}

    def save_affiliates(self):
        """保存分销商数据"""
        os.makedirs("data", exist_ok=True)
        with open("data/affiliates.json", 'w', encoding='utf-8') as f:
            json.dump(self.affiliates, f, ensure_ascii=False, indent=2)

    def register_affiliate(self, name, contact, platform=""):
        """注册新分销商"""
        # 生成唯一推广码
        code = hashlib.md5(f"{name}{datetime.now()}".encode()).hexdigest()[:8].upper()

        affiliate = {
            "id": len(self.affiliates["affiliates"]) + 1,
            "name": name,
            "contact": contact,
            "platform": platform,
            "code": code,
            "tier": "copper",
            "total_earned": 0,
            "total_sales": 0,
            "pending_payout": 0,
            "registered_at": datetime.now().isoformat(),
            "status": "active"
        }

        self.affiliates["affiliates"].append(affiliate)
        self.save_affiliates()
        return affiliate

    def generate_tracking_link(self, affiliate_code, product_id):
        """生成追踪链接"""
        base_url = "https://ahs757.github.io/self-survival-toolbox"
        tracking_url = f"{base_url}/products/{product_id}.html?ref={affiliate_code}"
        return tracking_url

    def record_sale(self, affiliate_code, product_id, amount):
        """记录分销销售"""
        affiliate = None
        for a in self.affiliates["affiliates"]:
            if a["code"] == affiliate_code:
                affiliate = a
                break

        if not affiliate:
            return None

        # 计算佣金
        tier = affiliate["tier"]
        rate = self.config["commission_rates"].get(tier, 0.3)
        commission = amount * rate

        # 记录佣金
        commission_record = {
            "id": len(self.affiliates["commissions"]) + 1,
            "affiliate_id": affiliate["id"],
            "affiliate_code": affiliate_code,
            "product_id": product_id,
            "sale_amount": amount,
            "commission_rate": rate,
            "commission_amount": commission,
            "date": datetime.now().isoformat(),
            "status": "pending"
        }

        self.affiliates["commissions"].append(commission_record)

        # 更新分销商数据
        affiliate["total_earned"] += commission
        affiliate["total_sales"] += amount
        affiliate["pending_payout"] += commission

        # 检查升级
        self.check_tier_upgrade(affiliate)

        self.save_affiliates()
        return commission_record

    def check_tier_upgrade(self, affiliate):
        """检查分销商等级升级"""
        total_earned = affiliate["total_earned"]
        thresholds = self.config["tier_thresholds"]

        new_tier = "copper"
        for tier, threshold in sorted(thresholds.items(), key=lambda x: x[1], reverse=True):
            if total_earned >= threshold:
                new_tier = tier
                break

        if new_tier != affiliate["tier"]:
            affiliate["tier"] = new_tier
            print(f"分销商 {affiliate['name']} 升级为 {new_tier} 等级！")

    def process_payouts(self):
        """处理佣金提现"""
        min_payout = self.config["min_payout"]
        payouts = []

        for affiliate in self.affiliates["affiliates"]:
            if affiliate["pending_payout"] >= min_payout:
                payout = {
                    "affiliate_id": affiliate["id"],
                    "affiliate_name": affiliate["name"],
                    "amount": affiliate["pending_payout"],
                    "date": datetime.now().isoformat(),
                    "status": "processed"
                }
                payouts.append(payout)
                affiliate["pending_payout"] = 0

        self.save_affiliates()
        return payouts

    def generate_affiliate_report(self):
        """生成分销报告"""
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_affiliates": len(self.affiliates["affiliates"]),
            "active_affiliates": len([a for a in self.affiliates["affiliates"] if a["status"] == "active"]),
            "total_commissions_paid": sum(c["commission_amount"] for c in self.affiliates["commissions"] if c["status"] == "paid"),
            "pending_commissions": sum(c["commission_amount"] for c in self.affiliates["commissions"] if c["status"] == "pending"),
            "top_affiliates": []
        }

        # 排序分销商
        sorted_affiliates = sorted(
            self.affiliates["affiliates"],
            key=lambda x: x["total_earned"],
            reverse=True
        )
        report["top_affiliates"] = sorted_affiliates[:10]

        return report

if __name__ == "__main__":
    bot = AffiliateMarketingBot()
    # 注册示例分销商
    affiliate = bot.register_affiliate("测试分销商", "test@example.com", "小红书")
    print(f"注册成功，推广码: {affiliate['code']}")

    # 生成追踪链接
    link = bot.generate_tracking_link(affiliate["code"], "efficiency-toolkit")
    print(f"推广链接: {link}")