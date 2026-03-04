#!/usr/bin/env python3
"""
迁移现有邮箱账户到多账户系统
"""

import os
import json
from datetime import datetime

CONFIG_DIR = os.path.expanduser("~/.openclaw/workspace/config")

def migrate_work_account():
    """迁移工作邮箱账户"""
    
    # 读取现有配置
    account_file = os.path.join(CONFIG_DIR, "gmail_account.txt")
    password_file = os.path.join(CONFIG_DIR, "gmail_app_password.txt")
    
    if not os.path.exists(account_file) or not os.path.exists(password_file):
        print("未找到现有的邮箱配置")
        return False
    
    # 读取邮箱地址
    email = None
    with open(account_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '@' in line:
                email = line
                break
    
    if not email:
        print("无法从账户文件中提取邮箱地址")
        return False
    
    # 读取应用密码
    app_password = None
    with open(password_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and len(line) == 16 and ' ' not in line:
                app_password = line
                break
    
    if not app_password:
        print("无法从密码文件中提取应用密码")
        return False
    
    # 创建新的JSON配置
    account_config = {
        "email": email,
        "app_password": app_password,
        "type": "work",
        "created": datetime.now().isoformat(),
        "migrated": True
    }
    
    config_file = os.path.join(CONFIG_DIR, "gmail_account_work.json")
    with open(config_file, 'w') as f:
        json.dump(account_config, f, indent=2)
    
    print(f"✅ 工作邮箱已迁移到多账户系统")
    print(f"   邮箱: {email}")
    print(f"   配置文件: {config_file}")
    
    return True

def test_migrated_account():
    """测试迁移后的账户"""
    from multi_gmail import test_account
    return test_account("work")

def main():
    print("=== 迁移现有邮箱账户到多账户系统 ===")
    print()
    
    # 迁移工作邮箱
    if migrate_work_account():
        print()
        print("=== 测试迁移后的账户 ===")
        test_migrated_account()
        
        print()
        print("=== 下一步 ===")
        print("1. 使用以下命令添加生活邮箱:")
        print("   ./mgmail.sh add life your_life_email@gmail.com life")
        print()
        print("2. 列出所有账户:")
        print("   ./mgmail.sh list")
        print()
        print("3. 查看工作邮箱邮件:")
        print("   ./mgmail.sh emails work 10")
    else:
        print("❌ 迁移失败")

if __name__ == '__main__':
    main()