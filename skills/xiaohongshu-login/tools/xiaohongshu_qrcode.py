#!/usr/bin/env python3
"""
小红书扫码登录原型
工作流：截取二维码图片发送到聊天框，完成验证
"""

import asyncio
import json
import os
import sys
import time
import base64
from pathlib import Path
from datetime import datetime

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
COOKIE_FILE = CONFIG_DIR / "xiaohongshu_cookies.json"
QRCODE_DIR = CONFIG_DIR / "qrcodes"
QRCODE_DIR.mkdir(parents=True, exist_ok=True)

class XiaohongshuQRCodeLogin:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.context = None
        self.qrcode_path = None
        self.login_success = False
        
    async def init_browser(self):
        """初始化浏览器"""
        print("🚀 启动浏览器（无头模式）...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,  # 强制无头模式
            args=[
                '--no-sandbox',
                '--disable-gpu',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-extensions'
            ]
        )
        self.context = await self.browser.new_context(
            viewport={"width": 1200, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = await self.context.new_page()
        print("✅ 浏览器初始化完成")
    
    async def save_cookies(self):
        """保存cookies到文件"""
        try:
            cookies = await self.context.cookies()
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 保存 {len(cookies)} 个Cookie到: {COOKIE_FILE}")
            return True
        except Exception as e:
            print(f"❌ 保存Cookie失败: {e}")
            return False
    
    async def open_xiaohongshu(self):
        """打开小红书主页"""
        print("🌐 访问小红书主页...")
        try:
            await self.page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)
            
            # 检查当前页面状态
            current_url = self.page.url
            print(f"📍 当前URL: {current_url}")
            
            # 截图主页
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            home_screenshot = QRCODE_DIR / f"xiaohongshu_home_{timestamp}.png"
            await self.page.screenshot(path=str(home_screenshot), full_page=True)
            print(f"📸 主页截图已保存: {home_screenshot}")
            
            return True
        except Exception as e:
            print(f"❌ 访问小红书失败: {e}")
            return False
    
    async def trigger_login(self):
        """触发登录流程"""
        print("🔑 尝试触发登录流程...")
        
        # 尝试多种方式触发登录
        login_selectors = [
            'text=登录',
            'text=立即登录',
            'text=登 录',
            'button:has-text("登录")',
            '.login-btn',
            '[data-testid="login-button"]',
            'a[href*="login"]',
            'div:has-text("登录")'
        ]
        
        for selector in login_selectors:
            try:
                element = await self.page.query_selector(selector)
                if element and await element.is_visible():
                    print(f"✅ 找到登录元素: {selector}")
                    
                    # 点击登录按钮
                    await element.click()
                    await asyncio.sleep(2)
                    
                    # 等待登录界面出现
                    await self.page.wait_for_timeout(3000)
                    
                    # 检查是否有二维码出现
                    qr_selectors = [
                        '.qrcode',
                        '.login-qrcode',
                        'img[src*="qrcode"]',
                        'canvas',
                        '[data-testid="qrcode"]'
                    ]
                    
                    for qr_selector in qr_selectors:
                        qr_element = await self.page.query_selector(qr_selector)
                        if qr_element and await qr_element.is_visible():
                            print(f"✅ 检测到二维码元素: {qr_selector}")
                            return True
                    
                    print("⚠️  点击了登录按钮，但未检测到二维码")
                    return True
            except Exception as e:
                print(f"⚠️  尝试选择器 {selector} 失败: {e}")
                continue
        
        print("❌ 未找到登录按钮，尝试直接访问登录页面")
        
        # 尝试直接访问登录页面
        try:
            await self.page.goto("https://www.xiaohongshu.com/user/login", wait_until="networkidle")
            await asyncio.sleep(3)
            return True
        except Exception as e:
            print(f"❌ 访问登录页面失败: {e}")
            return False
    
    async def capture_qrcode(self):
        """截取二维码图片"""
        print("📷 尝试截取二维码...")
        
        # 二维码可能的选择器
        qr_selectors = [
            '.qrcode',
            '.login-qrcode',
            'img[src*="qrcode"]',
            'canvas',
            '[data-testid="qrcode"]',
            '.qrcode-container',
            '.qrcode-wrapper',
            'div:has-text("扫码登录")'
        ]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for selector in qr_selectors:
            try:
                element = await self.page.query_selector(selector)
                if element and await element.is_visible():
                    print(f"✅ 找到二维码元素: {selector}")
                    
                    # 截取二维码区域
                    self.qrcode_path = QRCODE_DIR / f"xiaohongshu_qrcode_{timestamp}.png"
                    await element.screenshot(path=str(self.qrcode_path))
                    
                    # 也截取整个页面作为参考
                    full_screenshot = QRCODE_DIR / f"xiaohongshu_full_{timestamp}.png"
                    await self.page.screenshot(path=str(full_screenshot), full_page=True)
                    
                    print(f"📸 二维码截图已保存: {self.qrcode_path}")
                    print(f"📸 完整页面截图已保存: {full_screenshot}")
                    
                    # 获取二维码图片的base64编码
                    with open(self.qrcode_path, 'rb') as f:
                        qrcode_base64 = base64.b64encode(f.read()).decode('utf-8')
                    
                    return {
                        'success': True,
                        'qrcode_path': str(self.qrcode_path),
                        'full_screenshot': str(full_screenshot),
                        'qrcode_base64': qrcode_base64,
                        'timestamp': timestamp
                    }
            except Exception as e:
                print(f"⚠️  尝试选择器 {selector} 失败: {e}")
                continue
        
        # 如果没找到特定元素，截取整个页面
        print("⚠️  未找到特定二维码元素，截取整个页面")
        self.qrcode_path = QRCODE_DIR / f"xiaohongshu_page_{timestamp}.png"
        await self.page.screenshot(path=str(self.qrcode_path), full_page=True)
        
        with open(self.qrcode_path, 'rb') as f:
            qrcode_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        return {
            'success': True,
            'qrcode_path': str(self.qrcode_path),
            'full_screenshot': str(self.qrcode_path),
            'qrcode_base64': qrcode_base64,
            'timestamp': timestamp,
            'note': '截取了整个页面，请在其中查找二维码'
        }
    
    async def wait_for_login(self, timeout_seconds=300):
        """等待用户扫码登录"""
        print(f"⏳ 等待用户扫码登录（最多{timeout_seconds}秒）...")
        print("📱 请使用小红书APP扫描二维码")
        print("✅ 登录成功后脚本会自动检测")
        
        start_time = time.time()
        check_interval = 5  # 每5秒检查一次
        
        while time.time() - start_time < timeout_seconds:
            try:
                # 检查URL变化（登录成功后通常会跳转）
                current_url = self.page.url
                if "login" not in current_url and "user/login" not in current_url:
                    print(f"✅ URL变化检测到登录成功: {current_url}")
                    self.login_success = True
                    return True
                
                # 检查用户元素出现
                user_selectors = [
                    'text=我的',
                    '.user-avatar',
                    '[data-testid="user-menu"]',
                    'div:has-text("我")',
                    '.user-name'
                ]
                
                for selector in user_selectors:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        user_text = await element.text_content()
                        print(f"✅ 检测到用户元素: {user_text[:50]}...")
                        self.login_success = True
                        return True
                
                # 检查登录成功提示
                success_selectors = [
                    'text=登录成功',
                    'text=登录成功，正在跳转',
                    '.login-success'
                ]
                
                for selector in success_selectors:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        print("✅ 检测到登录成功提示")
                        self.login_success = True
                        return True
                
                # 显示等待时间
                elapsed = int(time.time() - start_time)
                if elapsed % 30 == 0:  # 每30秒显示一次状态
                    print(f"⏰ 已等待 {elapsed} 秒，继续等待...")
                
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                print(f"⚠️  检查登录状态时出错: {e}")
                await asyncio.sleep(check_interval)
        
        print(f"❌ 登录超时（{timeout_seconds}秒）")
        return False
    
    async def run_qrcode_login(self):
        """执行完整的扫码登录流程"""
        print("=" * 60)
        print("小红书扫码登录流程开始")
        print("=" * 60)
        
        try:
            # 1. 初始化浏览器
            await self.init_browser()
            
            # 2. 打开小红书
            if not await self.open_xiaohongshu():
                return None
            
            # 3. 触发登录
            if not await self.trigger_login():
                print("❌ 无法触发登录流程")
                return None
            
            # 4. 截取二维码
            qrcode_result = await self.capture_qrcode()
            if not qrcode_result['success']:
                print("❌ 无法截取二维码")
                return None
            
            print("=" * 60)
            print("✅ 二维码已准备就绪")
            print(f"📁 二维码文件: {qrcode_result['qrcode_path']}")
            print("=" * 60)
            
            # 返回二维码信息（主程序会处理发送到聊天框）
            result = {
                'status': 'qrcode_ready',
                'qrcode_path': qrcode_result['qrcode_path'],
                'qrcode_base64': qrcode_result['qrcode_base64'],
                'full_screenshot': qrcode_result['full_screenshot'],
                'timestamp': qrcode_result['timestamp'],
                'message': '请扫描二维码登录小红书'
            }
            
            return result
            
        except Exception as e:
            print(f"❌ 扫码登录流程出错: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def complete_login(self):
        """完成登录流程（在用户扫码后调用）"""
        print("🔄 检测登录状态...")
        
        try:
            # 等待登录成功
            if await self.wait_for_login():
                print("🎉 登录成功！")
                
                # 保存Cookie
                if await self.save_cookies():
                    print("💾 Cookie已保存")
                    
                    # 截图登录成功页面
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    success_screenshot = QRCODE_DIR / f"login_success_{timestamp}.png"
                    await self.page.screenshot(path=str(success_screenshot), full_page=True)
                    
                    return {
                        'status': 'login_success',
                        'cookie_file': str(COOKIE_FILE),
                        'screenshot': str(success_screenshot),
                        'message': '登录成功，Cookie已保存'
                    }
                else:
                    return {
                        'status': 'login_failed',
                        'message': '登录成功但保存Cookie失败'
                    }
            else:
                return {
                    'status': 'login_timeout',
                    'message': '登录超时，请重试'
                }
                
        except Exception as e:
            print(f"❌ 完成登录流程出错: {e}")
            return {
                'status': 'error',
                'message': f'登录流程出错: {str(e)}'
            }
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            print("👋 浏览器已关闭")

async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小红书扫码登录工具')
    parser.add_argument('action', choices=['qrcode', 'complete', 'test'],
                       help='执行的操作: qrcode=获取二维码, complete=完成登录, test=测试')
    
    args = parser.parse_args()
    
    # 创建实例（显示浏览器窗口）
    xhs = XiaohongshuQRCodeLogin(headless=False)
    
    try:
        if args.action == 'qrcode':
            # 获取二维码
            result = await xhs.run_qrcode_login()
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print('{"status": "error", "message": "获取二维码失败"}')
                
        elif args.action == 'complete':
            # 需要在获取二维码后调用
            print("⚠️  注意：请先运行 qrcode 操作获取二维码")
            result = await xhs.complete_login()
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif args.action == 'test':
            # 测试功能
            await xhs.init_browser()
            await xhs.open_xiaohongshu()
            print('{"status": "test_complete", "message": "测试完成"}')
            
    finally:
        await xhs.close()

if __name__ == "__main__":
    # 检查Playwright是否安装
    if not PLAYWRIGHT_AVAILABLE:
        print("请先安装Playwright:")
        print("  pip install playwright")
        print("  playwright install chromium")
        sys.exit(1)
    
    asyncio.run(main())