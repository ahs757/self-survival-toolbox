#!/usr/bin/env python3
"""
智能文件整理器 - 按类型/日期自动分类文件
作者: 效率工具包
版本: 2.0
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import argparse

class FileOrganizer:
    def __init__(self, config_file=None):
        self.config = self.load_config(config_file)
        self.stats = {
            'processed': 0,
            'moved': 0,
            'errors': 0,
            'skipped': 0
        }

    def load_config(self, config_file):
        """加载配置文件"""
        default_config = {
            'categories': {
                'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                'videos': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'],
                'music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
                'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h'],
                'data': ['.json', '.xml', '.csv', '.xlsx', '.xls', '.db', '.sqlite'],
                'executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'],
                'others': []
            },
            'date_format': '%Y-%m',
            'create_subfolders': True,
            'overwrite': False,
            'dry_run': False
        }

        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def get_file_category(self, file_path):
        """获取文件类别"""
        ext = Path(file_path).suffix.lower()

        for category, extensions in self.config['categories'].items():
            if ext in extensions:
                return category

        return 'others'

    def get_date_folder(self, file_path):
        """获取日期文件夹"""
        stat = os.stat(file_path)
        mod_time = datetime.fromtimestamp(stat.st_mtime)
        return mod_time.strftime(self.config['date_format'])

    def organize_by_type(self, source_dir, target_dir):
        """按文件类型整理"""
        print(f"开始按类型整理: {source_dir} -> {target_dir}")

        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)

                # 跳过目标目录中的文件
                if file_path.startswith(target_dir):
                    continue

                self.stats['processed'] += 1

                try:
                    # 获取文件类别
                    category = self.get_file_category(file_path)

                    # 创建目标文件夹
                    category_dir = os.path.join(target_dir, category)
                    os.makedirs(category_dir, exist_ok=True)

                    # 如果配置了日期子文件夹
                    if self.config['create_subfolders']:
                        date_folder = self.get_date_folder(file_path)
                        target_folder = os.path.join(category_dir, date_folder)
                        os.makedirs(target_folder, exist_ok=True)
                    else:
                        target_folder = category_dir

                    # 目标文件路径
                    target_path = os.path.join(target_folder, file)

                    # 处理重名文件
                    if os.path.exists(target_path):
                        if not self.config['overwrite']:
                            base, ext = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(target_path):
                                new_name = f"{base}_{counter}{ext}"
                                target_path = os.path.join(target_folder, new_name)
                                counter += 1

                    # 移动文件
                    if not self.config['dry_run']:
                        shutil.move(file_path, target_path)
                        print(f"移动: {file} -> {category}/")
                    else:
                        print(f"[预览] 移动: {file} -> {category}/")

                    self.stats['moved'] += 1

                except Exception as e:
                    print(f"错误处理 {file}: {e}")
                    self.stats['errors'] += 1

    def organize_by_date(self, source_dir, target_dir):
        """按修改日期整理"""
        print(f"开始按日期整理: {source_dir} -> {target_dir}")

        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)

                # 跳过目标目录中的文件
                if file_path.startswith(target_dir):
                    continue

                self.stats['processed'] += 1

                try:
                    # 获取日期文件夹
                    date_folder = self.get_date_folder(file_path)

                    # 创建目标文件夹
                    target_folder = os.path.join(target_dir, date_folder)
                    os.makedirs(target_folder, exist_ok=True)

                    # 目标文件路径
                    target_path = os.path.join(target_folder, file)

                    # 处理重名文件
                    if os.path.exists(target_path):
                        if not self.config['overwrite']:
                            base, ext = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(target_path):
                                new_name = f"{base}_{counter}{ext}"
                                target_path = os.path.join(target_folder, new_name)
                                counter += 1

                    # 移动文件
                    if not self.config['dry_run']:
                        shutil.move(file_path, target_path)
                        print(f"移动: {file} -> {date_folder}/")
                    else:
                        print(f"[预览] 移动: {file} -> {date_folder}/")

                    self.stats['moved'] += 1

                except Exception as e:
                    print(f"错误处理 {file}: {e}")
                    self.stats['errors'] += 1

    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*50)
        print("整理完成统计:")
        print(f"处理文件: {self.stats['processed']}")
        print(f"成功移动: {self.stats['moved']}")
        print(f"处理错误: {self.stats['errors']}")
        print(f"跳过文件: {self.stats['skipped']}")
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description='智能文件整理器')
    parser.add_argument('source', help='源文件夹路径')
    parser.add_argument('target', help='目标文件夹路径')
    parser.add_argument('--mode', choices=['type', 'date'], default='type',
                       help='整理模式: type(按类型) 或 date(按日期)')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际移动')

    args = parser.parse_args()

    # 检查源文件夹
    if not os.path.exists(args.source):
        print(f"错误: 源文件夹不存在: {args.source}")
        return

    # 创建整理器
    organizer = FileOrganizer(args.config)
    organizer.config['dry_run'] = args.dry_run

    # 执行整理
    if args.mode == 'type':
        organizer.organize_by_type(args.source, args.target)
    else:
        organizer.organize_by_date(args.source, args.target)

    # 打印统计
    organizer.print_stats()

if __name__ == '__main__':
    main()