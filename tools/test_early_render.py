import os, sys, glob, shutil, subprocess, time, cv2, imageio_ffmpeg

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
DEMOS_DIR = os.path.join(BASE_DIR, "demos_shtriban")
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

demo_file = "bio_blocks_pro_2026-11-15_05-19-00.dem"
killer = "Player_9"
approx_time = 74.8
num_frames = 90

full_path = os.path.join(DEMOS_DIR, demo_file)
mname, pnames, kills = parse_demo_kills(full_path)
moments = cluster_moments(kills)
match = None
for m in moments:
    if m['killer_name'] == killer and abs(m['kills'][0]['time'] - approx_time) < 10.0:
        match = m
        break

print(f"Match: {match['killer_name']}, kills: {len(match['kills'])}, times: {[k['time'] for k in match['kills']]}")
fk = match['kills'][0]['time']
lk = match['kills'][-1]['time']
mid_kill = (fk + lk) / 2.0
rec_start = max(1.0, mid_kill - 1.5)
rec_end = rec_start + 3.0

wait_jump = int(rec_start * 2.8) + 120
print(f"rec_start: {rec_start:.1f}s, wait_jump: {wait_jump}")

# Clean
for f in glob.glob(os.path.join(CSTRIKE_DIR, 'test_early*.bmp')):
    os.remove(f)

shutil.copy2(full_path, os.path.join(CSTRIKE_DIR, 'render_clip.dem'))

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
    f"dem_jump {rec_start:.1f}",
    *make_waits(wait_jump),
    f'follow "{killer}"',
    "spec_mode 4 0",
    "spec_mode_internal 4",
    *make_waits(25),
    "dem_pause 0",
    "dem_speed 1.0",
    "gamma 4",
    "brightness 4",
    f'follow "{killer}"',
    "spec_mode 4 0",
    *make_waits(15),
    "host_framerate 0.03333333333",
    "startmovie test_early 30",
    *make_waits(num_frames + 20),
    "endmovie",
    *make_waits(10),
    "quit"
]

with open(os.path.join(CSTRIKE_DIR, "test_early.cfg"), "w", encoding="utf-8") as f:
    f.write("\n".join(cfg_lines) + "\n")

t0 = time.time()
subprocess.run([
    HL_RECORDER, "-game", "cstrike", "-windowed", "-w", "1280", "-h", "720",
    "-novid", "+exec", "test_early.cfg"
], cwd=HL_DIR, timeout=40)
print(f"Recorded in {time.time()-t0:.1f}s")

bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'test_early*.bmp')))
print(f"Dumped {len(bmps)} frames")

# Scan kill notices in dumped frames
kills_found = 0
for idx, b in enumerate(bmps):
    fr = cv2.imread(b)
    dn = fr[10:120, 950:1270]
    red_pixels = ((dn[:,:,2] > 180) & (dn[:,:,0] < 100) & (dn[:,:,1] < 100)).sum()
    blue_pixels = ((dn[:,:,0] > 180) & (dn[:,:,2] < 100) & (dn[:,:,1] < 100)).sum()
    if red_pixels > 20 or blue_pixels > 20:
        kills_found += 1
print(f"Kill notice visible in {kills_found}/{len(bmps)} frames!")
