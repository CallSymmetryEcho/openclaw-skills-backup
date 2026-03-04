#!/usr/bin/env python3
"""
多Gmail账户管理工具
支持工作和生活邮箱分开管理
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

def load_accounts():
    """加载所有邮箱账户配置"""
    accounts = {}
    
    # 查找所有账户配置文件
    for filename in os.listdir(CONFIG_DIR):
        if filename.startswith("gmail_account_") and filename.endswith(".json"):
            account_name = filename.replace("gmail_account_", "").replace(".json", "")
            filepath = os.path.join(CONFIG_DIR, filename)
            
            try:
                with open(filepath, 'r') as f:
                    account_config = json.load(f)
                    accounts[account_name] = account_config
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"警告: 无法读取账户配置文件 {filename}")
    
    return accounts

def save_account(account_name, email_address, app_password, account_type="work"):
    """保存邮箱账户配置"""
    account_config = {
        "email": email_address,
        "app_password": app_password,
        "type": account_type,
        "created": datetime.now().isoformat()
    }
    
    filename = f"gmail_account_{account_name}.json"
    filepath = os.path.join(CONFIG_DIR, filename)
    
    with open(filepath, 'w') as f:
        json.dump(account_config, f, indent=2)
    
    print(f"✅ 账户 '{account_name}' 已保存到 {filepath}")
    return account_config

def list_accounts():
    """列出所有配置的邮箱账户"""
    accounts = load_accounts()
    
    if not accounts:
        print("📭 未找到任何邮箱账户配置")
        print("\n请使用以下命令添加账户:")
        print("  python3 multi_gmail.py add --name work --email your@work.com")
        return
    
    print("=" * 60)
    print("📧 已配置的邮箱账户")
    print("=" * 60)
    
    for i, (name, config) in enumerate(accounts.items(), 1):
        print(f"\n{i}. 账户名称: {name}")
        print(f"   邮箱地址: {config.get('email', '未设置')}")
        print(f"   账户类型: {config.get('type', '未知')}")
        print(f"   创建时间: {config.get('created', '未知')}")
    
    print("\n" + "=" * 60)

def test_account(account_name):
    """测试邮箱账户连接"""
    accounts = load_accounts()
    
    if account_name not in accounts:
        print(f"❌ 未找到账户 '{account_name}'")
        return False
    
    config = accounts[account_name]
    email_addr = config.get('email')
    password = config.get('app_password')
    
    if not email_addr or not password:
        print(f"❌ 账户 '{account_name}' 配置不完整")
        return False
    
    print(f"=== 测试账户: {account_name} ({email_addr}) ===")
    
    # 测试SMTP
    try:
        print("1. 测试SMTP发送连接...")
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(email_addr, password)
        smtp_server.quit()
        print("   ✓ SMTP连接成功")
    except Exception as e:
        print(f"   ✗ SMTP连接失败: {e}")
        return False
    
    # 测试IMAP
    try:
        print("2. 测试IMAP接收连接...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_addr, password)
        mail.select('inbox')
        
        # 获取邮件数量
        result, data = mail.search(None, 'ALL')
        if result == 'OK':
            email_ids = data[0].split()
            print(f"   ✓ IMAP连接成功，找到 {len(email_ids)} 封邮件")
        else:
            print("   ✓ IMAP连接成功")
        
        mail.logout()
    except Exception as e:
        print(f"   ✗ IMAP连接失败: {e}")
        return False
    
    print(f"\n✅ 账户 '{account_name}' 所有连接测试通过!")
    return True

def list_emails(account_name, limit=10):
    """列出指定账户的邮件"""
    accounts = load_accounts()
    
    if account_name not in accounts:
        print(f"❌ 未找到账户 '{account_name}'")
        return
    
    config = accounts[account_name]
    email_addr = config.get('email')
    password = config.get('app_password')
    
    try:
        # 连接Gmail IMAP服务器
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_addr, password)
        mail.select('inbox')
        
        # 搜索最新邮件
        result, data = mail.search(None, 'ALL')
        if result != 'OK':
            print("无法搜索邮件")
            return
        
        # 获取邮件ID列表
        email_ids = data[0].split()
        email_ids = email_ids[-limit:]  # 取最新的
        
        print(f"=== {account_name}账户 - 最新 {len(email_ids)} 封邮件 ===")
        
        for i, email_id in enumerate(reversed(email_ids), 1):
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            if result != 'OK':
                continue
            
            # 解析邮件
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # 解码主题
            subject = "无主题"
            if msg['Subject']:
                subject_header = decode_header(msg['Subject'])[0]
                subject_text = subject_header[0]
                if isinstance(subject_text, bytes):
                    encoding = subject_header[1] if subject_header[1] else 'utf-8'
                    subject = subject_text.decode(encoding, errors='ignore')
                else:
                    subject = subject_text
            
            # 发件人
            from_header = msg['From'] or "未知发件人"
            
            # 日期
            date_header = msg['Date'] or "未知日期"
            
            # 预览
            preview = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True)
                        if body:
                            charset = part.get_content_charset() or 'utf-8'
                            preview = body.decode(charset, errors='ignore')[:100]
                            break
            else:
                body = msg.get_payload(decode=True)
                if body:
                    charset = msg.get_content_charset() or 'utf-8'
                    preview = body.decode(charset, errors='ignore')[:100]
            
            print(f"\n{i}. [{date_header}]")
            print(f"   发件人: {from_header}")
            print(f"   主题: {subject}")
            if preview:
                print(f"   预览: {preview}...")
        
        mail.logout()
        
    except Exception as e:
        print(f"❌ 读取邮件失败: {e}")

def send_email(account_name, to_email, subject, body):
    """使用指定账户发送邮件"""
    accounts = load_accounts()
    
    if account_name not in accounts:
        print(f"❌ 未找到账户 '{account_name}'")
        return False
    
    config = accounts[account_name]
    from_email = config.get('email')
    password = config.get('app_password')
    
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加正文
        msg.attach(MIMEText(body, 'plain'))
        
        # 发送邮件
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(from_email, password)
        smtp_server.send_message(msg)
        smtp_server.quit()
        
        print(f"✅ 邮件已从 '{account_name}' 账户发送到 {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='多Gmail账户管理工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 添加账户命令
    add_parser = subparsers.add_parser('add', help='添加新邮箱账户')
    add_parser.add_argument('--name', required=True, help='账户名称 (如: work, life)')
    add_parser.add_argument('--email', required=True, help='邮箱地址')
    add_parser.add_argument('--type', default='work', choices=['work', 'life', 'other'], help='账户类型')
    
    # 列出账户命令
    subparsers.add_parser('list', help='列出所有邮箱账户')
    
    # 测试账户命令
    test_parser = subparsers.add_parser('test', help='测试邮箱账户连接')
    test_parser.add_argument('account', help='账户名称')
    
    # 列出邮件命令
    list_parser = subparsers.add_parser('emails', help='列出指定账户的邮件')
    list_parser.add_argument('account', help='账户名称')
    list_parser.add_argument('--limit', type=int, default=10, help='邮件数量限制')
    
    # 发送邮件命令
    send_parser = subparsers.add_parser('send', help='发送邮件')
    send_parser.add_argument('account', help='发送账户名称')
    send_parser.add_argument('to', help='收件人邮箱')
    send_parser.add_argument('subject', help='邮件主题')
    send_parser.add_argument('body', help='邮件正文')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'add':
        print("🔐 请提供应用专用密码 (16位字符，无空格):")
        app_password = input("应用密码: ").strip()
        
        if len(app_password) != 16 or ' ' in app_password:
            print("❌ 应用密码必须是16位字符且不能包含空格")
            print("请从 https://myaccount.google.com/apppasswords 生成")
            return
        
        save_account(args.name, args.email, app_password, args.type)
        
    elif args.command == 'list':
        list_accounts()
        
    elif args.command == 'test':
        test_account(args.account)
        
    elif args.command == 'emails':
        list_emails(args.account, args.limit)
        
    elif args.command == 'send':
        send_email(args.account, args.to, args.subject, args.body)

if __name__ == '__main__':
    main()