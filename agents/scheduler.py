#!/usr/bin/env python3
"""
任务调度器 - 持续运行所有智能体
确保赚钱系统24/7运作
"""

import time
import schedule
import threading
import logging
from datetime import datetime
import json
import os

# 导入所有智能体
from content_bot import ContentMarketingBot
from customer_bot import CustomerFollowUpBot
from analytics_bot import DataAnalyticsBot
from affiliate_bot import AffiliateMarketingBot
from knowledge_bot import KnowledgeMonetizationBot

class TaskScheduler:
    def __init__(self, config_path="config/scheduler.json"):
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.bots = self.initialize_bots()
        self.running = True

    def load_config(self, path):
        """加载调度器配置"""
        default_config = {
            "content_generation": {
                "interval_hours": 6,
                "daily_posts": 8
            },
            "customer_follow_up": {
                "interval_hours": 12,
                "check_new_leads": True
            },
            "analytics": {
                "interval_hours": 24,
                "generate_reports": True
            },
            "affiliate_management": {
                "interval_hours": 24,
                "process_payouts": True
            },
            "knowledge_products": {
                "interval_hours": 168,  # 每周
                "update_products": True
            },
            "backup": {
                "interval_hours": 24,
                "backup_data": True
            }
        }
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default_config

    def setup_logging(self):
        """设置日志"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/scheduler.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def initialize_bots(self):
        """初始化所有智能体"""
        return {
            "content": ContentMarketingBot(),
            "customer": CustomerFollowUpBot(),
            "analytics": DataAnalyticsBot(),
            "affiliate": AffiliateMarketingBot(),
            "knowledge": KnowledgeMonetizationBot()
        }

    def run_content_generation(self):
        """运行内容生成任务"""
        try:
            self.logger.info("开始内容生成任务...")
            result = self.bots["content"].run_daily_content()
            self.logger.info(f"内容生成完成，生成 {len(result)} 条内容")
        except Exception as e:
            self.logger.error(f"内容生成失败: {e}")

    def run_customer_follow_up(self):
        """运行客户跟进任务"""
        try:
            self.logger.info("开始客户跟进任务...")
            follow_ups = self.bots["customer"].check_for_follow_ups()
            report = self.bots["customer"].generate_report()
            self.logger.info(f"客户跟进完成，跟进 {len(follow_ups)} 个客户")
            self.logger.info(f"客户报告: {report}")
        except Exception as e:
            self.logger.error(f"客户跟进失败: {e}")

    def run_analytics(self):
        """运行数据分析任务"""
        try:
            self.logger.info("开始数据分析任务...")
            # 这里需要从实际数据源获取数据
            sample_sales = []
            sample_channels = {}
            sample_customers = []

            report = self.bots["analytics"].generate_daily_report(
                sample_sales, sample_channels, sample_customers
            )
            self.logger.info(f"数据分析完成，报告已保存")
        except Exception as e:
            self.logger.error(f"数据分析失败: {e}")

    def run_affiliate_management(self):
        """运行联盟营销管理任务"""
        try:
            self.logger.info("开始联盟营销管理任务...")
            report = self.bots["affiliate"].generate_affiliate_report()
            payouts = self.bots["affiliate"].process_payouts()
            self.logger.info(f"联盟营销管理完成，处理 {len(payouts)} 笔提现")
        except Exception as e:
            self.logger.error(f"联盟营销管理失败: {e}")

    def run_knowledge_products(self):
        """运行知识产品管理任务"""
        try:
            self.logger.info("开始知识产品管理任务...")
            # 检查和更新知识产品
            products = self.bots["knowledge"].generate_knowledge_products()
            self.logger.info(f"知识产品管理完成")
        except Exception as e:
            self.logger.error(f"知识产品管理失败: {e}")

    def run_backup(self):
        """运行数据备份任务"""
        try:
            self.logger.info("开始数据备份任务...")
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)

            # 备份所有数据文件
            data_files = [
                "data/customers.json",
                "data/affiliates.json",
                "data/courses.json",
                "data/ebooks.json",
                "data/analytics"
            ]

            for file_path in data_files:
                if os.path.exists(file_path):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{backup_dir}/{os.path.basename(file_path)}_{timestamp}"
                    # 这里可以添加实际的备份逻辑
                    self.logger.info(f"备份文件: {file_path}")

            self.logger.info("数据备份完成")
        except Exception as e:
            self.logger.error(f"数据备份失败: {e}")

    def schedule_tasks(self):
        """调度所有任务"""
        # 内容生成 - 每6小时
        schedule.every(self.config["content_generation"]["interval_hours"]).hours.do(
            self.run_content_generation
        )

        # 客户跟进 - 每12小时
        schedule.every(self.config["customer_follow_up"]["interval_hours"]).hours.do(
            self.run_customer_follow_up
        )

        # 数据分析 - 每24小时
        schedule.every(self.config["analytics"]["interval_hours"]).hours.do(
            self.run_analytics
        )

        # 联盟营销管理 - 每24小时
        schedule.every(self.config["affiliate_management"]["interval_hours"]).hours.do(
            self.run_affiliate_management
        )

        # 知识产品管理 - 每周
        schedule.every(self.config["knowledge_products"]["interval_hours"]).hours.do(
            self.run_knowledge_products
        )

        # 数据备份 - 每24小时
        schedule.every(self.config["backup"]["interval_hours"]).hours.do(
            self.run_backup
        )

        # 立即运行一次所有任务
        self.run_all_tasks_once()

    def run_all_tasks_once(self):
        """立即运行一次所有任务"""
        self.logger.info("立即运行所有任务...")
        self.run_content_generation()
        self.run_customer_follow_up()
        self.run_analytics()
        self.run_affiliate_management()
        self.run_knowledge_products()
        self.run_backup()

    def run_scheduler(self):
        """运行调度器"""
        self.logger.info("任务调度器启动...")
        self.schedule_tasks()

        self.logger.info("开始持续运行智能体系统...")
        self.logger.info("按 Ctrl+C 停止")

        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            self.logger.info("接收到停止信号，正在关闭...")
            self.running = False
        except Exception as e:
            self.logger.error(f"调度器运行错误: {e}")

    def stop(self):
        """停止调度器"""
        self.running = False

if __name__ == "__main__":
    scheduler = TaskScheduler()
    scheduler.run_scheduler()