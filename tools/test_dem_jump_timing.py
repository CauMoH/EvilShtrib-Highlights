"""
Test how many waits are required to reach various timestamps with dem_jump.
"""
import os, time, glob, subprocess, cv2, imageio_ffmpeg

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
DEMO_PATH = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban\bio_dusty_2x2_fl_2026-11-15_06-35-00.dem"

def make_waits(n):
    lines = []
    while n > 0:
        batch = min(20, n)
        lines.append(";".join(["wait"] * batch))
        n -= batch
    return lines

for waits_count in [500, 1000, 2000]:
    # Clean bmp
    for f in glob.glob(os.path.join(CSTRIKE_DIR, 'test_jump*.bmp')):
        os.remove(f)
        
    cfg_lines = [
        "dem_forcehltv 1",
        "viewdemo render_clip",
        *make_waits(80),
        "dem_jump 1332",
        *make_waits(waits_count),
        "startmovie test_jump 30",
        *make_waits(10),
        "endmovie",
        "quit"
    ]
    
    with open(os.path.join(CSTRIKE_DIR, "test_jump.cfg"), "w") as f:
        f.write("\n".join(cfg_lines) + "\n")
        
    t0 = time.time()
    subprocess.run([
        HL_RECORDER, "-game", "cstrike", "-windowed", "-w", "800", "-h", "600",
        "-novid", "+exec", "test_jump.cfg"
    ], cwd=HL_DIR, timeout=40)
    dur = time.time() - t0
    
    bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'test_jump*.bmp')))
    print(f"waits={waits_count} -> time={dur:.1f}s, dumped {len(bmps)} frames")
    if bmps:
        # Check round timer in top right of first frame
        fr = cv2.imread(bmps[0])
        # crop top right
        timer_crop = fr[0:100, 600:800]
        cv2.imwrite(rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\jump_{waits_count}.jpg", timer_crop)
