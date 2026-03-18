#!/usr/bin/env python3
"""
每日报告生成器 - 自动生成工作日报
作者: 效率工具包
版本: 2.0
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import re

class DailyReportGenerator:
    def __init__(self, config_file=None):
        self.config = self.load_config(config_file)
        self.today = datetime.now()

    def load_config(self, config_file):
        """加载配置文件"""
        default_config = {
            'output_dir': './reports',
            'template': 'default',
            'include_git': True,
            'include_files': True,
            'include_tasks': True,
            'work_hours': {'start': '09:00', 'end': '18:00'},
            'project_dirs': [],
            'git_repos': []
        }

        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def get_git_activity(self, repo_path, days=1):
        """获取Git活动"""
        if not os.path.exists(repo_path):
            return []

        activities = []

        try:
            # 获取提交历史
            since_date = (self.today - timedelta(days=days)).strftime('%Y-%m-%d')
            cmd = [
                'git', '-C', repo_path, 'log',
                '--since', since_date,
                '--pretty=format:%h|%an|%ad|%s',
                '--date=short'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|', 3)
                        if len(parts) == 4:
                            activities.append({
                                'hash': parts[0],
                                'author': parts[1],
                                'date': parts[2],
                                'message': parts[3]
                            })

            # 获取文件变更
            cmd = [
                'git', '-C', repo_path, 'diff',
                '--name-status', f'HEAD~{days}', 'HEAD'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                file_changes = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        status, file_path = line.split('\t', 1)
                        file_changes.append({
                            'status': status,
                            'file': file_path
                        })
                activities.append({'type': 'file_changes', 'changes': file_changes})

        except Exception as e:
            print(f"获取Git活动失败 {repo_path}: {e}")

        return activities

    def get_file_activity(self, directory, days=1):
        """获取文件活动"""
        activities = {
            'created': [],
            'modified': [],
            'deleted': []
        }

        if not os.path.exists(directory):
            return activities

        cutoff_time = (self.today - timedelta(days=days)).timestamp()

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                try:
                    stat = os.stat(file_path)

                    # 创建时间
                    if hasattr(stat, 'st_birthtime'):
                        create_time = stat.st_birthtime
                    else:
                        create_time = stat.st_ctime

                    # 修改时间
                    modify_time = stat.st_mtime

                    if create_time > cutoff_time:
                        activities['created'].append({
                            'file': file_path,
                            'time': datetime.fromtimestamp(create_time)
                        })

                    if modify_time > cutoff_time:
                        activities['modified'].append({
                            'file': file_path,
                            'time': datetime.fromtimestamp(modify_time)
                        })

                except Exception:
                    continue

        return activities

    def get_task_summary(self, task_file=None):
        """获取任务摘要"""
        if not task_file or not os.path.exists(task_file):
            return {
                'completed': [],
                'pending': [],
                'in_progress': []
            }

        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析Markdown任务列表
        tasks = {
            'completed': [],
            'pending': [],
            'in_progress': []
        }

        lines = content.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()

            # 检测章节
            if line.startswith('## '):
                current_section = line[3:].lower()
                continue

            # 检测任务项
            if line.startswith('- [x] '):
                tasks['completed'].append(line[6:])
            elif line.startswith('- [ ] '):
                tasks['pending'].append(line[6:])
            elif line.startswith('- [/] '):
                tasks['in_progress'].append(line[6:])

        return tasks

    def generate_report(self, report_date=None, include_sections=None):
        """生成每日报告"""
        if report_date:
            self.today = datetime.strptime(report_date, '%Y-%m-%d')

        if include_sections is None:
            include_sections = ['summary', 'git', 'files', 'tasks', 'plan']

        report_data = {
            'date': self.today.strftime('%Y-%m-%d'),
            'weekday': self.today.strftime('%A'),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sections': {}
        }

        # 生成各部分内容
        if 'summary' in include_sections:
            report_data['sections']['summary'] = self.generate_summary_section()

        if 'git' in include_sections and self.config['include_git']:
            report_data['sections']['git'] = self.generate_git_section()

        if 'files' in include_sections and self.config['include_files']:
            report_data['sections']['files'] = self.generate_files_section()

        if 'tasks' in include_sections and self.config['include_tasks']:
            report_data['sections']['tasks'] = self.generate_tasks_section()

        if 'plan' in include_sections:
            report_data['sections']['plan'] = self.generate_plan_section()

        return report_data

    def generate_summary_section(self):
        """生成摘要部分"""
        weekday_cn = {
            'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三',
            'Thursday': '星期四', 'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'
        }

        return {
            'date': self.today.strftime('%Y年%m月%d日'),
            'weekday': weekday_cn.get(self.today.strftime('%A'), self.today.strftime('%A')),
            'work_hours': f"{self.config['work_hours']['start']} - {self.config['work_hours']['end']}"
        }

    def generate_git_section(self):
        """生成Git部分"""
        git_activities = {}

        for repo_path in self.config['git_repos']:
            if os.path.exists(repo_path):
                repo_name = os.path.basename(repo_path)
                activities = self.get_git_activity(repo_path)
                if activities:
                    git_activities[repo_name] = activities

        return git_activities

    def generate_files_section(self):
        """生成文件活动部分"""
        file_activities = {}

        for project_dir in self.config['project_dirs']:
            if os.path.exists(project_dir):
                dir_name = os.path.basename(project_dir)
                activities = self.get_file_activity(project_dir)
                file_activities[dir_name] = activities

        return file_activities

    def generate_tasks_section(self):
        """生成任务部分"""
        task_file = self.config.get('task_file')
        return self.get_task_summary(task_file)

    def generate_plan_section(self):
        """生成计划部分"""
        return {
            'today_goals': [
                '完成项目文档编写',
                '代码审查和测试',
                '团队会议和沟通'
            ],
            'priority_tasks': [
                '高优先级：修复生产环境bug',
                '中优先级：完成功能开发',
                '低优先级：优化代码性能'
            ],
            'meetings': [
                '10:00 - 站会',
                '14:00 - 项目评审',
                '16:00 - 技术分享'
            ]
        }

    def format_report_text(self, report_data):
        """格式化文本报告"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"每日工作报告")
        lines.append("=" * 60)
        lines.append(f"日期: {report_data['date']} ({report_data['weekday']})")
        lines.append(f"生成时间: {report_data['generated_at']}")
        lines.append("")

        # 摘要部分
        if 'summary' in report_data['sections']:
            summary = report_data['sections']['summary']
            lines.append("📋 今日概览")
            lines.append("-" * 30)
            lines.append(f"工作时间: {summary['work_hours']}")
            lines.append("")

        # Git活动
        if 'git' in report_data['sections']:
            git = report_data['sections']['git']
            lines.append("🔧 代码提交")
            lines.append("-" * 30)
            for repo_name, activities in git.items():
                lines.append(f"仓库: {repo_name}")
                for activity in activities:
                    if isinstance(activity, dict) and 'message' in activity:
                        lines.append(f"  • {activity['hash']} - {activity['message']}")
                lines.append("")

        # 文件活动
        if 'files' in report_data['sections']:
            files = report_data['sections']['files']
            lines.append("📁 文件变更")
            lines.append("-" * 30)
            for dir_name, activities in files.items():
                if activities['created'] or activities['modified']:
                    lines.append(f"项目: {dir_name}")
                    if activities['created']:
                        lines.append("  新建文件:")
                        for item in activities['created'][:5]:  # 只显示前5个
                            lines.append(f"    + {os.path.basename(item['file'])}")
                    if activities['modified']:
                        lines.append("  修改文件:")
                        for item in activities['modified'][:5]:
                            lines.append(f"    ~ {os.path.basename(item['file'])}")
                    lines.append("")

        # 任务完成情况
        if 'tasks' in report_data['sections']:
            tasks = report_data['sections']['tasks']
            lines.append("✅ 任务完成情况")
            lines.append("-" * 30)
            lines.append(f"已完成: {len(tasks['completed'])} 项")
            for task in tasks['completed'][:5]:
                lines.append(f"  ✓ {task}")
            lines.append(f"进行中: {len(tasks['in_progress'])} 项")
            for task in tasks['in_progress'][:3]:
                lines.append(f"  ⟳ {task}")
            lines.append(f"待办: {len(tasks['pending'])} 项")
            for task in tasks['pending'][:3]:
                lines.append(f"  ○ {task}")
            lines.append("")

        # 明日计划
        if 'plan' in report_data['sections']:
            plan = report_data['sections']['plan']
            lines.append("📅 明日计划")
            lines.append("-" * 30)
            lines.append("目标:")
            for goal in plan['today_goals']:
                lines.append(f"  • {goal}")
            lines.append("优先任务:")
            for task in plan['priority_tasks']:
                lines.append(f"  • {task}")
            lines.append("会议安排:")
            for meeting in plan['meetings']:
                lines.append(f"  • {meeting}")
            lines.append("")

        lines.append("=" * 60)
        lines.append("报告生成完毕")

        return "\n".join(lines)

    def format_report_markdown(self, report_data):
        """格式化Markdown报告"""
        lines = []
        lines.append(f"# 每日工作报告")
        lines.append(f"")
        lines.append(f"**日期**: {report_data['date']} ({report_data['weekday']})")
        lines.append(f"**生成时间**: {report_data['generated_at']}")
        lines.append("")

        # 摘要部分
        if 'summary' in report_data['sections']:
            summary = report_data['sections']['summary']
            lines.append("## 📋 今日概览")
            lines.append(f"- 工作时间: {summary['work_hours']}")
            lines.append("")

        # Git活动
        if 'git' in report_data['sections']:
            git = report_data['sections']['git']
            lines.append("## 🔧 代码提交")
            for repo_name, activities in git.items():
                lines.append(f"### {repo_name}")
                for activity in activities:
                    if isinstance(activity, dict) and 'message' in activity:
                        lines.append(f"- `{activity['hash']}` {activity['message']}")
                lines.append("")

        # 文件活动
        if 'files' in report_data['sections']:
            files = report_data['sections']['files']
            lines.append("## 📁 文件变更")
            for dir_name, activities in files.items():
                if activities['created'] or activities['modified']:
                    lines.append(f"### {dir_name}")
                    if activities['created']:
                        lines.append("**新建文件:**")
                        for item in activities['created'][:5]:
                            lines.append(f"- + {os.path.basename(item['file'])}")
                    if activities['modified']:
                        lines.append("**修改文件:**")
                        for item in activities['modified'][:5]:
                            lines.append(f"- ~ {os.path.basename(item['file'])}")
                    lines.append("")

        # 任务完成情况
        if 'tasks' in report_data['sections']:
            tasks = report_data['sections']['tasks']
            lines.append("## ✅ 任务完成情况")
            lines.append(f"**已完成**: {len(tasks['completed'])} 项")
            for task in tasks['completed'][:5]:
                lines.append(f"- [x] {task}")
            lines.append(f"**进行中**: {len(tasks['in_progress'])} 项")
            for task in tasks['in_progress'][:3]:
                lines.append(f"- [/] {task}")
            lines.append(f"**待办**: {len(tasks['pending'])} 项")
            for task in tasks['pending'][:3]:
                lines.append(f"- [ ] {task}")
            lines.append("")

        # 明日计划
        if 'plan' in report_data['sections']:
            plan = report_data['sections']['plan']
            lines.append("## 📅 明日计划")
            lines.append("**目标:**")
            for goal in plan['today_goals']:
                lines.append(f"- {goal}")
            lines.append("**优先任务:**")
            for task in plan['priority_tasks']:
                lines.append(f"- {task}")
            lines.append("**会议安排:**")
            for meeting in plan['meetings']:
                lines.append(f"- {meeting}")
            lines.append("")

        return "\n".join(lines)

    def save_report(self, report_data, output_file=None, format='text'):
        """保存报告"""
        if not output_file:
            date_str = self.today.strftime('%Y-%m-%d')
            ext = 'md' if format == 'markdown' else 'txt'
            output_file = os.path.join(
                self.config['output_dir'],
                f"daily_report_{date_str}.{ext}"
            )

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # 生成报告内容
        if format == 'markdown':
            content = self.format_report_markdown(report_data)
        else:
            content = self.format_report_text(report_data)

        # 保存文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"报告已保存到: {output_file}")
        return output_file

def main():
    parser = argparse.ArgumentParser(description='每日报告生成器')
    parser.add_argument('--date', help='报告日期 (YYYY-MM-DD)')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', choices=['text', 'markdown', 'json'], default='text',
                       help='输出格式')
    parser.add_argument('--sections', nargs='+',
                       choices=['summary', 'git', 'files', 'tasks', 'plan'],
                       help='包含的章节')

    args = parser.parse_args()

    # 创建报告生成器
    generator = DailyReportGenerator(args.config)

    # 生成报告
    report_data = generator.generate_report(args.date, args.sections)

    # 保存报告
    output_file = generator.save_report(report_data, args.output, args.format)

    # 显示报告预览
    if args.format == 'json':
        print(json.dumps(report_data, ensure_ascii=False, indent=2))
    else:
        # 显示文本报告预览
        if args.format == 'markdown':
            preview = generator.format_report_markdown(report_data)
        else:
            preview = generator.format_report_text(report_data)
        print("\n报告预览:")
        print(preview[:500] + "..." if len(preview) > 500 else preview)

if __name__ == '__main__':
    main()