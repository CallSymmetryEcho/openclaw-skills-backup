#!/usr/bin/env python3
"""
小红书Cookie管理方案
由于小红书只支持手机号验证码登录，采用Cookie导入方案
"""

import json
import os
import sys
import subprocess
import tempfile
from pathlib import Path
import base64

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "workspace" / "config"
COOKIE_FILE = CONFIG_DIR / "xiaohongshu_cookies.json"
COOKIE_EXPORT_FILE = CONFIG_DIR / "xiaohongshu_cookies_export.txt"

def create_cookie_import_script(cookies_data):
    """创建Cookie导入脚本"""
    cookies_json = json.dumps(cookies_data, ensure_ascii=False)
    
    return f"""
const {{ test, expect }} = require('@playwright/test');

test('小红书Cookie导入测试', async ({{ page, context }}) => {{
  console.log('🍪 导入Cookie...');
  
  // 解析Cookie数据
  const cookies = {cookies_json};
  
  // 添加Cookie到浏览器上下文
  await context.addCookies(cookies);
  console.log(`✅ 导入 ${{cookies.length}} 个Cookie`);
  
  // 访问小红书主页
  await page.goto('https://www.xiaohongshu.com');
  console.log('🌐 访问小红书主页');
  
  // 等待页面加载
  await page.waitForTimeout(5000);
  
  // 检查登录状态
  const currentUrl = page.url();
  console.log('📍 当前URL:', currentUrl);
  
  // 截图
  await page.screenshot({{ path: '/tmp/xiaohongshu_cookie_test.png', fullPage: true }});
  console.log('📸 截图已保存: /tmp/xiaohongshu_cookie_test.png');
  
  // 检查是否已登录
  const userElement = page.locator('text=我的, .user-avatar, [data-testid="user-menu"]').first();
  if (await userElement.isVisible()) {{
    console.log('✅ Cookie有效，已登录状态');
    
    // 获取用户信息
    const userText = await userElement.textContent();
    console.log('👤 用户信息:', userText.substring(0, 50));
    
    return true;
  }} else {{
    console.log('❌ Cookie无效或已过期');
    
    // 检查是否有登录按钮
    const loginButton = page.locator('text=登录').first();
    if (await loginButton.isVisible()) {{
      console.log('⚠️  需要重新登录');
    }}
    
    return false;
  }}
}});
"""

def create_cookie_extraction_script():
    """创建Cookie提取脚本（用于手动登录后提取Cookie）"""
    return """
const {{ test, expect }} = require('@playwright/test');

test('小红书Cookie提取', async ({ page, context }) => {
  console.log('🔍 开始手动登录小红书...');
  
  // 访问登录页面
  await page.goto('https://www.xiaohongshu.com/user/login');
  console.log('🌐 请手动完成登录流程');
  console.log('📝 步骤:');
  console.log('1. 输入手机号');
  console.log('2. 获取验证码');
  console.log('3. 输入验证码');
  console.log('4. 完成登录');
  
  // 等待用户手动登录（长时间等待）
  console.log('⏳ 等待手动登录完成（60秒）...');
  await page.waitForTimeout(60000);
  
  // 检查是否登录成功
  const currentUrl = page.url();
  console.log('📍 当前URL:', currentUrl);
  
  if (!currentUrl.includes('login') && !currentUrl.includes('user')) {
    console.log('✅ 检测到登录成功');
    
    // 获取所有Cookie
    const cookies = await context.cookies();
    console.log(`🍪 获取到 ${cookies.length} 个Cookie`);
    
    // 显示Cookie信息（简化版）
    cookies.forEach((cookie, index) => {
      console.log(`${index + 1}. ${cookie.name}: ${cookie.value.substring(0, 20)}...`);
    });
    
    // 保存Cookie到文件
    const fs = require('fs');
    const cookieFile = '/tmp/xiaohongshu_cookies_manual.json';
    fs.writeFileSync(cookieFile, JSON.stringify(cookies, null, 2));
    console.log(`💾 Cookie已保存到: ${cookieFile}`);
    
    // 显示导入指令
    console.log('\\n📋 Cookie导入指令:');
    console.log(`cat ${cookieFile} | python3 -c "import json, sys; data=json.load(sys.stdin); print(json.dumps(data, ensure_ascii=False))" > ~/.openclaw/workspace/config/xiaohongshu_cookies.json`);
    
    return true;
  } else {
    console.log('❌ 登录未完成或失败');
    return false;
  }
});
"""

def create_browse_with_cookies_script():
    """创建使用Cookie浏览的脚本"""
    return """
const {{ test, expect }} = require('@playwright/test');

test('小红书Cookie浏览', async ({ page, context }) => {
  console.log('🏠 使用Cookie浏览小红书...');
  
  // 访问主页
  await page.goto('https://www.xiaohongshu.com');
  console.log('🌐 访问小红书主页');
  
  // 等待页面加载
  await page.waitForTimeout(5000);
  
  // 截图
  await page.screenshot({ path: '/tmp/xiaohongshu_browse_cookie.png', fullPage: true });
  console.log('📸 截图已保存');
  
  // 尝试获取推荐内容
  try {
    const posts = page.locator('.note-item, [data-testid="note-item"]');
    const count = await posts.count();
    console.log(`📝 找到 ${count} 篇笔记`);
    
    if (count > 0) {
      // 获取第一篇笔记详情
      const firstPost = posts.first();
      
      // 截图第一篇笔记
      await firstPost.screenshot({ path: '/tmp/xiaohongshu_first_note.png' });
      console.log('📸 第一篇笔记截图已保存');
      
      // 获取标题
      const titleElement = firstPost.locator('.title, .note-title').first();
      if (await titleElement.isVisible()) {
        const title = await titleElement.textContent();
        console.log('📌 笔记标题:', title.substring(0, 100));
      }
      
      // 获取作者
      const authorElement = firstPost.locator('.author, .user-name').first();
      if (await authorElement.isVisible()) {
        const author = await authorElement.textContent();
        console.log('👤 作者:', author);
      }
    }
  } catch (error) {
    console.log('⚠️  获取内容时出错:', error.message);
  }
  
  return true;
});
"""

def create_search_with_cookies_script(keyword):
    """创建使用Cookie搜索的脚本"""
    return f"""
const {{ test, expect }} = require('@playwright/test');

test('小红书Cookie搜索', async ({{ page, context }}) => {{
  console.log('🔍 搜索内容: {keyword}');
  
  // 访问搜索页面
  const searchUrl = `https://www.xiaohongshu.com/search_result?keyword=${{encodeURIComponent('{keyword}')}}`;
  await page.goto(searchUrl);
  console.log('🌐 访问搜索页面:', searchUrl);
  
  // 等待页面加载
  await page.waitForTimeout(5000);
  
  // 截图
  await page.screenshot({{ path: '/tmp/xiaohongshu_search_cookie.png', fullPage: true }});
  console.log('📸 搜索页面截图已保存');
  
  // 获取搜索结果
  try {{
    const resultCount = page.locator('.search-count, .result-count').first();
    if (await resultCount.isVisible()) {{
      const countText = await resultCount.textContent();
      console.log('📊 搜索结果:', countText);
    }}
    
    // 获取前几个结果
    const results = page.locator('.note-item, [data-testid="note-item"]');
    const count = await results.count();
    console.log(`🔍 找到 ${{count}} 个结果`);
    
    if (count > 0) {{
      // 显示前3个结果
      for (let i = 0; i < Math.min(3, count); i++) {{
        const result = results.nth(i);
        const titleElement = result.locator('.title, .note-title').first();
        if (await titleElement.isVisible()) {{
          const title = await titleElement.textContent();
          console.log(`  ${{i+1}}. ${{title.substring(0, 80)}}...`);
        }}
      }}
    }}
  }} catch (error) {{
    console.log('⚠️  获取搜索结果时出错:', error.message);
  }}
  
  return true;
}});
"""

def run_playwright_command(script_content, headless=True):
    """运行Playwright命令"""
    # 创建临时JavaScript文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(script_content)
        temp_file = f.name
    
    try:
        # 运行npx playwright
        cmd = ["npx", "playwright", "test", temp_file, "--reporter=line"]
        
        if not headless:
            cmd.append("--headed")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("=" * 60)
        print("Playwright输出:")
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        print("=" * 60)
        
        return result.returncode == 0
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_file)
        except:
            pass

def load_cookies():
    """加载Cookie文件"""
    if not COOKIE_FILE.exists():
        print(f"❌ Cookie文件不存在: {COOKIE_FILE}")
        print("请先手动登录并导出Cookie，或运行提取脚本")
        return None
    
    try:
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        print(f"✅ 加载 {len(cookies)} 个Cookie")
        return cookies
    except Exception as e:
        print(f"❌ 加载Cookie失败: {e}")
        return None

def save_cookies(cookies):
    """保存Cookie到文件"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Cookie已保存到: {COOKIE_FILE}")
        return True
    except Exception as e:
        print(f"❌ 保存Cookie失败: {e}")
        return False

def import_cookies_from_export():
    """从导出文件导入Cookie"""
    if not COOKIE_EXPORT_FILE.exists():
        print(f"❌ Cookie导出文件不存在: {COOKIE_EXPORT_FILE}")
        print("请先手动登录小红书，然后导出Cookie")
        return False
    
    try:
        with open(COOKIE_EXPORT_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 尝试解析不同格式的Cookie
        cookies = []
        
        # 格式1: JSON格式
        if content.startswith('[') or content.startswith('{'):
            try:
                cookies = json.loads(content)
                print("✅ 识别为JSON格式")
            except:
                pass
        
        # 格式2: 每行一个Cookie (name=value格式)
        if not cookies:
            lines = content.split('\\n')
            for line in lines:
                line = line.strip()
                if '=' in line:
                    parts = line.split('=', 1)
                    cookie = {
                        "name": parts[0].strip(),
                        "value": parts[1].strip(),
                        "domain": ".xiaohongshu.com",
                        "path": "/"
                    }
                    cookies.append(cookie)
            if cookies:
                print(f"✅ 识别为键值对格式，解析 {len(cookies)} 个Cookie")
        
        if cookies:
            return save_cookies(cookies)
        else:
            print("❌ 无法解析Cookie格式")
            print("请确保文件包含有效的Cookie数据")
            return False
            
    except Exception as e:
        print(f"❌ 导入Cookie失败: {e}")
        return False

def test_cookie_login():
    """测试Cookie登录"""
    print("🧪 测试小红书Cookie登录...")
    
    cookies = load_cookies()
    if not cookies:
        return False
    
    script = create_cookie_import_script(cookies)
    return run_playwright_command(script, headless=True)

def extract_cookies_manual():
    """手动提取Cookie（指导用户操作）"""
    print("📋 手动提取Cookie指南")
    print("=" * 60)
    print("步骤1: 运行提取脚本（显示浏览器窗口）")
    print("步骤2: 手动完成小红书登录")
    print("步骤3: 脚本自动保存Cookie")
    print("=" * 60)
    
    confirm = input("是否继续？(y/n): ").strip().lower()
    if confirm != 'y':
        print("操作取消")
        return False
    
    script = create_cookie_extraction_script()
    return run_playwright_command(script, headless=False)

def browse_with_cookies():
    """使用Cookie浏览"""
    print("🏠 使用Cookie浏览小红书...")
    
    cookies = load_cookies()
    if not cookies:
        return False
    
    # 先测试Cookie是否有效
    test_script = create_cookie_import_script(cookies)
    if not run_playwright_command(test_script, headless=True):
        print("❌ Cookie无效，请重新获取")
        return False
    
    # 浏览主页
    browse_script = create_browse_with_cookies_script()
    return run_playwright_command(browse_script, headless=True)

def search_with_cookies(keyword):
    """使用Cookie搜索"""
    print(f"🔍 使用Cookie搜索: {keyword}")
    
    cookies = load_cookies()
    if not cookies:
        return False
    
    # 先测试Cookie是否有效
    test_script = create_cookie_import_script(cookies)
    if not run_playwright_command(test_script, headless=True):
        print("❌ Cookie无效，请重新获取")
        return False
    
    # 搜索内容
    search_script = create_search_with_cookies_script(keyword)
    return run_playwright_command(search_script, headless=True)

def show_cookie_guide():
    """显示Cookie获取指南"""
    print("📖 小红书Cookie获取指南")
    print("=" * 60)
    print("方法1: 手动提取（推荐）")
    print("  1. 运行: ./tools/xiaohongshu_cookie.sh extract")
    print("  2. 在浏览器中手动登录小红书")
    print("  3. 脚本自动保存Cookie")
    print("")
    print("方法2: 从浏览器导出")
    print("  1. 在Chrome/Firefox中登录小红书")
    print("  2. 使用浏览器开发者工具导出Cookie")
    print("  3. 保存到: ~/.openclaw/workspace/config/xiaohongshu_cookies_export.txt")
    print("  4. 运行: ./tools/xiaohongshu_cookie.sh import")
    print("")
    print("方法3: 使用已有Cookie文件")
    print("  1. 准备Cookie JSON文件")
    print("  2. 复制到: ~/.openclaw/workspace/config/xiaohongshu_cookies.json")
    print("  3. 运行: ./tools/xiaohongshu_cookie.sh test")
    print("=" * 60)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小红书Cookie管理工具')
    parser.add_argument('action', choices=['guide', 'extract', 'import', 'test', 'browse', 'search', 'show'],
                       help='执行的操作')
    parser.add_argument('--keyword', help='搜索关键词（用于search操作）')
    parser.add_argument('--headed', action='store_true', help='显示浏览器窗口')
    
    args = parser.parse_args()
    
    # 确保配置目录存在
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.action == 'guide':
        show_cookie_guide()
    elif args.action == 'extract':
        extract_cookies_manual()
    elif args.action == 'import':
        import_cookies_from_export()
    elif args.action == 'test':
        test_cookie_login()
    elif args.action == 'browse':
        browse_with_cookies()
    elif args.action == 'search':
        if not args.keyword:
            print("❌ 请提供搜索关键词: --keyword '关键词'")
            return
        search_with_cookies(args.keyword)
    elif args.action == 'show':
        cookies = load_cookies()
        if cookies:
            print(json.dumps(cookies, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()