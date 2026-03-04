#!/usr/bin/env python3
"""
Notion 数据操作示例
展示如何创建数据库、写入数据、查询数据
"""

import sys
sys.path.insert(0, '/home/node/.openclaw/workspace/tools')

from notion_client import NotionClient
import json
from datetime import datetime

def example_create_project_database():
    """
    示例：创建一个项目管理数据库
    注意：Notion API目前不支持直接创建数据库，需要在Notion界面中创建
    """
    print("📝 Notion项目管理示例")
    print("=" * 60)
    
    client = NotionClient()
    
    # 1. 首先搜索现有的数据库
    print("\n1. 搜索现有的数据库...")
    databases = client.list_databases()
    
    if databases.get('results'):
        print(f"✅ 找到 {len(databases['results'])} 个数据库")
        for i, db in enumerate(databases['results'], 1):
            title = db.get('title', [{}])[0].get('text', {}).get('content', f'数据库 {i}')
            db_id = db.get('id')
            print(f"   {i}. {title} (ID: {db_id})")
    else:
        print("⚠️  没有找到现有数据库")
        print("\n💡 提示：你需要先在Notion界面中创建一个数据库")
        print("   1. 打开Notion")
        print("   2. 创建一个新页面")
        print("   3. 添加一个数据库（表格视图）")
        print("   4. 添加以下列：项目名称、状态、优先级、截止日期")
        return
    
    # 2. 如果有数据库，查询内容
    if databases.get('results'):
        db_id = databases['results'][0].get('id')
        db_title = databases['results'][0].get('title', [{}])[0].get('text', {}).get('content', '未命名')
        
        print(f"\n2. 查询数据库 '{db_title}' 的内容...")
        records = client.query_database(db_id, page_size=10)
        
        if records.get('results'):
            print(f"✅ 找到 {len(records['results'])} 条记录")
            for i, record in enumerate(records['results'], 1):
                properties = record.get('properties', {})
                print(f"\n   记录 {i}:")
                for prop_name, prop_value in properties.items():
                    prop_type = prop_value.get('type', 'unknown')
                    print(f"     - {prop_name} ({prop_type})")
        else:
            print("📭 数据库为空")
        
        # 3. 创建新记录示例
        print(f"\n3. 创建新记录示例...")
        print("   要在数据库中创建记录，使用以下代码：")
        print(f"""
   parent = {{"database_id": "{db_id}"}}
   properties = {{
       "项目名称": {{
           "title": [{{"text": {{"content": "新项目"}}}}]
       }},
       "状态": {{
           "select": {{"name": "进行中"}}
       }},
       "优先级": {{
           "select": {{"name": "高"}}
       }},
       "截止日期": {{
           "date": {{"start": "{datetime.now().strftime('%Y-%m-%d')}"}}
       }}
   }}
   
   page = client.create_page(parent, properties)
        """)

def example_read_and_write():
    """读取和写入数据示例"""
    print("\n" + "=" * 60)
    print("📊 读取和写入数据示例")
    print("=" * 60)
    
    client = NotionClient()
    
    # 搜索所有内容
    print("\n1. 搜索Notion工作区...")
    results = client.search(page_size=50)
    
    items = results.get('results', [])
    print(f"✅ 找到 {len(items)} 个条目")
    
    # 分类统计
    databases = [i for i in items if i.get('object') == 'database']
    pages = [i for i in items if i.get('object') == 'page']
    
    print(f"   - 数据库: {len(databases)}")
    print(f"   - 页面: {len(pages)}")
    
    # 显示详细信息
    if databases:
        print("\n2. 数据库详情:")
        for db in databases:
            title = db.get('title', [{}])[0].get('text', {}).get('content', '无标题')
            db_id = db.get('id')
            properties = db.get('properties', {})
            print(f"\n   📊 {title}")
            print(f"      ID: {db_id}")
            print(f"      属性: {', '.join(properties.keys())}")
    
    if pages:
        print("\n3. 页面详情 (前5个):")
        for page in pages[:5]:
            page_id = page.get('id')
            url = page.get('url', '')
            
            # 获取标题
            title = '无标题'
            props = page.get('properties', {})
            for prop_name, prop_value in props.items():
                if prop_value.get('type') == 'title':
                    title_items = prop_value.get('title', [])
                    if title_items:
                        title = title_items[0].get('text', {}).get('content', '无标题')
                    break
            
            print(f"   📄 {title}")
            print(f"      ID: {page_id}")
            print(f"      URL: {url}")

def example_quick_create():
    """快速创建示例"""
    print("\n" + "=" * 60)
    print("⚡ 快速创建示例")
    print("=" * 60)
    
    print("""
要在Notion中创建内容，你需要：

1. **创建一个数据库**（在Notion界面中）:
   - 打开Notion
   - 新建页面
   - 添加数据库（表格视图）
   - 设置列：项目名称、状态、优先级、截止日期

2. **使用API写入数据**:

```python
from notion_client import NotionClient

client = NotionClient()

# 替换为你的数据库ID
database_id = "your-database-id"

# 创建新项目记录
parent = {"database_id": database_id}
properties = {
    "项目名称": {
        "title": [{"text": {"content": "我的研究项目"}}]
    },
    "状态": {
        "select": {"name": "进行中"}
    },
    "优先级": {
        "select": {"name": "高"}
    },
    "截止日期": {
        "date": {"start": "2026-03-15"}
    }
}

# 创建页面
page = client.create_page(parent, properties)
print(f"✅ 创建成功: {page.get('url')}")
```

3. **查询数据**:

```python
# 查询数据库所有记录
records = client.query_database(database_id, page_size=100)

for record in records.get('results', []):
    properties = record.get('properties', {})
    
    # 获取项目名称
    name_prop = properties.get('项目名称', {})
    name = name_prop.get('title', [{}])[0].get('text', {}).get('content', '未命名')
    
    # 获取状态
    status_prop = properties.get('状态', {})
    status = status_prop.get('select', {}).get('name', '未知')
    
    print(f"{name} - {status}")
```
""")

def main():
    """主函数"""
    print("🚀 Notion 数据操作示例")
    print("=" * 60)
    
    try:
        # 示例1：项目管理
        example_create_project_database()
        
        # 示例2：读取和写入
        example_read_and_write()
        
        # 示例3：快速创建指南
        example_quick_create()
        
        print("\n" + "=" * 60)
        print("✅ 示例完成")
        print("=" * 60)
        print("\n💡 下一步建议：")
        print("1. 在Notion中创建一个数据库")
        print("2. 获取数据库ID")
        print("3. 使用API写入和查询数据")
        print("\n需要帮助？查看: ./skills/notion-integration/SKILL.md")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()