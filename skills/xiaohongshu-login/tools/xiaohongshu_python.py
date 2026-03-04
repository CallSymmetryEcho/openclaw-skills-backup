#!/usr/bin/env python3
"""
小红书Python版登录脚本 - 使用Python playwright模块
需要pip install playwright
"""

import asyncio
import json
import os
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright Python模块未安装")
    print("请运行: pip install playwright")
    print("然后运行: playwright install chromium")
    sys.exit(1)

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "workspace" / "config"
STATE_FILE = CONFIG_DIR / "xiaohongshu_state.json"
ACCOUNT_FILE = CONFIG_DIR / "xiaohongshu_account.json"

class XiaohongshuPython:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.context = None
        
    async def init_browser(self, load_state=True):
        """初始化浏览器"""
        print("🚀 启动浏览器（Python Playwright）...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-gpu']
        )
        
        context_args = {
            "viewport": {"width": 1280, "height": 800},
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        
        if load_state and STATE_FILE.exists():
            context_args["storage_state"] = STATE_FILE
            print("✅ 找到历史授权状态，正在注入 (包含 Cookie 和 LocalStorage)...")
            
        self.context = await self.browser.new_context(**context_args)
        
        # 隐藏 WebDriver 特征防爬虫检测
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        self.page = await self.context.new_page()
        print("✅ 浏览器初始化完成")
    
    async def save_cookies(self):
        """保存完整状态到文件(取代单一的保存Cookie)"""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            await self.context.storage_state(path=STATE_FILE)
            print(f"✅ 完整状态(含Cookie和LocalStorage)已保存到: {STATE_FILE}")
            return True
        except Exception as e:
            print(f"❌ 保存状态失败: {e}")
            return False
    
    async def load_cookies(self):
        """为了兼容旧的调用代码保留此方法，实际在init_browser中已加载"""
        if not STATE_FILE.exists():
            return False
        return True
    
    async def extract_cookies_manual(self):
        """手动提取Cookie（指导用户操作）"""
        print("📋 手动提取Cookie指南")
        print("=" * 60)
        print("步骤:")
        print("1. 浏览器窗口将打开")
        print("2. 手动登录小红书（手机号+验证码）")
        print("3. 登录成功后等待10秒")
        print("4. 脚本自动保存Cookie")
        print("=" * 60)
        
        # 初始化浏览器（非无头模式）
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=False,  # 显示浏览器窗口
            args=['--no-sandbox', '--disable-gpu']
        )
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        await self.context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        self.page = await self.context.new_page()
        
        try:
            # 访问登录页面
            await self.page.goto("https://www.xiaohongshu.com/user/login")
            print("🌐 已打开小红书登录页面")
            print("⏳ 请手动完成登录...")
            
            # 等待用户手动登录（60秒）
            for i in range(60):
                current_url = self.page.url
                if "login" not in current_url and "user" not in current_url:
                    print("✅ 检测到登录成功！")
                    
                    # 等待页面稳定
                    await asyncio.sleep(5)
                    
                    # 保存Cookie
                    if await self.save_cookies():
                        print("🎉 Cookie提取完成！")
                        
                        # 截图确认
                        await self.page.screenshot(path="/tmp/xiaohongshu_login_success_py.png", full_page=True)
                        print("📸 登录成功截图已保存")
                        
                        return True
                
                await asyncio.sleep(1)
                if i % 10 == 0:
                    print(f"⏰ 等待中... {i+1}/60秒")
            
            print("❌ 登录超时或未完成")
            return False
            
        finally:
            await self.browser.close()
    
    async def test_cookies(self):
        """测试Cookie有效性"""
        print("🧪 测试Cookie登录...")
        
        await self.init_browser()
        
        try:
            # 加载Cookie
            if not await self.load_cookies():
                print("❌ 无法加载Cookie，请先获取Cookie")
                return False
            
            # 访问主页
            await self.page.goto("https://www.xiaohongshu.com", wait_until="networkidle")
            
            # 检查登录状态
            current_url = self.page.url
            print(f"📍 当前URL: {current_url}")
            
            # 查找用户元素
            user_selectors = [
                'text=我的',
                '.user-avatar',
                '[data-testid="user-menu"]',
                'div:has-text("我")'
            ]
            
            user_logged_in = False
            for selector in user_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        user_text = await element.text_content()
                        print(f"✅ 已登录状态，用户元素: {user_text[:50]}...")
                        user_logged_in = True
                        break
                except:
                    continue
            
            if user_logged_in:
                # 截图
                await self.page.screenshot(path="/tmp/xiaohongshu_cookie_test_py.png", full_page=True)
                print("📸 Cookie测试截图已保存")
                return True
            else:
                print("❌ Cookie无效或已过期")
                return False
                
        finally:
            await self.browser.close()
    
    async def browse_with_cookies(self):
        """使用Cookie浏览"""
        print("🏠 使用Cookie浏览小红书...")
        
        await self.init_browser()
        
        try:
            # 加载Cookie
            if not await self.load_cookies():
                print("❌ 无法加载Cookie")
                return False
            
            # 访问主页
            await self.page.goto("https://www.xiaohongshu.com", wait_until="networkidle")
            await asyncio.sleep(3)
            
            # 截图
            await self.page.screenshot(path="/tmp/xiaohongshu_browse_py.png", full_page=True)
            print("📸 主页截图已保存")
            
            # 获取页面标题
            title = await self.page.title()
            print(f"📄 页面标题: {title}")
            
            # 尝试获取内容
            try:
                # 查找笔记
                posts = await self.page.query_selector_all('.note-item, [data-testid="note-item"], .feeds-container .note')
                print(f"📝 找到 {len(posts)} 篇笔记")
                
                if posts and len(posts) > 0:
                    # 获取第一篇笔记信息
                    first_post = posts[0]
                    
                    # 截图第一篇笔记
                    await first_post.screenshot(path="/tmp/xiaohongshu_first_note_py.png")
                    print("📸 第一篇笔记截图已保存")
                    
                    # 尝试获取标题
                    title_element = await first_post.query_selector('.title, .note-title, .content')
                    if title_element:
                        post_title = await title_element.text_content()
                        print(f"📌 笔记标题: {post_title[:100]}...")
                    
                    # 尝试获取作者
                    author_element = await first_post.query_selector('.author, .user-name, .nickname')
                    if author_element:
                        author = await author_element.text_content()
                        print(f"👤 作者: {author}")
                
            except Exception as e:
                print(f"⚠️  获取内容时出错: {e}")
            
            return True
            
        finally:
            await self.browser.close()
    
    async def search_with_cookies(self, keyword):
        """使用Cookie搜索"""
        print(f"🔍 搜索内容: {keyword}")
        
        await self.init_browser()
        
        try:
            # 加载Cookie
            if not await self.load_cookies():
                print("❌ 无法加载Cookie")
                return False
            
            # 访问搜索页面
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
            await self.page.goto(search_url, wait_until="networkidle")
            await asyncio.sleep(3)
            
            # 截图
            await self.page.screenshot(path=f"/tmp/xiaohongshu_search_{keyword}_py.png", full_page=True)
            print("📸 搜索页面截图已保存")
            
            # 获取搜索结果
            try:
                # 查找结果数量
                result_selectors = ['.search-count', '.result-count', 'div:has-text("结果")']
                for selector in result_selectors:
                    element = await self.page.query_selector(selector)
                    if element:
                        count_text = await element.text_content()
                        print(f"📊 搜索结果: {count_text}")
                        break
                
                # 查找具体结果
                results = await self.page.query_selector_all('.note-item, [data-testid="note-item"], .search-result-item')
                print(f"🔍 找到 {len(results)} 个结果")
                
                if results and len(results) > 0:
                    # 显示前3个结果
                    for i in range(min(3, len(results))):
                        result = results[i]
                        title_element = await result.query_selector('.title, .note-title, .content')
                        if title_element:
                            title = await title_element.text_content()
                            print(f"  {i+1}. {title[:80]}...")
                
            except Exception as e:
                print(f"⚠️  获取搜索结果时出错: {e}")
            
            return True
            
        finally:
            await self.browser.close()

async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小红书Python版Cookie管理')
    parser.add_argument('action', choices=['extract', 'test', 'browse', 'search'],
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
    xhs = XiaohongshuPython(headless=args.headless)
    
    if args.action == 'extract':
        # 提取Cookie需要显示浏览器
        xhs.headless = False
        await xhs.extract_cookies_manual()
        
    elif args.action == 'test':
        await xhs.test_cookies()
        
    elif args.action == 'browse':
        await xhs.browse_with_cookies()
        
    elif args.action == 'search':
        if not args.keyword:
            print("❌ 请提供搜索关键词: --keyword '关键词'")
            return
        await xhs.search_with_cookies(args.keyword)

if __name__ == "__main__":
    # 检查Playwright是否安装
    if not PLAYWRIGHT_AVAILABLE:
        print("请先安装Playwright:")
        print("  pip install playwright")
        print("  playwright install chromium")
        sys.exit(1)
    
    asyncio.run(main())