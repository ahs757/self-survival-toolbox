#!/usr/bin/env python3
"""
自动化内容发布流水线
作者: 自我生存工具箱
版本: 1.0
"""

import os
import json
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
import shutil

class ContentPublisher:
    def __init__(self, config_file=None):
        self.config = self.load_config(config_file)
        self.published_content = []
        self.load_published_history()

    def load_config(self, config_file):
        """加载配置文件"""
        default_config = {
            'content_dir': './content/seo-articles',
            'published_dir': './content/published',
            'draft_dir': './content/drafts',
            'schedule_file': './content/schedule.json',
            'publish_times': {
                'weekday': ['09:00', '12:00', '18:00'],
                'weekend': ['10:00', '15:00']
            },
            'platforms': ['blog', 'wechat', 'zhihu', 'xiaohongshu'],
            'auto_publish': True,
            'backup_before_publish': True
        }

        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def load_published_history(self):
        """加载发布历史"""
        history_file = os.path.join(self.config['published_dir'], 'publish_history.json')
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                self.published_content = json.load(f)

    def save_published_history(self):
        """保存发布历史"""
        history_file = os.path.join(self.config['published_dir'], 'publish_history.json')
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.published_content, f, ensure_ascii=False, indent=2)

    def scan_content(self):
        """扫描待发布内容"""
        content_dir = self.config['content_dir']
        if not os.path.exists(content_dir):
            return []

        articles = []
        for file in os.listdir(content_dir):
            if file.endswith('.md'):
                file_path = os.path.join(content_dir, file)

                # 检查是否已发布
                if self.is_published(file):
                    continue

                # 解析文章信息
                article_info = self.parse_article(file_path)
                if article_info:
                    articles.append(article_info)

        # 按日期排序
        articles.sort(key=lambda x: x.get('publish_date', ''), reverse=True)
        return articles

    def parse_article(self, file_path):
        """解析文章信息"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取标题
            lines = content.split('\n')
            title = ""
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

            # 提取发布日期
            publish_date = ""
            for line in lines:
                if '**发布时间**' in line:
                    # 格式：**发布时间**: 2026年3月18日
                    publish_date = line.split(':', 1)[1].strip()
                    break

            # 提取关键词
            keywords = []
            for line in lines:
                if '**关键词**' in line:
                    keywords_str = line.split(':', 1)[1].strip()
                    keywords = [k.strip() for k in keywords_str.split(',')]
                    break

            # 提取阅读时间
            read_time = ""
            for line in lines:
                if '**阅读时间**' in line:
                    read_time = line.split(':', 1)[1].strip()
                    break

            return {
                'filename': os.path.basename(file_path),
                'path': file_path,
                'title': title,
                'publish_date': publish_date,
                'keywords': keywords,
                'read_time': read_time,
                'content_preview': content[:200] + "..." if len(content) > 200 else content
            }

        except Exception as e:
            print(f"解析文章失败 {file_path}: {e}")
            return None

    def is_published(self, filename):
        """检查文章是否已发布"""
        for item in self.published_content:
            if item['filename'] == filename:
                return True
        return False

    def backup_article(self, article_info):
        """备份文章"""
        if not self.config['backup_before_publish']:
            return True

        try:
            backup_dir = os.path.join(self.config['published_dir'], 'backups')
            os.makedirs(backup_dir, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f"{timestamp}_{article_info['filename']}")

            shutil.copy2(article_info['path'], backup_file)
            print(f"备份完成: {backup_file}")
            return True

        except Exception as e:
            print(f"备份失败: {e}")
            return False

    def publish_to_blog(self, article_info):
        """发布到博客"""
        try:
            # 这里应该调用博客API发布文章
            # 由于需要真实的API，这里只是模拟

            print(f"📝 发布到博客: {article_info['title']}")

            # 模拟发布过程
            time.sleep(2)

            print(f"✅ 博客发布成功")
            return True

        except Exception as e:
            print(f"❌ 博客发布失败: {e}")
            return False

    def publish_to_wechat(self, article_info):
        """发布到微信公众号"""
        try:
            # 这里应该调用微信公众号API
            print(f"📱 发布到微信公众号: {article_info['title']}")

            # 模拟发布过程
            time.sleep(2)

            print(f"✅ 微信公众号发布成功")
            return True

        except Exception as e:
            print(f"❌ 微信公众号发布失败: {e}")
            return False

    def publish_to_zhihu(self, article_info):
        """发布到知乎"""
        try:
            # 这里应该调用知乎API
            print(f"📚 发布到知乎: {article_info['title']}")

            # 模拟发布过程
            time.sleep(2)

            print(f"✅ 知乎发布成功")
            return True

        except Exception as e:
            print(f"❌ 知乎发布失败: {e}")
            return False

    def publish_to_xiaohongshu(self, article_info):
        """发布到小红书"""
        try:
            # 这里应该调用小红书API
            print(f"📕 发布到小红书: {article_info['title']}")

            # 模拟发布过程
            time.sleep(2)

            print(f"✅ 小红书发布成功")
            return True

        except Exception as e:
            print(f"❌ 小红书发布失败: {e}")
            return False

    def publish_article(self, article_info, platforms=None):
        """发布文章到指定平台"""
        if platforms is None:
            platforms = self.config['platforms']

        print(f"🚀 开始发布文章: {article_info['title']}")

        # 备份文章
        if not self.backup_article(article_info):
            print("⚠️ 备份失败，但继续发布")

        results = {}
        for platform in platforms:
            if platform == 'blog':
                results['blog'] = self.publish_to_blog(article_info)
            elif platform == 'wechat':
                results['wechat'] = self.publish_to_wechat(article_info)
            elif platform == 'zhihu':
                results['zhihu'] = self.publish_to_zhihu(article_info)
            elif platform == 'xiaohongshu':
                results['xiaohongshu'] = self.publish_to_xiaohongshu(article_info)

        # 记录发布历史
        publish_record = {
            'filename': article_info['filename'],
            'title': article_info['title'],
            'publish_time': datetime.now().isoformat(),
            'platforms': platforms,
            'results': results
        }

        self.published_content.append(publish_record)
        self.save_published_history()

        # 移动到已发布目录
        self.move_to_published(article_info)

        return results

    def move_to_published(self, article_info):
        """移动文章到已发布目录"""
        try:
            published_dir = self.config['published_dir']
            os.makedirs(published_dir, exist_ok=True)

            target_path = os.path.join(published_dir, article_info['filename'])
            shutil.move(article_info['path'], target_path)

            print(f"📁 文章已移动到: {target_path}")

        except Exception as e:
            print(f"移动文件失败: {e}")

    def schedule_publish(self, article_info, publish_time):
        """定时发布"""
        try:
            schedule_file = self.config['schedule_file']
            if os.path.exists(schedule_file):
                with open(schedule_file, 'r', encoding='utf-8') as f:
                    schedule_data = json.load(f)
            else:
                schedule_data = []

            task = {
                'article': article_info,
                'publish_time': publish_time,
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            }

            schedule_data.append(task)

            with open(schedule_file, 'w', encoding='utf-8') as f:
                json.dump(schedule_data, f, ensure_ascii=False, indent=2)

            print(f"⏰ 定时发布设置成功: {publish_time}")
            return True

        except Exception as e:
            print(f"定时发布设置失败: {e}")
            return False

    def process_scheduled_tasks(self):
        """处理定时任务"""
        schedule_file = self.config['schedule_file']
        if not os.path.exists(schedule_file):
            return

        with open(schedule_file, 'r', encoding='utf-8') as f:
            schedule_data = json.load(f)

        now = datetime.now()
        updated = False

        for task in schedule_data:
            if task['status'] == 'pending':
                publish_time = datetime.fromisoformat(task['publish_time'])

                if now >= publish_time:
                    print(f"⏰ 执行定时发布: {task['article']['title']}")
                    results = self.publish_article(task['article'])
                    task['status'] = 'completed'
                    task['published_at'] = now.isoformat()
                    task['results'] = results
                    updated = True

        if updated:
            with open(schedule_file, 'w', encoding='utf-8') as f:
                json.dump(schedule_data, f, ensure_ascii=False, indent=2)

    def auto_publish_daily(self):
        """每日自动发布"""
        print(f"📅 每日自动发布检查: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # 处理定时任务
        self.process_scheduled_tasks()

        # 扫描待发布内容
        articles = self.scan_content()

        if not articles:
            print("📭 没有待发布内容")
            return

        print(f"📬 找到 {len(articles)} 篇待发布文章")

        # 发布最新的一篇文章
        latest_article = articles[0]
        print(f"📝 准备发布: {latest_article['title']}")

        results = self.publish_article(latest_article)

        success_count = sum(1 for v in results.values() if v)
        print(f"✅ 发布完成: {success_count}/{len(results)} 个平台成功")

    def generate_publish_report(self):
        """生成发布报告"""
        report = f"""
📊 内容发布报告
{'='*40}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📈 发布统计
- 总发布数: {len(self.published_content)}
- 本月发布: {self.get_monthly_count()}
- 本周发布: {self.get_weekly_count()}

📝 最近发布
"""

        # 最近5篇发布
        recent = sorted(self.published_content, key=lambda x: x['publish_time'], reverse=True)[:5]
        for i, item in enumerate(recent, 1):
            report += f"{i}. {item['title']} ({item['publish_time'][:10]})\n"

        report += f"\n📅 待发布内容\n"
        articles = self.scan_content()
        if articles:
            for i, article in enumerate(articles[:5], 1):
                report += f"{i}. {article['title']}\n"
        else:
            report += "暂无待发布内容\n"

        return report.strip()

    def get_monthly_count(self):
        """获取本月发布数量"""
        now = datetime.now()
        count = 0
        for item in self.published_content:
            publish_time = datetime.fromisoformat(item['publish_time'])
            if publish_time.year == now.year and publish_time.month == now.month:
                count += 1
        return count

    def get_weekly_count(self):
        """获取本周发布数量"""
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        count = 0
        for item in self.published_content:
            publish_time = datetime.fromisoformat(item['publish_time'])
            if publish_time >= week_start:
                count += 1
        return count

    def run_automation(self):
        """运行自动化"""
        print("🤖 启动内容发布自动化...")

        # 设置定时任务
        schedule.every().day.at("09:00").do(self.auto_publish_daily)
        schedule.every().day.at("12:00").do(self.auto_publish_daily)
        schedule.every().day.at("18:00").do(self.auto_publish_daily)

        print("⏰ 定时任务设置完成")
        print("🔄 自动化运行中... (按 Ctrl+C 停止)")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n🛑 自动化已停止")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='内容发布自动化工具')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--mode', choices=['scan', 'publish', 'schedule', 'report', 'auto'],
                       default='scan', help='运行模式')
    parser.add_argument('--file', help='指定文章文件')
    parser.add_argument('--platforms', nargs='+', help='目标平台')
    parser.add_argument('--schedule-time', help='定时发布时间')

    args = parser.parse_args()

    # 创建内容发布器
    publisher = ContentPublisher(args.config)

    try:
        if args.mode == 'scan':
            # 扫描待发布内容
            articles = publisher.scan_content()
            print(f"找到 {len(articles)} 篇待发布文章:")
            for i, article in enumerate(articles, 1):
                print(f"{i}. {article['title']} ({article['publish_date']})")

        elif args.mode == 'publish':
            if args.file:
                # 发布指定文件
                article_info = publisher.parse_article(args.file)
                if article_info:
                    publisher.publish_article(article_info, args.platforms)
                else:
                    print("❌ 无法解析文章文件")
            else:
                # 发布最新文章
                articles = publisher.scan_content()
                if articles:
                    publisher.publish_article(articles[0], args.platforms)
                else:
                    print("📭 没有待发布内容")

        elif args.mode == 'schedule':
            if not args.file or not args.schedule_time:
                print("❌ 定时发布需要指定文件和时间")
                return

            article_info = publisher.parse_article(args.file)
            if article_info:
                publisher.schedule_publish(article_info, args.schedule_time)
            else:
                print("❌ 无法解析文章文件")

        elif args.mode == 'report':
            report = publisher.generate_publish_report()
            print(report)

        elif args.mode == 'auto':
            publisher.run_automation()

    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"运行错误: {e}")

if __name__ == '__main__':
    main()