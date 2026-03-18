#!/usr/bin/env python3
"""
邮件自动化脚本 - 自动处理邮件
作者: 自动化脚本包
版本: 1.0
"""

import os
import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import re
import json
import time

class EmailAutomation:
    def __init__(self, config_file=None):
        self.config = self.load_config(config_file)
        self.imap_connection = None
        self.smtp_connection = None

    def load_config(self, config_file):
        """加载配置文件"""
        default_config = {
            'imap_server': 'imap.gmail.com',
            'imap_port': 993,
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': '',
            'password': '',
            'use_ssl': True,
            'auto_reply': True,
            'auto_forward': False,
            'forward_to': '',
            'categories': {
                'urgent': ['紧急', 'urgent', 'asap'],
                'work': ['工作', 'work', '项目', 'project'],
                'personal': ['个人', 'personal', '私人'],
                'newsletter': ['newsletter', '订阅', '推广', 'promotion'],
                'spam': ['垃圾', 'spam', '广告', 'ad']
            },
            'reply_templates': {
                'urgent': '您好，我已收到您的紧急邮件，会尽快处理。',
                'work': '您好，您的工作邮件已收到，我会在24小时内回复。',
                'default': '您好，您的邮件已收到，我会尽快回复。'
            }
        }

        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def connect_imap(self):
        """连接IMAP服务器"""
        try:
            if self.config['use_ssl']:
                self.imap_connection = imaplib.IMAP4_SSL(
                    self.config['imap_server'],
                    self.config['imap_port']
                )
            else:
                self.imap_connection = imaplib.IMAP4(
                    self.config['imap_server'],
                    self.config['imap_port']
                )

            self.imap_connection.login(
                self.config['email'],
                self.config['password']
            )

            print(f"IMAP连接成功: {self.config['email']}")
            return True

        except Exception as e:
            print(f"IMAP连接失败: {e}")
            return False

    def connect_smtp(self):
        """连接SMTP服务器"""
        try:
            self.smtp_connection = smtplib.SMTP(
                self.config['smtp_server'],
                self.config['smtp_port']
            )

            if self.config['use_ssl']:
                self.smtp_connection.starttls()

            self.smtp_connection.login(
                self.config['email'],
                self.config['password']
            )

            print(f"SMTP连接成功: {self.config['email']}")
            return True

        except Exception as e:
            print(f"SMTP连接失败: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.imap_connection:
            try:
                self.imap_connection.close()
                self.imap_connection.logout()
            except:
                pass

        if self.smtp_connection:
            try:
                self.smtp_connection.quit()
            except:
                pass

    def get_emails(self, folder='INBOX', limit=10, unread_only=True):
        """获取邮件列表"""
        if not self.imap_connection:
            if not self.connect_imap():
                return []

        try:
            self.imap_connection.select(folder)

            # 搜索邮件
            if unread_only:
                status, messages = self.imap_connection.search(None, 'UNSEEN')
            else:
                status, messages = self.imap_connection.search(None, 'ALL')

            if status != 'OK':
                return []

            email_ids = messages[0].split()
            emails = []

            # 获取最新的邮件
            for email_id in email_ids[-limit:]:
                status, msg_data = self.imap_connection.fetch(email_id, '(RFC822)')
                if status != 'OK':
                    continue

                msg = email.message_from_bytes(msg_data[0][1])

                # 解析邮件信息
                email_info = {
                    'id': email_id.decode(),
                    'from': msg['From'],
                    'to': msg['To'],
                    'subject': msg['Subject'],
                    'date': msg['Date'],
                    'body': self.get_email_body(msg),
                    'attachments': self.get_attachments(msg)
                }

                emails.append(email_info)

            return emails

        except Exception as e:
            print(f"获取邮件失败: {e}")
            return []

    def get_email_body(self, msg):
        """获取邮件正文"""
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        return body

    def get_attachments(self, msg):
        """获取附件列表"""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)

        return attachments

    def categorize_email(self, email_info):
        """分类邮件"""
        subject = email_info['subject'].lower() if email_info['subject'] else ''
        body = email_info['body'].lower() if email_info['body'] else ''

        for category, keywords in self.config['categories'].items():
            for keyword in keywords:
                if keyword.lower() in subject or keyword.lower() in body:
                    return category

        return 'other'

    def auto_reply(self, email_info, category):
        """自动回复邮件"""
        if not self.config['auto_reply']:
            return False

        # 选择回复模板
        template = self.config['reply_templates'].get(
            category,
            self.config['reply_templates']['default']
        )

        # 创建回复邮件
        reply_msg = MIMEMultipart()
        reply_msg['From'] = self.config['email']
        reply_msg['To'] = email_info['from']
        reply_msg['Subject'] = f"Re: {email_info['subject']}"

        reply_msg.attach(MIMEText(template, 'plain', 'utf-8'))

        try:
            if not self.smtp_connection:
                if not self.connect_smtp():
                    return False

            self.smtp_connection.send_message(reply_msg)
            print(f"自动回复成功: {email_info['from']}")
            return True

        except Exception as e:
            print(f"自动回复失败: {e}")
            return False

    def auto_forward(self, email_info):
        """自动转发邮件"""
        if not self.config['auto_forward'] or not self.config['forward_to']:
            return False

        try:
            if not self.smtp_connection:
                if not self.connect_smtp():
                    return False

            # 创建转发邮件
            forward_msg = MIMEMultipart()
            forward_msg['From'] = self.config['email']
            forward_msg['To'] = self.config['forward_to']
            forward_msg['Subject'] = f"Fwd: {email_info['subject']}"

            # 转发内容
            forward_body = f"""
            ---------- 转发邮件 ----------
            发件人: {email_info['from']}
            日期: {email_info['date']}
            主题: {email_info['subject']}

            {email_info['body']}
            """

            forward_msg.attach(MIMEText(forward_body, 'plain', 'utf-8'))

            self.smtp_connection.send_message(forward_msg)
            print(f"自动转发成功: {email_info['subject']}")
            return True

        except Exception as e:
            print(f"自动转发失败: {e}")
            return False

    def move_to_folder(self, email_id, target_folder):
        """移动邮件到指定文件夹"""
        try:
            self.imap_connection.copy(email_id, target_folder)
            self.imap_connection.store(email_id, '+FLAGS', '\\Deleted')
            self.imap_connection.expunge()
            print(f"邮件已移动到: {target_folder}")
            return True

        except Exception as e:
            print(f"移动邮件失败: {e}")
            return False

    def process_emails(self):
        """处理邮件"""
        print("开始处理邮件...")

        # 获取未读邮件
        emails = self.get_emails(unread_only=True)

        if not emails:
            print("没有未读邮件")
            return

        print(f"找到 {len(emails)} 封未读邮件")

        processed_count = 0
        replied_count = 0
        forwarded_count = 0

        for email_info in emails:
            try:
                # 分类邮件
                category = self.categorize_email(email_info)
                print(f"邮件分类: {email_info['subject']} -> {category}")

                # 自动回复
                if category in ['urgent', 'work', 'other']:
                    if self.auto_reply(email_info, category):
                        replied_count += 1

                # 自动转发
                if category in ['urgent', 'work']:
                    if self.auto_forward(email_info):
                        forwarded_count += 1

                # 移动邮件到对应文件夹
                if category in ['spam', 'newsletter']:
                    self.move_to_folder(email_info['id'], category.upper())

                processed_count += 1

                # 标记为已读
                self.imap_connection.store(email_info['id'], '+FLAGS', '\\Seen')

            except Exception as e:
                print(f"处理邮件失败 {email_info['subject']}: {e}")

        print(f"处理完成: 处理 {processed_count} 封，回复 {replied_count} 封，转发 {forwarded_count} 封")

    def generate_report(self):
        """生成邮件处理报告"""
        if not self.imap_connection:
            if not self.connect_imap():
                return {}

        try:
            # 获取所有邮件
            self.imap_connection.select('INBOX')
            status, messages = self.imap_connection.search(None, 'ALL')

            if status != 'OK':
                return {}

            total_emails = len(messages[0].split())

            # 获取未读邮件
            status, unread_messages = self.imap_connection.search(None, 'UNSEEN')
            unread_count = len(unread_messages[0].split()) if status == 'OK' else 0

            # 获取今天的邮件
            today = datetime.now().strftime('%d-%b-%Y')
            status, today_messages = self.imap_connection.search(None, f'ON {today}')
            today_count = len(today_messages[0].split()) if status == 'OK' else 0

            report = {
                'total_emails': total_emails,
                'unread_emails': unread_count,
                'today_emails': today_count,
                'timestamp': datetime.now().isoformat()
            }

            return report

        except Exception as e:
            print(f"生成报告失败: {e}")
            return {}

def main():
    import argparse

    parser = argparse.ArgumentParser(description='邮件自动化工具')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--mode', choices=['process', 'report', 'test'], default='process',
                       help='运行模式')
    parser.add_argument('--folder', default='INBOX', help='邮箱文件夹')
    parser.add_argument('--limit', type=int, default=10, help='处理邮件数量限制')

    args = parser.parse_args()

    # 创建邮件自动化实例
    email_auto = EmailAutomation(args.config)

    try:
        if args.mode == 'process':
            email_auto.process_emails()

        elif args.mode == 'report':
            report = email_auto.generate_report()
            print("邮件报告:")
            print(json.dumps(report, indent=2, ensure_ascii=False))

        elif args.mode == 'test':
            # 测试连接
            if email_auto.connect_imap():
                print("IMAP连接测试成功")
                email_auto.disconnect()

    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"运行错误: {e}")
    finally:
        email_auto.disconnect()

if __name__ == '__main__':
    main()