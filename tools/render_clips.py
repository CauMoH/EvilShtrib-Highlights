"""
Render Clips Pipeline for EvilShtrib-Highlights.
Automates CS 1.6 GoldSource demo rendering of top 10 moments and encodes into MP4 clips.
"""

import os
import sys
import glob
import shutil
import subprocess
import time
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from analyze_highlights import find_top_highlights

CSTRIKE_DIR = r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike'
HL_RECORDER = r'D:\SteamLibrary\steamapps\common\Half-Life\hl_recorder.exe'
DEMOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'demos')
CLIPS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clips')

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

def render_single_moment(moment, clip_num, total_clips):
    os.makedirs(CLIPS_DIR, exist_ok=True)
    out_mp4 = os.path.join(CLIPS_DIR, f"clip_{clip_num:02d}.mp4")
    
    print(f"\n=======================================================")
    print(f"RENDERING CLIP [{clip_num:02d}/{total_clips:02d}]: {os.path.basename(out_mp4)}")
    print(f"Map: {moment['map']} | Killer: {moment['killer_name']} (Slot #{moment['killer_id']})")
    print(f"Weapons: {', '.join(moment['weapons']).upper()} | Kills: {moment['num_kills']}")
    print(f"Demo Time: {moment['time_start']:.1f}s -> {moment['time_end']:.1f}s ({moment['duration']:.1f}s)")
    print(f"=======================================================")
    
    ensure_hl_recorder()
    clean_cstrike_artifacts()
    
    # 1. Copy demo to cstrike
    src_dem = os.path.join(DEMOS_DIR, moment['demo_file'])
    dst_dem = os.path.join(CSTRIKE_DIR, 'render_clip.dem')
    shutil.copy2(src_dem, dst_dem)
    
    # 2. Build rendering script
    num_frames = int(moment['duration'] * 30.0)
    cfg_path = os.path.join(CSTRIKE_DIR, 'render_clip.cfg')
    
    t_start = max(1.0, moment['time_start'])
    wait_jump_ticks = max(200, int(t_start * 0.75))
    
    # Build cycle commands to spectate killer_id in first person
    cycle_commands = []
    clicks = max(0, moment['killer_id'] - 1)
    for _ in range(clicks):
        cycle_commands.append("+attack")
        cycle_commands.append(";".join(["wait"] * 5))
        cycle_commands.append("-attack")
        cycle_commands.append(";".join(["wait"] * 25))
        
    script_lines = [
        "dem_forcehltv 1",
        "hud_saytext 1",
        "hud_deathnotice_time 6",
        "viewdemo render_clip",
        ";".join(["wait"] * 100),
        f"dem_jump {t_start:.1f}",
        ";".join(["wait"] * wait_jump_ticks),
        "spec_autodirector 0",
        "spec_autodirector_internal 0",
        "spec_mode 4 0",
        "spec_mode_internal 4",
        ";".join(["wait"] * 25),
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
        
    # 3. Launch CS 1.6 recorder
    t0 = time.time()
    proc = subprocess.Popen([
        HL_RECORDER,
        '-game', 'cstrike',
        '-windowed', '-w', '1280', '-h', '720',
        '-novid',
        '+exec', 'render_clip.cfg'
    ])
    
    seek_est = wait_jump_ticks / 30.0
    timeout_sec = max(45, int(moment['duration'] * 4 + seek_est * 2))
    try:
        proc.wait(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        print("  Process timeout reached, terminating...")
        proc.kill()
        
    t_render = time.time() - t0
    
    # 4. Collect frames
    bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'clip_frame*.bmp')))
    print(f"  Dumped {len(bmps)} frames in {t_render:.1f}s.")
    
    if not bmps:
        print(f"  [ERROR] No frames captured for clip {clip_num}!")
        clean_cstrike_artifacts()
        return None
        
    # Verify dynamic motion across frames
    if len(bmps) >= 60:
        f_start = cv2.imread(bmps[0])
        f_mid = cv2.imread(bmps[len(bmps)//2])
        f_end = cv2.imread(bmps[-1])
        motion_mid = float(np.mean(np.abs(f_start.astype(float) - f_mid.astype(float))))
        motion_end = float(np.mean(np.abs(f_mid.astype(float) - f_end.astype(float))))
        print(f"  Motion verification: start->mid delta={motion_mid:.2f}, mid->end delta={motion_end:.2f}")
        if motion_mid < 1.0 and motion_end < 1.0:
            print("  [WARNING] Low motion detected, clip might be paused!")
        
    # 5. Encode with FFmpeg (H.264 / avc1 + yuv420p + faststart for full Chrome/Web support)
    first_frame = cv2.imread(bmps[0])
    height, width, _ = first_frame.shape
    
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    input_pattern = os.path.join(CSTRIKE_DIR, 'clip_frame%05d.bmp')
    cmd = [
        ffmpeg_exe, '-y',
        '-framerate', '30',
        '-i', input_pattern,
        '-vf', 'eq=gamma=1.4:contrast=1.15:brightness=0.04',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-profile:v', 'main',
        '-crf', '20',
        '-movflags', '+faststart',
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    clean_cstrike_artifacts()
    
    file_size_mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"  [SUCCESS] {os.path.basename(out_mp4)} created: {len(bmps)} frames, {width}x{height}, {file_size_mb:.2f} MB!")
    
    moment['clip_file'] = os.path.basename(out_mp4)
    moment['video_frames'] = len(bmps)
    moment['video_size_mb'] = round(file_size_mb, 2)
    moment['resolution'] = f"{width}x{height}"
    return out_mp4

def render_all_top_highlights(count=10):
    highlights = find_top_highlights(count)
    results = []
    
    for idx, h in enumerate(highlights):
        clip_path = render_single_moment(h, idx + 1, len(highlights))
        if clip_path:
            results.append(h)
            
    print(f"\n=======================================================")
    print(f"ALL {len(results)} MP4 CLIPS SUCCESSFULLY RENDERED!")
    print(f"Folder: {CLIPS_DIR}")
    print(f"=======================================================")
    return results

if __name__ == '__main__':
    render_all_top_highlights(10)
