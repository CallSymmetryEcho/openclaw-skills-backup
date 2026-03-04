#!/usr/bin/env python3
"""
Notion API 集成工具
支持数据库查询、页面创建、内容更新等功能
"""

import requests
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "workspace" / "config"
API_KEY_FILE = CONFIG_DIR / "notion_api_key.txt"

class NotionClient:
    """Notion API 客户端"""
    
    def __init__(self, api_key=None):
        """初始化Notion客户端"""
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = self._load_api_key()
        
        if not self.api_key:
            raise ValueError("Notion API Key 未设置")
        
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def _load_api_key(self):
        """从文件加载API Key"""
        if API_KEY_FILE.exists():
            with open(API_KEY_FILE, 'r') as f:
                return f.read().strip()
        return None
    
    def test_connection(self):
        """测试API连接"""
        try:
            # 搜索页面来验证API Key
            url = f"{self.base_url}/search"
            response = requests.post(url, headers=self.headers, json={"page_size": 1})
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'message': 'API连接成功',
                    'results_count': len(data.get('results', [])),
                    'has_more': data.get('has_more', False)
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'message': response.text
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search(self, query="", filter_type=None, page_size=10):
        """搜索Notion内容"""
        url = f"{self.base_url}/search"
        
        payload = {
            "query": query,
            "page_size": page_size
        }
        
        if filter_type:
            payload["filter"] = {"value": filter_type, "property": "object"}
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def get_database(self, database_id):
        """获取数据库信息"""
        url = f"{self.base_url}/databases/{database_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def query_database(self, database_id, filter_obj=None, sorts=None, page_size=10):
        """查询数据库"""
        url = f"{self.base_url}/databases/{database_id}/query"
        
        payload = {
            "page_size": page_size
        }
        
        if filter_obj:
            payload["filter"] = filter_obj
        if sorts:
            payload["sorts"] = sorts
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def create_page(self, parent, properties, children=None):
        """创建页面"""
        url = f"{self.base_url}/pages"
        
        payload = {
            "parent": parent,
            "properties": properties
        }
        
        if children:
            payload["children"] = children
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def get_page(self, page_id):
        """获取页面信息"""
        url = f"{self.base_url}/pages/{page_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def update_page(self, page_id, properties):
        """更新页面"""
        url = f"{self.base_url}/pages/{page_id}"
        
        try:
            response = requests.patch(url, headers=self.headers, json={"properties": properties})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def list_databases(self, page_size=10):
        """列出所有数据库"""
        return self.search(filter_type="database", page_size=page_size)
    
    def list_pages(self, page_size=10):
        """列出所有页面"""
        return self.search(filter_type="page", page_size=page_size)

def print_databases(databases):
    """打印数据库列表"""
    print("\n📊 数据库列表:")
    print("-" * 60)
    
    for i, db in enumerate(databases.get('results', []), 1):
        # 安全地获取标题
        title_items = db.get('title', [])
        if title_items and len(title_items) > 0:
            title = title_items[0].get('text', {}).get('content', '无标题')
        else:
            title = '无标题'
        
        db_id = db.get('id', '未知')
        
        print(f"{i}. {title}")
        print(f"   ID: {db_id}")
        
        # 显示属性
        properties = db.get('properties', {})
        if properties:
            props_str = ", ".join([f"{k}({v.get('type', 'unknown')})" for k, v in list(properties.items())[:3]])
            print(f"   属性: {props_str}")
        print()

def print_pages(pages):
    """打印页面列表"""
    print("\n📄 页面列表:")
    print("-" * 60)
    
    for i, page in enumerate(pages.get('results', []), 1):
        # 获取页面标题
        title = "无标题"
        properties = page.get('properties', {})
        
        for prop_name, prop_value in properties.items():
            if prop_value.get('type') == 'title':
                title_items = prop_value.get('title', [])
                if title_items:
                    title = title_items[0].get('text', {}).get('content', '无标题')
                break
        
        page_id = page.get('id', '未知')
        url = page.get('url', '')
        
        print(f"{i}. {title}")
        print(f"   ID: {page_id}")
        print(f"   URL: {url}")
        print()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Notion API 工具')
    parser.add_argument('command', choices=[
        'test', 'search', 'databases', 'pages', 
        'query', 'create', 'update'
    ], help='要执行的命令')
    parser.add_argument('--query', '-q', help='搜索关键词')
    parser.add_argument('--database-id', '-d', help='数据库ID')
    parser.add_argument('--page-id', '-p', help='页面ID')
    parser.add_argument('--title', '-t', help='页面标题')
    parser.add_argument('--content', '-c', help='页面内容')
    
    args = parser.parse_args()
    
    try:
        # 初始化客户端
        client = NotionClient()
        
        if args.command == 'test':
            # 测试连接
            print("🧪 测试Notion API连接...")
            result = client.test_connection()
            
            if result['success']:
                print(f"✅ {result['message']}")
                print(f"📊 找到 {result['results_count']} 个结果")
            else:
                print(f"❌ 连接失败: {result.get('error', '未知错误')}")
                print(f"详情: {result.get('message', '')}")
        
        elif args.command == 'search':
            # 搜索内容
            query = args.query or input("请输入搜索关键词: ")
            print(f"🔍 搜索: {query}")
            
            results = client.search(query=query, page_size=10)
            
            if 'error' in results:
                print(f"❌ 搜索失败: {results['error']}")
            else:
                print(f"✅ 找到 {len(results.get('results', []))} 个结果")
                
                # 分类显示
                databases = [r for r in results.get('results', []) if r.get('object') == 'database']
                pages = [r for r in results.get('results', []) if r.get('object') == 'page']
                
                if databases:
                    print_databases({'results': databases})
                if pages:
                    print_pages({'results': pages})
        
        elif args.command == 'databases':
            # 列出数据库
            print("📊 获取数据库列表...")
            databases = client.list_databases(page_size=20)
            
            if 'error' in databases:
                print(f"❌ 获取失败: {databases['error']}")
            else:
                print_databases(databases)
        
        elif args.command == 'pages':
            # 列出页面
            print("📄 获取页面列表...")
            pages = client.list_pages(page_size=20)
            
            if 'error' in pages:
                print(f"❌ 获取失败: {pages['error']}")
            else:
                print_pages(pages)
        
        elif args.command == 'query':
            # 查询数据库
            if not args.database_id:
                print("❌ 请提供数据库ID (--database-id)")
                return
            
            print(f"🔍 查询数据库: {args.database_id}")
            results = client.query_database(args.database_id, page_size=10)
            
            if 'error' in results:
                print(f"❌ 查询失败: {results['error']}")
            else:
                print(f"✅ 找到 {len(results.get('results', []))} 条记录")
                
                for i, record in enumerate(results.get('results', []), 1):
                    print(f"\n记录 {i}:")
                    properties = record.get('properties', {})
                    for prop_name, prop_value in properties.items():
                        prop_type = prop_value.get('type', 'unknown')
                        print(f"  {prop_name} ({prop_type})")
        
        elif args.command == 'create':
            # 创建页面
            if not args.database_id and not args.page_id:
                print("❌ 请提供父级数据库ID (--database-id) 或页面ID (--page-id)")
                return
            
            title = args.title or input("请输入页面标题: ")
            
            if args.database_id:
                parent = {"database_id": args.database_id}
                properties = {
                    "Name": {
                        "title": [{"text": {"content": title}}]
                    }
                }
            else:
                parent = {"page_id": args.page_id}
                properties = {
                    "title": {
                        "title": [{"text": {"content": title}}]
                    }
                }
            
            print(f"📝 创建页面: {title}")
            result = client.create_page(parent, properties)
            
            if 'error' in result:
                print(f"❌ 创建失败: {result['error']}")
            else:
                print(f"✅ 页面创建成功")
                print(f"   ID: {result.get('id')}")
                print(f"   URL: {result.get('url')}")
        
        elif args.command == 'update':
            # 更新页面
            if not args.page_id:
                print("❌ 请提供页面ID (--page-id)")
                return
            
            print(f"📝 更新页面: {args.page_id}")
            # 这里可以添加更多更新逻辑
            print("更新功能待完善")
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()