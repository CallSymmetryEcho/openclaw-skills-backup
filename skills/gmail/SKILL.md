# Gmail Skill

## 描述
通过Gmail API读取和发送邮件的技能。使用gogcli工具与Gmail交互。

## 前提条件
1. 安装gogcli工具
2. 配置Gmail OAuth认证
3. 设置Gmail账户

## 安装步骤

### 1. 安装gogcli
```bash
# 方法1：使用curl安装
curl -fsSL https://gogcli.sh/install.sh | bash

# 方法2：从GitHub下载
git clone https://github.com/gogcli/gogcli.git
cd gogcli
npm install -g .
```

### 2. 配置Gmail认证
```bash
# 初始化配置
gog init

# 添加Gmail账户
gog auth add --provider gmail --account your-email@gmail.com

# 按照提示完成OAuth认证流程
```

### 3. 测试连接
```bash
# 列出标签
gog gmail labels --account your-email@gmail.com

# 读取最新邮件
gog gmail list --account your-email@gmail.com --limit 5
```

## 使用方法

### 读取邮件
```bash
# 列出最新邮件
gog gmail list --account your-email@gmail.com --limit 10

# 读取特定邮件
gog gmail get --account your-email@gmail.com --id <message-id>

# 搜索邮件
gog gmail search --account your-email@gmail.com --query "from:important@example.com"
```

### 发送邮件
```bash
# 发送简单邮件
gog gmail send --account your-email@gmail.com \
  --to recipient@example.com \
  --subject "测试邮件" \
  --body "这是邮件内容"

# 发送带附件的邮件
gog gmail send --account your-email@gmail.com \
  --to recipient@example.com \
  --subject "带附件的邮件" \
  --body "请查看附件" \
  --attach /path/to/file.pdf
```

## OpenClaw集成

### 创建邮件工具脚本
创建 `/home/node/.openclaw/workspace/tools/gmail.sh`:

```bash
#!/bin/bash
# Gmail工具脚本

ACCOUNT="your-email@gmail.com"
ACTION=$1
shift

case $ACTION in
  "list")
    gog gmail list --account $ACCOUNT --limit $1
    ;;
  "read")
    gog gmail get --account $ACCOUNT --id $1
    ;;
  "send")
    gog gmail send --account $ACCOUNT "$@"
    ;;
  "search")
    gog gmail search --account $ACCOUNT --query "$1"
    ;;
  *)
    echo "用法: gmail.sh <list|read|send|search> [参数]"
    exit 1
    ;;
esac
```

### 在OpenClaw中调用
```bash
# 读取最新5封邮件
exec(command="bash /home/node/.openclaw/workspace/tools/gmail.sh list 5")

# 发送邮件
exec(command="bash /home/node/.openclaw/workspace/tools/gmail.sh send --to recipient@example.com --subject '主题' --body '内容'")
```

## 安全注意事项

1. **保护认证信息**：gogcli的认证信息存储在 `~/.config/gogcli/` 目录中
2. **最小权限原则**：只授予必要的Gmail API权限
3. **定期清理**：定期清理不需要的邮件和附件

## 故障排除

### 常见问题
1. **认证失败**：重新运行 `gog auth add`
2. **API配额限制**：Gmail API有每日配额限制
3. **网络问题**：检查网络连接和代理设置

### 调试命令
```bash
# 检查认证状态
gog auth list

# 测试API连接
gog gmail labels --account your-email@gmail.com --debug

# 查看日志
tail -f ~/.config/gogcli/logs/gogcli.log
```

## 高级功能

### 邮件监控（可选）
如果需要监控新邮件，可以配置Gmail Pub/Sub：
```bash
# 设置邮件监控
openclaw webhooks gmail setup --account your-email@gmail.com
```

### 邮件模板
创建常用邮件模板：
```bash
# 模板文件
echo "尊敬的\${name}：\n\n您好！\n\n\${content}\n\n祝好！" > ~/.config/gogcli/templates/default.txt

# 使用模板发送
gog gmail send --account your-email@gmail.com \
  --to recipient@example.com \
  --subject "模板邮件" \
  --template default.txt \
  --var name="张三" \
  --var content="这是邮件内容"
```

## 更新日志
- 2026-03-02: 创建初始版本
- 技能作者: Rook