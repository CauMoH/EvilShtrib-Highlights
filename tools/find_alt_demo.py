import urllib.request, json, os, glob

maps_in_cstrike = set(os.path.splitext(os.path.basename(f))[0].lower() for f in glob.glob(r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike_downloads\maps\*.bsp'))

api_url = "https://evilzomb.ru/demo_parser.php"
req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    all_demos = json.loads(resp.read().decode('utf-8'))

print(f"Total demos: {len(all_demos)}")
candidates = []
for d in all_demos:
    fn = d['fileName'].lower()
    for m in maps_in_cstrike:
        if m in fn and m not in ['zm_lb', 'bio_arena_fl', 'bio_talka', 'bio_ziger_azt', 'bio_valak', 'zm_dust_world_rbt', 'zm_biohazard_base_mx004', 'bio_snow_na2', 'zm_restart_v3', 'bio_oldhouse']:
            candidates.append((m, d))
            break
    if len(candidates) >= 5:
        break

for m, d in candidates:
    print(f"Map: {m:20s} | {d['fileName']} | {d['fileUrl']}")
