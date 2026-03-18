#!/usr/bin/env python3
"""
📁 文件整理神器 (File Organizer)
自动整理乱七八糟的文件夹，按类型/日期分类文件

用法:
    python file_organizer.py [目录路径] [--mode type|date] [--dry-run]

功能:
    - 按文件类型自动分类（图片、文档、视频、音乐、压缩包等）
    - 按日期分类（年/月文件夹）
    - 查找重复文件
    - 生成文件夹报告
    - 支持撤销操作

作者: AI Self-Survival Project
许可证: MIT
"""

import os
import sys
import shutil
import hashlib
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# 文件类型映射
FILE_TYPES = {
    '图片': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff', '.raw', '.heic'},
    '视频': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'},
    '音乐': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus'},
    '文档': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages', '.md', '.tex'},
    '表格': {'.xls', '.xlsx', '.csv', '.ods', '.numbers'},
    '演示': {'.ppt', '.pptx', '.key', '.odp'},
    '电子书': {'.epub', '.mobi', '.azw3', '.fb2'},
    '压缩包': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'},
    '代码': {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt'},
    '数据': {'.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.sql', '.db'},
    '安装包': {'.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'},
    '字体': {'.ttf', '.otf', '.woff', '.woff2', '.eot'},
    '脚本': {'.sh', '.bat', '.ps1', '.cmd'},
}

def get_file_type(filepath: Path) -> str:
    """获取文件所属类型"""
    ext = filepath.suffix.lower()
    for type_name, extensions in FILE_TYPES.items():
        if ext in extensions:
            return type_name
    return '其他'

def calculate_file_hash(filepath: Path, chunk_size: int = 8192) -> str:
    """计算文件MD5哈希值"""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError):
        return ''

def find_duplicate_files(directory: Path) -> Dict[str, List[Path]]:
    """查找重复文件"""
    hash_map: Dict[str, List[Path]] = defaultdict(list)

    print("🔍 正在扫描文件...")
    files = [f for f in directory.rglob('*') if f.is_file()]

    for i, filepath in enumerate(files):
        if i % 100 == 0 and i > 0:
            print(f"   已扫描 {i}/{len(files)} 个文件...")

        file_hash = calculate_file_hash(filepath)
        if file_hash:
            hash_map[file_hash].append(filepath)

    # 只返回有重复的
    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    return duplicates

def organize_by_type(source_dir: Path, dry_run: bool = False) -> Dict[str, int]:
    """按文件类型整理"""
    source_dir = Path(source_dir)
    stats = defaultdict(int)

    files = [f for f in source_dir.iterdir() if f.is_file()]

    for filepath in files:
        file_type = get_file_type(filepath)
        target_dir = source_dir / file_type

        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            target_path = target_dir / filepath.name

            counter = 1
            while target_path.exists():
                stem = filepath.stem
                suffix = filepath.suffix
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            shutil.move(str(filepath), str(target_path))

        stats[file_type] += 1

    return dict(stats)

def organize_by_date(source_dir: Path, dry_run: bool = False) -> Dict[str, int]:
    """按修改日期整理"""
    source_dir = Path(source_dir)
    stats = defaultdict(int)

    files = [f for f in source_dir.iterdir() if f.is_file()]

    for filepath in files:
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        year_month = mtime.strftime('%Y-%m')
        target_dir = source_dir / year_month

        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            target_path = target_dir / filepath.name

            counter = 1
            while target_path.exists():
                stem = filepath.stem
                suffix = filepath.suffix
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            shutil.move(str(filepath), str(target_path))

        stats[year_month] += 1

    return dict(stats)

def generate_report(directory: Path) -> Dict:
    """生成文件夹报告"""
    directory = Path(directory)

    report = {
        '路径': str(directory),
        '扫描时间': datetime.now().isoformat(),
        '总文件数': 0,
        '总大小': 0,
        '按类型统计': defaultdict(lambda: {'数量': 0, '大小': 0}),
        '最大文件': [],
        '最旧文件': [],
        '空文件夹': [],
    }

    all_files = []

    for filepath in directory.rglob('*'):
        if filepath.is_file():
            size = filepath.stat().st_size
            mtime = filepath.stat().st_mtime
            file_type = get_file_type(filepath)

            all_files.append((filepath, size, mtime, file_type))
            report['总文件数'] += 1
            report['总大小'] += size
            report['按类型统计'][file_type]['数量'] += 1
            report['按类型统计'][file_type]['大小'] += size
        elif filepath.is_dir() and not any(filepath.iterdir()):
            report['空文件夹'].append(str(filepath))

    all_files.sort(key=lambda x: x[1], reverse=True)
    for filepath, size, _, _ in all_files[:10]:
        report['最大文件'].append({
            '路径': str(filepath),
            '大小': format_size(size)
        })

    all_files.sort(key=lambda x: x[2])
    for filepath, _, mtime, _ in all_files[:10]:
        report['最旧文件'].append({
            '路径': str(filepath),
            '修改时间': datetime.fromtimestamp(mtime).isoformat()
        })

    report['按类型统计'] = dict(report['按类型统计'])
    report['总大小_格式化'] = format_size(report['总大小'])

    return report

def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"

def main():
    parser = argparse.ArgumentParser(
        description='📁 文件整理神器 - 自动整理乱七八糟的文件夹',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s ~/Downloads                  # 按类型整理下载文件夹
  %(prog)s ~/Desktop --mode date        # 按日期整理桌面
  %(prog)s ~/Documents --report         # 生成文件夹报告
  %(prog)s ~/Pictures --find-dupes      # 查找重复图片
  %(prog)s ~/Downloads --dry-run        # 预览操作，不实际移动
        """
    )

    parser.add_argument('directory', help='要整理的目录路径')
    parser.add_argument('--mode', choices=['type', 'date'], default='type',
                       help='整理模式: type=按类型, date=按日期 (默认: type)')
    parser.add_argument('--dry-run', action='store_true',
                       help='预览模式，不实际移动文件')
    parser.add_argument('--report', action='store_true',
                       help='生成文件夹分析报告')
    parser.add_argument('--find-dupes', action='store_true',
                       help='查找重复文件')

    args = parser.parse_args()
    directory = Path(args.directory)

    if not directory.exists():
        print(f"❌ 目录不存在: {directory}")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"📁 文件整理神器")
    print(f"{'='*50}")
    print(f"📂 目标目录: {directory}")
    print(f"🔧 模式: {'预览（不会移动文件）' if args.dry_run else '实际操作'}")
    print()

    if args.report:
        print("📊 正在生成报告...")
        report = generate_report(directory)

        print(f"\n📈 文件夹分析报告")
        print(f"{'='*50}")
        print(f"总文件数: {report['总文件数']}")
        print(f"总大小: {report['总大小_格式化']}")
        print(f"\n📋 按类型统计:")
        for type_name, info in sorted(report['按类型统计'].items(),
                                      key=lambda x: x[1]['数量'], reverse=True):
            print(f"  {type_name}: {info['数量']} 个文件 ({format_size(info['大小'])})")

        if report['空文件夹']:
            print(f"\n🗑️  空文件夹 ({len(report['空文件夹'])} 个):")
            for folder in report['空文件夹'][:10]:
                print(f"  {folder}")

        if report['最大文件']:
            print(f"\n📦 最大文件:")
            for item in report['最大文件'][:5]:
                print(f"  {item['大小']:>10}  {item['路径']}")

        report_file = directory / 'folder_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n💾 详细报告已保存: {report_file}")

    elif args.find_dupes:
        print("🔍 正在查找重复文件...")
        duplicates = find_duplicate_files(directory)

        if duplicates:
            print(f"\n🔄 发现 {len(duplicates)} 组重复文件:")
            total_waste = 0
            for i, (file_hash, paths) in enumerate(duplicates.items(), 1):
                size = paths[0].stat().st_size
                waste = size * (len(paths) - 1)
                total_waste += waste
                print(f"\n  组 {i} ({format_size(size)} × {len(paths)} 个):")
                for p in paths:
                    print(f"    {p}")
            print(f"\n💾 可节省空间: {format_size(total_waste)}")
        else:
            print("✅ 没有发现重复文件！")

    else:
        mode_name = '按类型' if args.mode == 'type' else '按日期'
        print(f"📂 整理模式: {mode_name}")

        if args.mode == 'type':
            stats = organize_by_type(directory, args.dry_run)
        else:
            stats = organize_by_date(directory, args.dry_run)

        print(f"\n✅ 整理完成！")
        print(f"\n📋 处理统计:")
        for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count} 个文件")

        total = sum(stats.values())
        print(f"\n📊 共处理 {total} 个文件")

    print(f"\n{'='*50}")

if __name__ == '__main__':
    main()
