#!/usr/bin/env python3
"""
小红书扫码登录集成脚本
在OpenClaw中运行，获取二维码并发送到聊天框
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xiaohongshu_qrcode import XiaohongshuQRCodeLogin

async def main():
    """主函数：获取二维码并发送到聊天框"""
    print("🔐 小红书扫码登录流程开始")
    print("=" * 60)
    
    # 创建登录实例
    xhs = XiaohongshuQRCodeLogin(headless=True)
    
    try:
        # 1. 获取二维码
        print("📱 正在获取登录二维码...")
        result = await xhs.run_qrcode_login()
        
        if not result:
            print("❌ 获取二维码失败")
            return
        
        if result.get('status') != 'qrcode_ready':
            print(f"❌ 二维码准备失败: {result}")
            return
        
        # 2. 显示二维码信息
        qrcode_path = result.get('qrcode_path')
        qrcode_base64 = result.get('qrcode_base64')
        
        print("✅ 二维码已生成")
        print(f"📁 文件: {qrcode_path}")
        print(f"📊 Base64长度: {len(qrcode_base64) if qrcode_base64 else 0}")
        print("=" * 60)
        
        # 3. 准备发送到聊天框的消息
        message_content = f"""
🔐 **小红书扫码登录**

请使用小红书APP扫描以下二维码完成登录：

📱 **操作步骤**:
1. 打开小红书APP
2. 点击"我的" → 右上角扫一扫
3. 扫描下方二维码
4. 在APP中确认登录

⏳ **登录检测**:
扫码后，我会自动检测登录状态并保存Cookie。

✅ **完成后**:
登录成功后，Cookie将自动保存，后续可以直接使用。

⚠️ **注意**:
- 二维码有效期为5分钟
- 请确保网络畅通
- 登录后不要关闭浏览器窗口
"""
        
        # 4. 输出结果供OpenClaw处理
        output = {
            'status': 'ready',
            'action': 'send_qrcode',
            'message': message_content,
            'qrcode_path': qrcode_path,
            'qrcode_base64': qrcode_base64,
            'next_step': '等待用户扫码，然后运行 complete 操作'
        }
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
        # 5. 提示用户下一步
        print("\n" + "=" * 60)
        print("📤 **下一步**:")
        print("1. 二维码已准备好")
        print("2. 需要将二维码图片发送到聊天框")
        print("3. 用户扫码后，运行 complete 操作检测登录状态")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 扫码登录流程出错: {e}")
        import traceback
        traceback.print_exc()
        
        error_output = {
            'status': 'error',
            'message': f'扫码登录失败: {str(e)}'
        }
        print(json.dumps(error_output, ensure_ascii=False, indent=2))
        
    finally:
        # 注意：这里不关闭浏览器，因为需要保持会话等待扫码
        print("⚠️  浏览器会话保持中，等待扫码...")
        print("   如需关闭，请手动调用关闭函数")

if __name__ == "__main__":
    # 检查是否在OpenClaw环境中
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 用户中断操作")
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")