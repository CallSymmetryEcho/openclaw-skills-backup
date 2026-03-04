#!/bin/bash
# Gmail工具脚本
# 支持两种模式：gogcli模式 或 Python简单模式

CONFIG_DIR="$HOME/.openclaw/workspace/config"
ACCOUNT_FILE="$CONFIG_DIR/gmail_account.txt"
PYTHON_SCRIPT="$HOME/.openclaw/workspace/tools/gmail_simple.py"

# 检查配置文件
if [ ! -f "$ACCOUNT_FILE" ]; then
    echo "错误: 未找到Gmail账户配置文件"
    echo "请先运行: echo 'your-email@gmail.com' > $ACCOUNT_FILE"
    exit 1
fi

ACCOUNT=$(cat "$ACCOUNT_FILE" | tr -d '\n')

# 检查使用哪种模式
if command -v gog &> /dev/null; then
    MODE="gogcli"
elif command -v python3 &> /dev/null && [ -f "$PYTHON_SCRIPT" ]; then
    MODE="python"
else
    echo "警告: 未找到gogcli，使用Python模式"
    echo "请确保已配置应用专用密码"
    MODE="python"
fi

ACTION=$1
shift

case $ACTION in
  "list")
    LIMIT=${1:-10}
    echo "=== 最新 $LIMIT 封邮件 ==="
    if [ "$MODE" = "gogcli" ]; then
        gog gmail list --account "$ACCOUNT" --limit "$LIMIT" --format json 2>/dev/null || \
        gog gmail list --account "$ACCOUNT" --limit "$LIMIT"
    else
        python3 "$PYTHON_SCRIPT" list --limit "$LIMIT"
    fi
    ;;
  
  "read")
    if [ -z "$1" ]; then
        echo "错误: 需要提供邮件ID"
        echo "用法: $0 read <message-id>"
        exit 1
    fi
    echo "=== 读取邮件: $1 ==="
    if [ "$MODE" = "gogcli" ]; then
        gog gmail get --account "$ACCOUNT" --id "$1" --format json 2>/dev/null || \
        gog gmail get --account "$ACCOUNT" --id "$1"
    else
        echo "Python模式暂不支持读取特定邮件，请使用list命令查看"
    fi
    ;;
  
  "send")
    if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
        echo "错误: 需要提供收件人、主题和内容"
        echo "用法: $0 send <to> <subject> <body>"
        exit 1
    fi
    TO=$1
    SUBJECT=$2
    BODY=$3
    echo "=== 发送邮件 ==="
    echo "收件人: $TO"
    echo "主题: $SUBJECT"
    if [ "$MODE" = "gogcli" ]; then
        gog gmail send --account "$ACCOUNT" --to "$TO" --subject "$SUBJECT" --body "$BODY"
    else
        python3 "$PYTHON_SCRIPT" send "$TO" "$SUBJECT" "$BODY"
    fi
    ;;
  
  "search")
    if [ -z "$1" ]; then
        echo "错误: 需要提供搜索查询"
        echo "用法: $0 search <query>"
        exit 1
    fi
    QUERY=$1
    LIMIT=${2:-10}
    echo "=== 搜索: $QUERY ==="
    if [ "$MODE" = "gogcli" ]; then
        gog gmail search --account "$ACCOUNT" --query "$QUERY" --limit "$LIMIT" --format json 2>/dev/null || \
        gog gmail search --account "$ACCOUNT" --query "$QUERY" --limit "$LIMIT"
    else
        python3 "$PYTHON_SCRIPT" search "$QUERY" --limit "$LIMIT"
    fi
    ;;
  
  "labels")
    echo "=== 邮件标签 ==="
    if [ "$MODE" = "gogcli" ]; then
        gog gmail labels --account "$ACCOUNT" --format json 2>/dev/null || \
        gog gmail labels --account "$ACCOUNT"
    else
        echo "Python模式暂不支持标签功能"
    fi
    ;;
  
  "setup")
    echo "=== Gmail设置 ==="
    if [ "$MODE" = "gogcli" ]; then
        echo "模式: gogcli (OAuth认证)"
        echo "1. 已安装gogcli"
        echo "2. 配置Gmail账户: $ACCOUNT"
        echo "3. 运行认证: gog auth add --provider gmail --account $ACCOUNT"
    else
        echo "模式: Python (应用密码认证)"
        echo "1. 已安装Python3"
        echo "2. 配置Gmail账户: $ACCOUNT"
        echo "3. 配置应用专用密码"
        python3 "$PYTHON_SCRIPT" setup
    fi
    echo ""
    echo "当前账户: $ACCOUNT"
    echo "配置文件: $ACCOUNT_FILE"
    ;;
  
  "test")
    echo "=== 测试连接 ==="
    echo "账户: $ACCOUNT"
    echo "模式: $MODE"
    
    if [ "$MODE" = "gogcli" ]; then
        echo "获取标签列表..."
        gog gmail labels --account "$ACCOUNT" --limit 5
    else
        python3 "$PYTHON_SCRIPT" test
    fi
    ;;
  
  "python")
    # 直接调用Python脚本
    shift
    python3 "$PYTHON_SCRIPT" "$@"
    ;;
  
  *)
    echo "Gmail工具 - 用法:"
    echo "  当前模式: $MODE"
    echo ""
    echo "通用命令:"
    echo "  $0 list [数量]              # 列出最新邮件"
    echo "  $0 send <to> <subject> <body> # 发送邮件"
    echo "  $0 search <query> [数量]    # 搜索邮件"
    echo "  $0 setup                    # 显示设置说明"
    echo "  $0 test                     # 测试连接"
    echo ""
    if [ "$MODE" = "gogcli" ]; then
        echo "gogcli特有命令:"
        echo "  $0 read <message-id>        # 读取特定邮件"
        echo "  $0 labels                   # 列出所有标签"
        echo ""
        echo "配置说明:"
        echo "  认证: gog auth add --provider gmail --account $ACCOUNT"
    else
        echo "Python模式配置:"
        echo "  1. 设置Gmail账户: echo 'lianbin522957@gmail.com' > $ACCOUNT_FILE"
        echo "  2. 获取应用密码: 访问 https://myaccount.google.com/"
        echo "  3. 保存应用密码: 编辑 $CONFIG_DIR/gmail_app_password.txt"
        echo ""
        echo "直接调用Python脚本:"
        echo "  $0 python <命令> [参数]"
    fi
    exit 1
    ;;
esac