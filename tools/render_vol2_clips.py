"""
Render 12 Hyper-Action clips for Volume 2 from server shtriban.ru demos.
"""
import os, sys, glob, shutil, subprocess, time, imageio_ffmpeg

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
DEMOS_DIR = os.path.join(BASE_DIR, "demos_shtriban")
CLIPS_DIR = os.path.join(BASE_DIR, "clips_vol2")
os.makedirs(CLIPS_DIR, exist_ok=True)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

VOL2_MOMENTS = [
    # (demo_file, killer, approx_time, title, wpn_label, tag, fx_id, max_frames)
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", "Dk-Unknown", 153.4, "3X AK-47 TRIPLE", "AK-47 KALASHNIKOV SPRAY", "3X COMBO", 1, 160),
    ("bio_dusty_2x2_fl_2026-11-15_06-35-00.dem", "pyr0`", 176.2, "SG552 COMMAND DOUBLE", "SG552 COMMANDO HEADSHOTS", "DOUBLE HS", 2, 85),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", "Galdalfus", 854.0, "AK-47 RAPID DOUBLE", "AK-47 RIFLE DOUBLE TAP", "DOUBLE HS", 3, 110),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", "Dk-Unknown", 308.0, "GALIL SURVIVOR DEFENSE", "IDF GALIL HEADSHOT BURST", "DOUBLE HS", 4, 110),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", "aliendewd1", 1045.5, "FAMAS BURST DOUBLE", "FAMAS CLARION 3-ROUND", "DOUBLE HS", 5, 90),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", "kingkilla", 681.3, "DEAGLE CANNON DOUBLE", "DESERT EAGLE .50 ACTION", "DOUBLE KILL", 6, 120),
    ("bio_cube_rb3_2026-11-15_06-10-00.dem", "HappyKiD", 1253.6, "UMP45 POINT-BLANK", "UMP45 RAPID HEADSHOTS", "DOUBLE HS", 7, 90),
    ("bio_monument_2026-11-15_11-15-00.dem", "HappyKiD", 40.3, "AK-47 INSTANT DOUBLE", "AK-47 POINT-BLANK SPRAY", "DOUBLE KILL", 8, 80),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", "pyr0`", 301.9, "M249 SAW SUPPRESSION", "M249 HEAVY MACHINEGUN", "DOUBLE HS", 9, 150),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", "Player_9", 106.8, "M249 SAW SUPPRESSION", "M249 5.56 PARA MACHINEGUN", "DOUBLE KILL", 10, 110),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", "Fat Matt", 172.9, "SG550 SNIPER DEFENSE", "SG550 SNIPER + P228", "DOUBLE HS", 1, 170),
    ("bio_dusty_2x2_fl_2026-11-15_06-35-00.dem", "Dk-Unknown", 387.2, "STEYR AUG BULLPUP", "STEYR AUG ASSAULT RIFLE", "DOUBLE KILL", 4, 110),
]

def make_waits(n):
    lines = []
    while n > 0:
        batch = min(20, n)
        lines.append(";".join(["wait"] * batch))
        n -= batch
    return lines

def clean_artifacts():
    for f in glob.glob(os.path.join(CSTRIKE_DIR, 'vol2_frame*.bmp')):
        try: os.remove(f)
        except OSError: pass

def render_vol2_clip(item, idx, total):
    demo_file, killer, approx_time, title, wpn_label, tag, fx_id, max_frames = item
    out_mp4 = os.path.join(CLIPS_DIR, f"clip_{idx:02d}.mp4")
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 100*1024:
        print(f"[{idx:02d}/{total:02d}] Already exists: {os.path.basename(out_mp4)}")
        return out_mp4
        
    full_path = os.path.join(DEMOS_DIR, demo_file)
    mname, pnames, kills = parse_demo_kills(full_path)
    moments = cluster_moments(kills)
    match = None
    for m in moments:
        if m['killer_name'] == killer and abs(m['kills'][0]['time'] - approx_time) < 10.0:
            match = m
            break
            
    if not match:
        print(f"[{idx:02d}/{total:02d}] ERROR: Match not found for {killer} in {demo_file}")
        return None
        
    fk = match['kills'][0]['time']
    lk = match['kills'][-1]['time']
    rec_start = max(1.0, fk - 0.9)
    rec_end = lk + 0.9
    rec_dur = rec_end - rec_start
    num_frames = int(rec_dur * 30.0)
    if num_frames > max_frames:
        rec_end = rec_start + (max_frames / 30.0)
        num_frames = max_frames
        
    print(f"\n=======================================================")
    print(f"RENDERING VOL2 [{idx:02d}/{total:02d}]: {os.path.basename(out_mp4)}")
    print(f"Map: {match['map']} | Killer: {killer}")
    print(f"Action: {match['num_kills']} kills ({wpn_label})")
    print(f"Time: {rec_start:.1f}s -> {rec_end:.1f}s ({rec_dur:.1f}s, {num_frames} frames)")
    print(f"=======================================================")
    
    clean_artifacts()
    dst_dem = os.path.join(CSTRIKE_DIR, 'render_clip.dem')
    shutil.copy2(full_path, dst_dem)
    
    wait_jump = min(350, max(180, int(rec_start * 0.22)))
    
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
        "startmovie vol2_frame 30",
        *make_waits(num_frames + 25),
        "endmovie",
        *make_waits(10),
        "quit"
    ]
    
    cfg_path = os.path.join(CSTRIKE_DIR, "render_vol2.cfg")
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cfg_lines) + "\n")
        
    cmd = [
        HL_RECORDER,
        "-game", "cstrike",
        "-windowed", "-w", "1280", "-h", "720",
        "-novid",
        "+exec", "render_vol2.cfg"
    ]
    
    timeout_sec = max(45, int(rec_dur * 4 + 35))
    t0 = time.time()
    try:
        proc = subprocess.Popen(cmd, cwd=HL_DIR)
        proc.wait(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        print(f"Warning: Process timed out after {timeout_sec}s. Terminating...")
        proc.kill()
        proc.wait()
    print(f"Game process finished in {time.time()-t0:.1f}s")
    
    bmp_files = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'vol2_frame*.bmp')))
    print(f"Dumped {len(bmp_files)} frames from engine.")
    if len(bmp_files) < 15:
        print(f"ERROR: Only {len(bmp_files)} frames dumped!")
        clean_artifacts()
        return None
        
    cmd_enc = [
        FFMPEG_EXE, "-y",
        "-framerate", "30",
        "-i", os.path.join(CSTRIKE_DIR, "vol2_frame%05d.bmp"),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        out_mp4
    ]
    subprocess.run(cmd_enc, check=True, capture_output=True)
    clean_artifacts()
    print(f"SUCCESS: Saved {out_mp4} ({os.path.getsize(out_mp4)/(1024*1024):.2f} MB)")
    return out_mp4

if __name__ == "__main__":
    total = len(VOL2_MOMENTS)
    success = 0
    for idx, item in enumerate(VOL2_MOMENTS, 1):
        p = render_vol2_clip(item, idx, total)
        if p: success += 1
    print(f"\nFinished Volume 2 rendering: {success}/{total} clips rendered successfully.")
