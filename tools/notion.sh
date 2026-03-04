#!/bin/bash
# Notion API 工具命令行封装

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/notion_client.py"

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
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        return 1
    fi
    return 0
}

test_connection() {
    print_info "测试Notion API连接..."
    python3 "$PYTHON_SCRIPT" test
}

search_content() {
    local query="$1"
    if [ -z "$query" ]; then
        read -p "请输入搜索关键词: " query
    fi
    
    print_info "搜索: $query"
    python3 "$PYTHON_SCRIPT" search --query "$query"
}

list_databases() {
    print_info "获取数据库列表..."
    python3 "$PYTHON_SCRIPT" databases
}

list_pages() {
    print_info "获取页面列表..."
    python3 "$PYTHON_SCRIPT" pages
}

query_database() {
    local db_id="$1"
    if [ -z "$db_id" ]; then
        read -p "请输入数据库ID: " db_id
    fi
    
    print_info "查询数据库: $db_id"
    python3 "$PYTHON_SCRIPT" query --database-id "$db_id"
}

create_page() {
    local parent_id="$1"
    local title="$2"
    
    if [ -z "$parent_id" ]; then
        echo "请选择父级类型:"
        echo "1. 数据库"
        echo "2. 页面"
        read -p "选择 (1/2): " choice
        
        if [ "$choice" == "1" ]; then
            read -p "请输入数据库ID: " parent_id
            python3 "$PYTHON_SCRIPT" create --database-id "$parent_id" --title "$title"
        else
            read -p "请输入页面ID: " parent_id
            python3 "$PYTHON_SCRIPT" create --page-id "$parent_id" --title "$title"
        fi
    else
        python3 "$PYTHON_SCRIPT" create --database-id "$parent_id" --title "$title"
    fi
}

show_help() {
    echo "Notion API 工具"
    echo ""
    echo "用法: $0 <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  test                      测试API连接"
    echo "  search [关键词]           搜索内容"
    echo "  databases                 列出所有数据库"
    echo "  pages                     列出所有页面"
    echo "  query <数据库ID>          查询数据库"
    echo "  create <父级ID> [标题]    创建页面"
    echo "  help                      显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 test                   # 测试连接"
    echo "  $0 search \"项目\"          # 搜索包含\"项目\"的内容"
    echo "  $0 databases              # 列出数据库"
    echo "  $0 query <database_id>    # 查询特定数据库"
    echo ""
    echo "配置:"
    echo "  API Key文件: ~/.openclaw/workspace/config/notion_api_key.txt"
}

main() {
    local command="$1"
    shift
    
    # 检查Python
    if ! check_python; then
        return 1
    fi
    
    case "$command" in
        test)
            test_connection
            ;;
        search)
            search_content "$1"
            ;;
        databases)
            list_databases
            ;;
        pages)
            list_pages
            ;;
        query)
            query_database "$1"
            ;;
        create)
            create_page "$1" "$2"
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