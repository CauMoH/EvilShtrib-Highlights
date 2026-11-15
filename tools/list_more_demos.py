import urllib.request, re

req = urllib.request.Request(
    'https://evilzomb.ru/demo_parser.php',
    headers={'User-Agent': 'Mozilla/5.0'}
)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

matches = re.findall(r'href="([^"]+getzipdemo\.php\?hid=2155&file=([^"&]+))"', html)
print(f"Found {len(matches)} demos on evilzomb.ru:")
for url, name in matches[:10]:
    print(f"  {name} -> {url}")
