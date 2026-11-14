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
    
    script_lines = [
        "dem_forcehltv 1",
        "hud_saytext 1",
        "hud_deathnotice_time 6",
        "viewdemo render_clip",
        ";".join(["wait"] * 30),
        f"dem_jump {moment['time_start']:.1f}",
        ";".join(["wait"] * 15),
        f"trackplayer {moment['killer_id']}",
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
    
    timeout_sec = max(30, int(moment['duration'] * 4))
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
