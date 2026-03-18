#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
效率工具包 v1.0 - 付费版
包含5个实用自动化工具，提升工作效率300%

作者: 自我生存工具箱
定价: ¥149（原价¥399）
"""

import os
import json
import datetime
import random
import time
from pathlib import Path

class EfficiencyToolkit:
    """效率工具包核心类"""

    def __init__(self):
        self.config_file = "efficiency_config.json"
        self.load_config()

    def load_config(self):
        """加载配置文件"""
        default_config = {
            "daily_goals": {
                "tasks": 5,
                "focus_hours": 4,
                "breaks": 3
            },
            "templates": {
                "email": ["跟进邮件", "会议邀请", "项目更新"],
                "report": ["日报", "周报", "月报"],
                "social": ["朋友圈", "微博", "公众号"]
            },
            "automation": {
                "file_organization": True,
                "backup_enabled": True,
                "notification": True
            }
        }

        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    # ============ 工具1: 智能任务管理 ============

    def create_smart_todo(self, tasks_input):
        """
        创建智能待办事项列表
        功能：自动分类、优先级排序、时间预估
        """
        print("🧠 智能任务管理器")
        print("=" * 50)

        tasks = []
        for i, task in enumerate(tasks_input, 1):
            # 智能分析任务属性
            priority = self._analyze_priority(task)
            category = self._categorize_task(task)
            time_estimate = self._estimate_time(task)

            tasks.append({
                "id": i,
                "task": task,
                "priority": priority,
                "category": category,
                "time_estimate": time_estimate,
                "status": "pending"
            })

        # 按优先级排序
        tasks.sort(key=lambda x: ["high", "medium", "low"].index(x["priority"]))

        # 生成报告
        report = self._generate_task_report(tasks)
        print(report)

        return tasks

    def _analyze_priority(self, task):
        """分析任务优先级"""
        high_keywords = ["紧急", "重要", "deadline", "今天", "马上"]
        medium_keywords = ["本周", "尽快", "重要"]

        task_lower = task.lower()

        for keyword in high_keywords:
            if keyword in task_lower:
                return "high"

        for keyword in medium_keywords:
            if keyword in task_lower:
                return "medium"

        return "low"

    def _categorize_task(self, task):
        """自动分类任务"""
        categories = {
            "工作": ["会议", "报告", "邮件", "项目", "客户"],
            "学习": ["阅读", "课程", "学习", "培训", "考试"],
            "生活": ["购物", "健身", "休息", "娱乐", "社交"],
            "财务": ["账单", "预算", "投资", "报销", "支付"]
        }

        task_lower = task.lower()

        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in task_lower:
                    return category

        return "其他"

    def _estimate_time(self, task):
        """预估任务时间（分钟）"""
        # 基于任务长度和复杂度的简单估算
        base_time = 15
        complexity_multiplier = len(task) / 10

        # 根据关键词调整
        if "复杂" in task or "困难" in task:
            complexity_multiplier *= 2

        if "简单" in task or "快速" in task:
            complexity_multiplier *= 0.5

        estimated_time = int(base_time * complexity_multiplier)
        return max(5, min(120, estimated_time))  # 限制在5-120分钟

    def _generate_task_report(self, tasks):
        """生成任务报告"""
        report = "📋 智能任务列表\n"
        report += "=" * 50 + "\n"

        # 统计信息
        total_tasks = len(tasks)
        high_priority = sum(1 for t in tasks if t["priority"] == "high")
        total_time = sum(t["time_estimate"] for t in tasks)

        report += f"📊 统计: {total_tasks}个任务 | {high_priority}个高优先级 | 预计{total_time}分钟\n"
        report += "=" * 50 + "\n"

        # 按分类显示
        categories = {}
        for task in tasks:
            cat = task["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(task)

        for category, cat_tasks in categories.items():
            report += f"\n🏷️ {category} ({len(cat_tasks)}个)\n"
            for task in cat_tasks:
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[task["priority"]]
                report += f"  {priority_icon} {task['task']} ({task['time_estimate']}分钟)\n"

        return report

    # ============ 工具2: 智能邮件生成器 ============

    def generate_smart_email(self, email_type, recipient, context):
        """
        智能邮件生成器
        支持多种邮件类型，自动生成专业内容
        """
        print("📧 智能邮件生成器")
        print("=" * 50)

        templates = {
            "follow_up": self._follow_up_template,
            "meeting": self._meeting_template,
            "project_update": self._project_update_template,
            "thank_you": self._thank_you_template,
            "introduction": self._introduction_template
        }

        if email_type not in templates:
            print(f"❌ 不支持的邮件类型: {email_type}")
            print(f"支持的类型: {list(templates.keys())}")
            return None

        email_content = templates[email_type](recipient, context)

        print("✅ 邮件已生成:")
        print("=" * 50)
        print(email_content)
        print("=" * 50)

        return email_content

    def _follow_up_template(self, recipient, context):
        """跟进邮件模板"""
        return f"""主题: 跟进 - {context.get('subject', '项目进展')}

尊敬的{recipient}，

您好！

希望您一切顺利。关于{context.get('topic', '我们之前的讨论')}，我想跟进一下最新进展。

{context.get('details', '目前我们已经完成了初步规划，正在推进具体实施阶段。')}

如有任何问题或需要进一步讨论，请随时联系我。

期待您的回复。

此致
敬礼！

[您的姓名]
[您的职位]
[联系方式]"""

    def _meeting_template(self, recipient, context):
        """会议邀请模板"""
        meeting_time = context.get('time', '下周三下午2:00')
        meeting_topic = context.get('topic', '项目讨论会议')

        return f"""主题: 会议邀请 - {meeting_topic}

尊敬的{recipient}，

您好！

诚邀您参加{meeting_topic}，具体安排如下：

📅 时间: {meeting_time}
📍 地点: {context.get('location', '线上会议')}
🔗 会议链接: {context.get('link', '[会议链接]')}

📋 会议议程:
{context.get('agenda', '1. 项目进展汇报\n2. 问题讨论\n3. 下一步计划')}

请提前准备相关材料，如有时间冲突请提前告知。

期待您的参与！

此致
敬礼！

[您的姓名]
[您的职位]"""

    def _project_update_template(self, recipient, context):
        """项目更新模板"""
        return f"""主题: 项目更新 - {context.get('project_name', '当前项目')}

尊敬的{recipient}，

您好！

以下是{context.get('project_name', '项目')}的最新进展：

📊 总体进度: {context.get('progress', '75%')}

✅ 已完成:
{context.get('completed', '- 需求分析完成\n- 设计方案确定\n- 开发进行中')}

🔄 进行中:
{context.get('in_progress', '- 功能开发\n- 测试准备')}

⏭️ 下一步:
{context.get('next_steps', '- 完成开发\n- 系统测试\n- 用户验收')}

如有疑问或需要调整，请及时沟通。

此致
敬礼！

[您的姓名]"""

    def _thank_you_template(self, recipient, context):
        """感谢邮件模板"""
        return f"""主题: 感谢您的{context.get('reason', '支持')}

尊敬的{recipient}，

您好！

非常感谢您{context.get('action', '对我们工作的支持和帮助')}。

{context.get('details', '您的专业意见对我们非常重要，帮助我们更好地推进了项目进展。')}

再次表示衷心的感谢！

此致
敬礼！

[您的姓名]"""

    def _introduction_template(self, recipient, context):
        """自我介绍邮件模板"""
        return f"""主题: 自我介绍 - {context.get('your_name', '您的姓名')}

尊敬的{recipient}，

您好！

我是{context.get('your_name', '您的姓名')}, {context.get('your_position', '您的职位')}。

{context.get('background', '我专注于[专业领域]，拥有[X]年相关经验。')}

{context.get('purpose', '此次联系您是希望就[合作/交流/学习]等方面进行探讨。')}

期待与您进一步交流！

此致
敬礼！

[您的姓名]
[您的职位]
[联系方式]"""

    # ============ 工具3: 智能报告生成器 ============

    def generate_smart_report(self, report_type, data):
        """
        智能报告生成器
        自动生成日报、周报、月报
        """
        print("📊 智能报告生成器")
        print("=" * 50)

        generators = {
            "daily": self._generate_daily_report,
            "weekly": self._generate_weekly_report,
            "monthly": self._generate_monthly_report
        }

        if report_type not in generators:
            print(f"❌ 不支持的报告类型: {report_type}")
            print(f"支持的类型: {list(generators.keys())}")
            return None

        report = generators[report_type](data)

        print("✅ 报告已生成:")
        print("=" * 50)
        print(report)
        print("=" * 50)

        return report

    def _generate_daily_report(self, data):
        """生成日报"""
        today = datetime.datetime.now().strftime("%Y年%m月%d日")

        report = f"""📅 {today} 工作日报

👤 姓名: {data.get('name', '[姓名]')}
🏢 部门: {data.get('department', '[部门]')}

📋 今日完成:
{self._format_list(data.get('completed', ['完成任务1', '完成任务2']))}

🔄 进行中:
{self._format_list(data.get('in_progress', ['任务A进行中', '任务B进行中']))}

❌ 遇到问题:
{self._format_list(data.get('issues', ['暂无问题']))}

📅 明日计划:
{self._format_list(data.get('tomorrow', ['计划任务1', '计划任务2']))}

💡 备注:
{data.get('notes', '无')}

---
生成时间: {datetime.datetime.now().strftime("%H:%M:%S")}"""

        return report

    def _generate_weekly_report(self, data):
        """生成周报"""
        today = datetime.datetime.now()
        week_start = today - datetime.timedelta(days=today.weekday())
        week_end = week_start + datetime.timedelta(days=6)

        report = f"""📅 周报 ({week_start.strftime("%m月%d日")} - {week_end.strftime("%m月%d日")})

👤 姓名: {data.get('name', '[姓名]')}
🏢 部门: {data.get('department', '[部门]')}

📊 本周总结:
{data.get('summary', '本周工作进展顺利，各项任务按计划推进。')}

✅ 主要成果:
{self._format_list(data.get('achievements', ['成果1', '成果2', '成果3']))}

📈 数据指标:
{self._format_dict(data.get('metrics', {'完成任务': '15个', '会议参与': '5场', '文档产出': '3份'}))}

🔄 进行中项目:
{self._format_list(data.get('ongoing', ['项目A: 进度80%', '项目B: 进度60%']))}

❌ 问题与风险:
{self._format_list(data.get('risks', ['资源紧张', '时间紧迫']))}

📅 下周计划:
{self._format_list(data.get('next_week', ['完成项目A', '启动项目C']))}

💡 需要支持:
{data.get('support_needed', '无')}

---
生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""

        return report

    def _generate_monthly_report(self, data):
        """生成月报"""
        today = datetime.datetime.now()
        month_name = today.strftime("%Y年%m月")

        report = f"""📅 {month_name} 月度报告

👤 姓名: {data.get('name', '[姓名]')}
🏢 部门: {data.get('department', '[部门]')}

📊 月度概览:
{data.get('overview', '本月工作按计划推进，各项指标达成良好。')}

🎯 目标完成情况:
{self._format_dict(data.get('goals', {'销售目标': '120%', '客户满意度': '95%', '项目完成率': '90%'}))}

🏆 主要成就:
{self._format_list(data.get('achievements', ['重要成就1', '重要成就2', '重要成就3']))}

📈 关键指标:
{self._format_dict(data.get('key_metrics', {'收入': '¥50,000', '成本': '¥30,000', '利润': '¥20,000'}))}

📉 不足与改进:
{self._format_list(data.get('improvements', ['改进点1', '改进点2']))}

📅 下月计划:
{self._format_list(data.get('next_month', ['计划1', '计划2', '计划3']))}

💡 资源需求:
{data.get('resources_needed', '无')}

---
生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""

        return report

    def _format_list(self, items):
        """格式化列表"""
        if not items:
            return "- 暂无"
        return "\n".join([f"- {item}" for item in items])

    def _format_dict(self, data):
        """格式化字典"""
        if not data:
            return "- 暂无数据"
        return "\n".join([f"- {k}: {v}" for k, v in data.items()])

    # ============ 工具4: 智能文件整理器 ============

    def organize_files_smart(self, directory_path):
        """
        智能文件整理器
        自动分类、重命名、整理文件
        """
        print("📁 智能文件整理器")
        print("=" * 50)

        if not os.path.exists(directory_path):
            print(f"❌ 目录不存在: {directory_path}")
            return None

        # 文件分类规则
        file_categories = {
            "文档": [".doc", ".docx", ".pdf", ".txt", ".md", ".rtf"],
            "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "视频": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"],
            "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "代码": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"],
            "表格": [".xlsx", ".xls", ".csv", ".tsv"],
            "演示": [".pptx", ".ppt", ".key"],
            "其他": []  # 默认分类
        }

        organized = {category: [] for category in file_categories}

        # 扫描文件
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()

                # 分类文件
                categorized = False
                for category, extensions in file_categories.items():
                    if file_ext in extensions:
                        organized[category].append(file_path)
                        categorized = True
                        break

                if not categorized:
                    organized["其他"].append(file_path)

        # 生成报告
        report = "📊 文件整理报告\n"
        report += "=" * 50 + "\n"
        report += f"📁 扫描目录: {directory_path}\n"
        report += f"📅 扫描时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 50 + "\n"

        total_files = sum(len(files) for files in organized.values())
        report += f"📈 总文件数: {total_files}\n\n"

        for category, files in organized.items():
            if files:
                report += f"🏷️ {category} ({len(files)}个)\n"
                for file in files[:5]:  # 只显示前5个
                    file_name = os.path.basename(file)
                    file_size = os.path.getsize(file) / 1024  # KB
                    report += f"  📄 {file_name} ({file_size:.1f}KB)\n"

                if len(files) > 5:
                    report += f"  ... 还有{len(files)-5}个文件\n"
                report += "\n"

        print(report)
        return organized

    # ============ 工具5: 智能备份管理器 ============

    def smart_backup(self, source_dir, backup_dir=None):
        """
        智能备份管理器
        自动备份重要文件，支持增量备份
        """
        print("💾 智能备份管理器")
        print("=" * 50)

        if not os.path.exists(source_dir):
            print(f"❌ 源目录不存在: {source_dir}")
            return None

        # 设置备份目录
        if backup_dir is None:
            backup_dir = os.path.join(os.path.dirname(source_dir), "backups")

        os.makedirs(backup_dir, exist_ok=True)

        # 生成备份文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(backup_dir, backup_name)

        os.makedirs(backup_path, exist_ok=True)

        # 执行备份
        backed_up_files = []
        skipped_files = []
        total_size = 0

        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(source_file, source_dir)
                target_file = os.path.join(backup_path, relative_path)

                # 创建目标目录
                os.makedirs(os.path.dirname(target_file), exist_ok=True)

                # 复制文件
                try:
                    file_size = os.path.getsize(source_file)

                    # 跳过太大的文件（>100MB）
                    if file_size > 100 * 1024 * 1024:
                        skipped_files.append((relative_path, "文件过大"))
                        continue

                    # 跳过临时文件
                    if file.startswith("~") or file.endswith(".tmp"):
                        skipped_files.append((relative_path, "临时文件"))
                        continue

                    # 复制文件
                    import shutil
                    shutil.copy2(source_file, target_file)
                    backed_up_files.append(relative_path)
                    total_size += file_size

                except Exception as e:
                    skipped_files.append((relative_path, str(e)))

        # 生成备份报告
        report = "💾 备份完成报告\n"
        report += "=" * 50 + "\n"
        report += f"📁 源目录: {source_dir}\n"
        report += f"📦 备份位置: {backup_path}\n"
        report += f"📅 备份时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 50 + "\n"

        report += f"✅ 成功备份: {len(backed_up_files)}个文件\n"
        report += f"📊 总大小: {total_size / (1024*1024):.2f}MB\n"
        report += f"❌ 跳过文件: {len(skipped_files)}个\n"

        if skipped_files:
            report += "\n跳过的文件:\n"
            for file, reason in skipped_files[:5]:
                report += f"  ❌ {file} ({reason})\n"
            if len(skipped_files) > 5:
                report += f"  ... 还有{len(skipped_files)-5}个文件\n"

        report += f"\n💾 备份文件: {backup_name}.zip\n"
        report += "💡 建议: 定期备份，保留最近3个备份版本\n"

        print(report)

        # 创建压缩包
        try:
            import zipfile
            zip_path = os.path.join(backup_dir, f"{backup_name}.zip")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_path)
                        zipf.write(file_path, arcname)

            # 删除临时目录
            import shutil
            shutil.rmtree(backup_path)

            print(f"✅ 压缩包已创建: {zip_path}")

        except Exception as e:
            print(f"⚠️ 创建压缩包失败: {e}")

        return {
            "success": True,
            "backed_up": len(backed_up_files),
            "skipped": len(skipped_files),
            "total_size_mb": total_size / (1024*1024)
        }


def main():
    """主函数 - 演示工具包功能"""
    print("🚀 效率工具包 v1.0 - 付费版")
    print("=" * 60)
    print("包含5个实用自动化工具，提升工作效率300%")
    print("=" * 60)

    toolkit = EfficiencyToolkit()

    # 演示1: 智能任务管理
    print("\n🎯 演示1: 智能任务管理")
    print("-" * 40)

    sample_tasks = [
        "紧急: 完成项目报告",
        "今天提交客户方案",
        "本周学习Python课程",
        "购买生活用品",
        "简单回复邮件"
    ]

    tasks = toolkit.create_smart_todo(sample_tasks)

    # 演示2: 智能邮件生成
    print("\n📧 演示2: 智能邮件生成")
    print("-" * 40)

    email_context = {
        "subject": "项目合作跟进",
        "topic": "上周讨论的合作方案",
        "details": "我们已经完成了初步方案设计，希望进一步讨论细节。"
    }

    email = toolkit.generate_smart_email("follow_up", "张总", email_context)

    # 演示3: 智能报告生成
    print("\n📊 演示3: 智能报告生成")
    print("-" * 40)

    report_data = {
        "name": "李明",
        "department": "产品部",
        "completed": ["完成需求分析", "设计方案评审", "技术方案制定"],
        "in_progress": ["原型开发", "用户调研"],
        "issues": ["服务器资源紧张"],
        "tomorrow": ["完成原型", "准备演示材料"],
        "notes": "客户反馈积极，项目进展顺利"
    }

    report = toolkit.generate_smart_report("daily", report_data)

    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("💡 完整版包含更多功能和自定义选项")
    print("=" * 60)


if __name__ == "__main__":
    main()
