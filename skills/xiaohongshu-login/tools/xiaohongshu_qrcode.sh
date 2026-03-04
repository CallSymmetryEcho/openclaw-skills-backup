#!/bin/bash
# 小红书扫码登录工具

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/xiaohongshu_qrcode.py"
CONFIG_DIR="$HOME/.openclaw/workspace/config"
QRCODE_DIR="$CONFIG_DIR/qrcodes"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    print_info "检查依赖..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3未安装"
        return 1
    fi
    
    # 检查Playwright Python模块
    if ! python3 -c "import playwright" 2>/dev/null; then
        print_error "Playwright Python模块未安装"
        print_info "运行安装脚本: ./tools/install_deps.sh python"
        return 1
    fi
    
    # 创建配置目录
    mkdir -p "$QRCODE_DIR"
    
    return 0
}

show_qrcode() {
    print_info "获取小红书登录二维码..."
    
    # 运行Python脚本获取二维码
    result=$(python3 "$PYTHON_SCRIPT" qrcode)
    
    if echo "$result" | grep -q '"status": "qrcode_ready"'; then
        # 解析JSON结果
        qrcode_path=$(echo "$result" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('qrcode_path', ''))")
        qrcode_base64=$(echo "$result" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('qrcode_base64', ''))")
        
        if [ -n "$qrcode_path" ] && [ -f "$qrcode_path" ]; then
            print_success "二维码已生成: $qrcode_path"
            
            # 显示二维码信息
            echo ""
            echo "📱 请使用小红书APP扫描二维码登录"
            echo "⏳ 扫码后脚本会自动检测登录状态"
            echo ""
            
            # 这里应该发送图片到聊天框
            # 由于当前环境限制，我们先显示文件路径
            print_info "二维码文件位置: $qrcode_path"
            print_info "请将二维码图片发送到聊天框"
            
            return 0
        else
            print_error "无法获取二维码文件路径"
            return 1
        fi
    else
        print_error "获取二维码失败"
        echo "$result"
        return 1
    fi
}

complete_login() {
    print_info "检测登录状态..."
    
    result=$(python3 "$PYTHON_SCRIPT" complete)
    echo "$result"
    
    if echo "$result" | grep -q '"status": "login_success"'; then
        print_success "✅ 登录成功！Cookie已保存"
        return 0
    else
        print_error "登录失败或超时"
        return 1
    fi
}

test_login() {
    print_info "测试小红书访问..."
    
    result=$(python3 "$PYTHON_SCRIPT" test)
    echo "$result"
    
    if echo "$result" | grep -q '"status": "test_complete"'; then
        print_success "✅ 测试完成，可以访问小红书"
        return 0
    else
        print_error "测试失败"
        return 1
    fi
}

send_qrcode_to_chat() {
    print_info "发送二维码到聊天框..."
    
    # 获取最新的二维码文件
    latest_qrcode=$(ls -t "$QRCODE_DIR"/xiaohongshu_qrcode_*.png 2>/dev/null | head -1)
    
    if [ -z "$latest_qrcode" ]; then
        print_error "未找到二维码文件，请先运行 qrcode 命令"
        return 1
    fi
    
    print_info "找到二维码文件: $latest_qrcode"
    
    # 这里应该调用OpenClaw的消息发送功能
    # 由于当前环境限制，我们显示文件信息
    echo ""
    echo "📤 二维码准备发送到聊天框:"
    echo "文件: $latest_qrcode"
    echo "大小: $(du -h "$latest_qrcode" | cut -f1)"
    echo ""
    echo "⚠️  注意：在实际OpenClaw环境中，这里应该调用 message 工具发送图片"
    echo ""
    
    # 模拟发送（实际环境中应该使用 message 工具）
    print_warning "模拟发送二维码到聊天框..."
    print_info "在实际OpenClaw环境中，请使用:"
    echo "  message(action=send, media=\"$latest_qrcode\", caption=\"请扫描二维码登录小红书\")"
    
    return 0
}

show_help() {
    echo "小红书扫码登录工具"
    echo ""
    echo "工作流程："
    echo "  1. 获取二维码并发送到聊天框"
    echo "  2. 用户使用小红书APP扫码"
    echo "  3. 检测登录状态并保存Cookie"
    echo ""
    echo "用法: $0 <命令>"
    echo ""
    echo "命令:"
    echo "  qrcode     获取登录二维码"
    echo "  send       发送二维码到聊天框（模拟）"
    echo "  complete   检测登录状态"
    echo "  test       测试小红书访问"
    echo "  help       显示帮助"
    echo ""
    echo "完整流程示例:"
    echo "  $0 qrcode    # 获取二维码"
    echo "  $0 send      # 发送二维码到聊天框"
    echo "  # 用户扫码..."
    echo "  $0 complete  # 检测登录状态"
    echo ""
    echo "文件位置:"
    echo "  二维码目录: $QRCODE_DIR"
    echo "  Cookie文件: $CONFIG_DIR/xiaohongshu_cookies.json"
}

main() {
    local command="$1"
    
    # 检查依赖
    check_dependencies || return 1
    
    case "$command" in
        qrcode)
            show_qrcode
            ;;
        send)
            send_qrcode_to_chat
            ;;
        complete)
            complete_login
            ;;
        test)
            test_login
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            if [ -z "$command" ]; then
                show_help
            else
                print_error "未知命令: $command"
                show_help
                return 1
            fi
            ;;
    esac
}

main "$@"