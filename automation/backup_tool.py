#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件备份工具 - 支持增量备份、压缩、定时备份
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from datetime import datetime
from pathlib import Path


def get_file_hash(filepath):
    """计算文件MD5哈希"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None


def get_file_info(filepath):
    """获取文件信息"""
    stat = os.stat(filepath)
    return {
        "size": stat.st_size,
        "mtime": stat.st_mtime,
        "hash": get_file_hash(filepath)
    }


def collect_files(source_dir, exclude_patterns=None):
    """收集目录下所有文件"""
    files = {}
    exclude_patterns = exclude_patterns or []

    for root, dirs, filenames in os.walk(source_dir):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in filenames:
            if filename.startswith('.'):
                continue

            # 检查排除模式
            skip = False
            for pattern in exclude_patterns:
                if pattern in filename or pattern in root:
                    skip = True
                    break
            if skip:
                continue

            filepath = os.path.join(root, filename)
            relpath = os.path.relpath(filepath, source_dir)
            files[relpath] = get_file_info(filepath)

    return files


def load_backup_manifest(manifest_path):
    """加载备份清单"""
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_backup_manifest(manifest_path, manifest):
    """保存备份清单"""
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def incremental_backup(source_dir, backup_dir, exclude_patterns=None):
    """增量备份"""
    print(f"📂 源目录: {source_dir}")
    print(f"💾 备份目录: {backup_dir}")

    # 创建备份目录
    os.makedirs(backup_dir, exist_ok=True)

    # 加载上次备份清单
    manifest_path = os.path.join(backup_dir, '.backup_manifest.json')
    old_manifest = load_backup_manifest(manifest_path)

    # 收集当前文件
    print("🔍 扫描文件中...")
    current_files = collect_files(source_dir, exclude_patterns)

    # 比较差异
    new_files = []
    modified_files = []
    deleted_files = []

    for relpath, info in current_files.items():
        if relpath not in old_manifest:
            new_files.append(relpath)
        elif old_manifest[relpath]['hash'] != info['hash']:
            modified_files.append(relpath)

    for relpath in old_manifest:
        if relpath not in current_files:
            deleted_files.append(relpath)

    # 执行备份
    backed_up = 0
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for relpath in new_files + modified_files:
        src = os.path.join(source_dir, relpath)
        dst = os.path.join(backup_dir, relpath)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        backed_up += 1

        if relpath in new_files:
            print(f"  ✅ 新增: {relpath}")
        else:
            print(f"  🔄 更新: {relpath}")

    for relpath in deleted_files:
        print(f"  ❌ 已删除: {relpath}")

    # 保存清单
    save_backup_manifest(manifest_path, current_files)

    # 生成报告
    report = {
        "timestamp": timestamp,
        "source": source_dir,
        "backup": backup_dir,
        "stats": {
            "total_files": len(current_files),
            "new_files": len(new_files),
            "modified_files": len(modified_files),
            "deleted_files": len(deleted_files),
            "backed_up": backed_up
        }
    }

    print(f"\n📊 备份完成!")
    print(f"   总文件: {len(current_files)}")
    print(f"   新增: {len(new_files)}")
    print(f"   修改: {len(modified_files)}")
    print(f"   已删除: {len(deleted_files)}")
    print(f"   本次备份: {backed_up} 个文件")

    return report


def full_backup(source_dir, backup_dir, compress=False):
    """完整备份"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"

    print(f"📦 创建完整备份: {backup_name}")

    if compress:
        archive_path = shutil.make_archive(
            os.path.join(backup_dir, backup_name),
            'zip',
            source_dir
        )
        size_mb = os.path.getsize(archive_path) / (1024 * 1024)
        print(f"✅ 备份完成: {archive_path} ({size_mb:.1f} MB)")
    else:
        dst = os.path.join(backup_dir, backup_name)
        shutil.copytree(source_dir, dst)
        print(f"✅ 备份完成: {dst}")

    return backup_name


def main():
    parser = argparse.ArgumentParser(description="文件备份工具")
    parser.add_argument("source", help="源目录路径")
    parser.add_argument("backup", help="备份目录路径")
    parser.add_argument("-m", "--mode", choices=["incremental", "full"],
                        default="incremental", help="备份模式")
    parser.add_argument("-z", "--compress", action="store_true",
                        help="压缩备份 (仅完整备份模式)")
    parser.add_argument("-e", "--exclude", nargs="+", default=[],
                        help="排除模式列表")

    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"❌ 源目录不存在: {args.source}")
        return 1

    print("=" * 50)
    print("💾 文件备份工具")
    print("=" * 50)

    if args.mode == "incremental":
        incremental_backup(args.source, args.backup, args.exclude)
    else:
        full_backup(args.source, args.backup, args.compress)

    return 0


if __name__ == "__main__":
    sys.exit(main())
