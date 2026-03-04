#!/bin/bash
# 多Gmail账户管理脚本

CONFIG_DIR="$HOME/.openclaw/workspace/config"
TOOLS_DIR="$HOME/.openclaw/workspace/tools"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}=== 多Gmail账户管理 ===${NC}"
    echo
}

print_help() {
    print_header
    echo "用法: $0 <命令> [参数]"
    echo
    echo "命令:"
    echo "  list                    列出所有配置的邮箱账户"
    echo "  add <名称> <邮箱> <类型>  添加新账户 (类型: work/life/other)"
    echo "  test <账户名>            测试账户连接"
    echo "  emails <账户名> [数量]   查看指定账户的邮件"
    echo "  send <账户名> <收件人> <主题> <正文>  发送邮件"
    echo "  setup                   显示设置指南"
    echo
    echo "示例:"
    echo "  $0 list"
    echo "  $0 add work work@example.com work"
    echo "  $0 test work"
    echo "  $0 emails work 5"
    echo "  $0 send work friend@example.com 'Hello' 'Just checking in!'"
}

check_config_dir() {
    if [ ! -d "$CONFIG_DIR" ]; then
        mkdir -p "$CONFIG_DIR"
        echo -e "${GREEN}创建配置目录: $CONFIG_DIR${NC}"
    fi
}

cmd_list() {
    echo -e "${BLUE}📧 已配置的邮箱账户${NC}"
    echo "========================================"
    
    if ls "$CONFIG_DIR"/gmail_account_*.json 1>/dev/null 2>&1; then
        for config_file in "$CONFIG_DIR"/gmail_account_*.json; do
            account_name=$(basename "$config_file" | sed 's/gmail_account_//' | sed 's/.json//')
            email=$(grep -o '"email": "[^"]*"' "$config_file" | head -1 | cut -d'"' -f4)
            type=$(grep -o '"type": "[^"]*"' "$config_file" | head -1 | cut -d'"' -f4)
            
            echo -e "\n${YELLOW}账户: $account_name${NC}"
            echo "  邮箱: $email"
            echo "  类型: $type"
        done
    else
        echo -e "${YELLOW}未找到任何邮箱账户配置${NC}"
    fi
    
    echo "========================================"
}

cmd_add() {
    if [ $# -lt 3 ]; then
        echo -e "${RED}错误: 需要参数: 账户名称 邮箱地址 账户类型${NC}"
        echo "示例: $0 add work work@example.com work"
        return 1
    fi
    
    local account_name="$1"
    local email="$2"
    local account_type="$3"
    
    echo -e "${BLUE}添加账户: $account_name ($email)${NC}"
    echo -e "${YELLOW}请从 https://myaccount.google.com/apppasswords 生成16位应用密码${NC}"
    echo -n "请输入应用密码: "
    read -s app_password
    echo
    
    if [ ${#app_password} -ne 16 ] || [[ "$app_password" == *" "* ]]; then
        echo -e "${RED}错误: 应用密码必须是16位字符且不能包含空格${NC}"
        return 1
    fi
    
    # 创建JSON配置
    config_file="$CONFIG_DIR/gmail_account_${account_name}.json"
    cat > "$config_file" << EOF
{
  "email": "$email",
  "app_password": "$app_password",
  "type": "$account_type",
  "created": "$(date -Iseconds)"
}
EOF
    
    echo -e "${GREEN}✅ 账户 '$account_name' 已保存${NC}"
    echo -e "配置文件: $config_file"
    
    # 测试连接
    echo -e "\n${BLUE}测试连接...${NC}"
    cmd_test "$account_name"
}

cmd_test() {
    if [ $# -lt 1 ]; then
        echo -e "${RED}错误: 需要账户名称${NC}"
        return 1
    fi
    
    local account_name="$1"
    local config_file="$CONFIG_DIR/gmail_account_${account_name}.json"
    
    if [ ! -f "$config_file" ]; then
        echo -e "${RED}错误: 未找到账户 '$account_name'${NC}"
        return 1
    fi
    
    echo -e "${BLUE}测试账户: $account_name${NC}"
    python3 "$TOOLS_DIR/multi_gmail.py" test "$account_name"
}

cmd_emails() {
    if [ $# -lt 1 ]; then
        echo -e "${RED}错误: 需要账户名称${NC}"
        return 1
    fi
    
    local account_name="$1"
    local limit="${2:-10}"
    
    echo -e "${BLUE}查看 $account_name 账户的邮件 (最新 $limit 封)${NC}"
    python3 "$TOOLS_DIR/multi_gmail.py" emails "$account_name" --limit "$limit"
}

cmd_send() {
    if [ $# -lt 4 ]; then
        echo -e "${RED}错误: 需要参数: 账户名 收件人 主题 正文${NC}"
        echo "示例: $0 send work friend@example.com 'Hello' 'Just checking in!'"
        return 1
    fi
    
    local account_name="$1"
    local to="$2"
    local subject="$3"
    local body="$4"
    
    echo -e "${BLUE}从 $account_name 账户发送邮件${NC}"
    python3 "$TOOLS_DIR/multi_gmail.py" send "$account_name" "$to" "$subject" "$body"
}

cmd_setup() {
    print_header
    echo -e "${YELLOW}📋 多邮箱账户设置指南${NC}"
    echo "========================================"
    echo
    echo "1. 为每个Gmail账户生成应用密码:"
    echo "   - 访问 https://myaccount.google.com/apppasswords"
    echo "   - 选择 '邮件' 应用"
    echo "   - 生成16位密码 (无空格)"
    echo
    echo "2. 添加账户:"
    echo "   $0 add work work@example.com work"
    echo "   $0 add life personal@example.com life"
    echo
    echo "3. 测试连接:"
    echo "   $0 test work"
    echo "   $0 test life"
    echo
    echo "4. 查看邮件:"
    echo "   $0 emails work 5      # 查看工作邮箱最新5封邮件"
    echo "   $0 emails life 10     # 查看生活邮箱最新10封邮件"
    echo
    echo "5. 发送邮件:"
    echo "   $0 send work colleague@example.com 'Meeting' 'Reminder...'"
    echo "   $0 send life friend@example.com 'Hello' 'How are you?'"
    echo
    echo "========================================"
}

# 主程序
check_config_dir

case "$1" in
    list)
        cmd_list
        ;;
    add)
        shift
        cmd_add "$@"
        ;;
    test)
        shift
        cmd_test "$@"
        ;;
    emails)
        shift
        cmd_emails "$@"
        ;;
    send)
        shift
        cmd_send "$@"
        ;;
    setup)
        cmd_setup
        ;;
    help|--help|-h)
        print_help
        ;;
    *)
        if [ -z "$1" ]; then
            print_help
        else
            echo -e "${RED}未知命令: $1${NC}"
            echo "使用 '$0 help' 查看帮助"
        fi
        ;;
esac