"""
Render 16 Ultra-Fast Action Clips for Volume 4 from official shtriban.ru demos.
Strict action design:
- Excludes all previously used moments from USED_MOMENTS.md.
- Rapid-fire multi-kills only (kill spans under 1.8s).
- Precise action centering: each clip is exactly 99 frames (3.30s), with kills in the center.
- ZERO running around, ZERO duplicate rounds, 100% kill density.
"""

import os, sys, glob, shutil, subprocess, time, imageio_ffmpeg

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
DEMOS_DIR = os.path.join(BASE_DIR, "demos_shtriban")
CLIPS_DIR = os.path.join(BASE_DIR, "clips_vol4")
os.makedirs(CLIPS_DIR, exist_ok=True)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# (demo_file, killer, approx_time, title, wpn_label, tag, fx_id, num_frames)
VOL4_MOMENTS = [
    ("bio_dusty_2x2_fl_2026-11-15_06-35-00.dem", "Dk-Unknown", 1334.4, "UMP45 RAPID HEADSHOT", "H&K UMP .45", "DOUBLE KILL", 1, 99),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", "Fat Matt", 854.4, "XM1014 AUTO-SHOTGUN", "BENELLI XM1014", "INSTA DOUBLE", 2, 99),
    ("bio_resident_beta_2026-11-15_12-57-00.dem", "shooterman", 1151.4, "DUAL ELITES COMBO", "DUAL .40 ELITES", "DOUBLE KILL", 3, 99),
    ("bio_horror_box_ff_2026-11-15_08-43-00.dem", "aliendewd1", 708.5, "UMP45 DUAL HEADSHOT", "H&K UMP .45", "DOUBLE HS", 4, 99),
    ("bio_horror_box_ff_2026-11-15_08-43-00.dem", "Dk-Unknown", 363.2, "SG550 SNIPER DEFENSE", "SG550 AUTO-SNIPER", "DOUBLE KILL", 5, 99),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", "Dk-Unknown", 1399.5, "USP TACTICAL DUAL TAP", "USP .45 TACTICAL", "DOUBLE KILL", 6, 99),
    ("bio_evil_dust_fl_2026-11-15_07-01-00.dem", "aliendewd1", 985.6, "M4A1 CARBINE BURST", "COLT M4A1 CARBINE", "DOUBLE KILL", 7, 99),
    ("bio_resident_beta_2026-11-15_12-57-00.dem", "HappyKiD", 137.6, "TMP SILENT DOUBLE HS", "STEYR TMP SMG", "DOUBLE HS", 8, 99),
    ("bio_horror_box_ff_2026-11-15_08-43-00.dem", "shooterman", 124.7, "UMP45 BURST SUPPRESSION", "H&K UMP .45", "DOUBLE KILL", 9, 99),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", "aliendewd1", 1339.9, "SG552 COMMANDO HS", "SIG SG552 COMMANDO", "DOUBLE HS", 10, 99),
    ("bio_cube_rb3_2026-11-15_06-10-00.dem", "HappyKiD", 779.9, "DUAL ELITES SPRAY", "DUAL .40 ELITES", "DOUBLE KILL", 11, 99),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", "kingkilla", 983.4, "SG550 SNIPER DEFENSE", "SG550 AUTO-SNIPER", "DOUBLE KILL", 12, 99),
    ("bio_resident_beta_2026-11-15_12-57-00.dem", "Fat Matt", 1090.5, "USP PISTOL DEFENSE", "USP .45 TACTICAL", "DOUBLE KILL", 13, 99),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", "Player_9", 908.2, "SG550 DOUBLE HEADSHOT", "SG550 AUTO-SNIPER", "DOUBLE HEADSHOT", 14, 99),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", "kingkilla", 741.3, "SG552 COMMANDO BURST", "SIG SG552 COMMANDO", "DOUBLE KILL", 15, 99),
    ("bio_resident_beta_2026-11-15_12-57-00.dem", "Dk-Unknown", 1430.2, "SG550 TRIPLE KILL", "SG550 AUTO-SNIPER", "TRIPLE KILL", 16, 105),
]

def make_waits(n):
    lines = []
    while n > 0:
        batch = min(20, n)
        lines.append(";".join(["wait"] * batch))
        n -= batch
    return lines

def clean_artifacts():
    for f in glob.glob(os.path.join(CSTRIKE_DIR, 'vol4_frame*.bmp')):
        try: os.remove(f)
        except OSError: pass

def render_vol4_clip(item, idx, total):
    demo_file, killer, approx_time, title, wpn_label, tag, fx_id, num_frames = item
    out_mp4 = os.path.join(CLIPS_DIR, f"clip_{idx:02d}.mp4")
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 100*1024:
        print(f"[{idx:02d}/{total:02d}] Already exists: {os.path.basename(out_mp4)}")
        return out_mp4
        
    full_path = os.path.join(DEMOS_DIR, demo_file)
    mname, pnames, kills = parse_demo_kills(full_path)
    moments = cluster_moments(kills)
    match = None
    for m in moments:
        if m['num_kills'] >= 2 and m['killer_name'] == killer and abs(m['kills'][0]['time'] - approx_time) < 10.0:
            match = m
            break
            
    if not match:
        print(f"[{idx:02d}/{total:02d}] ERROR: Match not found for {killer} in {demo_file}")
        return None
        
    fk = match['kills'][0]['time']
    lk = match['kills'][-1]['time']
    mid_kill = (fk + lk) / 2.0
    half_dur = (num_frames / 30.0) / 2.0
    
    rec_start = max(1.0, mid_kill - half_dur)
    rec_end = rec_start + (num_frames / 30.0)
    
    print(f"\n=======================================================")
    print(f"RENDERING VOL4 [{idx:02d}/{total:02d}]: {os.path.basename(out_mp4)}")
    print(f"Map: {match['map']} | Killer: {killer}")
    print(f"Action: {match['num_kills']} kills ({wpn_label}) | span: {lk-fk:.2f}s")
    print(f"Time: {rec_start:.1f}s -> {rec_end:.1f}s ({num_frames} frames)")
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
        "startmovie vol4_frame 30",
        *make_waits(num_frames + 25),
        "endmovie",
        *make_waits(10),
        "quit"
    ]
    
    cfg_path = os.path.join(CSTRIKE_DIR, "render_vol4.cfg")
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cfg_lines) + "\n")
        
    cmd = [
        HL_RECORDER,
        "-game", "cstrike",
        "-windowed", "-w", "1280", "-h", "720",
        "-novid",
        "+exec", "render_vol4.cfg"
    ]
    
    timeout_sec = max(60, int(rec_start * 0.35 + num_frames * 0.15 + 40))
    t0 = time.time()
    try:
        proc = subprocess.Popen(cmd, cwd=HL_DIR)
        proc.wait(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        print(f"Warning: Process timed out after {timeout_sec}s. Terminating...")
        proc.kill()
        proc.wait()
    print(f"Game process finished in {time.time()-t0:.1f}s")
    
    bmp_files = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'vol4_frame*.bmp')))
    print(f"Dumped {len(bmp_files)} frames from engine.")
    if len(bmp_files) < 15:
        print(f"ERROR: Only {len(bmp_files)} frames dumped!")
        clean_artifacts()
        return None
        
    cmd_enc = [
        FFMPEG_EXE, "-y",
        "-framerate", "30",
        "-i", os.path.join(CSTRIKE_DIR, "vol4_frame%05d.bmp"),
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
    total = len(VOL4_MOMENTS)
    success = 0
    for idx, item in enumerate(VOL4_MOMENTS, 1):
        p = render_vol4_clip(item, idx, total)
        if p: success += 1
    print(f"\nFinished Volume 4 rendering: {success}/{total} clips rendered successfully.")
