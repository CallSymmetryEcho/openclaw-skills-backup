#!/bin/bash
# 小红书登录命令行工具（简单版）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/xiaohongshu_simple.py"
CONFIG_DIR="$HOME/.openclaw/workspace/config"
ACCOUNT_FILE="$CONFIG_DIR/xiaohongshu_account.json"

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
    if ! python3 -c "import playwright" 2>/dev/null; then
        print_warning "Playwright未安装，正在安装..."
        pip3 install playwright
        playwright install chromium
    fi
    
    # 检查配置文件目录
    if [ ! -d "$CONFIG_DIR" ]; then
        mkdir -p "$CONFIG_DIR"
        print_info "创建配置目录: $CONFIG_DIR"
    fi
    
    return 0
}

setup_account() {
    print_info "设置小红书账号信息"
    python3 "$PYTHON_SCRIPT" setup
}

test_login() {
    print_info "测试小红书登录"
    python3 "$PYTHON_SCRIPT" test
}

login() {
    print_info "执行小红书登录"
    python3 "$PYTHON_SCRIPT" login
}

browse() {
    print_info "浏览小红书主页"
    python3 "$PYTHON_SCRIPT" browse
}

search() {
    local keyword="$1"
    if [ -z "$keyword" ]; then
        print_error "请提供搜索关键词"
        echo "用法: $0 search \"关键词\""
        exit 1
    fi
    
    print_info "搜索内容: $keyword"
    python3 "$PYTHON_SCRIPT" search --keyword "$keyword"
}

show_help() {
    echo "小红书自动化登录工具"
    echo ""
    echo "用法: $0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  setup             交互式设置账号信息"
    echo "  test              测试登录功能"
    echo "  login             执行登录"
    echo "  browse            浏览主页（需要先登录）"
    echo "  search <关键词>   搜索内容"
    echo "  help              显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 setup"
    echo "  $0 test"
    echo "  $0 search \"美食推荐\""
    echo ""
    echo "环境变量:"
    echo "  DEBUG=1           启用调试模式"
    echo "  HEADLESS=false    显示浏览器窗口"
    echo ""
    echo "配置文件位置:"
    echo "  $ACCOUNT_FILE"
}

# 主逻辑
main() {
    local command="$1"
    
    # 检查依赖
    check_dependencies || exit 1
    
    case "$command" in
        setup)
            setup_account
            ;;
        test)
            test_login
            ;;
        login)
            login
            ;;
        browse)
            browse
            ;;
        search)
            shift
            search "$@"
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
                exit 1
            fi
            ;;
    esac
}

# 设置环境变量
if [ "$DEBUG" = "1" ]; then
    set -x
fi

if [ "$HEADLESS" = "false" ]; then
    export HEADLESS_ARG="--visible"
else
    export HEADLESS_ARG="--headless"
fi

# 执行主函数
main "$@"