#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日报告生成器 - 生成系统状态、文件变化等每日摘要
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path


def get_system_summary():
    """获取系统摘要"""
    try:
        from system_monitor import get_cpu_usage, get_memory_info, get_disk_info
        return {
            "cpu": get_cpu_usage(),
            "memory": get_memory_info(),
            "disks": get_disk_info()
        }
    except:
        return None


def scan_recent_files(directory, hours=24):
    """扫描最近修改的文件"""
    recent_files = []
    cutoff = datetime.now().timestamp() - (hours * 3600)

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            if filename.startswith('.'):
                continue

            filepath = os.path.join(root, filename)
            try:
                mtime = os.path.getmtime(filepath)
                if mtime > cutoff:
                    recent_files.append({
                        "path": os.path.relpath(filepath, directory),
                        "size": os.path.getsize(filepath),
                        "modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                    })
            except:
                continue

    recent_files.sort(key=lambda x: x['modified'], reverse=True)
    return recent_files


def generate_daily_report(project_dir):
    """生成每日报告"""
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    report = {
        "date": today,
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "project_dir": project_dir,
        "sections": []
    }

    # 1. 项目概况
    total_size = 0
    total_files = 0
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if not f.startswith('.'):
                total_files += 1
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                except:
                    pass

    report["sections"].append({
        "title": "📁 项目概况",
        "content": {
            "总文件数": total_files,
            "总大小": f"{total_size / 1024:.1f} KB"
        }
    })

    # 2. 最近修改的文件
    recent = scan_recent_files(project_dir, hours=24)
    report["sections"].append({
        "title": "📝 今日修改",
        "content": {
            "修改文件数": len(recent),
            "文件列表": [f["path"] for f in recent[:10]]
        }
    })

    # 3. 目录结构
    dir_summary = {}
    for item in os.listdir(project_dir):
        item_path = os.path.join(project_dir, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            file_count = sum(1 for _, _, files in os.walk(item_path)
                           for f in files if not f.startswith('.'))
            dir_summary[item] = f"{file_count} 个文件"

    report["sections"].append({
        "title": "📂 目录结构",
        "content": dir_summary
    })

    return report


def format_report_text(report):
    """格式化为文本"""
    lines = [
        "=" * 50,
        f"📊 每日报告 - {report['date']}",
        "=" * 50,
        f"⏰ 生成时间: {report['generated_at']}",
        f"📂 项目目录: {report['project_dir']}",
        ""
    ]

    for section in report["sections"]:
        lines.append(section["title"])
        lines.append("-" * 30)
        for key, value in section["content"].items():
            if isinstance(value, list):
                lines.append(f"  {key}:")
                for item in value:
                    lines.append(f"    - {item}")
            else:
                lines.append(f"  {key}: {value}")
        lines.append("")

    lines.append("=" * 50)
    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="每日报告生成器")
    parser.add_argument("-d", "--dir", default=".", help="项目目录")
    parser.add_argument("-o", "--output", help="输出文件")
    parser.add_argument("-f", "--format", choices=["text", "json"], default="text")

    args = parser.parse_args()
    project_dir = os.path.abspath(args.dir)

    report = generate_daily_report(project_dir)

    if args.format == "json":
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        output = format_report_text(report)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"报告已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
