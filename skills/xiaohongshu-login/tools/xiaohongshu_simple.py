#!/usr/bin/env python3
"""
小红书简单登录脚本 - 使用npx playwright命令
"""

import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "workspace" / "config"
ACCOUNT_FILE = CONFIG_DIR / "xiaohongshu_account.json"

def run_playwright_command(script_content, output_file=None):
    """运行Playwright命令"""
    # 创建临时JavaScript文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(script_content)
        temp_file = f.name
    
    try:
        # 运行npx playwright
        cmd = ["npx", "playwright", "test", temp_file, "--reporter=line"]
        if output_file:
            cmd.extend(["--output", output_file])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Playwright执行成功")
            return True
        else:
            print(f"❌ Playwright执行失败: {result.stderr}")
            return False
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_file)
        except:
            pass

def create_login_script(username, password, login_type="phone"):
    """创建登录脚本"""
    return f"""
const {{ test, expect }} = require('@playwright/test');

test('小红书登录测试', async ({{ page }}) => {{
  console.log('🚀 启动浏览器...');
  
  // 访问小红书登录页面
  await page.goto('https://www.xiaohongshu.com/user/login');
  console.log('🌐 访问登录页面');
  
  // 等待页面加载
  await page.waitForTimeout(3000);
  
  // 截图当前页面
  await page.screenshot({{ path: '/tmp/xiaohongshu_login_page.png', fullPage: true }});
  console.log('📸 登录页面截图已保存');
  
  // 根据登录类型选择输入框
  if ('{login_type}' === 'phone') {{
    // 手机号登录
    const phoneInput = page.locator('input[type="tel"], input[placeholder*="手机"]').first();
    if (await phoneInput.isVisible()) {{
      await phoneInput.fill('{username}');
      console.log('📱 输入手机号');
    }}
  }} else {{
    // 邮箱登录
    const emailInput = page.locator('input[type="email"], input[placeholder*="邮箱"]').first();
    if (await emailInput.isVisible()) {{
      await emailInput.fill('{username}');
      console.log('📧 输入邮箱');
    }}
  }}
  
  // 输入密码
  const passwordInput = page.locator('input[type="password"]').first();
  if (await passwordInput.isVisible()) {{
    await passwordInput.fill('{password}');
    console.log('🔒 输入密码');
  }}
  
  await page.waitForTimeout(1000);
  
  // 查找登录按钮
  const loginButton = page.locator('button:has-text("登录"), button[type="submit"]').first();
  if (await loginButton.isVisible()) {{
    console.log('🖱️ 点击登录按钮');
    await loginButton.click();
    
    // 等待登录完成
    await page.waitForTimeout(5000);
    
    // 检查登录结果
    const currentUrl = page.url();
    console.log('📍 当前URL:', currentUrl);
    
    if (!currentUrl.includes('login') && !currentUrl.includes('user')) {{
      console.log('✅ 登录成功！');
      
      // 截图成功页面
      await page.screenshot({{ path: '/tmp/xiaohongshu_login_success.png', fullPage: true }});
      console.log('📸 登录成功截图已保存');
      
      // 访问主页
      await page.goto('https://www.xiaohongshu.com');
      await page.waitForTimeout(3000);
      
      // 截图主页
      await page.screenshot({{ path: '/tmp/xiaohongshu_homepage.png', fullPage: true }});
      console.log('📸 主页截图已保存');
      
      return true;
    }} else {{
      console.log('❌ 登录失败，仍在登录页面');
      
      // 检查错误信息
      const errorElement = page.locator('.error-message, .ant-message-error').first();
      if (await errorElement.isVisible()) {{
        const errorText = await errorElement.textContent();
        console.log('❌ 错误信息:', errorText);
      }}
      
      // 检查验证码
      const captchaElement = page.locator('img[src*="captcha"], .captcha-image').first();
      if (await captchaElement.isVisible()) {{
        console.log('⚠️  需要验证码');
        await captchaElement.screenshot({{ path: '/tmp/xiaohongshu_captcha.png' }});
        console.log('📸 验证码图片已保存: /tmp/xiaohongshu_captcha.png');
        console.log('请手动查看验证码图片并输入验证码');
      }}
      
      return false;
    }}
  }} else {{
    console.log('❌ 未找到登录按钮');
    return false;
  }}
}});
"""

def create_browse_script():
    """创建浏览脚本"""
    return """
const {{ test, expect }} = require('@playwright/test');

test('小红书浏览测试', async ({{ page }}) => {{
  console.log('🏠 浏览小红书主页...');
  
  // 直接访问主页
  await page.goto('https://www.xiaohongshu.com');
  console.log('🌐 访问主页');
  
  // 等待页面加载
  await page.waitForTimeout(5000);
  
  // 截图
  await page.screenshot({{ path: '/tmp/xiaohongshu_browse.png', fullPage: true }});
  console.log('📸 主页截图已保存: /tmp/xiaohongshu_browse.png');
  
  // 获取页面标题
  const title = await page.title();
  console.log('📄 页面标题:', title);
  
  // 尝试查找内容
  const posts = page.locator('.note-item, [data-testid="note-item"]');
  const count = await posts.count();
  console.log('📝 找到笔记数量:', count);
  
  if (count > 0) {{
    const firstPost = posts.first();
    const titleElement = firstPost.locator('.title, .note-title').first();
    if (await titleElement.isVisible()) {{
      const postTitle = await titleElement.textContent();
      console.log('📌 第一篇笔记标题:', postTitle.substring(0, 50) + '...');
    }}
  }}
  
  return true;
}});
"""

def create_search_script(keyword):
    """创建搜索脚本"""
    return f"""
const {{ test, expect }} = require('@playwright/test');

test('小红书搜索测试', async ({{ page }}) => {{
  console.log('🔍 搜索内容: {keyword}');
  
  // 访问搜索页面
  const searchUrl = `https://www.xiaohongshu.com/search_result?keyword=${{encodeURIComponent('{keyword}')}}`;
  await page.goto(searchUrl);
  console.log('🌐 访问搜索页面:', searchUrl);
  
  // 等待页面加载
  await page.waitForTimeout(5000);
  
  // 截图
  await page.screenshot({{ path: '/tmp/xiaohongshu_search.png', fullPage: true }});
  console.log('📸 搜索结果截图已保存: /tmp/xiaohongshu_search.png');
  
  // 获取搜索结果
  const resultCount = page.locator('.search-count, .result-count').first();
  if (await resultCount.isVisible()) {{
    const countText = await resultCount.textContent();
    console.log('📊 搜索结果:', countText);
  }}
  
  return true;
}});
"""

def setup_account():
    """设置账号信息"""
    print("🛠️  设置小红书账号信息")
    
    username = input("请输入用户名/手机号/邮箱: ").strip()
    password = input("请输入密码: ").strip()
    login_type = input("登录类型 (phone/email，默认phone): ").strip() or "phone"
    
    account_info = {
        "username": username,
        "password": password,
        "login_type": login_type,
        "remember_me": True
    }
    
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(ACCOUNT_FILE, 'w', encoding='utf-8') as f:
        json.dump(account_info, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 账号信息已保存到: {ACCOUNT_FILE}")
    print("⚠️  注意：密码以明文存储，请确保文件安全")

def load_account():
    """加载账号信息"""
    if not ACCOUNT_FILE.exists():
        print(f"❌ 账号配置文件不存在: {ACCOUNT_FILE}")
        print("请先运行: ./tools/xiaohongshu_login.sh setup")
        return None
    
    try:
        with open(ACCOUNT_FILE, 'r', encoding='utf-8') as f:
            account_info = json.load(f)
        print(f"✅ 加载账号信息: {account_info.get('username', '未知用户')}")
        return account_info
    except Exception as e:
        print(f"❌ 加载账号信息失败: {e}")
        return None

def test_login():
    """测试登录"""
    print("🧪 测试小红书登录...")
    
    account = load_account()
    if not account:
        return False
    
    script = create_login_script(
        account['username'],
        account['password'],
        account.get('login_type', 'phone')
    )
    
    return run_playwright_command(script)

def browse():
    """浏览主页"""
    print("🏠 浏览小红书主页...")
    
    script = create_browse_script()
    return run_playwright_command(script)

def search(keyword):
    """搜索内容"""
    print(f"🔍 搜索: {keyword}")
    
    script = create_search_script(keyword)
    return run_playwright_command(script)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小红书自动化登录（简单版）')
    parser.add_argument('action', choices=['setup', 'test', 'browse', 'search'],
                       help='执行的操作')
    parser.add_argument('--keyword', help='搜索关键词（用于search操作）')
    
    args = parser.parse_args()
    
    if args.action == 'setup':
        setup_account()
    elif args.action == 'test':
        test_login()
    elif args.action == 'browse':
        browse()
    elif args.action == 'search':
        if not args.keyword:
            print("❌ 请提供搜索关键词: --keyword '关键词'")
            return
        search(args.keyword)

if __name__ == "__main__":
    main()