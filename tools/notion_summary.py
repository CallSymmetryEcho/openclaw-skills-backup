#!/usr/bin/env python3
"""
Notion数据库内容总结报告
"""

import sys
sys.path.insert(0, '/home/node/.openclaw/workspace/tools')

from notion_client import NotionClient
import json
from datetime import datetime

def generate_summary_report():
    """生成Notion数据库总结报告"""
    client = NotionClient()
    
    print("📊 Notion数据库内容总结报告")
    print("=" * 80)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 获取所有数据库
    print("🔍 搜索数据库...")
    databases = client.list_databases(page_size=50)
    
    if 'error' in databases:
        print(f"❌ 获取数据库失败: {databases['error']}")
        return
    
    db_list = databases.get('results', [])
    print(f"✅ 找到 {len(db_list)} 个数据库\n")
    
    # 分类统计
    categories = {
        '目标计划': ['Yearly Goals', 'Long term targets list', 'Daily Plan & Reflect'],
        '学习研究': ['Note book for  Learning', '实验操作'],
        '生活健康': ['锻炼时间和项目', '学菜小手册'],
        '旅行规划': ['Travel Plans'],
        '项目管理': ['小项目'],
        '汽车相关': ['Car part expense', 'estimate_price', 'similar car marketvalue', 'KBB estimation'],
        '其他': []
    }
    
    # 将数据库分类
    categorized_dbs = {cat: [] for cat in categories}
    
    for db in db_list:
        # 获取数据库标题
        title_items = db.get('title', [])
        if title_items and len(title_items) > 0:
            title = title_items[0].get('text', {}).get('content', '无标题')
        else:
            title = '无标题'
        
        db_id = db.get('id')
        properties = db.get('properties', {})
        
        # 分类
        found_category = False
        for category, keywords in categories.items():
            if any(keyword in title for keyword in keywords):
                categorized_dbs[category].append({
                    'title': title,
                    'id': db_id,
                    'properties': properties
                })
                found_category = True
                break
        
        if not found_category:
            categorized_dbs['其他'].append({
                'title': title,
                'id': db_id,
                'properties': properties
            })
    
    # 打印分类报告
    for category, dbs in categorized_dbs.items():
        if dbs:
            print(f"\n📁 {category} ({len(dbs)}个数据库)")
            print("-" * 40)
            
            for db in dbs:
                print(f"  📊 {db['title']}")
                print(f"     ID: {db['id']}")
                
                # 显示主要属性
                props = list(db['properties'].items())[:3]
                if props:
                    props_str = ", ".join([f"{k}({v.get('type', 'unknown')})" for k, v in props])
                    print(f"     属性: {props_str}")
                print()
    
    # 详细查询几个重要数据库
    print("\n" + "=" * 80)
    print("📈 重要数据库内容概览")
    print("=" * 80)
    
    important_dbs = [
        ('Yearly Goals', 'baf8e1b4-3f6a-47ac-a87c-5d83d32a3b14'),
        ('Daily Plan & Reflect', '9fa3d13f-18fc-481e-bf1e-b5ae1437fb31'),
        ('实验操作', 'da46bc38-80af-4cb4-ac7a-ab624cc89df0'),
        ('Long term targets list', 'a6df98ae-cde7-4a83-b21b-ffb476dde31a')
    ]
    
    for db_name, db_id in important_dbs:
        print(f"\n🔍 {db_name}")
        print("-" * 40)
        
        # 查询数据库内容
        results = client.query_database(db_id, page_size=5)
        
        if 'error' in results:
            print(f"  ❌ 查询失败: {results['error']}")
            continue
        
        records = results.get('results', [])
        print(f"  记录数量: {len(records)}")
        
        # 显示前几条记录
        for i, record in enumerate(records[:3], 1):
            properties = record.get('properties', {})
            
            # 获取标题
            title = '无标题'
            for prop_name, prop_value in properties.items():
                if prop_value.get('type') == 'title':
                    title_items = prop_value.get('title', [])
                    if title_items:
                        title = title_items[0].get('text', {}).get('content', '无标题')
                    break
            
            print(f"  {i}. {title}")
            
            # 显示关键属性
            for prop_name, prop_value in properties.items():
                prop_type = prop_value.get('type', 'unknown')
                if prop_type in ['select', 'multi_select', 'status', 'date']:
                    value = extract_property_value(prop_value, prop_type)
                    if value:
                        print(f"     {prop_name}: {value}")
        
        print()
    
    # 统计信息
    print("\n" + "=" * 80)
    print("📊 统计信息")
    print("=" * 80)
    
    total_records = 0
    for db_name, db_id in important_dbs:
        results = client.query_database(db_id, page_size=1)
        if 'error' not in results:
            total_records += len(results.get('results', []))
    
    print(f"📈 数据库总数: {len(db_list)}")
    print(f"📝 重要数据库记录总数: {total_records}")
    print(f"🏷️  分类数量: {len([cat for cat, dbs in categorized_dbs.items() if dbs])}")
    
    # 使用建议
    print("\n" + "=" * 80)
    print("💡 使用建议")
    print("=" * 80)
    print("""
1. **目标管理**: 使用 'Yearly Goals' 和 'Long term targets list' 跟踪长期目标
2. **日常计划**: 使用 'Daily Plan & Reflect' 进行日常规划和反思
3. **研究记录**: 使用 '实验操作' 记录实验步骤和结果
4. **学习笔记**: 使用 'Note book for Learning' 整理学习资料
5. **健康管理**: 使用 '锻炼时间和项目' 跟踪健身计划
6. **生活技能**: 使用 '学菜小手册' 记录烹饪经验
7. **项目管理**: 使用 '小项目' 管理个人项目
8. **汽车管理**: 使用汽车相关数据库跟踪车辆维护和费用
    """)
    
    print("\n" + "=" * 80)
    print("✅ 报告生成完成")
    print("=" * 80)

def extract_property_value(prop_value, prop_type):
    """根据属性类型提取值"""
    if prop_type == 'title':
        title_items = prop_value.get('title', [])
        if title_items:
            return title_items[0].get('text', {}).get('content', '')
        return ''
    
    elif prop_type == 'multi_select':
        select_items = prop_value.get('multi_select', [])
        if select_items:
            names = [item.get('name', '') for item in select_items]
            return ', '.join(names)
        return ''
    
    elif prop_type == 'select':
        select_item = prop_value.get('select', {})
        return select_item.get('name', '')
    
    elif prop_type == 'date':
        date_item = prop_value.get('date', {})
        if date_item:
            start = date_item.get('start', '')
            end = date_item.get('end', '')
            if end:
                return f"{start} 到 {end}"
            return start
        return ''
    
    elif prop_type == 'status':
        status_item = prop_value.get('status', {})
        return status_item.get('name', '')
    
    else:
        return ''

if __name__ == "__main__":
    generate_summary_report()