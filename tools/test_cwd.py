import os, shutil, subprocess, time

HL_DIR = r'D:\SteamLibrary\steamapps\common\Half-Life'
CSTRIKE_DIR = os.path.join(HL_DIR, 'cstrike')
HL_RECORDER = os.path.join(HL_DIR, 'hl_recorder.exe')
DEMO_SRC = r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611141954-zm_lb.dem'
DEMO_DST = os.path.join(CSTRIKE_DIR, 'render_clip.dem')

if os.path.exists(DEMO_DST):
    try: os.remove(DEMO_DST)
    except Exception as e: print("Remove error:", e)

shutil.copy2(DEMO_SRC, DEMO_DST)
print(f"Copied demo: {os.path.exists(DEMO_DST)}, size: {os.path.getsize(DEMO_DST)}")

with open(os.path.join(CSTRIKE_DIR, 'test_cwd.cfg'), 'w') as f:
    f.write('dem_forcehltv 1\nviewdemo render_clip\nwait;wait;wait;wait;wait\nquit\n')

p = subprocess.Popen([
    HL_RECORDER, '-game', 'cstrike', '-windowed', '-w', '640', '-h', '480', '-condebug', '+exec', 'test_cwd.cfg'
], cwd=HL_DIR)

p.wait(timeout=60)
print("Process exited with code:", p.returncode)
