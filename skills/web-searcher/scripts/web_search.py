#!/usr/bin/env python3
"""
Web Search Script - Automates browser-based web searches
Usage: python3 web_search.py "your search query"
"""

import sys
import subprocess
import json
import time

def run_browser_command(action, **kwargs):
    """Run a browser tool command via OpenClaw CLI"""
    cmd = ["openclaw", "browser", action]
    
    for key, value in kwargs.items():
        cmd.extend([f"--{key}", str(value)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def search_google(query):
    """Perform a Google search using browser automation"""
    print(f"Searching for: {query}")
    
    # URL encode the query
    encoded_query = query.replace(" ", "+")
    search_url = f"https://www.google.com/search?q={encoded_query}"
    
    # Try to use browser tool
    try:
        # First check if browser is running
        stdout, stderr, code = run_browser_command("status")
        
        if "not running" in stderr.lower() or code != 0:
            print("Starting browser...")
            run_browser_command("start", profile="openclaw")
            time.sleep(3)
        
        # Open the search URL
        print(f"Opening: {search_url}")
        stdout, stderr, code = run_browser_command("open", url=search_url, profile="openclaw")
        
        if code != 0:
            print(f"Browser error: {stderr}")
            return None
            
        print("Search completed. Check browser output.")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 web_search.py 'your search query'")
        print("Example: python3 web_search.py 'recent breakthrough nanosynthesis 2024'")
        sys.exit(1)
    
    query = sys.argv[1]
    search_google(query)
