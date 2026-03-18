#!/usr/bin/env python3
"""
智能体2：客户跟进系统
自动管理客户关系、发送跟进消息
"""

import json
import os
from datetime import datetime, timedelta

class CustomerFollowUpBot:
    def __init__(self, data_path="data/customers.json"):
        self.data_path = data_path
        self.customers = self.load_customers()
        self.message_templates = self.load_templates()

    def load_customers(self):
        """加载客户数据"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"leads": [], "customers": [], "vip": []}

    def save_customers(self):
        """保存客户数据"""
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(self.customers, f, ensure_ascii=False, indent=2)

    def load_templates(self):
        """加载消息模板"""
        return {
            "welcome": "您好！感谢关注效率工具包！我是您的专属顾问，有任何问题随时问我~",
            "follow_up": "您好！看到您之前咨询过我们的产品，现在有限时优惠活动，需要了解一下吗？",
            "purchase_thanks": "感谢购买！您的产品已发送，请查收邮件。如有问题随时联系我~",
            "vip_upgrade": "恭喜您升级为VIP客户！享受专属福利和优先支持~",
            "feedback": "使用我们的产品后感觉如何？期待您的反馈，帮助我们做得更好！"
        }

    def add_lead(self, name, contact, source, interest=""):
        """添加潜在客户"""
        lead = {
            "id": len(self.customers["leads"]) + 1,
            "name": name,
            "contact": contact,
            "source": source,
            "interest": interest,
            "created_at": datetime.now().isoformat(),
            "status": "new",
            "notes": []
        }
        self.customers["leads"].append(lead)
        self.save_customers()
        return lead

    def convert_lead_to_customer(self, lead_id, product_purchased):
        """将潜在客户转化为付费客户"""
        lead = None
        for i, l in enumerate(self.customers["leads"]):
            if l["id"] == lead_id:
                lead = self.customers["leads"].pop(i)
                break

        if lead:
            customer = {
                "id": len(self.customers["customers"]) + 1,
                "name": lead["name"],
                "contact": lead["contact"],
                "source": lead["source"],
                "products": [product_purchased],
                "first_purchase": datetime.now().isoformat(),
                "last_purchase": datetime.now().isoformat(),
                "total_spent": product_purchased.get("price", 0),
                "status": "active"
            }
            self.customers["customers"].append(customer)
            self.save_customers()
            return customer
        return None

    def send_follow_up(self, customer_id):
        """发送跟进消息"""
        customer = None
        for c in self.customers["customers"]:
            if c["id"] == customer_id:
                customer = c
                break

        if customer:
            last_purchase = datetime.fromisoformat(customer["last_purchase"])
            days_since = (datetime.now() - last_purchase).days

            if days_since > 30:
                message = self.message_templates["follow_up"]
            elif days_since > 7:
                message = self.message_templates["feedback"]
            else:
                message = self.message_templates["purchase_thanks"]

            # 记录跟进
            follow_up = {
                "date": datetime.now().isoformat(),
                "message": message,
                "days_since_purchase": days_since
            }

            if "follow_ups" not in customer:
                customer["follow_ups"] = []
            customer["follow_ups"].append(follow_up)

            self.save_customers()
            return follow_up
        return None

    def check_for_follow_ups(self):
        """检查需要跟进的客户"""
        now = datetime.now()
        needs_follow_up = []

        for customer in self.customers["customers"]:
            last_purchase = datetime.fromisoformat(customer["last_purchase"])
            days_since = (now - last_purchase).days

            # 7天、30天、90天跟进
            if days_since in [7, 30, 90]:
                needs_follow_up.append({
                    "customer": customer,
                    "days_since": days_since,
                    "message": self.send_follow_up(customer["id"])
                })

        return needs_follow_up

    def generate_report(self):
        """生成客户报告"""
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_leads": len(self.customers["leads"]),
            "total_customers": len(self.customers["customers"]),
            "vip_customers": len(self.customers["vip"]),
            "new_leads_today": 0,
            "conversions_today": 0,
            "revenue_today": 0
        }

        # 统计今日数据
        today = datetime.now().strftime("%Y-%m-%d")
        for lead in self.customers["leads"]:
            if lead["created_at"].startswith(today):
                report["new_leads_today"] += 1

        for customer in self.customers["customers"]:
            if customer["first_purchase"].startswith(today):
                report["conversions_today"] += 1
                report["revenue_today"] += customer["total_spent"]

        return report

if __name__ == "__main__":
    bot = CustomerFollowUpBot()
    report = bot.generate_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))