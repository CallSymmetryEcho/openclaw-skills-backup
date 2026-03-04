#!/usr/bin/env python3
"""
使用Cookie搜索小红书内容
"""

import asyncio
import json
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright未安装")
    sys.exit(1)

COOKIE_FILE = Path.home() / ".openclaw" / "workspace" / "config" / "xiaohongshu_cookies.json"

class XiaohongshuSearcher:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        
    async def init_browser(self):
        """初始化浏览器"""
        print("🚀 启动浏览器...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-gpu']
        )
        self.context = await self.browser.new_context(
            viewport={"width": 1200, "height": 800}
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
            
            # 先访问小红书域名，然后添加Cookie
            await self.page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded")
            await asyncio.sleep(2)
            
            # 添加Cookie到上下文
            await self.context.add_cookies(cookies)
            print("✅ Cookie加载完成")
            return True
            
        except Exception as e:
            print(f"❌ 加载Cookie失败: {e}")
            return False
    
    async def search(self, keyword):
        """搜索内容"""
        print(f"\n🔍 搜索: {keyword}")
        
        try:
            # 构建搜索URL
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes"
            
            print(f"🌐 访问搜索页面...")
            await self.page.goto(search_url, wait_until="networkidle")
            await asyncio.sleep(5)  # 等待内容加载
            
            # 截图保存搜索结果
            screenshot_path = Path.home() / ".openclaw" / "workspace" / "config" / "xiaohongshu_search.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 搜索结果截图已保存: {screenshot_path}")
            
            # 提取搜索结果
            print("\n📊 提取搜索结果...")
            
            # 尝试多种选择器提取笔记标题
            selectors = [
                '.note-item .title',
                '.feeds-page .note-item',
                '[data-v-] .title',
                '.search-result-item',
                '.note-container',
                'div[class*="note"]',
                'div[class*="content"]'
            ]
            
            results = []
            
            for selector in selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements:
                        print(f"✅ 找到元素: {selector} ({len(elements)} 个)")
                        
                        for i, element in enumerate(elements[:10]):  # 只取前10个
                            try:
                                # 获取文本内容
                                text = await element.text_content()
                                if text and len(text.strip()) > 5:
                                    results.append({
                                        'selector': selector,
                                        'text': text.strip()[:200]  # 限制长度
                                    })
                            except:
                                continue
                        
                        if len(results) >= 5:
                            break
                            
                except Exception as e:
                    continue
            
            # 也尝试获取页面标题和描述
            try:
                page_title = await self.page.title()
                print(f"📄 页面标题: {page_title}")
            except:
                page_title = "未知"
            
            return {
                'success': True,
                'keyword': keyword,
                'page_title': page_title,
                'results_count': len(results),
                'results': results,
                'screenshot': str(screenshot_path)
            }
            
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            print("👋 浏览器已关闭")

async def main():
    """主函数"""
    keyword = "Nature Communication"
    
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    
    print("=" * 60)
    print(f"小红书搜索: {keyword}")
    print("=" * 60)
    
    searcher = XiaohongshuSearcher()
    
    try:
        # 初始化浏览器
        await searcher.init_browser()
        
        # 加载Cookie
        if not await searcher.load_cookies():
            print("❌ 无法加载Cookie")
            return
        
        # 执行搜索
        result = await searcher.search(keyword)
        
        # 显示结果
        print("\n" + "=" * 60)
        print("📊 搜索结果")
        print("=" * 60)
        
        if result['success']:
            print(f"✅ 搜索成功")
            print(f"📄 页面标题: {result['page_title']}")
            print(f"📊 找到 {result['results_count']} 条结果")
            
            if result['results']:
                print("\n📋 内容摘要:")
                for i, item in enumerate(result['results'][:5], 1):
                    print(f"\n{i}. {item['text'][:150]}...")
            else:
                print("\n⚠️  未提取到具体内容，请查看截图")
            
            print(f"\n📸 截图文件: {result['screenshot']}")
        else:
            print(f"❌ 搜索失败: {result.get('error', '未知错误')}")
        
        # 输出JSON格式结果
        print("\n" + "=" * 60)
        print("📊 JSON输出")
        print("=" * 60)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await searcher.close()

if __name__ == "__main__":
    asyncio.run(main())