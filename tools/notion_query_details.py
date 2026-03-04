#!/usr/bin/env python3
"""
详细查询Notion数据库内容
"""

import sys
sys.path.insert(0, '/home/node/.openclaw/workspace/tools')

from notion_client import NotionClient
import json

def query_database_details(database_id, limit=10):
    """详细查询数据库内容"""
    client = NotionClient()
    
    print(f"🔍 查询数据库: {database_id}")
    print("=" * 60)
    
    # 查询数据库
    results = client.query_database(database_id, page_size=limit)
    
    if 'error' in results:
        print(f"❌ 查询失败: {results['error']}")
        return
    
    records = results.get('results', [])
    print(f"✅ 找到 {len(records)} 条记录\n")
    
    for i, record in enumerate(records, 1):
        print(f"📄 记录 {i}:")
        print("-" * 40)
        
        properties = record.get('properties', {})
        
        for prop_name, prop_value in properties.items():
            prop_type = prop_value.get('type', 'unknown')
            
            # 根据类型提取值
            value = extract_property_value(prop_value, prop_type)
            
            if value:
                print(f"  {prop_name}: {value}")
        
        print()

def extract_property_value(prop_value, prop_type):
    """根据属性类型提取值"""
    if prop_type == 'title':
        # 标题类型
        title_items = prop_value.get('title', [])
        if title_items:
            return title_items[0].get('text', {}).get('content', '')
        return ''
    
    elif prop_type == 'rich_text':
        # 富文本类型
        rich_text_items = prop_value.get('rich_text', [])
        if rich_text_items:
            # 拼接所有文本
            texts = [item.get('text', {}).get('content', '') for item in rich_text_items]
            return ' '.join(texts)
        return ''
    
    elif prop_type == 'multi_select':
        # 多选类型
        select_items = prop_value.get('multi_select', [])
        if select_items:
            names = [item.get('name', '') for item in select_items]
            return ', '.join(names)
        return ''
    
    elif prop_type == 'select':
        # 单选类型
        select_item = prop_value.get('select', {})
        return select_item.get('name', '')
    
    elif prop_type == 'date':
        # 日期类型
        date_item = prop_value.get('date', {})
        if date_item:
            start = date_item.get('start', '')
            end = date_item.get('end', '')
            if end:
                return f"{start} 到 {end}"
            return start
        return ''
    
    elif prop_type == 'number':
        # 数字类型
        return prop_value.get('number', '')
    
    elif prop_type == 'url':
        # URL类型
        return prop_value.get('url', '')
    
    elif prop_type == 'status':
        # 状态类型
        status_item = prop_value.get('status', {})
        return status_item.get('name', '')
    
    elif prop_type == 'people':
        # 人员类型
        people_items = prop_value.get('people', [])
        if people_items:
            names = [item.get('name', '') for item in people_items]
            return ', '.join(names)
        return ''
    
    elif prop_type == 'files':
        # 文件类型
        file_items = prop_value.get('files', [])
        if file_items:
            names = [item.get('name', '') for item in file_items]
            return ', '.join(names)
        return ''
    
    elif prop_type == 'created_time':
        # 创建时间
        return prop_value.get('created_time', '')
    
    else:
        # 其他类型
        return str(prop_value)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='详细查询Notion数据库')
    parser.add_argument('database_id', help='数据库ID')
    parser.add_argument('--limit', '-l', type=int, default=10, help='记录数量限制')
    
    args = parser.parse_args()
    
    query_database_details(args.database_id, args.limit)

if __name__ == "__main__":
    main()