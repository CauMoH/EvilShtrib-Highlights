"""
Measure dem_jump seeking speed in GoldSrc
"""
import os, time, glob, subprocess, cv2

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
DEMO_PATH = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban\bio_blocks_pro_2026-11-15_05-19-00.dem"

def make_waits(n):
    lines = []
    while n > 0:
        batch = min(20, n)
        lines.append(";".join(["wait"] * batch))
        n -= batch
    return lines

# Let's test dem_jump to 400s and 800s with different wait counts
for target_time, wait_count in [(200, 500), (400, 900), (600, 1400)]:
    cfg_lines = [
        "dem_forcehltv 1",
        "viewdemo render_clip",
        *make_waits(80),
        f"dem_jump {target_time}",
        *make_waits(wait_count),
        "startmovie test_speed 30",
        *make_waits(10),
        "endmovie",
        "quit"
    ]
    with open(os.path.join(CSTRIKE_DIR, "test_speed.cfg"), "w") as f:
        f.write("\n".join(cfg_lines) + "\n")
        
    for f in glob.glob(os.path.join(CSTRIKE_DIR, 'test_speed*.bmp')):
        os.remove(f)
        
    t0 = time.time()
    subprocess.run([
        HL_RECORDER, "-game", "cstrike", "-windowed", "-w", "800", "-h", "600",
        "-novid", "+exec", "test_speed.cfg"
    ], cwd=HL_DIR, timeout=45)
    dur = time.time() - t0
    bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'test_speed*.bmp')))
    print(f"Target={target_time}s, waits={wait_count} -> finished in {dur:.1f}s, dumped {len(bmps)} frames")
