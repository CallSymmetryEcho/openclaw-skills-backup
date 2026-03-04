#!/bin/bash
# 小红书Cookie管理工具

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/xiaohongshu_cookie.py"
CONFIG_DIR="$HOME/.openclaw/workspace/config"
COOKIE_FILE="$CONFIG_DIR/xiaohongshu_cookies.json"
EXPORT_FILE="$CONFIG_DIR/xiaohongshu_cookies_export.txt"

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
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3未安装"
        return 1
    fi
    
    # 检查Playwright
    if ! npx playwright --version &> /dev/null; then
        print_warning "Playwright未安装"
        print_info "正在安装Playwright..."
        npx playwright install chromium || {
            print_error "安装Playwright失败"
            return 1
        }
    fi
    
    # 检查配置文件目录
    if [ ! -d "$CONFIG_DIR" ]; then
        mkdir -p "$CONFIG_DIR"
        print_info "创建配置目录: $CONFIG_DIR"
    fi
    
    return 0
}

show_guide() {
    print_info "显示Cookie获取指南"
    python3 "$PYTHON_SCRIPT" guide
}

extract_cookies() {
    print_info "手动提取Cookie（需要显示浏览器）"
    print_warning "注意：这将打开浏览器窗口，请手动登录小红书"
    read -p "是否继续？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 "$PYTHON_SCRIPT" extract --headed
    else
        print_info "操作取消"
    fi
}

import_cookies() {
    print_info "从导出文件导入Cookie"
    
    if [ ! -f "$EXPORT_FILE" ]; then
        print_error "导出文件不存在: $EXPORT_FILE"
        print_info "请先手动登录小红书，然后导出Cookie到此文件"
        return 1
    fi
    
    python3 "$PYTHON_SCRIPT" import
}

test_cookies() {
    print_info "测试Cookie登录"
    python3 "$PYTHON_SCRIPT" test
}

browse_with_cookies() {
    print_info "使用Cookie浏览小红书"
    python3 "$PYTHON_SCRIPT" browse
}

search_with_cookies() {
    local keyword="$1"
    if [ -z "$keyword" ]; then
        print_error "请提供搜索关键词"
        echo "用法: $0 search \"关键词\""
        return 1
    fi
    
    print_info "使用Cookie搜索: $keyword"
    python3 "$PYTHON_SCRIPT" search --keyword "$keyword"
}

show_cookies() {
    print_info "显示当前Cookie"
    if [ -f "$COOKIE_FILE" ]; then
        python3 "$PYTHON_SCRIPT" show
    else
        print_error "Cookie文件不存在: $COOKIE_FILE"
    fi
}

check_cookie_status() {
    print_info "检查Cookie状态"
    
    if [ ! -f "$COOKIE_FILE" ]; then
        print_error "❌ Cookie文件不存在"
        print_info "请先获取Cookie："
        echo "  1. $0 guide    # 查看获取指南"
        echo "  2. $0 extract  # 手动提取（推荐）"
        echo "  3. $0 import   # 从导出文件导入"
        return 1
    fi
    
    cookie_count=$(python3 -c "import json; data=json.load(open('$COOKIE_FILE')); print(len(data))" 2>/dev/null || echo "0")
    
    if [ "$cookie_count" -gt 0 ]; then
        print_success "✅ Cookie文件存在，包含 $cookie_count 个Cookie"
        return 0
    else
        print_error "❌ Cookie文件无效或为空"
        return 1
    fi
}

show_help() {
    echo "小红书Cookie管理工具"
    echo ""
    echo "由于小红书只支持手机号验证码登录，采用Cookie方案"
    echo ""
    echo "用法: $0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  guide             显示Cookie获取指南"
    echo "  extract           手动提取Cookie（打开浏览器）"
    echo "  import            从导出文件导入Cookie"
    echo "  test              测试Cookie登录"
    echo "  browse            使用Cookie浏览主页"
    echo "  search <关键词>   使用Cookie搜索内容"
    echo "  show              显示当前Cookie"
    echo "  status            检查Cookie状态"
    echo "  help              显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 guide          # 查看完整指南"
    echo "  $0 extract        # 手动提取Cookie"
    echo "  $0 test           # 测试Cookie是否有效"
    echo "  $0 search \"美食\"  # 搜索美食内容"
    echo ""
    echo "文件位置:"
    echo "  Cookie文件: $COOKIE_FILE"
    echo "  导出文件: $EXPORT_FILE"
    echo ""
    echo "注意:"
    echo "  1. 首次使用需要先获取Cookie"
    echo "  2. Cookie可能会过期，需要定期更新"
    echo "  3. 确保网络可以访问小红书"
}

# 主逻辑
main() {
    local command="$1"
    
    # 检查依赖
    check_dependencies || return 1
    
    case "$command" in
        guide)
            show_guide
            ;;
        extract)
            extract_cookies
            ;;
        import)
            import_cookies
            ;;
        test)
            test_cookies
            ;;
        browse)
            browse_with_cookies
            ;;
        search)
            shift
            search_with_cookies "$@"
            ;;
        show)
            show_cookies
            ;;
        status)
            check_cookie_status
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

# 执行主函数
main "$@"