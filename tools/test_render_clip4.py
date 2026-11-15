import os, sys, glob, shutil, subprocess, time

HL_DIR = r'D:\SteamLibrary\steamapps\common\Half-Life'
CSTRIKE_DIR = os.path.join(HL_DIR, 'cstrike')
HL_RECORDER = os.path.join(HL_DIR, 'hl_recorder.exe')
DEMO_PATH = r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611141954-zm_lb.dem'
OUT_MP4 = r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\clips_evilzomb\clip_04.mp4'

for f in glob.glob(os.path.join(CSTRIKE_DIR, 'clip_frame*.bmp')):
    try: os.remove(f)
    except OSError: pass

shutil.copy2(DEMO_PATH, os.path.join(CSTRIKE_DIR, 'render_clip.dem'))

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
    "dem_jump 933.1",
    *make_waits(260),
    "spec_autodirector 0",
    "spec_autodirector_internal 0",
    "spec_mode 4 0",
    "spec_mode_internal 4",
    *make_waits(20),
]

for _ in range(6):
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
    *make_waits(215),
    "endmovie",
    "quit"
])

cfg_path = os.path.join(CSTRIKE_DIR, 'render_clip.cfg')
with open(cfg_path, 'w') as f:
    f.write("\n".join(cfg_lines) + "\n")

print(f"Starting hl_recorder with cwd={HL_DIR}...")
t0 = time.time()
p = subprocess.Popen([
    HL_RECORDER,
    '-game', 'cstrike',
    '-windowed', '-w', '1280', '-h', '720',
    '-novid',
    '+exec', 'render_clip.cfg'
], cwd=HL_DIR)

try:
    p.wait(timeout=90)
    print(f"hl_recorder exited normally in {time.time()-t0:.1f}s")
except subprocess.TimeoutExpired:
    print(f"Timeout reached after {time.time()-t0:.1f}s! Killing...")
    p.kill()

bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'clip_frame*.bmp')))
print(f"Dumped {len(bmps)} frames.")
if bmps:
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg, '-y',
        '-framerate', '30',
        '-i', os.path.join(CSTRIKE_DIR, 'clip_frame%05d.bmp'),
        '-vf', 'eq=gamma=1.35:contrast=1.12:brightness=0.03',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '19',
        '-movflags', '+faststart',
        OUT_MP4
    ]
    subprocess.run(cmd, check=True)
    for f in bmps:
        try: os.remove(f)
        except OSError: pass
    print(f"[SUCCESS] Created {OUT_MP4}: {os.path.getsize(OUT_MP4)/1024/1024:.2f} MB")
