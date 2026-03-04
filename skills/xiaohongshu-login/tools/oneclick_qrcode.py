#!/usr/bin/env python3
"""
小红书一键扫码登录 - OpenClaw集成版
在OpenClaw中运行，自动获取二维码并提示发送到聊天框
"""

import asyncio
import json
import sys
import os
import base64
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from xiaohongshu_qrcode import XiaohongshuQRCodeLogin
    IMPORT_SUCCESS = True
except ImportError as e:
    IMPORT_SUCCESS = False
    print(f"❌ 导入失败: {e}")
    print("请确保已安装依赖: pip install playwright")

async def get_qrcode():
    """获取二维码"""
    print("🔐 开始获取小红书登录二维码...")
    
    xhs = XiaohongshuQRCodeLogin(headless=True)
    
    try:
        result = await xhs.run_qrcode_login()
        await xhs.close()
        
        if result and result.get('status') == 'qrcode_ready':
            return {
                'success': True,
                'qrcode_path': result['qrcode_path'],
                'qrcode_base64': result['qrcode_base64'],
                'message': '二维码获取成功'
            }
        else:
            return {
                'success': False,
                'message': '获取二维码失败',
                'error': result
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'获取二维码时出错: {str(e)}'
        }

def generate_openclaw_instructions(qrcode_path, qrcode_base64=None):
    """生成OpenClaw操作指令"""
    
    instructions = f"""
## 🎯 小红书扫码登录 - 操作指令

### 步骤1: 获取二维码 ✅
二维码已生成: `{qrcode_path}`

### 步骤2: 发送二维码到聊天框
在OpenClaw中执行:
```python
message(
    action="send",
    media="{qrcode_path}",
    caption="请使用小红书APP扫描二维码登录"
)
```

### 步骤3: 用户扫码
1. 打开小红书APP
2. 点击"我的" → 右上角扫一扫
3. 扫描发送的二维码
4. 在APP中确认登录

### 步骤4: 检测登录状态
用户扫码后，在OpenClaw中执行:
```bash
exec(command="cd ~/.openclaw/workspace/skills/xiaohongshu-login && python3 ./tools/xiaohongshu_qrcode.py complete")
```

### 步骤5: 验证登录
如果登录成功，会显示:
```
✅ 登录成功！Cookie已保存
```

### 文件信息
- 二维码文件: `{qrcode_path}`
- Cookie文件: `~/.openclaw/workspace/config/xiaohongshu_cookies.json`
- 二维码目录: `~/.openclaw/workspace/config/qrcodes/`

### 注意事项
1. 二维码有效期为5分钟
2. 请确保网络可以访问小红书
3. 登录后不要立即关闭浏览器
4. Cookie保存后可用于后续操作
"""
    
    return instructions

async def main():
    """主函数"""
    
    if not IMPORT_SUCCESS:
        print("❌ 依赖未安装")
        print("请先运行: cd ~/.openclaw/workspace/skills/xiaohongshu-login && ./tools/install_deps.sh python")
        return
    
    print("=" * 60)
    print("小红书一键扫码登录")
    print("=" * 60)
    
    # 获取二维码
    print("📱 正在获取登录二维码...")
    result = await get_qrcode()
    
    if not result['success']:
        print(f"❌ 失败: {result['message']}")
        if 'error' in result:
            print(f"错误详情: {result['error']}")
        return
    
    qrcode_path = result['qrcode_path']
    
    print("✅ 二维码获取成功!")
    print(f"📁 文件: {qrcode_path}")
    
    # 检查文件是否存在
    if not os.path.exists(qrcode_path):
        print(f"❌ 二维码文件不存在: {qrcode_path}")
        return
    
    # 显示文件信息
    file_size = os.path.getsize(qrcode_path)
    print(f"📊 文件大小: {file_size / 1024:.1f} KB")
    
    # 生成操作指令
    instructions = generate_openclaw_instructions(qrcode_path, result.get('qrcode_base64'))
    
    print("\n" + "=" * 60)
    print("📋 操作指令")
    print("=" * 60)
    print(instructions)
    
    # 输出JSON格式结果（供程序化处理）
    output = {
        'status': 'qrcode_ready',
        'qrcode_path': qrcode_path,
        'file_size_kb': file_size / 1024,
        'instructions': instructions,
        'next_action': 'send_qrcode_to_chat',
        'message_action': {
            'action': 'send',
            'media': qrcode_path,
            'caption': '请使用小红书APP扫描二维码登录'
        }
    }
    
    print("\n" + "=" * 60)
    print("📊 JSON输出（供程序化处理）")
    print("=" * 60)
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 用户中断操作")
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()