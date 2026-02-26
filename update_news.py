#!/usr/bin/env python3
"""
Script de actualizare știri pentru AziNewsfolosind RSS feeds
Rulează zilnic la 8:00 dimineața
"""

import requests
import xml.etree.ElementTree as ET
import re
import os
import json
from datetime import datetime

# GitHub config
REPO_DIR = "/home/linuxtest2/.openclaw/workspace/garcon_daily"

def fetch_digi24_rss():
    """Preia știri de pe Digi24 RSS (legal)"""
    news = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        r = requests.get("https://www.digi24.ro/rss", headers=headers, timeout=15)
        if r.status_code == 200:
            # Parse XML
            root = ET.fromstring(r.text)
            
            # Digi24 RSS namespace
            ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
            
            for item in root.findall('.//item')[:15]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                
                if title_elem is not None and link_elem is not None:
                    title = title_elem.text or ""
                    link = link_elem.text or ""
                    description = desc_elem.text or "" if desc_elem is not None else ""
                    
                    # Clean title
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                # Get image from enclosure
                enclosure = item.find('enclosure')
                image_url = ""
                if enclosure is not None:
                    image_url = enclosure.get('url', '')
                    
                    # Determine category from URL
                    category = "Actualitate"
                    if '/politica/' in link:
                        category = "Politică"
                    elif '/economie/' in link:
                        category = "Economie"
                    elif '/externe/' in link or '/ue/' in link:
                        category = "Extern"
                    elif '/sport/' in link:
                        category = "Sport"
                    elif '/educatie/' in link:
                        category = "Educație"
                    elif '/sanatate/' in link:
                        category = "Sănătate"
                    elif '/tech/' in link or '/sci-tech/' in link:
                        category = "Tech"
                    
                    if title and len(title) > 15:
                        # Clean description - remove HTML
                        desc_clean = re.sub(r'<[^>]+>', '', description).strip()
                        if len(desc_clean) > 200:
                            desc_clean = desc_clean[:200] + "..."
                        
                        news.append({
                            "title": title[:150],
                            "content": f"{desc_clean} Citește mai mult pe Digi24.",
                            "category": category,
                            "url": link,
                            "image": image_url
                        })
                        
    except Exception as e:
        print(f"Eroare RSS Digi24: {e}")
    
    return news

def update_app_py(news_list):
    """Actualizează fișierul app.py cu noile știri"""
    app_py_path = os.path.join(REPO_DIR, "app.py")
    
    with open(app_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build news list for Python
    news_json = []
    for news in news_list[:15]:
        news_json.append(f'''        {{
            "title": "{news['title'].replace('"', '\\"')[:100]}",
            "content": \"\"\"{news['content'].replace('"', '\\"')[:200]}\"\"\",
            "category": "{news['category']}",
            "url": "{news['url']}",
            "image": "{news.get('image', '')}"
        }}''')
    
    news_str = "[\n" + ",\n".join(news_json) + "\n    ]"
    
    # Replace fallback_news
    import re
    pattern = r'fallback_news = \[[\s\S]*?\]'
    replacement = f'fallback_news = {news_str}'
    
    new_content = re.sub(pattern, replacement, content)
    
    with open(app_py_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Actualizate {len(news_list)} știri din RSS")

def git_push():
    """Face commit și push la GitHub"""
    os.chdir(REPO_DIR)
    
    os.system('git config user.email "garcon@bot.ai"')
    os.system('git config user.name "GarconBot"')
    
    os.system('git add app.py')
    os.system('git commit -m "Auto-update stiri din RSS - ' + datetime.now().strftime('%Y-%m-%d %H:%M') + '"')
    
    # Push using token
    token = os.environ.get("GH_TOKEN", "")
    if token:
        os.system(f'git push https://garconaibot:{token}@github.com/garconaibot/azinews.git master')
    else:
        os.system('git push origin master')
    
    print("Push complet!")

def main():
    print(f"[{datetime.now()}] Începe actualizarea știrilor din RSS...")
    
    # Fetch news from RSS
    print("Preia de pe Digi24 RSS...")
    news = fetch_digi24_rss()
    print(f"  -> {len(news)} știri găsite")
    
    if news:
        print("Actualizează app.py...")
        update_app_py(news)
        
        print("Face push la GitHub...")
        git_push()
        
        print("✅ Actualizare completă din RSS!")
    else:
        print("⚠️ Nu s-au găsit știri din RSS")

if __name__ == "__main__":
    main()
