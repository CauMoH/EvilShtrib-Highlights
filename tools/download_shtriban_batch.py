import urllib.request
import zipfile
import io
import os

DEMOS = [
    "bio_monument_2026-11-15_11-15-00.zip",
    "bio_heat_rb2_2026-11-15_08-17-00.zip",
    "bio_green_peaks_rb7_2026-11-15_07-52-00.zip",
    "bio_dusty_2x2_fl_2026-11-15_06-35-00.zip",
    "bio_cube_rb3_2026-11-15_06-10-00.zip",
    "bio_blocks_rb5_2026-11-15_05-44-00.zip",
]

base_url = "https://stats.shtriban.ru/demos/"
out_dir = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban"
os.makedirs(out_dir, exist_ok=True)

for name in DEMOS:
    url = base_url + name
    print(f"Downloading {name}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for item in z.namelist():
                out_path = os.path.join(out_dir, item)
                with open(out_path, "wb") as f:
                    f.write(z.read(item))
                print(f"  Extracted: {item} ({os.path.getsize(out_path)/(1024*1024):.1f} MB)")
    except Exception as e:
        print(f"  Error on {name}: {e}")

print("Batch download complete!")
