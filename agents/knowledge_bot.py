#!/usr/bin/env python3
"""
智能体5：知识付费平台
创建和销售在线课程、电子书、咨询服务
"""

import json
import os
from datetime import datetime, timedelta

class KnowledgeMonetizationBot:
    def __init__(self, config_path="config/knowledge.json"):
        self.config = self.load_config(config_path)
        self.courses = self.load_courses()
        self.ebooks = self.load_ebooks()
        self.consultations = []

    def load_config(self, path):
        """加载知识付费配置"""
        default_config = {
            "course_platforms": ["小鹅通", "知识星球", "腾讯课堂"],
            "ebook_formats": ["PDF", "EPUB", "MOBI"],
            "consultation_rates": {
                "30min": 199,
                "60min": 399,
                "package_3": 999,
                "package_10": 2999
            },
            "royalty_rates": {
                "platform": 0.3,
                "affiliate": 0.2,
                "creator": 0.5
            }
        }
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default_config

    def load_courses(self):
        """加载课程数据"""
        path = "data/courses.json"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"courses": [], "enrollments": []}

    def load_ebooks(self):
        """加载电子书数据"""
        path = "data/ebooks.json"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"ebooks": [], "sales": []}

    def create_course(self, title, description, price, modules):
        """创建新课程"""
        course = {
            "id": len(self.courses["courses"]) + 1,
            "title": title,
            "description": description,
            "price": price,
            "modules": modules,
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "enrollments": 0,
            "revenue": 0
        }

        self.courses["courses"].append(course)
        self.save_courses()
        return course

    def create_ebook(self, title, content_outline, price):
        """创建电子书"""
        ebook = {
            "id": len(self.ebooks["ebooks"]) + 1,
            "title": title,
            "content_outline": content_outline,
            "price": price,
            "formats": self.config["ebook_formats"],
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "sales": 0,
            "revenue": 0
        }

        self.ebooks["ebooks"].append(ebook)
        self.save_ebooks()
        return ebook

    def book_consultation(self, client_name, client_contact, duration="60min"):
        """预订咨询服务"""
        rate = self.config["consultation_rates"].get(duration, 399)

        consultation = {
            "id": len(self.consultations) + 1,
            "client_name": client_name,
            "client_contact": client_contact,
            "duration": duration,
            "rate": rate,
            "booked_at": datetime.now().isoformat(),
            "status": "confirmed"
        }

        self.consultations.append(consultation)
        return consultation

    def save_courses(self):
        """保存课程数据"""
        os.makedirs("data", exist_ok=True)
        with open("data/courses.json", 'w', encoding='utf-8') as f:
            json.dump(self.courses, f, ensure_ascii=False, indent=2)

    def save_ebooks(self):
        """保存电子书数据"""
        os.makedirs("data", exist_ok=True)
        with open("data/ebooks.json", 'w', encoding='utf-8') as f:
            json.dump(self.ebooks, f, ensure_ascii=False, indent=2)

    def generate_knowledge_products(self):
        """生成知识产品创意"""
        products = {
            "courses": [
                {
                    "title": "Python自动化办公从入门到精通",
                    "description": "零基础学会用Python自动化处理Excel、Word、邮件等办公任务",
                    "price": 299,
                    "modules": [
                        "Python基础语法",
                        "Excel自动化处理",
                        "Word文档批量生成",
                        "邮件自动发送",
                        "定时任务自动化"
                    ]
                },
                {
                    "title": "副业赚钱实战营",
                    "description": "从零开始打造被动收入系统",
                    "price": 499,
                    "modules": [
                        "副业选择与定位",
                        "产品设计与开发",
                        "营销推广策略",
                        "客户管理与转化",
                        "自动化运营系统"
                    ]
                }
            ],
            "ebooks": [
                {
                    "title": "效率工具包使用手册",
                    "description": "详细教程和最佳实践",
                    "price": 29
                },
                {
                    "title": "2026年副业赚钱指南",
                    "description": "最新赚钱方法和趋势分析",
                    "price": 19
                }
            ],
            "consultations": [
                {
                    "title": "一对一职业规划",
                    "description": "30分钟深度咨询，制定个人发展计划",
                    "price": 199
                },
                {
                    "title": "副业启动指导",
                    "description": "60分钟实战指导，快速启动你的副业",
                    "price": 399
                }
            ]
        }

        return products

    def create_all_products(self):
        """创建所有知识产品"""
        products = self.generate_knowledge_products()
        created = []

        # 创建课程
        for course_data in products["courses"]:
            course = self.create_course(
                course_data["title"],
                course_data["description"],
                course_data["price"],
                course_data["modules"]
            )
            created.append({"type": "course", "product": course})

        # 创建电子书
        for ebook_data in products["ebooks"]:
            ebook = self.create_ebook(
                ebook_data["title"],
                ebook_data["description"],
                ebook_data["price"]
            )
            created.append({"type": "ebook", "product": ebook})

        return created

if __name__ == "__main__":
    bot = KnowledgeMonetizationBot()
    products = bot.create_all_products()
    print(f"创建了 {len(products)} 个知识产品")
    for p in products:
        print(f"- {p['type']}: {p['product']['title']}")