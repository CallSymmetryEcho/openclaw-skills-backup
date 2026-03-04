---
name: web-searcher
description: Web search and information retrieval using browser automation. Use when the user needs to search for recent information, research topics, find papers, check news, or gather data from the internet. Triggers on requests like "search for...", "look up...", "find information about...", "what's the latest on...", or any research query requiring current web data.
---

# Web Searcher

## Overview

Performs web searches and extracts information from websites using browser automation. Ideal for:
- Researching recent developments (2024-2025)
- Finding academic papers and publications
- Checking news and current events
- Gathering technical information
- Verifying facts and data

## When to Use

Use this skill when:
1. User asks about recent events or breakthroughs ("recent breakthrough in nano synthesis")
2. User needs current information not in training data
3. User wants to find specific papers, articles, or sources
4. Research requires up-to-date web data

## Workflow

### Step 1: Start Browser
```bash
browser start --profile=openclaw
```

Or use Chrome profile if user has extension connected:
```bash
browser start --profile=chrome
```

### Step 2: Navigate and Search
```bash
browser open --url="https://www.google.com/search?q=YOUR_QUERY"
```

### Step 3: Extract Results
Use `browser snapshot` to capture page content, then analyze and summarize findings.

### Step 4: Deep Dive
For specific articles, use `browser open` on the URL and extract key information.

## Search Strategies

**For recent research:**
- Use Google Scholar: `site:scholar.google.com`
- Add year filters: `2024` or `2025`
- Use terms like "breakthrough", "recent advances", "latest"

**For technical topics:**
- Search arXiv: `site:arxiv.org`
- Search specific journals or conferences
- Use technical keywords from the domain

**For news:**
- Use Google News
- Check reputable science/tech outlets
- Filter by date when possible

## Resources

### scripts/web_search.py
Automated web search script that:
- Opens browser
- Performs Google search
- Extracts top results
- Summarizes findings

Run with: `python3 scripts/web_search.py "your search query"`
