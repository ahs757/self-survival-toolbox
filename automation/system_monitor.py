#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统监控工具 - 监控CPU、内存、磁盘使用情况
"""

import os
import sys
import json
import time
import platform
import argparse
from datetime import datetime
from pathlib import Path

# 尝试导入psutil，没有则使用内置方法
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def get_cpu_usage():
    """获取CPU使用率"""
    if HAS_PSUTIL:
        return psutil.cpu_percent(interval=1)
    else:
        # Windows备用方法
        if platform.system() == "Windows":
            import subprocess
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'loadpercentage'],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.isdigit():
                    return float(line)
        return -1


def get_memory_info():
    """获取内存信息"""
    if HAS_PSUTIL:
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "percent": mem.percent
        }
    else:
        if platform.system() == "Windows":
            import subprocess
            result = subprocess.run(
                ['wmic', 'OS', 'get', 'TotalVisibleMemorySize,FreePhysicalMemory'],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 2:
                    total_kb = int(parts[1])
                    free_kb = int(parts[0])
                    used_kb = total_kb - free_kb
                    return {
                        "total_gb": round(total_kb / (1024**2), 2),
                        "used_gb": round(used_kb / (1024**2), 2),
                        "available_gb": round(free_kb / (1024**2), 2),
                        "percent": round(used_kb / total_kb * 100, 1)
                    }
        return {"total_gb": 0, "used_gb": 0, "available_gb": 0, "percent": 0}


def get_disk_info():
    """获取磁盘信息"""
    disks = []
    if HAS_PSUTIL:
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": usage.percent
                })
            except PermissionError:
                continue
    else:
        if platform.system() == "Windows":
            import string
            from ctypes import windll
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append(f"{letter}:\\")
                bitmask >>= 1
            for drive in drives:
                try:
                    import shutil
                    total, used, free = shutil.disk_usage(drive)
                    disks.append({
                        "device": drive,
                        "mountpoint": drive,
                        "total_gb": round(total / (1024**3), 2),
                        "used_gb": round(used / (1024**3), 2),
                        "free_gb": round(free / (1024**3), 2),
                        "percent": round(used / total * 100, 1)
                    })
                except:
                    continue
    return disks


def get_top_processes(n=5):
    """获取占用资源最多的进程"""
    if HAS_PSUTIL:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        return processes[:n]
    return []


def generate_report(output_format="text"):
    """生成系统状态报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "timestamp": now,
        "platform": platform.platform(),
        "cpu_percent": get_cpu_usage(),
        "memory": get_memory_info(),
        "disks": get_disk_info(),
        "top_processes": get_top_processes()
    }

    if output_format == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)

    # 文本格式
    lines = [
        "=" * 50,
        "📊 系统状态报告",
        "=" * 50,
        f"⏰ 时间: {now}",
        f"💻 平台: {platform.platform()}",
        "",
        "🔲 CPU 使用率:",
        f"   {data['cpu_percent']}%",
        "",
        "💾 内存使用:",
        f"   总计: {data['memory']['total_gb']} GB",
        f"   已用: {data['memory']['used_gb']} GB ({data['memory']['percent']}%)",
        f"   可用: {data['memory']['available_gb']} GB",
        "",
        "💿 磁盘使用:",
    ]

    for disk in data['disks']:
        lines.append(f"   {disk['device']} - {disk['used_gb']}/{disk['total_gb']} GB ({disk['percent']}%)")

    if data['top_processes']:
        lines.append("")
        lines.append("🔝 资源占用TOP进程:")
        for i, proc in enumerate(data['top_processes'], 1):
            lines.append(f"   {i}. {proc.get('name', 'N/A')} (PID: {proc.get('pid', 'N/A')}) - CPU: {proc.get('cpu_percent', 0)}%")

    lines.append("")
    lines.append("=" * 50)

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="系统监控工具")
    parser.add_argument("-f", "--format", choices=["text", "json"], default="text",
                        help="输出格式 (默认: text)")
    parser.add_argument("-o", "--output", help="输出到文件")
    parser.add_argument("-w", "--watch", type=int, help="持续监控间隔(秒)")
    parser.add_argument("-n", "--processes", type=int, default=5,
                        help="显示TOP进程数量 (默认: 5)")

    args = parser.parse_args()

    if args.watch:
        print("按 Ctrl+C 退出监控...")
        try:
            while True:
                os.system('cls' if platform.system() == 'Windows' else 'clear')
                print(generate_report(args.format))
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\n监控已停止")
    else:
        report = generate_report(args.format)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到: {args.output}")
        else:
            print(report)


if __name__ == "__main__":
    main()
