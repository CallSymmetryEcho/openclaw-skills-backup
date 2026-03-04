#!/usr/bin/env python3
"""
简单测试Cookie有效性
"""

import json
import os
from pathlib import Path

COOKIE_FILE = Path.home() / ".openclaw" / "workspace" / "config" / "xiaohongshu_cookies.json"

def test_cookie_file():
    """测试Cookie文件"""
    print("🔍 检查Cookie文件...")
    
    if not COOKIE_FILE.exists():
        print("❌ Cookie文件不存在")
        return False
    
    try:
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        print(f"✅ Cookie文件存在，包含 {len(cookies)} 个Cookie")
        
        # 显示关键Cookie信息
        print("\n📋 Cookie摘要:")
        for i, cookie in enumerate(cookies[:5]):  # 只显示前5个
            print(f"  {i+1}. {cookie.get('name', '未知')}: {cookie.get('value', '')[:30]}...")
        
        if len(cookies) > 5:
            print(f"  ... 还有 {len(cookies)-5} 个Cookie")
        
        # 检查关键Cookie
        important_cookies = ['a1', 'web_session', 'webId', 'xhsTrackerId']
        found_cookies = []
        
        for cookie in cookies:
            if cookie.get('name') in important_cookies:
                found_cookies.append(cookie.get('name'))
        
        print(f"\n🔑 关键Cookie找到: {found_cookies}")
        
        # 检查过期时间
        has_expiry = any('expiry' in cookie for cookie in cookies)
        print(f"⏰ 包含过期时间: {'是' if has_expiry else '否'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取Cookie文件失败: {e}")
        return False

def check_cookie_validity():
    """检查Cookie有效性（基础检查）"""
    print("\n🧪 基础Cookie有效性检查...")
    
    if not COOKIE_FILE.exists():
        return False
    
    try:
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        # 基本有效性检查
        if len(cookies) < 3:
            print("⚠️  Cookie数量较少，可能不完整")
            return False
        
        # 检查是否有小红书域名
        xhs_domains = ['.xiaohongshu.com', 'www.xiaohongshu.com']
        has_xhs_domain = any(
            any(domain in cookie.get('domain', '') for domain in xhs_domains)
            for cookie in cookies
        )
        
        if not has_xhs_domain:
            print("⚠️  未检测到小红书域名Cookie")
            return False
        
        print("✅ Cookie基础检查通过")
        return True
        
    except Exception as e:
        print(f"❌ Cookie检查失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("小红书Cookie有效性测试")
    print("=" * 60)
    
    # 测试Cookie文件
    file_ok = test_cookie_file()
    
    if not file_ok:
        print("\n❌ Cookie文件测试失败")
        return
    
    # 基础有效性检查
    validity_ok = check_cookie_validity()
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    if validity_ok:
        print("✅ **Cookie有效性测试通过**")
        print("\n🎉 可以尝试使用Cookie浏览小红书:")
        print("1. 运行: ./tools/xiaohongshu_cookie.sh browse")
        print("2. 或运行: ./tools/xiaohongshu_cookie.sh search \"关键词\"")
    else:
        print("⚠️  **Cookie可能无效或不完整**")
        print("\n🔧 建议:")
        print("1. 重新获取Cookie: ./tools/xiaohongshu_cookie.sh extract")
        print("2. 或使用扫码登录重新获取")
    
    print("\n📁 Cookie文件位置:", COOKIE_FILE)
    print("📏 文件大小:", os.path.getsize(COOKIE_FILE), "字节")

if __name__ == "__main__":
    main()