import os, glob, subprocess, cv2, shutil

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")

for f in glob.glob(os.path.join(CSTRIKE_DIR, "test_gald*.bmp")):
    os.remove(f)

demo_src = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban\bio_blocks_pro_2026-11-15_05-19-00.dem"
shutil.copy2(demo_src, os.path.join(CSTRIKE_DIR, "render_clip.dem"))

def make_waits(n):
    lines = []
    while n > 0:
        batch = min(20, n)
        lines.append(";".join(["wait"] * batch))
        n -= batch
    return lines

cfg_lines = [
    "dem_forcehltv 1",
    "hud_saytext 1",
    "hud_deathnotice_time 6",
    "viewdemo render_clip",
    *make_waits(80),
    "dem_jump 72.0",
    *make_waits(320),
    'follow "Galdalfus"',
    "spec_mode 4 0",
    "spec_mode_internal 4",
    *make_waits(25),
    "dem_pause 0",
    "dem_speed 1.0",
    "gamma 4",
    "brightness 4",
    'follow "Galdalfus"',
    "spec_mode 4 0",
    *make_waits(15),
    "host_framerate 0.03333333333",
    "startmovie test_gald 30",
    *make_waits(100),
    "endmovie",
    *make_waits(10),
    "quit"
]

with open(os.path.join(CSTRIKE_DIR, "test_gald.cfg"), "w") as f:
    f.write("\n".join(cfg_lines) + "\n")

subprocess.run([
    HL_RECORDER, "-game", "cstrike", "-windowed", "-w", "1280", "-h", "720",
    "-novid", "+exec", "test_gald.cfg"
], cwd=HL_DIR, timeout=40)

bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, "test_gald*.bmp")))
print(f"Dumped {len(bmps)} frames")

kills_found = 0
for idx, b in enumerate(bmps):
    fr = cv2.imread(b)
    dn = fr[10:120, 950:1270]
    red_pixels = ((dn[:,:,2] > 180) & (dn[:,:,0] < 100) & (dn[:,:,1] < 100)).sum()
    blue_pixels = ((dn[:,:,0] > 180) & (dn[:,:,2] < 100) & (dn[:,:,1] < 100)).sum()
    if red_pixels > 20 or blue_pixels > 20:
        kills_found += 1
print(f"Kill notice visible in {kills_found}/{len(bmps)} frames!")
if bmps:
    cv2.imwrite(r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\v5_debug\gald_sample.jpg", cv2.imread(bmps[len(bmps)//2]))
