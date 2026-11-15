import os, urllib.request, zipfile

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban"
os.makedirs(DEMOS_DIR, exist_ok=True)

to_download = [
    "bio_re-ziger_2026-11-15_12-31-00.zip",
    "bio_omega_b2_2026-11-15_12-06-00.zip",
    "bio_nova_b2_2026-11-15_11-41-00.zip",
    "bio_mono_b1_2026-11-15_10-50-00.zip",
    "bio_lego_ez_2026-11-15_09-33-00.zip",
    "bio_india_b2__2026-11-15_09-08-00.zip"
]

base_url = "https://stats.shtriban.ru/demos/"

for zname in to_download:
    dem_name = zname.replace(".zip", ".dem")
    final_dem = os.path.join(DEMOS_DIR, dem_name)
    if os.path.exists(final_dem):
        print(f"Already exists: {dem_name}")
        continue
        
    zurl = base_url + zname
    zpath = os.path.join(DEMOS_DIR, zname)
    print(f"Downloading {zname}...")
    try:
        req = urllib.request.Request(zurl, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(zpath, "wb") as out:
            out.write(resp.read())
            
        print(f"Extracting {zname}...")
        with zipfile.ZipFile(zpath, "r") as z:
            z.extractall(DEMOS_DIR)
        os.remove(zpath)
        print(f"Saved: {final_dem}")
    except Exception as e:
        print(f"Failed to download {zname}: {e}")
