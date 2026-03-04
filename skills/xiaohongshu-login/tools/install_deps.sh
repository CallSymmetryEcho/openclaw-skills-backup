#!/bin/bash
# 小红书技能依赖安装脚本

set -e

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

check_python() {
    print_info "检查Python环境..."
    
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python $python_version 已安装"
        return 0
    else
        print_error "Python3未安装"
        return 1
    fi
}

check_pip() {
    print_info "检查pip..."
    
    if python3 -m pip --version &> /dev/null; then
        pip_version=$(python3 -m pip --version 2>&1 | awk '{print $2}')
        print_success "pip $pip_version 已安装"
        return 0
    else
        print_error "pip未安装"
        return 1
    fi
}

install_playwright_python() {
    print_info "安装Playwright Python模块..."
    
    if python3 -c "import playwright" 2>/dev/null; then
        playwright_version=$(python3 -c "import playwright; print(playwright.__version__)" 2>/dev/null || echo "未知版本")
        print_success "Playwright Python模块已安装 ($playwright_version)"
        return 0
    fi
    
    print_info "正在安装playwright..."
    python3 -m pip install playwright
    
    if python3 -c "import playwright" 2>/dev/null; then
        playwright_version=$(python3 -c "import playwright; print(playwright.__version__)" 2>/dev/null)
        print_success "Playwright Python模块安装成功 ($playwright_version)"
        return 0
    else
        print_error "Playwright Python模块安装失败"
        return 1
    fi
}

install_playwright_browsers() {
    print_info "安装Playwright浏览器..."
    
    # 检查是否已安装Chromium
    if [ -d "$HOME/.cache/ms-playwright" ]; then
        print_success "Playwright浏览器已安装"
        return 0
    fi
    
    print_info "正在安装Chromium浏览器..."
    python3 -m playwright install chromium
    
    if [ -d "$HOME/.cache/ms-playwright" ]; then
        print_success "Chromium浏览器安装成功"
        return 0
    else
        print_error "Chromium浏览器安装失败"
        return 1
    fi
}

check_npx_playwright() {
    print_info "检查npx playwright..."
    
    if npx playwright --version &> /dev/null; then
        npx_version=$(npx playwright --version 2>&1)
        print_success "npx playwright 可用 ($npx_version)"
        return 0
    else
        print_warning "npx playwright 不可用"
        return 1
    fi
}

create_config_dir() {
    print_info "创建配置目录..."
    
    CONFIG_DIR="$HOME/.openclaw/workspace/config"
    if [ ! -d "$CONFIG_DIR" ]; then
        mkdir -p "$CONFIG_DIR"
        print_success "配置目录创建成功: $CONFIG_DIR"
    else
        print_success "配置目录已存在: $CONFIG_DIR"
    fi
}

test_installation() {
    print_info "测试安装..."
    
    # 测试Python playwright
    if python3 -c "import playwright" 2>/dev/null; then
        print_success "✅ Python playwright模块工作正常"
    else
        print_error "❌ Python playwright模块测试失败"
        return 1
    fi
    
    # 测试npx playwright
    if npx playwright --version &> /dev/null; then
        print_success "✅ npx playwright工作正常"
    else
        print_warning "⚠️  npx playwright不可用（不影响Python版本）"
    fi
    
    # 测试配置文件目录
    CONFIG_DIR="$HOME/.openclaw/workspace/config"
    if [ -d "$CONFIG_DIR" ]; then
        print_success "✅ 配置目录可访问"
    else
        print_error "❌ 配置目录不可访问"
        return 1
    fi
    
    return 0
}

show_usage() {
    echo "小红书技能依赖安装脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  all             安装所有依赖（默认）"
    echo "  python          只安装Python playwright模块"
    echo "  browsers        只安装浏览器"
    echo "  test            测试安装"
    echo "  help            显示帮助"
    echo ""
    echo "示例:"
    echo "  $0               # 安装所有依赖"
    echo "  $0 test          # 测试安装"
    echo ""
    echo "依赖包括:"
    echo "  1. Python playwright模块"
    echo "  2. Chromium浏览器"
    echo "  3. 配置目录"
}

main() {
    local action="${1:-all}"
    
    case "$action" in
        all)
            check_python || exit 1
            check_pip || exit 1
            install_playwright_python || exit 1
            install_playwright_browsers || exit 1
            check_npx_playwright
            create_config_dir
            test_installation
            ;;
        python)
            check_python || exit 1
            check_pip || exit 1
            install_playwright_python || exit 1
            ;;
        browsers)
            install_playwright_browsers || exit 1
            ;;
        test)
            test_installation || exit 1
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            print_error "未知选项: $action"
            show_usage
            exit 1
            ;;
    esac
    
    echo ""
    print_success "安装完成！"
    echo ""
    echo "下一步:"
    echo "  1. 获取小红书Cookie: ./tools/xiaohongshu_cookie.sh extract"
    echo "  2. 测试Cookie: ./tools/xiaohongshu_cookie.sh test"
    echo "  3. 浏览内容: ./tools/xiaohongshu_cookie.sh browse"
}

main "$@"