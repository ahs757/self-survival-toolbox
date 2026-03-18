#!/usr/bin/env python3
"""
备份工具 - 增量/完整备份
作者: 效率工具包
版本: 2.0
"""

import os
import sys
import json
import shutil
import hashlib
import zipfile
import argparse
from pathlib import Path
from datetime import datetime
import time

class BackupTool:
    def __init__(self, config_file=None):
        self.config = self.load_config(config_file)
        self.stats = {
            'files_processed': 0,
            'files_backed_up': 0,
            'files_skipped': 0,
            'files_failed': 0,
            'total_size': 0,
            'start_time': None,
            'end_time': None
        }

    def load_config(self, config_file):
        """加载配置文件"""
        default_config = {
            'backup_dir': './backups',
            'compression_level': 6,
            'exclude_patterns': [
                '*.tmp', '*.temp', '*.log', '*.cache',
                '__pycache__', '.git', '.svn', '.DS_Store',
                'Thumbs.db', '*.pyc', '*.pyo'
            ],
            'include_hidden': False,
            'max_backup_age': 30,  # 天
            'incremental_enabled': True
        }

        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def should_exclude(self, file_path):
        """检查文件是否应该排除"""
        filename = os.path.basename(file_path)

        # 检查隐藏文件
        if not self.config['include_hidden'] and filename.startswith('.'):
            return True

        # 检查排除模式
        for pattern in self.config['exclude_patterns']:
            if pattern.startswith('*'):
                if filename.endswith(pattern[1:]):
                    return True
            elif pattern in file_path:
                return True

        return False

    def calculate_file_hash(self, file_path):
        """计算文件哈希值"""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
                return file_hash.hexdigest()
        except Exception:
            return None

    def get_file_info(self, file_path):
        """获取文件信息"""
        try:
            stat = os.stat(file_path)
            return {
                'path': file_path,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'hash': self.calculate_file_hash(file_path)
            }
        except Exception as e:
            print(f"获取文件信息失败 {file_path}: {e}")
            return None

    def create_full_backup(self, source_dirs, backup_name=None):
        """创建完整备份"""
        if not backup_name:
            backup_name = f"full_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        backup_dir = os.path.join(self.config['backup_dir'], backup_name)
        os.makedirs(backup_dir, exist_ok=True)

        print(f"开始完整备份: {source_dirs} -> {backup_dir}")
        self.stats['start_time'] = time.time()

        manifest = {
            'type': 'full',
            'name': backup_name,
            'timestamp': datetime.now().isoformat(),
            'sources': source_dirs,
            'files': []
        }

        for source_dir in source_dirs:
            if not os.path.exists(source_dir):
                print(f"警告: 源目录不存在: {source_dir}")
                continue

            self.backup_directory(source_dir, backup_dir, manifest)

        # 保存清单文件
        manifest_file = os.path.join(backup_dir, 'manifest.json')
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        # 创建压缩包
        if self.config['compression_level'] > 0:
            self.compress_backup(backup_dir, backup_name)

        self.stats['end_time'] = time.time()
        self.print_stats()

        return backup_dir

    def create_incremental_backup(self, source_dirs, last_backup_dir, backup_name=None):
        """创建增量备份"""
        if not backup_name:
            backup_name = f"incremental_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        backup_dir = os.path.join(self.config['backup_dir'], backup_name)
        os.makedirs(backup_dir, exist_ok=True)

        print(f"开始增量备份: {source_dirs} -> {backup_dir}")
        self.stats['start_time'] = time.time()

        # 加载上次备份清单
        last_manifest_file = os.path.join(last_backup_dir, 'manifest.json')
        if not os.path.exists(last_manifest_file):
            print("错误: 上次备份清单不存在，执行完整备份")
            return self.create_full_backup(source_dirs, backup_name)

        with open(last_manifest_file, 'r', encoding='utf-8') as f:
            last_manifest = json.load(f)

        # 创建文件哈希映射
        last_files = {}
        for file_info in last_manifest['files']:
            last_files[file_info['path']] = file_info

        manifest = {
            'type': 'incremental',
            'name': backup_name,
            'timestamp': datetime.now().isoformat(),
            'sources': source_dirs,
            'base_backup': os.path.basename(last_backup_dir),
            'files': []
        }

        for source_dir in source_dirs:
            if not os.path.exists(source_dir):
                print(f"警告: 源目录不存在: {source_dir}")
                continue

            self.backup_directory_incremental(source_dir, backup_dir, last_files, manifest)

        # 保存清单文件
        manifest_file = os.path.join(backup_dir, 'manifest.json')
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        # 创建压缩包
        if self.config['compression_level'] > 0:
            self.compress_backup(backup_dir, backup_name)

        self.stats['end_time'] = time.time()
        self.print_stats()

        return backup_dir

    def backup_directory(self, source_dir, backup_dir, manifest):
        """备份目录"""
        for root, dirs, files in os.walk(source_dir):
            # 过滤排除的目录
            dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d))]

            for file in files:
                file_path = os.path.join(root, file)

                if self.should_exclude(file_path):
                    continue

                self.stats['files_processed'] += 1

                try:
                    # 获取相对路径
                    rel_path = os.path.relpath(file_path, source_dir)

                    # 目标路径
                    target_path = os.path.join(backup_dir, rel_path)
                    target_dir = os.path.dirname(target_path)

                    # 创建目标目录
                    os.makedirs(target_dir, exist_ok=True)

                    # 复制文件
                    shutil.copy2(file_path, target_path)

                    # 获取文件信息
                    file_info = self.get_file_info(file_path)
                    if file_info:
                        file_info['relative_path'] = rel_path
                        manifest['files'].append(file_info)
                        self.stats['total_size'] += file_info['size']

                    self.stats['files_backed_up'] += 1
                    print(f"备份: {rel_path}")

                except Exception as e:
                    print(f"备份失败 {file_path}: {e}")
                    self.stats['files_failed'] += 1

    def backup_directory_incremental(self, source_dir, backup_dir, last_files, manifest):
        """增量备份目录"""
        for root, dirs, files in os.walk(source_dir):
            # 过滤排除的目录
            dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d))]

            for file in files:
                file_path = os.path.join(root, file)

                if self.should_exclude(file_path):
                    continue

                self.stats['files_processed'] += 1

                try:
                    # 获取相对路径
                    rel_path = os.path.relpath(file_path, source_dir)

                    # 获取当前文件信息
                    current_info = self.get_file_info(file_path)
                    if not current_info:
                        self.stats['files_failed'] += 1
                        continue

                    # 检查文件是否变化
                    last_info = last_files.get(rel_path)
                    if last_info and last_info['hash'] == current_info['hash']:
                        # 文件未变化，跳过
                        self.stats['files_skipped'] += 1
                        print(f"跳过（未变化）: {rel_path}")
                        continue

                    # 目标路径
                    target_path = os.path.join(backup_dir, rel_path)
                    target_dir = os.path.dirname(target_path)

                    # 创建目标目录
                    os.makedirs(target_dir, exist_ok=True)

                    # 复制文件
                    shutil.copy2(file_path, target_path)

                    # 添加到清单
                    current_info['relative_path'] = rel_path
                    manifest['files'].append(current_info)
                    self.stats['total_size'] += current_info['size']

                    self.stats['files_backed_up'] += 1
                    action = "新增" if not last_info else "更新"
                    print(f"{action}: {rel_path}")

                except Exception as e:
                    print(f"备份失败 {file_path}: {e}")
                    self.stats['files_failed'] += 1

    def compress_backup(self, backup_dir, backup_name):
        """压缩备份"""
        zip_file = os.path.join(self.config['backup_dir'], f"{backup_name}.zip")

        print(f"创建压缩包: {zip_file}")

        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED,
                           compresslevel=self.config['compression_level']) as zf:
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, backup_dir)
                    zf.write(file_path, arc_path)

        # 删除原始备份目录
        shutil.rmtree(backup_dir)

        print(f"压缩完成: {zip_file}")

    def restore_backup(self, backup_file, restore_dir, selective_files=None):
        """恢复备份"""
        print(f"开始恢复: {backup_file} -> {restore_dir}")

        if backup_file.endswith('.zip'):
            # 解压ZIP文件
            temp_dir = backup_file + '_temp'
            with zipfile.ZipFile(backup_file, 'r') as zf:
                zf.extractall(temp_dir)
            backup_dir = temp_dir
        else:
            backup_dir = backup_file

        # 加载清单
        manifest_file = os.path.join(backup_dir, 'manifest.json')
        if not os.path.exists(manifest_file):
            print("错误: 备份清单不存在")
            return False

        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # 创建恢复目录
        os.makedirs(restore_dir, exist_ok=True)

        # 恢复文件
        restored_count = 0
        for file_info in manifest['files']:
            rel_path = file_info['relative_path']

            # 选择性恢复
            if selective_files and rel_path not in selective_files:
                continue

            source_path = os.path.join(backup_dir, rel_path)
            target_path = os.path.join(restore_dir, rel_path)

            if os.path.exists(source_path):
                # 创建目标目录
                os.makedirs(os.path.dirname(target_path), exist_ok=True)

                # 复制文件
                shutil.copy2(source_path, target_path)
                restored_count += 1
                print(f"恢复: {rel_path}")

        # 清理临时目录
        if backup_file.endswith('.zip') and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        print(f"恢复完成: {restored_count} 个文件")
        return True

    def list_backups(self):
        """列出所有备份"""
        backup_dir = self.config['backup_dir']
        if not os.path.exists(backup_dir):
            print("备份目录不存在")
            return []

        backups = []
        for item in os.listdir(backup_dir):
            item_path = os.path.join(backup_dir, item)

            if item.endswith('.zip'):
                # ZIP备份
                backups.append({
                    'name': item,
                    'path': item_path,
                    'type': 'zip',
                    'size': os.path.getsize(item_path),
                    'created': datetime.fromtimestamp(os.path.getctime(item_path))
                })
            elif os.path.isdir(item_path):
                # 目录备份
                manifest_file = os.path.join(item_path, 'manifest.json')
                if os.path.exists(manifest_file):
                    with open(manifest_file, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                    backups.append({
                        'name': item,
                        'path': item_path,
                        'type': manifest.get('type', 'unknown'),
                        'files': len(manifest.get('files', [])),
                        'created': datetime.fromisoformat(manifest['timestamp'])
                    })

        # 按创建时间排序
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups

    def cleanup_old_backups(self):
        """清理旧备份"""
        max_age = self.config['max_backup_age']
        if max_age <= 0:
            return

        print(f"清理 {max_age} 天前的备份")

        backups = self.list_backups()
        now = datetime.now()
        cleaned_count = 0

        for backup in backups:
            age_days = (now - backup['created']).days
            if age_days > max_age:
                try:
                    if backup['type'] == 'zip':
                        os.remove(backup['path'])
                    else:
                        shutil.rmtree(backup['path'])
                    print(f"删除: {backup['name']} ({age_days} 天前)")
                    cleaned_count += 1
                except Exception as e:
                    print(f"删除失败 {backup['name']}: {e}")

        print(f"清理完成: 删除了 {cleaned_count} 个旧备份")

    def print_stats(self):
        """打印统计信息"""
        if self.stats['start_time'] and self.stats['end_time']:
            duration = self.stats['end_time'] - self.stats['start_time']
        else:
            duration = 0

        print("\n" + "="*50)
        print("备份完成统计:")
        print(f"处理文件: {self.stats['files_processed']}")
        print(f"成功备份: {self.stats['files_backed_up']}")
        print(f"跳过文件: {self.stats['files_skipped']}")
        print(f"失败文件: {self.stats['files_failed']}")
        print(f"总大小: {self.stats['total_size']/(1024**2):.2f} MB")
        print(f"耗时: {duration:.2f} 秒")
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description='备份工具')
    parser.add_argument('--mode', choices=['full', 'incremental', 'restore', 'list', 'cleanup'],
                       default='full', help='备份模式')
    parser.add_argument('--source', nargs='+', help='源目录路径')
    parser.add_argument('--backup-dir', help='备份目录路径')
    parser.add_argument('--name', help='备份名称')
    parser.add_argument('--restore-dir', help='恢复目录路径')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--last-backup', help='上次备份路径（用于增量备份）')
    parser.add_argument('--selective', nargs='+', help='选择性恢复的文件')

    args = parser.parse_args()

    # 创建备份工具
    backup_tool = BackupTool(args.config)

    if args.backup_dir:
        backup_tool.config['backup_dir'] = args.backup_dir

    if args.mode == 'full':
        if not args.source:
            print("错误: 完整备份需要指定源目录")
            return
        backup_tool.create_full_backup(args.source, args.name)

    elif args.mode == 'incremental':
        if not args.source or not args.last_backup:
            print("错误: 增量备份需要指定源目录和上次备份路径")
            return
        backup_tool.create_incremental_backup(args.source, args.last_backup, args.name)

    elif args.mode == 'restore':
        if not args.backup_file or not args.restore_dir:
            print("错误: 恢复需要指定备份文件和恢复目录")
            return
        backup_tool.restore_backup(args.backup_file, args.restore_dir, args.selective)

    elif args.mode == 'list':
        backups = backup_tool.list_backups()
        print("备份列表:")
        for backup in backups:
            print(f"  {backup['name']} - {backup['type']} - {backup['created']}")

    elif args.mode == 'cleanup':
        backup_tool.cleanup_old_backups()

if __name__ == '__main__':
    main()