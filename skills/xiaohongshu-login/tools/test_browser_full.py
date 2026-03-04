#!/usr/bin/env python3
"""
小红书浏览功能全面测试
测试各种页面和交互场景
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright未安装")
    sys.exit(1)

COOKIE_FILE = Path.home() / ".openclaw" / "workspace" / "config" / "xiaohongshu_cookies.json"
TEST_RESULTS_DIR = Path.home() / ".openclaw" / "workspace" / "config" / "test_results"
TEST_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

class XiaohongshuBrowserTest:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.results = []
        
    async def init_browser(self):
        """初始化浏览器"""
        print("🚀 初始化浏览器...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
        )
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.page = await self.context.new_page()
        print("✅ 浏览器初始化完成")
    
    async def load_cookies(self):
        """加载Cookie"""
        if not COOKIE_FILE.exists():
            print(f"❌ Cookie文件不存在: {COOKIE_FILE}")
            return False
        
        try:
            with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            print(f"📋 加载 {len(cookies)} 个Cookie")
            
            # 先访问小红书，再添加Cookie
            await self.page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded")
            await asyncio.sleep(2)
            
            await self.context.add_cookies(cookies)
            print("✅ Cookie加载完成")
            return True
            
        except Exception as e:
            print(f"❌ 加载Cookie失败: {e}")
            return False
    
    async def test_homepage(self):
        """测试主页浏览"""
        print("\n" + "="*60)
        print("📱 测试1: 主页浏览")
        print("="*60)
        
        try:
            await self.page.goto("https://www.xiaohongshu.com", wait_until="networkidle")
            await asyncio.sleep(3)
            
            # 截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = TEST_RESULTS_DIR / f"homepage_{timestamp}.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            
            # 获取页面信息
            title = await self.page.title()
            url = self.page.url
            
            # 检测登录状态
            login_indicators = [
                '.user-avatar',
                '[data-testid="user-menu"]',
                'text=我的',
                '.login-success'
            ]
            
            logged_in = False
            for selector in login_indicators:
                try:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        logged_in = True
                        break
                except:
                    continue
            
            result = {
                'test': 'homepage',
                'success': True,
                'title': title,
                'url': url,
                'logged_in': logged_in,
                'screenshot': str(screenshot_path)
            }
            
            print(f"✅ 主页加载成功")
            print(f"📄 标题: {title}")
            print(f"🔗 URL: {url}")
            print(f"🔑 登录状态: {'已登录' if logged_in else '未登录'}")
            print(f"📸 截图: {screenshot_path}")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'test': 'homepage',
                'success': False,
                'error': str(e)
            }
            print(f"❌ 主页测试失败: {e}")
            self.results.append(result)
            return result
    
    async def test_explore_page(self):
        """测试发现/探索页面"""
        print("\n" + "="*60)
        print("🔍 测试2: 发现页面")
        print("="*60)
        
        try:
            await self.page.goto("https://www.xiaohongshu.com/explore", wait_until="networkidle")
            await asyncio.sleep(3)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = TEST_RESULTS_DIR / f"explore_{timestamp}.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            
            # 获取内容数量
            content_selectors = ['.note-item', '.feeds-item', '[data-v-]']
            content_count = 0
            
            for selector in content_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if len(elements) > content_count:
                        content_count = len(elements)
                except:
                    continue
            
            result = {
                'test': 'explore',
                'success': True,
                'content_count': content_count,
                'screenshot': str(screenshot_path)
            }
            
            print(f"✅ 发现页面加载成功")
            print(f"📊 内容数量: {content_count}")
            print(f"📸 截图: {screenshot_path}")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'test': 'explore',
                'success': False,
                'error': str(e)
            }
            print(f"❌ 发现页面测试失败: {e}")
            self.results.append(result)
            return result
    
    async def test_user_profile(self):
        """测试用户个人页面"""
        print("\n" + "="*60)
        print("👤 测试3: 用户个人页面")
        print("="*60)
        
        try:
            # 尝试访问一个示例用户页面（使用小红书官方账号）
            await self.page.goto("https://www.xiaohongshu.com/user/profile/5c7a9c8b000000001001f536", 
                               wait_until="networkidle")
            await asyncio.sleep(3)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = TEST_RESULTS_DIR / f"profile_{timestamp}.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            
            # 获取用户信息
            user_info = {}
            try:
                nickname_elem = await self.page.query_selector('.user-nickname, .nickname')
                if nickname_elem:
                    user_info['nickname'] = await nickname_elem.text_content()
            except:
                pass
            
            result = {
                'test': 'user_profile',
                'success': True,
                'user_info': user_info,
                'screenshot': str(screenshot_path)
            }
            
            print(f"✅ 用户页面加载成功")
            print(f"👤 用户信息: {user_info}")
            print(f"📸 截图: {screenshot_path}")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'test': 'user_profile',
                'success': False,
                'error': str(e)
            }
            print(f"❌ 用户页面测试失败: {e}")
            self.results.append(result)
            return result
    
    async def test_scroll_loading(self):
        """测试滚动加载更多内容"""
        print("\n" + "="*60)
        print("📜 测试4: 滚动加载")
        print("="*60)
        
        try:
            await self.page.goto("https://www.xiaohongshu.com/explore", wait_until="networkidle")
            await asyncio.sleep(2)
            
            # 记录初始内容数量
            initial_count = len(await self.page.query_selector_all('.note-item'))
            print(f"📊 初始内容数量: {initial_count}")
            
            # 滚动页面
            for i in range(3):
                await self.page.evaluate("window.scrollBy(0, 800)")
                await asyncio.sleep(2)
                print(f"📜 滚动 {i+1}/3 完成")
            
            # 记录滚动后内容数量
            final_count = len(await self.page.query_selector_all('.note-item'))
            print(f"📊 滚动后内容数量: {final_count}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = TEST_RESULTS_DIR / f"scroll_{timestamp}.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            
            result = {
                'test': 'scroll_loading',
                'success': True,
                'initial_count': initial_count,
                'final_count': final_count,
                'new_items': final_count - initial_count,
                'screenshot': str(screenshot_path)
            }
            
            print(f"✅ 滚动加载测试成功")
            print(f"📈 新增内容: {final_count - initial_count}")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'test': 'scroll_loading',
                'success': False,
                'error': str(e)
            }
            print(f"❌ 滚动加载测试失败: {e}")
            self.results.append(result)
            return result
    
    async def test_note_detail(self):
        """测试笔记详情页"""
        print("\n" + "="*60)
        print("📝 测试5: 笔记详情页")
        print("="*60)
        
        try:
            # 先获取一个笔记链接
            await self.page.goto("https://www.xiaohongshu.com/explore", wait_until="networkidle")
            await asyncio.sleep(2)
            
            # 尝试点击第一个笔记
            note_links = await self.page.query_selector_all('a[href*="/explore/"]')
            if note_links:
                await note_links[0].click()
                await asyncio.sleep(3)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = TEST_RESULTS_DIR / f"note_detail_{timestamp}.png"
                await self.page.screenshot(path=str(screenshot_path), full_page=True)
                
                result = {
                    'test': 'note_detail',
                    'success': True,
                    'url': self.page.url,
                    'screenshot': str(screenshot_path)
                }
                
                print(f"✅ 笔记详情页加载成功")
                print(f"🔗 URL: {self.page.url}")
                
                self.results.append(result)
                return result
            else:
                raise Exception("未找到笔记链接")
                
        except Exception as e:
            result = {
                'test': 'note_detail',
                'success': False,
                'error': str(e)
            }
            print(f"❌ 笔记详情页测试失败: {e}")
            self.results.append(result)
            return result
    
    async def test_search_function(self):
        """测试搜索功能（通过URL直接访问）"""
        print("\n" + "="*60)
        print("🔎 测试6: 搜索功能")
        print("="*60)
        
        try:
            # 直接访问搜索结果页面
            search_keywords = ["美食", "旅行", "穿搭"]
            search_results = []
            
            for keyword in search_keywords:
                print(f"\n🔍 搜索: {keyword}")
                search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
                await self.page.goto(search_url, wait_until="networkidle")
                await asyncio.sleep(3)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = TEST_RESULTS_DIR / f"search_{keyword}_{timestamp}.png"
                await self.page.screenshot(path=str(screenshot_path), full_page=True)
                
                # 获取搜索结果数量
                result_count = len(await self.page.query_selector_all('.note-item, .search-result-item'))
                
                search_results.append({
                    'keyword': keyword,
                    'result_count': result_count,
                    'screenshot': str(screenshot_path)
                })
                
                print(f"  ✅ 搜索完成，找到 {result_count} 个结果")
            
            result = {
                'test': 'search',
                'success': True,
                'searches': search_results
            }
            
            print(f"\n✅ 搜索功能测试完成")
            print(f"📊 测试了 {len(search_keywords)} 个关键词")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                'test': 'search',
                'success': False,
                'error': str(e)
            }
            print(f"❌ 搜索功能测试失败: {e}")
            self.results.append(result)
            return result
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("🧪 小红书浏览功能全面测试")
        print("="*60)
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # 初始化
        await self.init_browser()
        if not await self.load_cookies():
            print("❌ Cookie加载失败，测试终止")
            return
        
        # 运行所有测试
        await self.test_homepage()
        await self.test_explore_page()
        await self.test_user_profile()
        await self.test_scroll_loading()
        await self.test_note_detail()
        await self.test_search_function()
        
        # 生成测试报告
        await self.generate_report()
    
    async def generate_report(self):
        """生成测试报告"""
        print("\n" + "="*60)
        print("📊 测试报告")
        print("="*60)
        
        passed = sum(1 for r in self.results if r['success'])
        failed = len(self.results) - passed
        
        print(f"\n📈 测试统计:")
        print(f"  ✅ 通过: {passed}/{len(self.results)}")
        print(f"  ❌ 失败: {failed}/{len(self.results)}")
        
        print(f"\n📋 详细结果:")
        for i, result in enumerate(self.results, 1):
            status = "✅" if result['success'] else "❌"
            print(f"  {i}. {status} {result['test']}")
        
        # 保存JSON报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.results),
                'passed': passed,
                'failed': failed
            },
            'results': self.results
        }
        
        report_path = TEST_RESULTS_DIR / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 详细报告已保存: {report_path}")
        print(f"📁 所有截图保存在: {TEST_RESULTS_DIR}")
        
        return report
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            print("\n👋 浏览器已关闭")

async def main():
    """主函数"""
    tester = XiaohongshuBrowserTest()
    
    try:
        await tester.run_all_tests()
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await tester.close()

if __name__ == "__main__":
    asyncio.run(main())