#!/usr/bin/env python3
"""
Gmail简单工具 - 使用应用专用密码
支持读取和发送邮件
"""

import os
import sys
import json
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import argparse
from datetime import datetime

# 配置文件路径
CONFIG_DIR = os.path.expanduser("~/.openclaw/workspace/config")
ACCOUNT_FILE = os.path.join(CONFIG_DIR, "gmail_account.txt")
PASSWORD_FILE = os.path.join(CONFIG_DIR, "gmail_app_password.txt")

def load_config():
    """加载Gmail配置"""
    config = {}
    
    # 读取账户
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
            if lines:
                config['email'] = lines[0]
    
    # 读取应用密码
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
            if lines:
                config['app_password'] = lines[0]
    
    return config

def check_config():
    """检查配置是否完整"""
    config = load_config()
    
    if 'email' not in config:
        print("错误: 未配置Gmail账户")
        print(f"请编辑文件: {ACCOUNT_FILE}")
        print("内容格式: your-email@gmail.com")
        return False
    
    if 'app_password' not in config:
        print("错误: 未配置应用专用密码")
        print(f"请编辑文件: {PASSWORD_FILE}")
        print("内容格式: xxxx xxxx xxxx xxxx (16位应用密码)")
        print("\n如何获取应用密码:")
        print("1. 访问 https://myaccount.google.com/")
        print("2. 登录 lianbin522957@gmail.com")
        print("3. 进入'安全' → '应用专用密码'")
        print("4. 生成新密码并复制")
        return False
    
    return True

def send_email(to_email, subject, body):
    """发送邮件"""
    config = load_config()
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = config['email']
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # 添加正文
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # 连接Gmail SMTP服务器
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # 启用TLS加密
        
        # 登录
        server.login(config['email'], config['app_password'])
        
        # 发送邮件
        server.send_message(msg)
        server.quit()
        
        print(f"✓ 邮件发送成功!")
        print(f"  发件人: {config['email']}")
        print(f"  收件人: {to_email}")
        print(f"  主题: {subject}")
        return True
        
    except Exception as e:
        print(f"✗ 发送失败: {e}")
        return False

def list_emails(limit=10):
    """列出最新邮件"""
    config = load_config()
    
    try:
        # 连接Gmail IMAP服务器
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(config['email'], config['app_password'])
        mail.select('inbox')  # 选择收件箱
        
        # 搜索最新邮件
        result, data = mail.search(None, 'ALL')
        if result != 'OK':
            print("无法搜索邮件")
            return
        
        # 获取邮件ID列表
        email_ids = data[0].split()
        email_ids = email_ids[-limit:]  # 取最新的
        
        print(f"=== 最新 {len(email_ids)} 封邮件 ===")
        
        for i, email_id in enumerate(reversed(email_ids), 1):
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            if result != 'OK':
                continue
            
            # 解析邮件
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # 解码主题
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            
            # 解码发件人
            from_header, encoding = decode_header(msg['From'])[0]
            if isinstance(from_header, bytes):
                from_header = from_header.decode(encoding if encoding else 'utf-8')
            
            # 日期
            date = msg['Date']
            
            print(f"\n{i}. [{date}]")
            print(f"   发件人: {from_header}")
            print(f"   主题: {subject}")
            
            # 显示前100个字符的预览
            body = get_email_body(msg)
            if body:
                preview = body[:100].replace('\n', ' ')
                if len(body) > 100:
                    preview += "..."
                print(f"   预览: {preview}")
        
        mail.logout()
        
    except Exception as e:
        print(f"✗ 读取邮件失败: {e}")

def get_email_body(msg):
    """提取邮件正文"""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain":
            return msg.get_payload(decode=True).decode()
    
    return ""

def search_emails(query, limit=10):
    """搜索邮件"""
    config = load_config()
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(config['email'], config['app_password'])
        mail.select('inbox')
        
        # 搜索邮件
        result, data = mail.search(None, f'(TEXT "{query}")')
        if result != 'OK':
            print(f"搜索失败: {query}")
            return
        
        email_ids = data[0].split()
        email_ids = email_ids[-limit:]
        
        print(f"=== 搜索 '{query}' - 找到 {len(email_ids)} 封邮件 ===")
        
        for i, email_id in enumerate(reversed(email_ids), 1):
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            if result != 'OK':
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            
            from_header, encoding = decode_header(msg['From'])[0]
            if isinstance(from_header, bytes):
                from_header = from_header.decode(encoding if encoding else 'utf-8')
            
            print(f"\n{i}. [{msg['Date']}]")
            print(f"   发件人: {from_header}")
            print(f"   主题: {subject}")
        
        mail.logout()
        
    except Exception as e:
        print(f"✗ 搜索失败: {e}")

def setup_guide():
    """显示设置指南"""
    print("=== Gmail配置指南 ===")
    print("\n1. 配置Gmail账户:")
    print(f"   编辑文件: {ACCOUNT_FILE}")
    print("   内容: lianbin522957@gmail.com")
    
    print("\n2. 获取应用专用密码:")
    print("   a. 访问 https://myaccount.google.com/")
    print("   b. 登录 lianbin522957@gmail.com")
    print("   c. 进入'安全' → '应用专用密码'")
    print("   d. 选择'邮件'应用")
    print("   e. 生成16位密码 (格式: xxxx xxxx xxxx xxxx)")
    
    print(f"\n3. 保存应用密码:")
    print(f"   编辑文件: {PASSWORD_FILE}")
    print("   内容: [你的16位应用密码]")
    
    print("\n4. 测试连接:")
    print("   python3 gmail_simple.py test")

def test_connection():
    """测试连接"""
    if not check_config():
        return
    
    config = load_config()
    print("=== 测试Gmail连接 ===")
    print(f"账户: {config['email']}")
    
    try:
        # 测试SMTP连接
        print("\n1. 测试SMTP发送连接...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config['email'], config['app_password'])
        server.quit()
        print("   ✓ SMTP连接成功")
        
        # 测试IMAP连接
        print("\n2. 测试IMAP接收连接...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(config['email'], config['app_password'])
        mail.select('inbox')
        result, data = mail.search(None, 'ALL')
        mail.logout()
        print(f"   ✓ IMAP连接成功，找到 {len(data[0].split())} 封邮件")
        
        print("\n✅ 所有连接测试通过!")
        
    except Exception as e:
        print(f"\n✗ 连接测试失败: {e}")
        print("\n可能的原因:")
        print("1. 应用密码错误")
        print("2. 未启用IMAP访问 (在Gmail设置中启用)")
        print("3. 网络连接问题")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Gmail简单工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 发送邮件命令
    send_parser = subparsers.add_parser('send', help='发送邮件')
    send_parser.add_argument('to', help='收件人邮箱')
    send_parser.add_argument('subject', help='邮件主题')
    send_parser.add_argument('body', help='邮件内容')
    
    # 列出邮件命令
    list_parser = subparsers.add_parser('list', help='列出邮件')
    list_parser.add_argument('-n', '--limit', type=int, default=10, help='显示数量')
    
    # 搜索邮件命令
    search_parser = subparsers.add_parser('search', help='搜索邮件')
    search_parser.add_argument('query', help='搜索关键词')
    search_parser.add_argument('-n', '--limit', type=int, default=10, help='显示数量')
    
    # 设置指南命令
    subparsers.add_parser('setup', help='显示设置指南')
    
    # 测试命令
    subparsers.add_parser('test', help='测试连接')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'send':
        if check_config():
            send_email(args.to, args.subject, args.body)
    
    elif args.command == 'list':
        if check_config():
            list_emails(args.limit)
    
    elif args.command == 'search':
        if check_config():
            search_emails(args.query, args.limit)
    
    elif args.command == 'setup':
        setup_guide()
    
    elif args.command == 'test':
        test_connection()

if __name__ == '__main__':
    main()