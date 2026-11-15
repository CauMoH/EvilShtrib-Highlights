import os, shutil, subprocess, glob, time, cv2

HL_DIR = r'D:\SteamLibrary\steamapps\common\Half-Life'
CSTRIKE_DIR = os.path.join(HL_DIR, 'cstrike')
HL_RECORDER = os.path.join(HL_DIR, 'hl_recorder.exe')

for f in glob.glob(os.path.join(CSTRIKE_DIR, 'test_frame*.bmp')):
    try: os.remove(f)
    except OSError: pass

shutil.copy2(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611141907-zm_biohazard_base_mx004.dem', os.path.join(CSTRIKE_DIR, 'render_clip.dem'))

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
    "dem_jump 1037.0",
    *make_waits(260),
    'follow "Player_6"',
    "spec_mode 4 0",
    "spec_mode_internal 4",
    *make_waits(20),
    "dem_pause 0",
    "dem_speed 1.0",
    "gamma 4",
    "brightness 4",
    "host_framerate 0.03333333",
    "startmovie test_frame 30",
    *make_waits(90),
    "endmovie",
    "quit"
]

with open(os.path.join(CSTRIKE_DIR, 'test_follow.cfg'), 'w') as f:
    f.write("\n".join(cfg_lines) + "\n")

p = subprocess.Popen([
    HL_RECORDER, '-game', 'cstrike', '-windowed', '-w', '1280', '-h', '720', '-novid', '+exec', 'test_follow.cfg'
], cwd=HL_DIR)

p.wait(timeout=60)
bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'test_frame*.bmp')))
print(f"Dumped {len(bmps)} test frames.")

if bmps:
    # Save frame 30 and frame 60
    img30 = cv2.imread(bmps[min(30, len(bmps)-1)])
    img60 = cv2.imread(bmps[min(60, len(bmps)-1)])
    cv2.imwrite(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\test_follow_30.jpg', img30)
    cv2.imwrite(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\test_follow_60.jpg', img60)
    h, w = img30.shape[:2]
    wpn30 = img30[int(h*0.5):, int(w*0.5):]
    print(f"Frame 30 mean: {img30.mean():.1f}, wpn mean: {wpn30.mean():.1f}, wpn std: {wpn30.std():.1f}")
    for f in bmps:
        try: os.remove(f)
        except OSError: pass
