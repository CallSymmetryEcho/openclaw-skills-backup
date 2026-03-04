---
name: obsidian-tech-notes
description: Create technical documentation in Obsidian with standardized YAML frontmatter format. Use when user asks me to write technical notes, technical documentation, or archive technical solutions into Obsidian vault. Apply the standardized YAML frontmatter template to all markdown files created for the user's knowledge base.
---

# Obsidian Technical Notes

Create technical documentation with consistent YAML frontmatter formatting for Bin Lian's Obsidian vault.

## Frontmatter Template

Every technical note must begin with this YAML frontmatter:

```yaml
---
title: 
tags: 
cover: 
created: YYYY-MM-DD
author: Bin Lian
copyright_author: 
categories: 
---
```

### Field Guidelines

| Field | Value | Notes |
|-------|-------|-------|
| `title` | 笔记标题 | 从内容中提取或用户指定 |
| `tags` | #tag1 #tag2 | 相关技术标签，如 #docker #nas |
| `cover` | 留空或图片路径 | 封面图，通常留空 |
| `created` | 当前日期 | 格式：YYYY-MM-DD |
| `author` | Bin Lian | 固定值 |
| `copyright_author` | 留空 | 如有转载则填原作者 |
| `categories` | 分类 | 如 docker, coding, research |

## Workflow

1. **When triggered**: User asks to write/archive technical notes into Obsidian
2. **Apply template**: Insert YAML frontmatter at the very beginning of the file
3. **Fill fields**: Populate based on content context
4. **Save to vault**: Place in appropriate folder under `~/obisidian/`

## Asset Template

For convenience, the raw template is stored at:
`assets/tech-note-template.md`

## Examples

### Example 1: Docker Storage
```yaml
---
title: Docker 容器与外部存储连接方案
tags: #docker #nas #smb #storage #volume #部署
cover: 
created: 2026-03-02
author: Bin Lian
copyright_author: 
categories: docker
---
```

### Example 2: Lammps Learning
```yaml
---
title: Lammps 力场参数设置笔记
tags: #lammps #md #simulation #molecular-dynamics
cover: 
created: 2026-03-02
author: Bin Lian
copyright_author: 
categories: research
---
```

## Folder Conventions

- Docker相关: `markdown note/docker/`
- 编程技巧: `markdown note/` 或 `Coding skill/`
- 研究笔记: `markdown note/` 或具体项目文件夹
- 机器学习: `machine learning/`
- 阅读笔记: `阅读笔记/`

## Important

- **Must include**: YAML frontmatter is mandatory for all tech notes
- **Date format**: Use YYYY-MM-DD, not localized format
- **Author field**: Always "Bin Lian" for original content
- **File naming**: Use descriptive Chinese or English names with .md extension
