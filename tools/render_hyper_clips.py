import os
import sys
import glob
import shutil
import subprocess
import time
import imageio_ffmpeg

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
DEMOS_DIR = os.path.join(BASE_DIR, "demos")
CLIPS_DIR = os.path.join(BASE_DIR, "clips_hyper")
os.makedirs(CLIPS_DIR, exist_ok=True)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

selected_moments_spec = [
    ("auto-2611142046-bio_ziger_azt.dem", "Player_21", 111.5, "5X MULTI-KILL SPREE", "FAMAS, GRENADE & DEAGLE", "5X COMBO", 1),
    ("auto-2611141907-zm_biohazard_base_mx004.dem", "Player_10", 298.8, "TRIPLE HEADSHOT", "UMP45 RAPID HEADSHOTS", "3X HEADSHOT", 2),
    ("auto-2611142112-bio_talka.dem", "Player_21", 532.2, "GALIL HEADSHOT STREAK", "IDF GALIL PRECISION SPRAY", "TRIPLE KILL", 3),
    ("auto-2611141820-bio_snow_na2.dem", "Player_22", 818.8, "M4A1 TRIPLE SPRAY", "M4A1 POINT-BLANK SPRAY", "TRIPLE KILL", 4),
    ("auto-2611142343-bio_oldhouse.dem", "Player_8", 1127.5, "DOUBLE TAP HEADSHOT", "M4A1 CARBINE DOUBLE", "DOUBLE HS", 5),
    ("auto-2611142138-bio_arena_fl.dem", "Player_21", 604.9, "INSTANT DOUBLE HEADSHOT", "M4A1 SILENCED HEADSHOTS", "DOUBLE HS", 6),
    ("auto-2611141820-bio_snow_na2.dem", "Player_15", 1468.3, "CLUSTER BOMB TRIPLE", "HE GRENADE WIPEOUT", "3X GRENADE", 7),
    ("auto-2611142046-bio_ziger_azt.dem", "Player_2", 194.1, "QUAD GRENADE BARRAGE", "HE GRENADES INVASION STOP", "4X GRENADE", 8),
    ("auto-2611141907-zm_biohazard_base_mx004.dem", "Player_6", 1038.9, "GALIL SURVIVOR DEFENSE", "IDF GALIL HEADSHOT DEFENSE", "TRIPLE HS", 9),
    ("auto-2611142020-bio_valak.dem", "Player_21", 996.9, "TACTICAL COMBO TRIPLE", "UMP45, GRENADE & USP", "TRIPLE KILL", 10),
    ("auto-2611142207-zm_restart_v3.dem", "Player_12", 753.5, "M4A1 ASSAULT DEFENSE", "M4A1 CARVED HEADSHOTS", "TRIPLE KILL", 11),
    ("auto-2611142258-zm_2day_rbt_f4.dem", "Player_1", 614.6, "XM1014 SHOTGUN DOUBLE", "XM1014 AUTO-SHOTGUN PUMP", "DOUBLE HS", 12),
]

def make_waits(n):
    lines = []
    while n > 0:
        batch = min(20, n)
        lines.append(";".join(["wait"] * batch))
        n -= batch
    return lines

def clean_artifacts():
    for f in glob.glob(os.path.join(CSTRIKE_DIR, 'hyper_frame*.bmp')):
        try: os.remove(f)
        except OSError: pass

def render_clip(demo_file, killer, approx_time, title, wpn_label, tag, fx_id, idx, total):
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
        print(f"[{idx:02d}/{total:02d}] ERROR: Could not find moment for {killer} in {demo_file}")
        return None
        
    fk = match['kills'][0]['time']
    lk = match['kills'][-1]['time']
    rec_start = max(1.0, fk - 0.9)
    rec_end = lk + 0.9
    rec_dur = rec_end - rec_start
    num_frames = int(rec_dur * 30.0)
    
    print(f"\n=======================================================")
    print(f"RENDERING [{idx:02d}/{total:02d}]: {os.path.basename(out_mp4)}")
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
        "host_framerate 0.03333333",
        "startmovie hyper_frame 30",
        *make_waits(num_frames),
        "endmovie",
        "quit"
    ]
    
    cfg_path = os.path.join(CSTRIKE_DIR, 'render_clip.cfg')
    with open(cfg_path, 'w') as f:
        f.write("\n".join(cfg_lines) + "\n")
        
    t0 = time.time()
    p = subprocess.Popen([
        HL_RECORDER,
        '-game', 'cstrike',
        '-windowed', '-w', '1280', '-h', '720',
        '-novid',
        '+exec', 'render_clip.cfg'
    ], cwd=HL_DIR)
    
    timeout_sec = max(60, int(rec_dur * 4 + 45))
    try:
        p.wait(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        print("  Timeout reached, killing...")
        p.kill()
        
    bmps = sorted(glob.glob(os.path.join(CSTRIKE_DIR, 'hyper_frame*.bmp')))
    print(f"  Dumped {len(bmps)} frames in {time.time()-t0:.1f}s.")
    
    if not bmps:
        print(f"  [ERROR] No frames captured for clip {idx}!")
        clean_artifacts()
        return None
        
    cmd = [
        FFMPEG_EXE, '-y',
        '-framerate', '30',
        '-i', os.path.join(CSTRIKE_DIR, 'hyper_frame%05d.bmp'),
        '-vf', 'eq=gamma=1.35:contrast=1.12:brightness=0.03',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '18',
        '-movflags', '+faststart',
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    clean_artifacts()
    
    mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"  [SUCCESS] {os.path.basename(out_mp4)}: {len(bmps)} frames ({mb:.2f} MB)")
    return out_mp4

def render_all():
    total = len(selected_moments_spec)
    for idx, (dem, killer, approx_time, title, wpn, tag, fx) in enumerate(selected_moments_spec, 1):
        render_clip(dem, killer, approx_time, title, wpn, tag, fx, idx, total)
    print("\nALL 12 HYPER-ACTION CLIPS RENDERED!")

if __name__ == "__main__":
    render_all()
