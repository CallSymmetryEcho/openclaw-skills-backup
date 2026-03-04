#!/bin/bash
# 小红书登录测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGIN_SCRIPT="$SCRIPT_DIR/xiaohongshu_login.sh"

echo "🧪 小红书登录技能测试"
echo "======================"

# 1. 检查脚本是否存在
if [ ! -f "$LOGIN_SCRIPT" ]; then
    echo "❌ 登录脚本不存在: $LOGIN_SCRIPT"
    exit 1
fi

echo "✅ 登录脚本存在"

# 2. 检查Python脚本
PYTHON_SCRIPT="$SCRIPT_DIR/xiaohongshu_login.py"
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Python脚本不存在: $PYTHON_SCRIPT"
    exit 1
fi

echo "✅ Python脚本存在"

# 3. 检查Playwright
echo "🔍 检查Playwright..."
if npx playwright --version 2>/dev/null; then
    echo "✅ Playwright已安装 (通过npx)"
elif python3 -c "import playwright" 2>/dev/null; then
    echo "✅ Playwright已安装 (通过pip)"
else
    echo "⚠️  Playwright未安装"
    echo "注意: 脚本使用npx playwright，确保npx可用"
fi

# 4. 检查Chromium
echo "🔍 检查Chromium浏览器..."
if [ -d "$HOME/.cache/ms-playwright" ]; then
    echo "✅ Chromium已安装"
else
    echo "⚠️  Chromium未安装"
    echo "正在安装Chromium..."
    playwright install chromium || {
        echo "❌ 安装Chromium失败"
        exit 1
    }
    echo "✅ Chromium安装成功"
fi

# 5. 测试帮助命令
echo "🔍 测试帮助命令..."
"$LOGIN_SCRIPT" help > /dev/null && echo "✅ 帮助命令正常" || {
    echo "❌ 帮助命令失败"
    exit 1
}

# 6. 检查配置文件目录
CONFIG_DIR="$HOME/.openclaw/workspace/config"
if [ -d "$CONFIG_DIR" ]; then
    echo "✅ 配置目录存在: $CONFIG_DIR"
else
    echo "⚠️  配置目录不存在，创建中..."
    mkdir -p "$CONFIG_DIR"
    echo "✅ 配置目录创建成功"
fi

# 7. 检查账号配置文件
ACCOUNT_FILE="$CONFIG_DIR/xiaohongshu_account.json"
if [ -f "$ACCOUNT_FILE" ]; then
    echo "✅ 账号配置文件存在"
    echo "📄 配置文件内容:"
    cat "$ACCOUNT_FILE" | python3 -m json.tool 2>/dev/null || cat "$ACCOUNT_FILE"
else
    echo "⚠️  账号配置文件不存在"
    echo "请运行: $LOGIN_SCRIPT setup 来设置账号"
fi

echo ""
echo "🎉 测试完成！"
echo ""
echo "下一步:"
echo "1. 设置账号: $LOGIN_SCRIPT setup"
echo "2. 测试登录: $LOGIN_SCRIPT test"
echo "3. 浏览主页: $LOGIN_SCRIPT browse"
echo ""
echo "注意: 首次运行可能需要处理验证码"