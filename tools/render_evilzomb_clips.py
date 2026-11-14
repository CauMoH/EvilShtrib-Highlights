import os
import sys
import glob
import shutil
import subprocess
import time
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from select_10_demo_highlights import selected_moments

CSTRIKE_DIR = r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike'
HL_RECORDER = r'D:\SteamLibrary\steamapps\common\Half-Life\hl_recorder.exe'
DEMOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'demos')
CLIPS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clips_evilzomb')
os.makedirs(CLIPS_DIR, exist_ok=True)

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def ensure_hl_recorder():
    hl_exe = r'D:\SteamLibrary\steamapps\common\Half-Life\hl.exe'
    if not os.path.exists(HL_RECORDER) or os.path.getsize(HL_RECORDER) != os.path.getsize(hl_exe):
        shutil.copy2(hl_exe, HL_RECORDER)

def clean_cstrike_artifacts():
    for f in glob.glob(os.path.join(CSTRIKE_DIR, 'clip_frame*.bmp')):
        try: os.remove(f)
        except OSError: pass
    for f in [os.path.join(CSTRIKE_DIR, 'render_clip.dem'), os.path.join(CSTRIKE_DIR, 'render_clip.cfg')]:
        try: os.remove(f)
        except OSError: pass

def render_moment(moment, clip_idx, total_clips):
    out_mp4 = os.path.join(CLIPS_DIR, f"clip_{clip_idx:02d}.mp4")
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 100*1024:
        print(f"[{clip_idx:02d}/{total_clips:02d}] Already exists: {os.path.basename(out_mp4)}")
        return out_mp4
        
    print(f"\n=======================================================")
    print(f"RENDERING [{clip_idx:02d}/{total_clips:02d}]: {os.path.basename(out_mp4)}")
    print(f"Map: {moment['map']} | Killer: {moment['killer_name']} (Slot #{moment['killer_id']})")
    print(f"Weapons: {', '.join(moment['weapons']).upper()} | Kills: {moment['num_kills']}")
    print(f"Time: {moment['time_start']:.1f}s -> {moment['time_end']:.1f}s ({moment['duration']:.1f}s)")
    print(f"=======================================================")
    
    ensure_hl_recorder()
    clean_cstrike_artifacts()
    
    # Copy demo
    src_dem = moment['demo_file']
    if not os.path.isabs(src_dem):
        src_dem = os.path.join(DEMOS_DIR, src_dem)
    dst_dem = os.path.join(CSTRIKE_DIR, 'render_clip.dem')
    shutil.copy2(src_dem, dst_dem)
    
    num_frames = int(moment['duration'] * 30.0)
    cfg_path = os.path.join(CSTRIKE_DIR, 'render_clip.cfg')
    
    t_start = max(1.0, moment['time_start'])
    wait_jump_ticks = min(600, max(220, int(t_start * 0.35)))
    
    cycle_commands = []
    clicks = max(0, moment['killer_id'] - 1)
    for _ in range(clicks):
        cycle_commands.append("+attack")
        cycle_commands.append(";".join(["wait"] * 4))
        cycle_commands.append("-attack")
        cycle_commands.append(";".join(["wait"] * 15))
        
    script_lines = [
        "dem_forcehltv 1",
        "hud_saytext 1",
        "hud_deathnotice_time 6",
        "viewdemo render_clip",
        ";".join(["wait"] * 80),
        f"dem_jump {t_start:.1f}",
        ";".join(["wait"] * wait_jump_ticks),
        "spec_autodirector 0",
        "spec_autodirector_internal 0",
        "spec_mode 4 0",
        "spec_mode_internal 4",
        ";".join(["wait"] * 20),
        *cycle_commands,
        "dem_pause 0",
        "dem_speed 1.0",
        "gamma 4",
        "brightness 4",
        "host_framerate 0.03333333",
        "startmovie clip_frame 30",
        ";".join(["wait"] * num_frames),
        "endmovie",
        "quit"
    ]
    
    with open(cfg_path, 'w') as f:
        f.write("\n".join(script_lines) + "\n")
        
    t0 = time.time()
    proc = subprocess.Popen([
        HL_RECORDER,
        '-game', 'cstrike',
        '-windowed', '-w', '1280', '-h', '720',
        '-novid',
        '+exec', 'render_clip.cfg'
    ])
    
    timeout_sec = max(90, int(moment['duration'] * 5 + 60))
    try:
        proc.wait(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        print("  Timeout reached, killing...")
        proc.kill()
        
    t_render = time.time() - t0
    
    bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'clip_frame*.bmp')))
    print(f"  Dumped {len(bmps)} frames in {t_render:.1f}s.")
    
    if not bmps:
        print(f"  [ERROR] No frames captured for clip {clip_idx}!")
        clean_cstrike_artifacts()
        return None
        
    input_pattern = os.path.join(CSTRIKE_DIR, 'clip_frame%05d.bmp')
    cmd = [
        FFMPEG_EXE, '-y',
        '-framerate', '30',
        '-i', input_pattern,
        '-vf', 'eq=gamma=1.35:contrast=1.12:brightness=0.03',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-profile:v', 'main',
        '-crf', '19',
        '-movflags', '+faststart',
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    clean_cstrike_artifacts()
    
    mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"  [SUCCESS] {os.path.basename(out_mp4)}: {len(bmps)} frames ({mb:.2f} MB)")
    return out_mp4

def render_all():
    # If clip 1 already exists in clips/clip_01.mp4 from our test, copy it over
    src_c1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clips', 'clip_01.mp4')
    dst_c1 = os.path.join(CLIPS_DIR, 'clip_01.mp4')
    if os.path.exists(src_c1) and not os.path.exists(dst_c1):
        shutil.copy2(src_c1, dst_c1)
        
    for idx, m in enumerate(selected_moments, 1):
        render_moment(m, idx, len(selected_moments))
        
    print("\nALL 10 REAL SERVER CLIPS RENDERED!")

if __name__ == '__main__':
    render_all()
