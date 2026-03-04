# OpenClaw Workspace

![Backup Status](https://img.shields.io/badge/backup-automated-success)
![Last Updated](https://img.shields.io/badge/last%20updated-2026--03--04-blue)

## 备份信息
- **备份时间**: Wed Mar  4 05:17:35 UTC 2026
- **备份内容**: skills目录 + 相关tools脚本
- **隐私保护**: 排除所有个人隐私数据和无关脚本
- **自动备份**: 每周五凌晨2:00

## 目录结构

```
.
├── skills/          # OpenClaw技能定义和文档
├── tools/           # 与技能相关的工具脚本
├── AGENTS.md        # 代理配置文档
├── README.md        # 本文件
└── .gitignore       # Git忽略配置
```

## 包含的技能

| 技能名称 | 描述 | 对应工具 |
|---------|------|---------|
| notion-integration | Notion API集成 | notion.sh, notion_client.py, ... |
| gmail | Gmail多账户管理 | gmail.sh, mgmail.sh, ... |
| project-manager | 项目管理工具 | project-manager.sh |
| xiaohongshu-login | 小红书登录自动化 | xiaohongshu_login.sh, ... |
| obsidian-tech-notes | Obsidian技术笔记 | - |
| web-searcher | 网页搜索工具 | - |
| lesson | 经验记录工具 | - |

## 隐私保护声明

此备份严格排除了以下隐私数据：
- `memory/` 目录 - 记忆日志（包含个人隐私）
- `config/` 目录 - 配置文件（包含API密钥等敏感信息）
- `projects/` 目录 - 个人项目文件
- `USER.md`, `MEMORY.md` - 个人身份信息

## 排除的脚本（本地保留）

以下脚本与skills无关，留在本地：
- 财务图表脚本 (treasury_*.py/sh)
- 代理协作示例 (agent_collaboration_example.py)
- 备份管理脚本 (backup_manager.sh, backup-skills-cron.sh)
- 代理管理工具 (agent_manager.sh)
- NAS备份脚本 (backup-private-nas.sh)

## 使用说明

每个技能目录包含完整的文档和使用示例。tools目录中的脚本与skills配合使用。

## 恢复方法

```bash
# 克隆仓库
git clone https://github.com/CallSymmetryEcho/openclaw-skills-backup.git

# 复制到workspace
cp -r skills/ ~/.openclaw/workspace/
cp -r tools/ ~/.openclaw/workspace/
```

## 自动备份配置

此仓库通过cron每周五自动备份。
详细配置见 ".github/workflows/" 或备份服务器cron配置。

## 许可证

根据具体技能文件中的许可证说明使用。
