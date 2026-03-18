#!/usr/bin/env python3
"""
系统监控工具 - 实时监控电脑状态
作者: 效率工具包
版本: 2.0
"""

import os
import sys
import time
import json
import psutil
import platform
from datetime import datetime
from pathlib import Path
import argparse

class SystemMonitor:
    def __init__(self, log_file=None):
        self.log_file = log_file or f"system_monitor_{datetime.now().strftime('%Y%m%d')}.log"
        self.history = []
        self.max_history = 1000

    def get_system_info(self):
        """获取系统基本信息"""
        return {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': platform.node(),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }

    def get_cpu_info(self):
        """获取CPU信息"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()

        # 每个核心的使用率
        cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)

        return {
            'usage_percent': cpu_percent,
            'core_count': cpu_count,
            'frequency_current': cpu_freq.current if cpu_freq else None,
            'frequency_min': cpu_freq.min if cpu_freq else None,
            'frequency_max': cpu_freq.max if cpu_freq else None,
            'per_core_usage': cpu_per_core,
            'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
        }

    def get_memory_info(self):
        """获取内存信息"""
        virtual = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            'virtual': {
                'total': virtual.total,
                'available': virtual.available,
                'used': virtual.used,
                'free': virtual.free,
                'percent': virtual.percent,
                'total_gb': round(virtual.total / (1024**3), 2),
                'used_gb': round(virtual.used / (1024**3), 2),
                'available_gb': round(virtual.available / (1024**3), 2)
            },
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            }
        }

    def get_disk_info(self):
        """获取磁盘信息"""
        disks = []

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2)
                })
            except PermissionError:
                continue

        # 磁盘IO
        try:
            disk_io = psutil.disk_io_counters()
            io_info = {
                'read_count': disk_io.read_count,
                'write_count': disk_io.write_count,
                'read_bytes': disk_io.read_bytes,
                'write_bytes': disk_io.write_bytes
            }
        except:
            io_info = None

        return {
            'partitions': disks,
            'io_counters': io_info
        }

    def get_network_info(self):
        """获取网络信息"""
        # 网络接口
        interfaces = []
        for name, addrs in psutil.net_if_addrs().items():
            interface_info = {
                'name': name,
                'addresses': []
            }
            for addr in addrs:
                interface_info['addresses'].append({
                    'family': str(addr.family),
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast
                })
            interfaces.append(interface_info)

        # 网络连接
        try:
            connections = psutil.net_connections()
            connection_count = len(connections)
        except:
            connection_count = 0

        # 网络IO
        try:
            net_io = psutil.net_io_counters()
            io_info = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            }
        except:
            io_info = None

        return {
            'interfaces': interfaces,
            'connection_count': connection_count,
            'io_counters': io_info
        }

    def get_process_info(self, top_n=10):
        """获取进程信息"""
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # 按CPU使用率排序
        top_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:top_n]

        # 按内存使用率排序
        top_memory = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:top_n]

        return {
            'total_processes': len(processes),
            'top_cpu': top_cpu,
            'top_memory': top_memory
        }

    def get_temperature_info(self):
        """获取温度信息（如果支持）"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                temp_info = {}
                for name, entries in temps.items():
                    temp_info[name] = []
                    for entry in entries:
                        temp_info[name].append({
                            'label': entry.label or name,
                            'current': entry.current,
                            'high': entry.high,
                            'critical': entry.critical
                        })
                return temp_info
        except:
            pass
        return None

    def collect_all_data(self):
        """收集所有系统数据"""
        timestamp = datetime.now().isoformat()

        data = {
            'timestamp': timestamp,
            'system': self.get_system_info(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info(),
            'processes': self.get_process_info(),
            'temperature': self.get_temperature_info()
        }

        return data

    def generate_report(self, data=None, format='text'):
        """生成监控报告"""
        if data is None:
            data = self.collect_all_data()

        if format == 'json':
            return json.dumps(data, ensure_ascii=False, indent=2)

        # 文本格式报告
        report = []
        report.append("=" * 60)
        report.append("系统监控报告")
        report.append("=" * 60)
        report.append(f"生成时间: {data['timestamp']}")
        report.append("")

        # 系统信息
        sys_info = data['system']
        report.append("💻 系统信息")
        report.append("-" * 30)
        report.append(f"操作系统: {sys_info['platform']}")
        report.append(f"主机名: {sys_info['hostname']}")
        report.append(f"启动时间: {sys_info['boot_time']}")
        report.append("")

        # CPU信息
        cpu_info = data['cpu']
        report.append("🔧 CPU信息")
        report.append("-" * 30)
        report.append(f"核心数: {cpu_info['core_count']}")
        report.append(f"使用率: {cpu_info['usage_percent']}%")
        if cpu_info['frequency_current']:
            report.append(f"当前频率: {cpu_info['frequency_current']:.0f} MHz")
        if cpu_info['load_average']:
            report.append(f"负载均衡: {', '.join(map(str, cpu_info['load_average']))}")
        report.append("")

        # 内存信息
        mem_info = data['memory']
        report.append("🧠 内存信息")
        report.append("-" * 30)
        vmem = mem_info['virtual']
        report.append(f"总计: {vmem['total_gb']} GB")
        report.append(f"已用: {vmem['used_gb']} GB ({vmem['percent']}%)")
        report.append(f"可用: {vmem['available_gb']} GB")
        if mem_info['swap']['total'] > 0:
            swap = mem_info['swap']
            report.append(f"交换分区: {swap['used']/(1024**3):.2f}/{swap['total']/(1024**3):.2f} GB ({swap['percent']}%)")
        report.append("")

        # 磁盘信息
        disk_info = data['disk']
        report.append("💾 磁盘信息")
        report.append("-" * 30)
        for disk in disk_info['partitions']:
            report.append(f"设备: {disk['device']} ({disk['mountpoint']})")
            report.append(f"  总计: {disk['total_gb']} GB")
            report.append(f"  已用: {disk['used_gb']} GB ({disk['percent']}%)")
            report.append(f"  可用: {disk['free_gb']} GB")
        report.append("")

        # 网络信息
        net_info = data['network']
        report.append("🌐 网络信息")
        report.append("-" * 30)
        report.append(f"活动连接数: {net_info['connection_count']}")
        if net_info['io_counters']:
            io = net_info['io_counters']
            report.append(f"发送: {io['bytes_sent']/(1024**2):.2f} MB")
            report.append(f"接收: {io['bytes_recv']/(1024**2):.2f} MB")
        report.append("")

        # 进程信息
        proc_info = data['processes']
        report.append("⚙️ 进程信息")
        report.append("-" * 30)
        report.append(f"总进程数: {proc_info['total_processes']}")
        report.append("CPU使用率Top 5:")
        for i, proc in enumerate(proc_info['top_cpu'][:5], 1):
            report.append(f"  {i}. {proc['name']} (PID: {proc['pid']}) - {proc['cpu_percent']}%")
        report.append("")

        # 温度信息
        temp_info = data['temperature']
        if temp_info:
            report.append("🌡️ 温度信息")
            report.append("-" * 30)
            for sensor, readings in temp_info.items():
                for reading in readings:
                    if reading['current']:
                        report.append(f"{reading['label']}: {reading['current']}°C")
            report.append("")

        report.append("=" * 60)

        return "\n".join(report)

    def monitor_continuous(self, interval=5, duration=None):
        """持续监控"""
        print(f"开始持续监控，间隔: {interval}秒")
        if duration:
            print(f"监控时长: {duration}秒")

        start_time = time.time()
        count = 0

        try:
            while True:
                # 检查持续时间
                if duration and (time.time() - start_time) > duration:
                    break

                # 收集数据
                data = self.collect_all_data()
                self.history.append(data)

                # 限制历史记录
                if len(self.history) > self.max_history:
                    self.history = self.history[-self.max_history:]

                # 记录日志
                self.log_data(data)

                # 显示简要信息
                count += 1
                print(f"\n[{count}] {data['timestamp']}")
                print(f"CPU: {data['cpu']['usage_percent']}% | "
                      f"内存: {data['memory']['virtual']['percent']}% | "
                      f"磁盘: {data['disk']['partitions'][0]['percent']}%")

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n监控已停止")

    def log_data(self, data):
        """记录数据到日志文件"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"日志写入失败: {e}")

    def generate_summary_report(self):
        """生成汇总报告"""
        if not self.history:
            return "无监控数据"

        # 计算平均值
        cpu_avg = sum(d['cpu']['usage_percent'] for d in self.history) / len(self.history)
        mem_avg = sum(d['memory']['virtual']['percent'] for d in self.history) / len(self.history)

        report = []
        report.append("📊 监控汇总报告")
        report.append("=" * 40)
        report.append(f"监控时长: {len(self.history)} 个数据点")
        report.append(f"平均CPU使用率: {cpu_avg:.1f}%")
        report.append(f"平均内存使用率: {mem_avg:.1f}%")

        # 找出峰值
        max_cpu = max(self.history, key=lambda x: x['cpu']['usage_percent'])
        max_mem = max(self.history, key=lambda x: x['memory']['virtual']['percent'])

        report.append(f"CPU峰值: {max_cpu['cpu']['usage_percent']}% ({max_cpu['timestamp']})")
        report.append(f"内存峰值: {max_mem['memory']['virtual']['percent']}% ({max_mem['timestamp']})")

        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='系统监控工具')
    parser.add_argument('--mode', choices=['once', 'continuous', 'report'], default='once',
                       help='监控模式')
    parser.add_argument('--interval', type=int, default=5,
                       help='监控间隔（秒）')
    parser.add_argument('--duration', type=int,
                       help='监控时长（秒）')
    parser.add_argument('--output', '-o', help='输出报告文件路径')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='输出格式')
    parser.add_argument('--log-file', help='日志文件路径')

    args = parser.parse_args()

    # 创建监控器
    monitor = SystemMonitor(args.log_file)

    if args.mode == 'once':
        # 单次监控
        data = monitor.collect_all_data()
        report = monitor.generate_report(data, args.format)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到: {args.output}")
        else:
            print(report)

    elif args.mode == 'continuous':
        # 持续监控
        monitor.monitor_continuous(args.interval, args.duration)

        # 生成汇总报告
        summary = monitor.generate_summary_report()
        print("\n" + summary)

    elif args.mode == 'report':
        # 从日志文件生成报告
        if args.log_file and os.path.exists(args.log_file):
            with open(args.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        monitor.history.append(data)
                    except:
                        continue

            summary = monitor.generate_summary_report()
            print(summary)
        else:
            print("错误: 日志文件不存在")

if __name__ == '__main__':
    main()