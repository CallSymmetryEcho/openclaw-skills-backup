# OpenClaw备份指南 - 分离式备份策略

## 🎯 备份策略
采用分离式备份策略，保护隐私同时分享有用技能：

### 🔓 公开数据 (GitHub备份)
- `skills/` 目录 - 所有技能文件
- 相关工具脚本
- 核心文档（不含隐私）

### 🔒 隐私数据 (NAS/本地备份)
- `memory/` 目录 - 记忆日志
- `config/` 目录 - 配置文件（API密钥等）
- `projects/` 目录 - 个人项目文件
- 个人文档（USER.md, MEMORY.md等）

## 🚀 快速开始

### 方法1: 使用备份管理器（推荐）
```bash
# 显示备份状态
cd ~/.openclaw/workspace
./tools/backup_manager.sh status

# 仅备份skills到GitHub（公开）
./tools/backup_manager.sh skills

# 仅备份隐私数据到NAS/本地
./tools/backup_manager.sh private

# 完整备份（skills + 隐私数据）
./tools/backup_manager.sh all
```

### 方法2: 单独运行备份脚本
```bash
# 1. 配置GitHub备份（仅skills）
nano ~/.openclaw/workspace/tools/backup_skills_only.sh
# 设置: GITHUB_USER, GITHUB_TOKEN

# 2. 配置NAS备份（隐私数据）
nano ~/.openclaw/workspace/tools/backup_private_to_nas.sh
# 设置: NAS_MOUNT_POINT, NAS_BACKUP_PATH

# 3. 运行备份
./tools/backup_skills_only.sh      # 备份skills到GitHub
./tools/backup_private_to_nas.sh   # 备份隐私数据到NAS
```

### 方法2: 手动Git设置
```bash
# 1. 初始化Git仓库
cd ~/.openclaw/workspace
./tools/init_git.sh

# 2. 设置GitHub远程仓库
./tools/setup_github.sh 你的GitHub用户名 仓库名

# 3. 推送到GitHub
git push -u origin main
```

## 🔑 GitHub配置

### 1. 创建GitHub个人访问令牌
1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择 "classic" 令牌
4. 权限选择: `repo` (完全控制仓库)
5. 生成并复制令牌

### 2. 创建GitHub仓库
1. 访问: https://github.com/new
2. 仓库名: `openclaw-skills-backup` (或其他名称)
3. 描述: "OpenClaw skills backup"
4. 选择: Private (推荐)
5. 创建仓库

## 📋 备份脚本说明

### `backup_to_github.sh`
- 自动备份所有重要文件
- 创建临时备份目录
- 推送到GitHub私有仓库
- 支持自动创建新仓库

### `init_git.sh`
- 初始化本地Git仓库
- 添加所有文件
- 创建初始提交
- 显示Git状态

### `setup_github.sh`
- 设置GitHub远程仓库
- 需要GitHub用户名和仓库名
- 配置远程URL

## 🔄 定期备份

### 手动备份
```bash
# 每次需要备份时运行
cd ~/.openclaw/workspace
./tools/backup_to_github.sh
```

### 自动备份（使用cron）
```bash
# 编辑cron任务
crontab -e

# 添加以下行（每天凌晨2点备份）
0 2 * * * cd /home/node/.openclaw/workspace && ./tools/backup_to_github.sh >> /tmp/openclaw_backup.log 2>&1
```

## 🛡️ 安全注意事项

### 敏感信息保护
以下文件包含敏感信息，备份时请注意：
- `config/notion_api_key.txt` - Notion API密钥
- `config/gmail_account_*.json` - Gmail账户信息
- `config/xiaohongshu_cookies.json` - 小红书Cookie

### 建议
1. 使用GitHub私有仓库
2. 定期更新访问令牌
3. 不要在公开代码中硬编码凭据
4. 考虑使用GitHub Secrets存储敏感信息

## 🔧 故障排除

### 问题: Git推送失败
```bash
# 检查远程仓库
git remote -v

# 检查网络连接
curl -I https://github.com

# 检查Git凭据
git config --list | grep credential
```

### 问题: 权限不足
```bash
# 确保有写入权限
ls -la ~/.openclaw/workspace/.git

# 检查GitHub令牌权限
# 需要至少 'repo' 权限
```

### 问题: 仓库不存在
```bash
# 先创建GitHub仓库
# 然后设置远程仓库
./tools/setup_github.sh 用户名 仓库名
```

## 📞 帮助

### 查看脚本帮助
```bash
./tools/backup_to_github.sh --help
./tools/init_git.sh --help
./tools/setup_github.sh --help
```

### 查看Git状态
```bash
cd ~/.openclaw/workspace
git status
git log --oneline -5
```

## 🎯 最佳实践

1. **定期备份**: 每周至少备份一次
2. **版本控制**: 每次重要更改后提交
3. **测试恢复**: 定期测试从备份恢复
4. **多地点备份**: 考虑使用多个备份位置
5. **文档更新**: 备份后更新备份记录

---

**最后更新**: 2026-03-04  
**备份状态**: 工具已就绪，等待GitHub配置  
**建议**: 立即配置GitHub并运行首次备份