#!/usr/bin/env python3
"""
🏷️ 批量重命名工具
智能批量重命名文件，支持多种模式

用法:
    python batch_rename.py [目录] --pattern "照片_{n}" --ext .jpg
    python batch_rename.py [目录] --add-prefix "2024_"
    python batch_rename.py [目录] --replace "old:new"
    python batch_rename.py [目录] --sequence --start 1 --digits 3

作者: AI Self-Survival Project
许可证: MIT
"""

import os
import re
import argparse
from pathlib import Path

def batch_rename(directory: Path, **options):
    """批量重命名文件"""
    directory = Path(directory)
    files = sorted([f for f in directory.iterdir() if f.is_file()])

    if not files:
        print("❌ 目录中没有文件")
        return

    ext_filter = options.get('ext')
    if ext_filter:
        files = [f for f in files if f.suffix.lower() == ext_filter.lower()]

    print(f"📂 找到 {len(files)} 个文件需要处理\n")

    renamed = []
    for i, filepath in enumerate(files):
        new_name = filepath.name

        if options.get('pattern'):
            # 模式重命名: {n}=序号, {name}=原名, {ext}=扩展名
            new_name = options['pattern']
            new_name = new_name.replace('{n}', str(i + 1).zfill(options.get('digits', 1)))
            new_name = new_name.replace('{name}', filepath.stem)
            new_name = new_name.replace('{ext}', filepath.suffix)
            if not new_name.endswith(filepath.suffix):
                new_name += filepath.suffix

        if options.get('add_prefix'):
            new_name = options['add_prefix'] + new_name

        if options.get('add_suffix'):
            stem = Path(new_name).stem
            ext = Path(new_name).suffix
            new_name = stem + options['add_suffix'] + ext

        if options.get('lowercase'):
            new_name = new_name.lower()

        if options.get('uppercase'):
            new_name = new_name.upper()

        if options.get('replace'):
            old, new = options['replace'].split(':')
            new_name = new_name.replace(old, new)

        if options.get('sequence'):
            digits = options.get('digits', 3)
            ext = filepath.suffix
            new_name = f"{str(i + options.get('start', 1)).zfill(digits)}{ext}"

        if options.get('remove_spaces'):
            new_name = new_name.replace(' ', '_')

        if options.get('remove_special'):
            new_name = re.sub(r'[^\w\u4e00-\u9fff._-]', '', new_name)

        new_path = filepath.parent / new_name

        if new_path != filepath:
            # 处理重名
            counter = 1
            while new_path.exists() and new_path != filepath:
                stem = Path(new_name).stem
                ext = Path(new_name).suffix
                new_path = filepath.parent / f"{stem}_{counter}{ext}"
                counter += 1

            if not options.get('dry_run'):
                filepath.rename(new_path)

            status = "📝" if not options.get('dry_run') else "👁️"
            print(f"  {status} {filepath.name} → {new_path.name}")
            renamed.append((filepath.name, new_path.name))

    mode = "预览" if options.get('dry_run') else "执行"
    print(f"\n✅ {mode}完成！共处理 {len(renamed)} 个文件")

def main():
    parser = argparse.ArgumentParser(
        description='🏷️ 批量重命名工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s . --sequence --digits 3             # 001.jpg, 002.jpg, ...
  %(prog)s . --pattern "照片_{n}" --ext .jpg   # 照片_1.jpg, 照片_2.jpg
  %(prog)s . --add-prefix "2024_"              # 2024_oldname.txt
  %(prog)s . --replace "IMG:Photo"             # IMG_001 → Photo_001
  %(prog)s . --lowercase --remove-spaces       # 规范化文件名
  %(prog)s . --dry-run                         # 预览模式
        """
    )

    parser.add_argument('directory', default='.', nargs='?', help='目标目录')
    parser.add_argument('--pattern', help='命名模式 ({n}=序号, {name}=原名)')
    parser.add_argument('--add-prefix', help='添加前缀')
    parser.add_argument('--add-suffix', help='添加后缀')
    parser.add_argument('--replace', help='替换文本 (old:new)')
    parser.add_argument('--sequence', action='store_true', help='纯序号模式')
    parser.add_argument('--ext', help='只处理指定扩展名的文件')
    parser.add_argument('--start', type=int, default=1, help='序号起始值')
    parser.add_argument('--digits', type=int, default=3, help='序号位数')
    parser.add_argument('--lowercase', action='store_true', help='转小写')
    parser.add_argument('--uppercase', action='store_true', help='转大写')
    parser.add_argument('--remove-spaces', action='store_true', help='空格转下划线')
    parser.add_argument('--remove-special', action='store_true', help='移除特殊字符')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')

    args = parser.parse_args()
    batch_rename(args.directory, **vars(args))

if __name__ == '__main__':
    main()
