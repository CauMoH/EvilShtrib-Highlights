import os, sys, gzip, urllib.request, shutil, subprocess, time, glob

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments
import imageio_ffmpeg

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos"
HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
OUT_MP4 = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\clips_evilzomb\clip_04.mp4"
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

url = "https://gs13.myarena.pro/getzipdemo.php?hid=2155&dem=cstrike/auto-2611142258-zm_2day_rbt_f4.dem"
dem_name = "auto-2611142258-zm_2day_rbt_f4.dem"
dem_path = os.path.join(DEMOS_DIR, dem_name)

if not os.path.exists(dem_path) or os.path.getsize(dem_path) < 1024*1024:
    print(f"Downloading {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = gzip.decompress(resp.read())
    with open(dem_path, 'wb') as f:
        f.write(data)
    print(f"Downloaded and decompressed {dem_name}: {len(data)/(1024*1024):.1f} MB")

mname, pnames, kills = parse_demo_kills(dem_path)
candidates = cluster_moments(kills)
if not candidates:
    print("No moments found!")
    sys.exit(1)

candidates.sort(key=lambda x: -x['score'])
best = candidates[0]
w_str = ", ".join(best['weapons']).upper()
print(f"Selected Moment: Map={best['map']} | Killer={best['killer_name']} (Slot #{best['killer_id']}) | Kills={best['num_kills']} ({w_str}) | Score={best['score']}")
print(f"Time: {best['time_start']:.1f}s -> {best['time_end']:.1f}s ({best['duration']:.1f}s)")

# Clean artifacts
for f in glob.glob(os.path.join(CSTRIKE_DIR, 'clip_frame*.bmp')):
    try: os.remove(f)
    except OSError: pass

shutil.copy2(dem_path, os.path.join(CSTRIKE_DIR, 'render_clip.dem'))

def make_waits(n):
    lines = []
    while n > 0:
        batch = min(20, n)
        lines.append(";".join(["wait"] * batch))
        n -= batch
    return lines

t_start = max(1.0, best['time_start'])
wait_jump = min(350, max(180, int(t_start * 0.25)))
num_frames = int(best['duration'] * 30.0)

cfg_lines = [
    "dem_forcehltv 1",
    "hud_saytext 1",
    "hud_deathnotice_time 6",
    "viewdemo render_clip",
    *make_waits(80),
    f"dem_jump {t_start:.1f}",
    *make_waits(wait_jump),
    "spec_autodirector 0",
    "spec_autodirector_internal 0",
    "spec_mode 4 0",
    "spec_mode_internal 4",
    *make_waits(20),
]

clicks = max(0, best['killer_id'] - 1)
for _ in range(clicks):
    cfg_lines.append("+attack")
    cfg_lines.extend(make_waits(4))
    cfg_lines.append("-attack")
    cfg_lines.extend(make_waits(15))

cfg_lines.extend([
    "dem_pause 0",
    "dem_speed 1.0",
    "gamma 4",
    "brightness 4",
    "host_framerate 0.03333333",
    "startmovie clip_frame 30",
    *make_waits(num_frames),
    "endmovie",
    "quit"
])

cfg_path = os.path.join(CSTRIKE_DIR, 'render_clip.cfg')
with open(cfg_path, 'w') as f:
    f.write("\n".join(cfg_lines) + "\n")

print(f"Wrote cfg. Launching hl_recorder (cwd={HL_DIR})...")
t0 = time.time()
p = subprocess.Popen([
    HL_RECORDER,
    '-game', 'cstrike',
    '-windowed', '-w', '1280', '-h', '720',
    '-novid',
    '+exec', 'render_clip.cfg'
], cwd=HL_DIR)

timeout_sec = max(60, int(best['duration'] * 4 + 40))
try:
    p.wait(timeout=timeout_sec)
    print(f"hl_recorder exited in {time.time()-t0:.1f}s.")
except subprocess.TimeoutExpired:
    print(f"Timeout {timeout_sec}s reached! Killing...")
    p.kill()

bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'clip_frame*.bmp')))
print(f"Dumped {len(bmps)} frames.")
if bmps:
    cmd = [
        FFMPEG_EXE, '-y',
        '-framerate', '30',
        '-i', os.path.join(CSTRIKE_DIR, 'clip_frame%05d.bmp'),
        '-vf', 'eq=gamma=1.35:contrast=1.12:brightness=0.03',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '19',
        '-movflags', '+faststart',
        OUT_MP4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    for f in bmps:
        try: os.remove(f)
        except OSError: pass
    print(f"[SUCCESS] {OUT_MP4}: {len(bmps)} frames ({os.path.getsize(OUT_MP4)/(1024*1024):.2f} MB)")
