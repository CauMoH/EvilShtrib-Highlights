import os
import sys
import json
import gzip
import urllib.request

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos"
os.makedirs(DEMOS_DIR, exist_ok=True)

TARGET_MAPS = [
    "bio_arena_fl",
    "bio_talka",
    "bio_ziger_azt",
    "bio_valak",
    "zm_lb",
    "zm_dust_world_rbt",
    "zm_biohazard_base_mx004",
    "bio_snow_na2",
    "zm_restart_v3",
    "bio_oldhouse"
]

def fetch_and_download():
    api_url = "https://evilzomb.ru/demo_parser.php"
    print(f"Fetching demo list from {api_url}...")
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        all_demos = json.loads(resp.read().decode('utf-8'))
        
    print(f"Total demos available: {len(all_demos)}")
    
    selected = {}
    for d in all_demos:
        fn = d['fileName']
        for target_m in TARGET_MAPS:
            if target_m not in selected and target_m in fn.lower():
                selected[target_m] = d
                break
        if len(selected) == len(TARGET_MAPS):
            break
            
    print(f"\nSelected {len(selected)} target demos:")
    for m, d in selected.items():
        print(f"  [{m}]: {d['fileName']} ({d.get('size', 'N/A')}) -> {d['fileUrl']}")
        
    # Download and decompress each
    for idx, (m, d) in enumerate(selected.items(), 1):
        clean_name = d['fileName'].replace('.dem.zip', '.dem').replace('.zip', '')
        out_dem = os.path.join(DEMOS_DIR, clean_name)
        if os.path.exists(out_dem) and os.path.getsize(out_dem) > 1024*1024:
            print(f"[{idx}/{len(selected)}] Already downloaded: {clean_name}")
            continue
            
        print(f"\n[{idx}/{len(selected)}] Downloading {clean_name} from {d['fileUrl']}...")
        req = urllib.request.Request(d['fileUrl'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=45) as resp:
            compressed = resp.read()
            
        print(f"  Downloaded {len(compressed)} bytes. Decompressing gzip...")
        decompressed = gzip.decompress(compressed)
        with open(out_dem, 'wb') as f:
            f.write(decompressed)
        print(f"  Saved {out_dem} ({len(decompressed)/(1024*1024):.1f} MB)")

if __name__ == '__main__':
    fetch_and_download()
