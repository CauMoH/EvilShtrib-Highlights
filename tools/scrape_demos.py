import urllib.request
import re

url = 'https://evilzomb.ru/hltv/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
print(f"Total script blocks: {len(scripts)}")
for idx, s in enumerate(scripts):
    if any(k in s.lower() for k in ['file', 'hltv', 'table', 'ajax', 'fetch', 'json']):
        print(f"--- Script {idx} ---")
        print(s[:1500])

script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I)
print(f"Script srcs: {len(script_srcs)}")
for src in script_srcs:
    if any(k in src.lower() for k in ['hltv', 'file', 'custom']):
        print("  src:", src)
