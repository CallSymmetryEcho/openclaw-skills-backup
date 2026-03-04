# Notion 集成技能 - 快速参考

## 🎯 核心信息（必读）

### 用户数据库概览
**总数据库**: 50个  
**主要分类**:
1. **目标计划** - 年度目标、长期目标、日常计划
2. **学习研究** - 实验记录、学习笔记  
3. **生活健康** - 锻炼、烹饪
4. **项目管理** - 小项目
5. **汽车管理** - 费用、估值

### 🔑 关键数据库ID（常用）
| 数据库 | ID | 用途 |
|--------|----|------|
| Yearly Goals | `baf8e1b4-3f6a-47ac-a87c-5d83d32a3b14` | 年度目标 |
| Daily Plan & Reflect | `9fa3d13f-18fc-481e-bf1e-b5ae1437fb31` | 日常计划 |
| 实验操作 | `da46bc38-80af-4cb4-ac7a-ab624cc89df0` | 研究记录 |
| Long term targets | `a6df98ae-cde7-4a83-b21b-ffb476dde31a` | 长期目标 |

## ⚡ 快速命令

### 基础操作
```bash
# 测试连接
./tools/notion.sh test

# 列出所有数据库
./tools/notion.sh databases

# 查询数据库（使用上表ID）
./tools/notion.sh query baf8e1b4-3f6a-47ac-a87c-5d83d32a3b14

# 搜索内容
./tools/notion.sh search "实验"
```

### 详细查询
```bash
# 查看数据库详细内容
python3 ./tools/notion_query_details.py <database_id>

# 生成总结报告
python3 ./tools/notion_summary.py
```

## 🐍 Python快速使用

```python
from notion_client import NotionClient
client = NotionClient()

# 1. 查询年度目标
records = client.query_database("baf8e1b4-3f6a-47ac-a87c-5d83d32a3b14")

# 2. 创建今日计划
parent = {"database_id": "9fa3d13f-18fc-481e-bf1e-b5ae1437fb31"}
properties = {
    "Name": {"title": [{"text": {"content": "今日计划"}}]},
    "Tags": {"multi_select": [{"name": "每日task"}]}
}
client.create_page(parent, properties)

# 3. 搜索实验记录
results = client.search(query="Ag particles", page_size=5)
```

## 📊 数据库内容摘要

### Yearly Goals (年度目标)
- 2024 yearly Goal (validated)
- 毕业吉他演奏会  
- 2026 年度计划 (In Process)
- 2025 yearly goal (validated)

### 实验操作 (研究记录)
- B. Subtilis - broth-based incubation procedure (Bio)
- Sillicon Nanowires synthesis(HF etchant) (Synthesis)
- Ag particles grow (Functionlize)
- lithography (Technique)

### Long term targets
- 早上要去拿车牌 (Done 🙌, 2023-08-09)
- ME396K lecture (Done 🙌, 2023-09-02)
- 文章1 MARSS2023 review (Done 🙌, 2023-08-06)

## 🛠️ 工具文件位置

```
~/.openclaw/workspace/
├── config/notion_api_key.txt          # API Key
├── tools/notion_client.py             # 主客户端
├── tools/notion.sh                    # 命令行工具
├── tools/notion_query_details.py      # 详细查询
└── tools/notion_summary.py            # 总结报告
```

## 💡 使用模式

### 用户偏好
- 工作与生活分离
- 按需访问，不主动监控
- 偏好命令行工具
- 重视安全和文档

### 典型场景
1. **研究记录** - 查询/添加实验步骤
2. **目标跟踪** - 更新年度/长期目标状态  
3. **日常规划** - 创建今日计划
4. **知识管理** - 整理学习笔记

## 🚨 注意事项

1. **API Key**: 已配置，无需重复设置
2. **连接状态**: 已验证成功
3. **权限**: 完整读写权限
4. **错误处理**: 工具已包含完善错误处理

## 📞 快速帮助

**问题**: 找不到数据库  
**解决**: `./tools/notion.sh databases` 查看完整列表

**问题**: 查询失败  
**解决**: 检查数据库ID是否正确，使用完整32字符ID

**问题**: 创建页面失败  
**解决**: 确认属性名称和类型与数据库匹配

---

**最后更新**: 2026-03-04  
**状态**: ✅ 完全可用  
**建议**: 使用上表数据库ID快速操作，避免重复搜索