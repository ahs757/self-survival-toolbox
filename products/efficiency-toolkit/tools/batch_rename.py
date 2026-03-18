#!/usr/bin/env python3
"""
批量重命名工具 - 支持5种重命名模式
作者: 效率工具包
版本: 2.0
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime

class BatchRenamer:
    def __init__(self):
        self.stats = {
            'total': 0,
            'renamed': 0,
            'errors': 0,
            'skipped': 0
        }

    def add_prefix_suffix(self, directory, prefix="", suffix="", extension_filter=None):
        """添加前缀/后缀"""
        print(f"添加前缀: '{prefix}', 后缀: '{suffix}'")

        for filename in os.listdir(directory):
            if extension_filter and not filename.endswith(extension_filter):
                continue

            old_path = os.path.join(directory, filename)
            if not os.path.isfile(old_path):
                continue

            self.stats['total'] += 1

            try:
                # 分离文件名和扩展名
                name, ext = os.path.splitext(filename)

                # 新文件名
                new_name = f"{prefix}{name}{suffix}{ext}"
                new_path = os.path.join(directory, new_name)

                # 检查是否重名
                if new_path == old_path:
                    self.stats['skipped'] += 1
                    continue

                if os.path.exists(new_path):
                    print(f"跳过: {filename} (目标已存在)")
                    self.stats['skipped'] += 1
                    continue

                # 重命名
                os.rename(old_path, new_path)
                print(f"重命名: {filename} -> {new_name}")
                self.stats['renamed'] += 1

            except Exception as e:
                print(f"错误: {filename} - {e}")
                self.stats['errors'] += 1

    def sequential_numbering(self, directory, pattern="file_{:03d}", start=1, extension_filter=None):
        """顺序编号"""
        print(f"顺序编号模式: {pattern}")

        files = []
        for filename in os.listdir(directory):
            if extension_filter and not filename.endswith(extension_filter):
                continue

            old_path = os.path.join(directory, filename)
            if os.path.isfile(old_path):
                files.append((filename, old_path))

        # 按修改时间排序
        files.sort(key=lambda x: os.path.getmtime(x[1]))

        for i, (filename, old_path) in enumerate(files, start):
            self.stats['total'] += 1

            try:
                # 分离扩展名
                ext = Path(filename).suffix

                # 生成新文件名
                new_name = pattern.format(i) + ext
                new_path = os.path.join(directory, new_name)

                # 检查是否重名
                if new_path == old_path:
                    self.stats['skipped'] += 1
                    continue

                # 重命名
                os.rename(old_path, new_path)
                print(f"重命名: {filename} -> {new_name}")
                self.stats['renamed'] += 1

            except Exception as e:
                print(f"错误: {filename} - {e}")
                self.stats['errors'] += 1

    def replace_text(self, directory, old_text, new_text, case_sensitive=True, extension_filter=None):
        """替换文本"""
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(re.escape(old_text), flags)

        print(f"替换文本: '{old_text}' -> '{new_text}'")

        for filename in os.listdir(directory):
            if extension_filter and not filename.endswith(extension_filter):
                continue

            old_path = os.path.join(directory, filename)
            if not os.path.isfile(old_path):
                continue

            self.stats['total'] += 1

            try:
                # 检查是否包含目标文本
                if not pattern.search(filename):
                    self.stats['skipped'] += 1
                    continue

                # 替换文本
                new_name = pattern.sub(new_text, filename)
                new_path = os.path.join(directory, new_name)

                # 检查是否重名
                if new_path == old_path:
                    self.stats['skipped'] += 1
                    continue

                if os.path.exists(new_path):
                    print(f"跳过: {filename} (目标已存在)")
                    self.stats['skipped'] += 1
                    continue

                # 重命名
                os.rename(old_path, new_path)
                print(f"重命名: {filename} -> {new_name}")
                self.stats['renamed'] += 1

            except Exception as e:
                print(f"错误: {filename} - {e}")
                self.stats['errors'] += 1

    def change_case(self, directory, case_type="lower", extension_filter=None):
        """改变大小写"""
        print(f"改变大小写: {case_type}")

        for filename in os.listdir(directory):
            if extension_filter and not filename.endswith(extension_filter):
                continue

            old_path = os.path.join(directory, filename)
            if not os.path.isfile(old_path):
                continue

            self.stats['total'] += 1

            try:
                # 分离文件名和扩展名
                name, ext = os.path.splitext(filename)

                # 改变大小写
                if case_type == "lower":
                    new_name = name.lower() + ext
                elif case_type == "upper":
                    new_name = name.upper() + ext
                elif case_type == "title":
                    new_name = name.title() + ext
                elif case_type == "capitalize":
                    new_name = name.capitalize() + ext
                else:
                    self.stats['skipped'] += 1
                    continue

                new_path = os.path.join(directory, new_name)

                # 检查是否重名
                if new_path == old_path:
                    self.stats['skipped'] += 1
                    continue

                if os.path.exists(new_path):
                    print(f"跳过: {filename} (目标已存在)")
                    self.stats['skipped'] += 1
                    continue

                # 重命名
                os.rename(old_path, new_path)
                print(f"重命名: {filename} -> {new_name}")
                self.stats['renamed'] += 1

            except Exception as e:
                print(f"错误: {filename} - {e}")
                self.stats['errors'] += 1

    def add_date(self, directory, date_format="%Y%m%d", position="prefix", extension_filter=None):
        """添加日期"""
        print(f"添加日期: 格式={date_format}, 位置={position}")

        for filename in os.listdir(directory):
            if extension_filter and not filename.endswith(extension_filter):
                continue

            old_path = os.path.join(directory, filename)
            if not os.path.isfile(old_path):
                continue

            self.stats['total'] += 1

            try:
                # 获取文件修改时间
                mtime = os.path.getmtime(old_path)
                date_str = datetime.fromtimestamp(mtime).strftime(date_format)

                # 分离文件名和扩展名
                name, ext = os.path.splitext(filename)

                # 添加日期
                if position == "prefix":
                    new_name = f"{date_str}_{name}{ext}"
                else:  # suffix
                    new_name = f"{name}_{date_str}{ext}"

                new_path = os.path.join(directory, new_name)

                # 检查是否重名
                if new_path == old_path:
                    self.stats['skipped'] += 1
                    continue

                if os.path.exists(new_path):
                    print(f"跳过: {filename} (目标已存在)")
                    self.stats['skipped'] += 1
                    continue

                # 重命名
                os.rename(old_path, new_path)
                print(f"重命名: {filename} -> {new_name}")
                self.stats['renamed'] += 1

            except Exception as e:
                print(f"错误: {filename} - {e}")
                self.stats['errors'] += 1

    def print_stats(self):
        """打印统计信息"""
        print("\n" + "="*50)
        print("重命名完成统计:")
        print(f"总文件数: {self.stats['total']}")
        print(f"成功重命名: {self.stats['renamed']}")
        print(f"跳过文件: {self.stats['skipped']}")
        print(f"处理错误: {self.stats['errors']}")
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description='批量重命名工具')
    parser.add_argument('directory', help='目标文件夹路径')
    parser.add_argument('--mode', required=True,
                       choices=['prefix_suffix', 'sequential', 'replace', 'case', 'date'],
                       help='重命名模式')

    # 前缀后缀模式
    parser.add_argument('--prefix', default="", help='添加前缀')
    parser.add_argument('--suffix', default="", help='添加后缀')

    # 顺序编号模式
    parser.add_argument('--pattern', default="file_{:03d}", help='编号模式')
    parser.add_argument('--start', type=int, default=1, help='起始编号')

    # 替换文本模式
    parser.add_argument('--old-text', help='要替换的文本')
    parser.add_argument('--new-text', default="", help='替换为的文本')
    parser.add_argument('--case-sensitive', action='store_true', help='区分大小写')

    # 大小写模式
    parser.add_argument('--case-type', choices=['lower', 'upper', 'title', 'capitalize'],
                       default='lower', help='大小写类型')

    # 日期模式
    parser.add_argument('--date-format', default="%Y%m%d", help='日期格式')
    parser.add_argument('--position', choices=['prefix', 'suffix'], default='prefix',
                       help='日期位置')

    # 通用选项
    parser.add_argument('--ext', help='文件扩展名过滤')

    args = parser.parse_args()

    # 检查目录
    if not os.path.exists(args.directory):
        print(f"错误: 目录不存在: {args.directory}")
        return

    # 创建重命名器
    renamer = BatchRenamer()

    # 执行重命名
    if args.mode == 'prefix_suffix':
        renamer.add_prefix_suffix(args.directory, args.prefix, args.suffix, args.ext)
    elif args.mode == 'sequential':
        renamer.sequential_numbering(args.directory, args.pattern, args.start, args.ext)
    elif args.mode == 'replace':
        if not args.old_text:
            print("错误: 替换模式需要指定 --old-text")
            return
        renamer.replace_text(args.directory, args.old_text, args.new_text,
                           args.case_sensitive, args.ext)
    elif args.mode == 'case':
        renamer.change_case(args.directory, args.case_type, args.ext)
    elif args.mode == 'date':
        renamer.add_date(args.directory, args.date_format, args.position, args.ext)

    # 打印统计
    renamer.print_stats()

if __name__ == '__main__':
    main()