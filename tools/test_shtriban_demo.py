import urllib.request, zipfile, io, os, sys
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

out_dir = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban"
os.makedirs(out_dir, exist_ok=True)
url = 'https://stats.shtriban.ru/demos/bio_evil_dust_fl_2026-11-15_07-01-00.zip'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read()
with zipfile.ZipFile(io.BytesIO(data)) as z:
    dem_name = z.namelist()[0]
    out_path = os.path.join(out_dir, dem_name)
    with open(out_path, 'wb') as f:
        f.write(z.read(dem_name))

mname, pnames, kills = parse_demo_kills(out_path)
clusters = cluster_moments(kills)
print(f"Map: {mname} | Kills: {len(kills)} | Clusters: {len(clusters)}")
for c in clusters[:8]:
    victims = []
    for k in c['kills']:
        hs = " [HS]" if k.get('headshot') else ""
        victims.append(f"{k['victim_name']}{hs} ({k.get('weapon')})")
    print(f"  {c['killer_name']} ({c['num_kills']} kills, score {c['score']}): {', '.join(victims)}")
