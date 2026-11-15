import os, sys, glob, shutil, subprocess, time, imageio_ffmpeg

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
CLIPS_DIR = os.path.join(BASE_DIR, "clips_vol3")
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

demo_path = os.path.join(BASE_DIR, "demos_backup", "bio_asalto_f_2026-11-14_17-27-00.dem")
killer = "Shadow-Death"
approx_time = 58.7
title = "SG550 SNIPER DOUBLE"
wpn_label = "SG550 COMMANDO SNIPER"
tag = "DOUBLE KILL"
max_frames = 170
out_mp4 = os.path.join(CLIPS_DIR, "clip_02.mp4")

mname, pnames, kills = parse_demo_kills(demo_path)
moments = cluster_moments(kills)
match = None
for m in moments:
    if m['killer_name'] == killer and abs(m['kills'][0]['time'] - approx_time) < 10.0:
        match = m
        break

if not match:
    print("ERROR: Match not found!")
    sys.exit(1)

fk = match['kills'][0]['time']
lk = match['kills'][-1]['time']
rec_start = max(1.0, fk - 0.9)
rec_end = lk + 0.9
rec_dur = rec_end - rec_start
num_frames = int(rec_dur * 30.0)
if num_frames > max_frames:
    rec_end = rec_start + (max_frames / 30.0)
    num_frames = max_frames

print(f"Rendering Clip 02: {match['map']} | {killer} | {rec_dur:.1f}s ({num_frames} frames)")

for f in glob.glob(os.path.join(CSTRIKE_DIR, 'vol3_frame*.bmp')):
    try: os.remove(f)
    except OSError: pass

dst_dem = os.path.join(CSTRIKE_DIR, 'render_clip.dem')
shutil.copy2(demo_path, dst_dem)

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
    *make_waits(90),
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
    "startmovie vol3_frame 30",
    *make_waits(num_frames + 25),
    "endmovie",
    *make_waits(10),
    "quit"
]

cfg_path = os.path.join(CSTRIKE_DIR, "render_vol3.cfg")
with open(cfg_path, "w", encoding="utf-8") as f:
    f.write("\n".join(cfg_lines) + "\n")

cmd = [
    HL_RECORDER,
    "-game", "cstrike",
    "-windowed", "-w", "1280", "-h", "720",
    "-novid",
    "+exec", "render_vol3.cfg"
]

t0 = time.time()
proc = subprocess.Popen(cmd, cwd=HL_DIR)
proc.wait(timeout=120)
print(f"Game finished in {time.time()-t0:.1f}s")

bmp_files = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'vol3_frame*.bmp')))
print(f"Dumped {len(bmp_files)} frames.")
if len(bmp_files) < 15:
    print("ERROR: Too few frames!")
    sys.exit(1)

cmd_enc = [
    FFMPEG_EXE, "-y",
    "-framerate", "30",
    "-i", os.path.join(CSTRIKE_DIR, "vol3_frame%05d.bmp"),
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "16",
    "-pix_fmt", "yuv420p",
    out_mp4
]
subprocess.run(cmd_enc, check=True, capture_output=True)
for f in bmp_files:
    try: os.remove(f)
    except OSError: pass

print(f"SUCCESS: Saved {out_mp4} ({os.path.getsize(out_mp4)/(1024*1024):.2f} MB)")
