import sys, os, gzip, urllib.request
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills

temp_dem = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\temp_test.dem"
url = "https://gs13.myarena.pro/getzipdemo.php?hid=2155&dem=cstrike/auto-2611142138-bio_arena_fl.dem"
print("Downloading demo...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=25) as resp:
    data = gzip.decompress(resp.read())
    with open(temp_dem, "wb") as f:
        f.write(data)

print(f"Downloaded and decompressed demo ({len(data)} bytes). Parsing...")
map_name, players, kills = parse_demo_kills(temp_dem)
print(f"Map: {map_name}")
print(f"Players: {len(players)}")
print(f"Kills detected: {len(kills)}")
for k in kills[:12]:
    print(f"  {k['killer_name']} -> {k['victim_name']} ({k['weapon']}) [HS={k['headshot']}] @ {k['time']:.1f}s")

if os.path.exists(temp_dem):
    os.remove(temp_dem)
