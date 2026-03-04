#!/usr/bin/env python3
"""
小红书自动化登录脚本
使用Playwright进行浏览器自动化
"""

import asyncio
import json
import os
import sys
import subprocess
from pathlib import Path

# 尝试导入Playwright，如果失败则使用npx
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright Python模块未安装，将使用npx playwright")

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "workspace" / "config"
ACCOUNT_FILE = CONFIG_DIR / "xiaohongshu_account.json"
COOKIE_FILE = CONFIG_DIR / "xiaohongshu_cookies.json"

class XiaohongshuLogin:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.account_info = None
        
    def load_account(self):
        """加载账号信息"""
        if not ACCOUNT_FILE.exists():
            print(f"❌ 账号配置文件不存在: {ACCOUNT_FILE}")
            print("请先运行: ./tools/xiaohongshu_login.sh setup")
            return False
            
        try:
            with open(ACCOUNT_FILE, 'r', encoding='utf-8') as f:
                self.account_info = json.load(f)
            print(f"✅ 加载账号信息: {self.account_info.get('username', '未知用户')}")
            return True
        except Exception as e:
            print(f"❌ 加载账号信息失败: {e}")
            return False
    
    async def init_browser(self):
        """初始化浏览器"""
        print("🚀 启动浏览器...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-gpu']
        )
        self.page = await self.browser.new_page()
        
        # 设置用户代理和视口
        await self.page.set_viewport_size({"width": 1280, "height": 800})
        print("✅ 浏览器初始化完成")
    
    async def navigate_to_login(self):
        """导航到登录页面"""
        print("🌐 访问小红书登录页面...")
        
        # 尝试直接访问登录页面
        login_url = "https://www.xiaohongshu.com/user/login"
        try:
            await self.page.goto(login_url, wait_until="networkidle", timeout=30000)
            
            # 检查当前URL，小红书可能会重定向
            current_url = self.page.url
            print(f"📍 当前URL: {current_url}")
            
            # 检查是否已经在登录页面
            if "login" in current_url or "user" in current_url:
                print("✅ 已到达登录页面")
                return True
            else:
                print("⚠️  可能已登录或重定向到其他页面")
                # 尝试查找登录按钮
                login_button = await self.page.query_selector('text=登录')
                if login_button:
                    print("🔍 找到登录按钮，点击...")
                    await login_button.click()
                    await asyncio.sleep(2)
                    return True
                
                return False
                
        except Exception as e:
            print(f"❌ 访问登录页面失败: {e}")
            return False
    
    async def perform_login(self):
        """执行登录操作"""
        if not self.account_info:
            print("❌ 账号信息未加载")
            return False
            
        username = self.account_info.get('username', '')
        password = self.account_info.get('password', '')
        login_type = self.account_info.get('login_type', 'phone')
        
        print(f"🔑 尝试登录: {username} ({login_type})")
        
        try:
            # 等待登录表单加载
            await self.page.wait_for_selector('input[type="text"], input[type="tel"], input[type="email"]', timeout=10000)
            
            # 根据登录类型选择输入框
            if login_type == 'phone':
                # 手机号登录
                phone_input = await self.page.query_selector('input[type="tel"], input[placeholder*="手机"]')
                if phone_input:
                    await phone_input.fill(username)
                    print("📱 输入手机号")
            else:
                # 邮箱登录
                email_input = await self.page.query_selector('input[type="email"], input[placeholder*="邮箱"]')
                if email_input:
                    await email_input.fill(username)
                    print("📧 输入邮箱")
            
            # 输入密码
            password_input = await self.page.query_selector('input[type="password"]')
            if password_input:
                await password_input.fill(password)
                print("🔒 输入密码")
            
            # 等待一下让页面更新
            await asyncio.sleep(1)
            
            # 查找并点击登录按钮
            login_button = await self.page.query_selector('button:has-text("登录"), button[type="submit"]')
            if login_button:
                print("🖱️ 点击登录按钮")
                await login_button.click()
                
                # 等待登录完成
                await asyncio.sleep(3)
                
                # 检查登录是否成功
                current_url = self.page.url
                if "login" not in current_url and "user" not in current_url:
                    print("✅ 登录成功！")
                    
                    # 保存cookies
                    await self.save_cookies()
                    
                    # 截图确认
                    screenshot_path = "/tmp/xiaohongshu_login_success.png"
                    await self.page.screenshot(path=screenshot_path, full_page=True)
                    print(f"📸 登录成功截图: {screenshot_path}")
                    
                    return True
                else:
                    print("❌ 登录失败，仍在登录页面")
                    # 检查是否有错误信息
                    error_msg = await self.page.query_selector('.error-message, .ant-message-error')
                    if error_msg:
                        error_text = await error_msg.text_content()
                        print(f"❌ 错误信息: {error_text}")
                    
                    # 检查是否需要验证码
                    captcha = await self.page.query_selector('img[src*="captcha"], .captcha-image')
                    if captcha:
                        print("⚠️  需要验证码，请手动处理")
                        # 保存验证码图片
                        captcha_path = "/tmp/xiaohongshu_captcha.png"
                        await captcha.screenshot(path=captcha_path)
                        print(f"📸 验证码图片: {captcha_path}")
                        
                        # 这里可以扩展：等待用户输入验证码
                        print("请查看验证码图片并输入验证码:")
                        # captcha_code = input("验证码: ")
                        # 然后输入验证码并继续
                    
                    return False
            else:
                print("❌ 未找到登录按钮")
                return False
                
        except Exception as e:
            print(f"❌ 登录过程中出错: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def save_cookies(self):
        """保存cookies到文件"""
        try:
            cookies = await self.page.context.cookies()
            with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            print(f"✅ Cookies已保存到: {COOKIE_FILE}")
            return True
        except Exception as e:
            print(f"❌ 保存cookies失败: {e}")
            return False
    
    async def load_cookies(self):
        """从文件加载cookies"""
        if not COOKIE_FILE.exists():
            return False
            
        try:
            with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            await self.page.context.add_cookies(cookies)
            print(f"✅ Cookies已加载: {len(cookies)}个")
            return True
        except Exception as e:
            print(f"❌ 加载cookies失败: {e}")
            return False
    
    async def test_login(self):
        """测试登录功能"""
        print("🧪 测试小红书登录...")
        
        # 加载账号
        if not self.load_account():
            return False
        
        # 初始化浏览器
        await self.init_browser()
        
        try:
            # 尝试加载cookies
            cookies_loaded = await self.load_cookies()
            
            if cookies_loaded:
                # 直接访问主页测试cookies是否有效
                await self.page.goto("https://www.xiaohongshu.com", wait_until="networkidle", timeout=15000)
                
                # 检查是否已登录
                user_element = await self.page.query_selector('text=我的, .user-avatar, [data-testid="user-menu"]')
                if user_element:
                    print("✅ Cookies有效，已登录状态")
                    return True
                else:
                    print("⚠️ Cookies无效或已过期，需要重新登录")
            
            # 需要重新登录
            print("🔄 需要重新登录...")
            
            # 导航到登录页面
            if not await self.navigate_to_login():
                print("❌ 无法访问登录页面")
                return False
            
            # 执行登录
            login_success = await self.perform_login()
            
            if login_success:
                print("✅ 登录测试成功！")
                return True
            else:
                print("❌ 登录测试失败")
                return False
                
        finally:
            # 关闭浏览器
            if self.browser:
                await self.browser.close()
                print("🔒 浏览器已关闭")
    
    async def browse_homepage(self):
        """浏览主页"""
        print("🏠 浏览小红书主页...")
        
        if not self.load_account():
            return False
        
        await self.init_browser()
        
        try:
            # 尝试加载cookies
            await self.load_cookies()
            
            # 访问主页
            await self.page.goto("https://www.xiaohongshu.com", wait_until="networkidle", timeout=15000)
            
            # 截图
            screenshot_path = "/tmp/xiaohongshu_homepage.png"
            await self.page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 主页截图: {screenshot_path}")
            
            # 获取页面标题
            title = await self.page.title()
            print(f"📄 页面标题: {title}")
            
            # 尝试获取一些内容
            try:
                # 查找推荐内容
                posts = await self.page.query_selector_all('.note-item, [data-testid="note-item"]')
                print(f"📝 找到 {len(posts)} 篇笔记")
                
                if posts and len(posts) > 0:
                    # 获取第一篇笔记的标题
                    first_post = posts[0]
                    title_element = await first_post.query_selector('.title, .note-title')
                    if title_element:
                        post_title = await title_element.text_content()
                        print(f"📌 第一篇笔记标题: {post_title[:50]}...")
            
            except Exception as e:
                print(f"⚠️  获取内容时出错: {e}")
            
            return True
            
        finally:
            if self.browser:
                await self.browser.close()
    
    async def search_content(self, keyword):
        """搜索内容"""
        print(f"🔍 搜索: {keyword}")
        
        if not self.load_account():
            return False
        
        await self.init_browser()
        
        try:
            # 尝试加载cookies
            await self.load_cookies()
            
            # 访问搜索页面
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
            await self.page.goto(search_url, wait_until="networkidle", timeout=15000)
            
            # 截图
            screenshot_path = f"/tmp/xiaohongshu_search_{keyword}.png"
            await self.page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 搜索结果截图: {screenshot_path}")
            
            # 获取搜索结果数量
            try:
                result_count = await self.page.query_selector('.search-count, .result-count')
                if result_count:
                    count_text = await result_count.text_content()
                    print(f"📊 搜索结果: {count_text}")
            except:
                pass
            
            return True
            
        finally:
            if self.browser:
                await self.browser.close()

async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小红书自动化登录')
    parser.add_argument('action', choices=['test', 'login', 'browse', 'search', 'setup'],
                       help='执行的操作')
    parser.add_argument('--keyword', help='搜索关键词（用于search操作）')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='无头模式（默认）')
    parser.add_argument('--visible', action='store_false', dest='headless',
                       help='显示浏览器窗口')
    
    args = parser.parse_args()
    
    # 确保配置目录存在
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 创建实例
    xhs = XiaohongshuLogin(headless=args.headless)
    
    if args.action == 'setup':
        # 交互式设置账号
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
        
        with open(ACCOUNT_FILE, 'w', encoding='utf-8') as f:
            json.dump(account_info, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 账号信息已保存到: {ACCOUNT_FILE}")
        print("⚠️  注意：密码以明文存储，请确保文件安全")
        
    elif args.action == 'test':
        await xhs.test_login()
        
    elif args.action == 'login':
        if xhs.load_account():
            await xhs.init_browser()
            try:
                await xhs.navigate_to_login()
                await xhs.perform_login()
            finally:
                if xhs.browser:
                    await xhs.browser.close()
        
    elif args.action == 'browse':
        await xhs.browse_homepage()
        
    elif args.action == 'search':
        if not args.keyword:
            print("❌ 请提供搜索关键词: --keyword '关键词'")
            return
        await xhs.search_content(args.keyword)

if __name__ == "__main__":
    asyncio.run(main())