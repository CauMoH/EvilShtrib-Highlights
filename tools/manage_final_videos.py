import os, shutil

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
FINAL_DIR = os.path.join(BASE_DIR, "final_videos")
os.makedirs(FINAL_DIR, exist_ok=True)

for fn in ["EvilShtrib_60s_Vol2.mp4", "EvilShtrib_60s_Vol3.mp4"]:
    src = os.path.join(BASE_DIR, fn)
    dst = os.path.join(FINAL_DIR, fn)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {fn} -> {dst} ({os.path.getsize(dst)/(1024*1024):.2f} MB)")

print("\nFiles in final_videos:")
for f in os.listdir(FINAL_DIR):
    fp = os.path.join(FINAL_DIR, f)
    print(f"  {f} ({os.path.getsize(fp)/(1024*1024):.2f} MB)")
