import urllib.request
import re
import os

url = 'https://stats.shtriban.ru/hlstats.php?mode=demos&game=cstrike'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    print(f"Page length: {len(html)}")
    
    # Let's search for links or table entries
    links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html)
    demo_links = [l for l in links if '.dem' in l or 'download' in l.lower() or 'demos' in l.lower()]
    print(f"Found {len(demo_links)} relevant links:")
    for l in demo_links[:20]:
        print(" ", l)
        
    # Search for table rows with demos
    # Let's see some snippets containing .dem
    snippets = [m.start() for m in re.finditer(r'\.dem', html)]
    print(f"\nFound {len(snippets)} occurrences of '.dem'")
    for pos in snippets[:10]:
        start = max(0, pos - 150)
        end = min(len(html), pos + 150)
        print("--- SNIPPET ---")
        print(html[start:end])

except Exception as e:
    print("Error:", e)
