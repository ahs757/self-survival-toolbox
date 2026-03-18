#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
收入追踪和分析系统
功能：自动追踪收入、分析转化率、生成报告
"""

import json
import datetime
import os
from pathlib import Path

class IncomeTracker:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.income_file = self.base_dir / "automation" / "income_data.json"
        self.analytics_file = self.base_dir / "automation" / "income_analytics.json"
        self.reports_dir = self.base_dir / "automation" / "reports"

        # 确保目录存在
        self.reports_dir.mkdir(exist_ok=True)

        # 加载数据
        self.income_data = self.load_income_data()
        self.analytics = self.load_analytics()

    def load_income_data(self):
        """加载收入数据"""
        if self.income_file.exists():
            with open(self.income_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "transactions": [],
            "daily_summary": {},
            "monthly_summary": {},
            "products": {},
            "traffic_sources": {}
        }

    def load_analytics(self):
        """加载分析数据"""
        if self.analytics_file.exists():
            with open(self.analytics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "total_revenue": 0,
            "total_transactions": 0,
            "average_order_value": 0,
            "conversion_rate": 0,
            "top_products": [],
            "top_traffic_sources": [],
            "daily_trends": [],
            "monthly_trends": []
        }

    def save_data(self):
        """保存数据"""
        with open(self.income_file, 'w', encoding='utf-8') as f:
            json.dump(self.income_data, f, ensure_ascii=False, indent=2)
        with open(self.analytics_file, 'w', encoding='utf-8') as f:
            json.dump(self.analytics, f, ensure_ascii=False, indent=2)

    def record_transaction(self, product, amount, source="直接访问", customer_info=None):
        """记录交易"""
        transaction = {
            "id": f"TXN_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "product": product,
            "amount": amount,
            "source": source,
            "customer_info": customer_info or {},
            "timestamp": datetime.datetime.now().isoformat(),
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "month": datetime.datetime.now().strftime("%Y-%m")
        }

        self.income_data["transactions"].append(transaction)

        # 更新每日汇总
        date_key = transaction["date"]
        if date_key not in self.income_data["daily_summary"]:
            self.income_data["daily_summary"][date_key] = {
                "revenue": 0,
                "transactions": 0,
                "products": {}
            }

        self.income_data["daily_summary"][date_key]["revenue"] += amount
        self.income_data["daily_summary"][date_key]["transactions"] += 1

        if product not in self.income_data["daily_summary"][date_key]["products"]:
            self.income_data["daily_summary"][date_key]["products"][product] = 0
        self.income_data["daily_summary"][date_key]["products"][product] += 1

        # 更新每月汇总
        month_key = transaction["month"]
        if month_key not in self.income_data["monthly_summary"]:
            self.income_data["monthly_summary"][month_key] = {
                "revenue": 0,
                "transactions": 0,
                "products": {}
            }

        self.income_data["monthly_summary"][month_key]["revenue"] += amount
        self.income_data["monthly_summary"][month_key]["transactions"] += 1

        if product not in self.income_data["monthly_summary"][month_key]["products"]:
            self.income_data["monthly_summary"][month_key]["products"][product] = 0
        self.income_data["monthly_summary"][month_key]["products"][product] += 1

        # 更新产品统计
        if product not in self.income_data["products"]:
            self.income_data["products"][product] = {
                "revenue": 0,
                "transactions": 0,
                "average_price": 0
            }

        self.income_data["products"][product]["revenue"] += amount
        self.income_data["products"][product]["transactions"] += 1
        self.income_data["products"][product]["average_price"] = (
            self.income_data["products"][product]["revenue"] /
            self.income_data["products"][product]["transactions"]
        )

        # 更新流量来源统计
        if source not in self.income_data["traffic_sources"]:
            self.income_data["traffic_sources"][source] = {
                "revenue": 0,
                "transactions": 0,
                "conversion_rate": 0
            }

        self.income_data["traffic_sources"][source]["revenue"] += amount
        self.income_data["traffic_sources"][source]["transactions"] += 1

        # 更新分析数据
        self.update_analytics()

        # 保存数据
        self.save_data()

        return transaction

    def update_analytics(self):
        """更新分析数据"""
        transactions = self.income_data["transactions"]

        if not transactions:
            return

        # 总收入和交易数
        self.analytics["total_revenue"] = sum(t["amount"] for t in transactions)
        self.analytics["total_transactions"] = len(transactions)

        # 平均订单价值
        self.analytics["average_order_value"] = (
            self.analytics["total_revenue"] / self.analytics["total_transactions"]
            if self.analytics["total_transactions"] > 0 else 0
        )

        # 产品排名
        products = self.income_data["products"]
        self.analytics["top_products"] = sorted(
            products.items(),
            key=lambda x: x[1]["revenue"],
            reverse=True
        )[:5]

        # 流量来源排名
        traffic_sources = self.income_data["traffic_sources"]
        self.analytics["top_traffic_sources"] = sorted(
            traffic_sources.items(),
            key=lambda x: x[1]["revenue"],
            reverse=True
        )[:5]

        # 每日趋势（最近7天）
        daily_summary = self.income_data["daily_summary"]
        today = datetime.datetime.now()
        daily_trends = []

        for i in range(7):
            date = today - datetime.timedelta(days=i)
            date_key = date.strftime("%Y-%m-%d")
            if date_key in daily_summary:
                daily_trends.append({
                    "date": date_key,
                    "revenue": daily_summary[date_key]["revenue"],
                    "transactions": daily_summary[date_key]["transactions"]
                })
            else:
                daily_trends.append({
                    "date": date_key,
                    "revenue": 0,
                    "transactions": 0
                })

        self.analytics["daily_trends"] = list(reversed(daily_trends))

        # 每月趋势（最近6个月）
        monthly_summary = self.income_data["monthly_summary"]
        monthly_trends = []

        for i in range(6):
            date = today - datetime.timedelta(days=30*i)
            month_key = date.strftime("%Y-%m")
            if month_key in monthly_summary:
                monthly_trends.append({
                    "month": month_key,
                    "revenue": monthly_summary[month_key]["revenue"],
                    "transactions": monthly_summary[month_key]["transactions"]
                })
            else:
                monthly_trends.append({
                    "month": month_key,
                    "revenue": 0,
                    "transactions": 0
                })

        self.analytics["monthly_trends"] = list(reversed(monthly_trends))

    def get_daily_report(self, date=None):
        """获取每日报告"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")

        if date not in self.income_data["daily_summary"]:
            return {
                "date": date,
                "revenue": 0,
                "transactions": 0,
                "products": {},
                "message": "今日暂无收入",
                "daily_target": 500,
                "completion": 0,
                "status": "未达标"
            }

        summary = self.income_data["daily_summary"][date]

        # 计算目标完成度
        daily_target = 500  # 每日目标500元
        completion = (summary["revenue"] / daily_target * 100) if daily_target > 0 else 0

        return {
            "date": date,
            "revenue": summary["revenue"],
            "transactions": summary["transactions"],
            "products": summary["products"],
            "daily_target": daily_target,
            "completion": completion,
            "status": "达标" if completion >= 100 else "未达标"
        }

    def get_monthly_report(self, month=None):
        """获取每月报告"""
        if month is None:
            month = datetime.datetime.now().strftime("%Y-%m")

        if month not in self.income_data["monthly_summary"]:
            return {
                "month": month,
                "revenue": 0,
                "transactions": 0,
                "products": {},
                "message": "本月暂无收入",
                "targets": {
                    "conservative": 500,
                    "ideal": 2000,
                    "challenge": 5000
                },
                "completion": {
                    "conservative": 0,
                    "ideal": 0,
                    "challenge": 0
                },
                "status": "未达标"
            }

        summary = self.income_data["monthly_summary"][month]

        # 计算目标完成度
        monthly_targets = {
            "conservative": 500,   # 保守目标
            "ideal": 2000,         # 理想目标
            "challenge": 5000      # 挑战目标
        }

        completion = {}
        for target_name, target_value in monthly_targets.items():
            completion[target_name] = (summary["revenue"] / target_value * 100) if target_value > 0 else 0

        return {
            "month": month,
            "revenue": summary["revenue"],
            "transactions": summary["transactions"],
            "products": summary["products"],
            "targets": monthly_targets,
            "completion": completion,
            "status": "挑战目标达成" if completion["challenge"] >= 100 else (
                "理想目标达成" if completion["ideal"] >= 100 else (
                    "保守目标达成" if completion["conservative"] >= 100 else "未达标"
                )
            )
        }

    def generate_report(self, report_type="daily", date=None):
        """生成报告文件"""
        if report_type == "daily":
            report = self.get_daily_report(date)
            filename = f"daily_report_{report['date']}.md"
        elif report_type == "monthly":
            report = self.get_monthly_report(date)
            filename = f"monthly_report_{report['month']}.md"
        else:
            raise ValueError("报告类型必须是 'daily' 或 'monthly'")

        # 生成报告内容
        if report_type == "daily":
            content = self._generate_daily_report_content(report)
        else:
            content = self._generate_monthly_report_content(report)

        # 保存报告
        filepath = self.reports_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def _generate_daily_report_content(self, report):
        """生成每日报告内容"""
        avg_order = report['revenue']/report['transactions'] if report['transactions'] > 0 else 0

        return f"""# 📊 每日收入报告

**日期**: {report['date']}
**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 今日业绩

| 指标 | 数值 | 目标 | 完成度 |
|------|------|------|--------|
| 总收入 | ¥{report['revenue']:.2f} | ¥{report['daily_target']:.2f} | {report['completion']:.1f}% |
| 交易数 | {report['transactions']} | - | - |
| 平均订单 | ¥{avg_order:.2f} | - | - |

**状态**: {report['status']}

## 📦 产品销售详情

| 产品 | 销量 | 收入 |
|------|------|------|
"""

        # 添加产品详情
        for product, count in report['products'].items():
            content += f"| {product} | {count} | ¥{count * 29:.2f} |\n"  # 假设平均价格29元

        content += f"""
## 📊 趋势分析

### 最近7天收入趋势
| 日期 | 收入 | 交易数 |
|------|------|--------|
"""

        # 添加趋势数据
        for trend in self.analytics['daily_trends']:
            content += f"| {trend['date']} | ¥{trend['revenue']:.2f} | {trend['transactions']} |\n"

        content += f"""
## 🎯 明日目标

- **收入目标**: ¥{report['daily_target']:.2f}
- **交易目标**: {max(5, report['transactions'] + 2)}单
- **重点产品**: 效率工具包 v2.0

## 💡 改进建议

1. **流量优化**: 增加小红书发布频率
2. **转化优化**: 优化支付页面，减少跳失率
3. **产品优化**: 考虑增加新功能或捆绑销售

---
*报告由自动化收入追踪系统生成*
"""

    def _generate_monthly_report_content(self, report):
        """生成每月报告内容"""
        avg_order = report['revenue']/report['transactions'] if report['transactions'] > 0 else 0

        return f"""# 📊 月度收入报告

**月份**: {report['month']}
**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 月度业绩

| 指标 | 数值 | 保守目标 | 理想目标 | 挑战目标 |
|------|------|----------|----------|----------|
| 总收入 | ¥{report['revenue']:.2f} | ¥{report['targets']['conservative']:.2f} | ¥{report['targets']['ideal']:.2f} | ¥{report['targets']['challenge']:.2f} |
| 完成度 | - | {report['completion']['conservative']:.1f}% | {report['completion']['ideal']:.1f}% | {report['completion']['challenge']:.1f}% |
| 交易数 | {report['transactions']} | - | - | - |
| 平均订单 | ¥{avg_order:.2f} | - | - | - |

**状态**: {report['status']}

## 📦 产品销售详情

| 产品 | 销量 | 收入 | 占比 |
|------|------|------|------|
"""

        # 添加产品详情
        total_revenue = report['revenue']
        for product, count in report['products'].items():
            revenue = count * 29  # 假设平均价格29元
            percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
            content += f"| {product} | {count} | ¥{revenue:.2f} | {percentage:.1f}% |\n"

        content += f"""
## 📊 流量来源分析

| 来源 | 交易数 | 收入 | 转化率 |
|------|--------|------|--------|
"""

        # 添加流量来源数据
        for source, data in self.income_data['traffic_sources'].items():
            content += f"| {source} | {data['transactions']} | ¥{data['revenue']:.2f} | {data['conversion_rate']:.1f}% |\n"

        content += f"""
## 📈 月度趋势

| 月份 | 收入 | 交易数 | 增长率 |
|------|------|--------|--------|
"""

        # 添加月度趋势数据
        for i, trend in enumerate(self.analytics['monthly_trends']):
            if i == 0:
                growth = "0%"
            else:
                prev_revenue = self.analytics['monthly_trends'][i-1]['revenue']
                if prev_revenue > 0:
                    growth = f"{((trend['revenue'] - prev_revenue) / prev_revenue * 100):.1f}%"
                else:
                    growth = "N/A"
            content += f"| {trend['month']} | ¥{trend['revenue']:.2f} | {trend['transactions']} | {growth} |\n"

        content += f"""
## 🎯 下月目标

- **保守目标**: ¥{report['targets']['conservative'] * 1.5:.2f} (增长50%)
- **理想目标**: ¥{report['targets']['ideal'] * 1.5:.2f} (增长50%)
- **挑战目标**: ¥{report['targets']['challenge'] * 1.5:.2f} (增长50%)

## 💡 战略建议

1. **产品策略**:
   - 推出新产品线
   - 优化现有产品功能
   - 考虑订阅模式

2. **营销策略**:
   - 增加内容发布频率
   - 优化SEO关键词
   - 开展促销活动

3. **运营策略**:
   - 提升客户服务质量
   - 建立客户反馈机制
   - 优化交付流程

---
*报告由自动化收入追踪系统生成*
"""

    def simulate_transaction(self):
        """模拟交易（用于测试）"""
        products = [
            ("效率工具包 v2.0", 29),
            ("自动化脚本包", 19),
            ("朋友圈文案库", 9.9),
            ("全能套餐", 39)
        ]

        sources = ["GitHub", "知乎", "小红书", "微信群", "朋友圈", "SEO", "直接访问"]

        product, price = random.choice(products)
        source = random.choice(sources)

        return self.record_transaction(product, price, source)

def main():
    """主函数"""
    tracker = IncomeTracker()

    print("=== 收入追踪和分析系统 ===")
    print(f"当前时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 生成每日报告
    daily_report = tracker.get_daily_report()
    print("📊 今日收入报告:")
    print(f"  - 日期: {daily_report['date']}")
    print(f"  - 收入: ¥{daily_report['revenue']:.2f}")
    print(f"  - 交易数: {daily_report['transactions']}")
    print(f"  - 状态: {daily_report['status']}")
    print()

    # 生成月度报告
    monthly_report = tracker.get_monthly_report()
    print("📈 本月收入报告:")
    print(f"  - 月份: {monthly_report['month']}")
    print(f"  - 收入: ¥{monthly_report['revenue']:.2f}")
    print(f"  - 交易数: {monthly_report['transactions']}")
    print(f"  - 状态: {monthly_report['status']}")
    print()

    # 显示产品排名
    print("🏆 产品销售排名:")
    for i, (product, data) in enumerate(tracker.analytics['top_products'], 1):
        print(f"  {i}. {product}: ¥{data['revenue']:.2f} ({data['transactions']}笔)")
    print()

    # 生成报告文件
    print("📝 正在生成报告文件...")
    daily_file = tracker.generate_report("daily")
    monthly_file = tracker.generate_report("monthly")
    print(f"  - 每日报告: {daily_file}")
    print(f"  - 月度报告: {monthly_file}")
    print()

    # 模拟交易（用于测试）
    print("🧪 模拟交易测试...")
    for i in range(3):
        transaction = tracker.simulate_transaction()
        print(f"  - 交易{i+1}: {transaction['product']} - ¥{transaction['amount']}")
    print()

    print("✨ 收入追踪系统运行完成！")

if __name__ == "__main__":
    import random
    main()
