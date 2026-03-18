#!/usr/bin/env python3
"""
智能体3：数据分析和优化
分析销售数据、优化营销策略
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class DataAnalyticsBot:
    def __init__(self, data_dir="data/analytics"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def analyze_sales(self, sales_data):
        """分析销售数据"""
        analysis = {
            "total_sales": len(sales_data),
            "total_revenue": sum(s.get("price", 0) for s in sales_data),
            "avg_order_value": 0,
            "top_products": [],
            "sales_by_day": defaultdict(int),
            "sales_by_platform": defaultdict(int)
        }

        if analysis["total_sales"] > 0:
            analysis["avg_order_value"] = analysis["total_revenue"] / analysis["total_sales"]

        # 分析产品表现
        product_sales = defaultdict(lambda: {"count": 0, "revenue": 0})
        for sale in sales_data:
            product = sale.get("product", "unknown")
            price = sale.get("price", 0)
            product_sales[product]["count"] += 1
            product_sales[product]["revenue"] += price

            # 按天统计
            date = sale.get("date", datetime.now().strftime("%Y-%m-%d"))
            analysis["sales_by_day"][date] += price

            # 按平台统计
            platform = sale.get("platform", "unknown")
            analysis["sales_by_platform"][platform] += price

        # 排序产品
        analysis["top_products"] = sorted(
            product_sales.items(),
            key=lambda x: x[1]["revenue"],
            reverse=True
        )

        return analysis

    def optimize_pricing(self, product_data, competitor_data=None):
        """优化定价策略"""
        recommendations = []

        for product, data in product_data.items():
            current_price = data.get("price", 0)
            sales_count = data.get("sales", 0)
            conversion_rate = data.get("conversion_rate", 0)

            # 基于销售表现的定价建议
            if sales_count < 5:
                recommendations.append({
                    "product": product,
                    "action": "降低价格",
                    "reason": "销量太低，建议降价20%",
                    "suggested_price": current_price * 0.8
                })
            elif sales_count > 50 and conversion_rate > 0.05:
                recommendations.append({
                    "product": product,
                    "action": "提高价格",
                    "reason": "销量好且转化率高，可提价10%",
                    "suggested_price": current_price * 1.1
                })
            else:
                recommendations.append({
                    "product": product,
                    "action": "保持价格",
                    "reason": "表现稳定",
                    "suggested_price": current_price
                })

        return recommendations

    def analyze_marketing_channels(self, channel_data):
        """分析营销渠道效果"""
        channel_analysis = []

        for channel, data in channel_data.items():
            cost = data.get("cost", 0)
            revenue = data.get("revenue", 0)
            leads = data.get("leads", 0)
            conversions = data.get("conversions", 0)

            roi = (revenue - cost) / cost if cost > 0 else 0
            conversion_rate = conversions / leads if leads > 0 else 0
            cost_per_lead = cost / leads if leads > 0 else 0

            channel_analysis.append({
                "channel": channel,
                "cost": cost,
                "revenue": revenue,
                "roi": roi,
                "conversion_rate": conversion_rate,
                "cost_per_lead": cost_per_lead,
                "recommendation": self.get_channel_recommendation(roi, conversion_rate)
            })

        return sorted(channel_analysis, key=lambda x: x["roi"], reverse=True)

    def get_channel_recommendation(self, roi, conversion_rate):
        """获取渠道优化建议"""
        if roi > 2:
            return "增加投入"
        elif roi > 0.5:
            return "保持投入"
        elif roi > 0:
            return "优化内容"
        else:
            return "减少投入"

    def generate_daily_report(self, sales_data, channel_data, customer_data):
        """生成每日报告"""
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": {
                "total_sales": len(sales_data),
                "total_revenue": sum(s.get("price", 0) for s in sales_data),
                "new_customers": len([c for c in customer_data if c.get("first_purchase", "").startswith(datetime.now().strftime("%Y-%m-%d"))]),
                "avg_order_value": 0
            },
            "top_performing_products": [],
            "channel_performance": [],
            "recommendations": []
        }

        if report["summary"]["total_sales"] > 0:
            report["summary"]["avg_order_value"] = report["summary"]["total_revenue"] / report["summary"]["total_sales"]

        # 分析销售
        sales_analysis = self.analyze_sales(sales_data)
        report["top_performing_products"] = sales_analysis["top_products"][:5]

        # 分析渠道
        channel_analysis = self.analyze_marketing_channels(channel_data)
        report["channel_performance"] = channel_analysis

        # 生成建议
        if report["summary"]["total_sales"] < 10:
            report["recommendations"].append("增加营销内容发布频率")
        if report["summary"]["avg_order_value"] < 50:
            report["recommendations"].append("推出套餐产品，提高客单价")

        # 保存报告
        self.save_report(report)
        return report

    def save_report(self, report):
        """保存报告"""
        date = report["date"]
        filename = f"{self.data_dir}/report_{date}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return filename

if __name__ == "__main__":
    bot = DataAnalyticsBot()
    # 示例数据
    sample_sales = [
        {"product": "效率工具包", "price": 29, "date": "2026-03-18", "platform": "小红书"},
        {"product": "自动化脚本", "price": 19, "date": "2026-03-18", "platform": "知乎"},
    ]
    analysis = bot.analyze_sales(sample_sales)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))