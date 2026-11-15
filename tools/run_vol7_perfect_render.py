import os, sys, shutil, subprocess, time, json, cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
CLIPS_DIR = os.path.join(BASE_DIR, "clips_vol7")
FINAL_DIR = os.path.join(BASE_DIR, "final_videos")
os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/verdana.ttf"
font12 = ImageFont.truetype(FONT_PATH, 12)

def make_waits(n):
    lines = []
    while n > 0:
        b = min(20, n)
        lines.append(";".join(["wait"] * b))
        n -= b
    return lines

def render_name_tpl(name):
    img = Image.new("L", (250, 25), 0)
    d = ImageDraw.Draw(img)
    d.text((0, 0), name, fill=255, font=font12)
    arr = np.array(img)
    ys, xs = np.where(arr > 80)
    if len(ys) == 0: return None
    return arr[ys.min():ys.max()+1, xs.min():xs.max()+1]

def clean_cstrike():
    for f in os.listdir(CSTRIKE_DIR):
        if f.endswith(".bmp") or f.endswith(".tga"):
            try: os.remove(os.path.join(CSTRIKE_DIR, f))
            except OSError: pass

def probe_killer_cycle(demo_path, t_jump, killer_name, max_cycles=14):
    clean_cstrike()
    shutil.copy2(demo_path, os.path.join(CSTRIKE_DIR, "probe_dem.dem"))
    
    cfg = [
        "dem_forcehltv 1",
        "spec_autodirector 0",
        "viewdemo probe_dem",
        *make_waits(100),
        "dem_pause 1",
        f"dem_jump {t_jump:.1f}",
        *make_waits(int(t_jump * 2.2) + 120),
        "dem_pause 0",
        "dem_speed 1.0",
        "spec_mode 4 0",
        *make_waits(5),
        "snapshot" # Cycle 0
    ]
    for c in range(1, max_cycles):
        cfg.extend([
            "+attack",
            *make_waits(5),
            "-attack",
            *make_waits(5),
            "spec_mode 4 0",
            *make_waits(5),
            "snapshot"
        ])
    cfg.append("quit")
    
    with open(os.path.join(CSTRIKE_DIR, "probe_vol7.cfg"), "w") as f:
        f.write("\n".join(cfg) + "\n")
        
    timeout = max(30, int(t_jump * 0.12) + 25)
    print(f"  [Probe] Searching cycle for '{killer_name}' at {t_jump:.1f}s...", flush=True)
    subprocess.run([
        HL_RECORDER, "-game", "cstrike", "-windowed", "-w", "1280", "-h", "720",
        "-novid", "+exec", "probe_vol7.cfg"
    ], cwd=HL_DIR, timeout=timeout)
    
    snaps = sorted([f for f in os.listdir(CSTRIKE_DIR) if (f.endswith(".bmp") or f.endswith(".tga")) and not f.startswith("vol7_")])
    tpl = render_name_tpl(killer_name)
    best_c = 0
    best_score = -1.0
    best_ct = 0
    
    # First priority: CT players matching killer name
    ct_candidates = []
    for idx, s in enumerate(snaps):
        p = os.path.join(CSTRIKE_DIR, s)
        img = cv2.imread(p)
        if img is None: continue
        h, w = img.shape[:2]
        crop = img[int(h*0.91):int(h*0.98), int(w*0.35):int(w*0.65)]
        b, g, r = crop[:,:,0], crop[:,:,1], crop[:,:,2]
        cyan_mask = ((b > 130) & (g > 130) & (r < 155)).astype(np.uint8) * 255
        ct_p = int((cyan_mask > 0).sum())
        
        score = 0.0
        if tpl is not None and ct_p > 40:
            res = cv2.matchTemplate(cyan_mask, tpl, cv2.TM_CCOEFF_NORMED)
            score = float(res.max())
            ct_candidates.append((idx, score, ct_p))
            
        print(f"    Cycle {idx:02d}: CT={ct_p:3d}, Match={score:.3f}", flush=True)
        
    if ct_candidates:
        ct_candidates.sort(key=lambda x: x[1], reverse=True)
        best_c, best_score, best_ct = ct_candidates[0]
    else:
        # Fallback to any CT cycle
        for idx, s in enumerate(snaps):
            p = os.path.join(CSTRIKE_DIR, s)
            img = cv2.imread(p)
            if img is None: continue
            h, w = img.shape[:2]
            crop = img[int(h*0.91):int(h*0.98), int(w*0.35):int(w*0.65)]
            b, g, r = crop[:,:,0], crop[:,:,1], crop[:,:,2]
            cyan_mask = ((b > 130) & (g > 130) & (r < 155)).astype(np.uint8) * 255
            ct_p = int((cyan_mask > 0).sum())
            if ct_p > best_ct:
                best_ct = ct_p
                best_c = idx
                best_score = 0.1
                
    clean_cstrike()
    try: os.remove(os.path.join(CSTRIKE_DIR, "probe_dem.dem"))
    except OSError: pass
    
    print(f"  [Probe Result] Selected Cycle {best_c} (Score={best_score:.3f}, CT={best_ct})", flush=True)
    return best_c, best_score

def render_clip(cand, clip_idx, num_frames, cycle_count):
    demo_path = cand['full_path']
    t_kill = cand['time']
    lead_in = (num_frames / 30.0) * 0.42
    t_start = max(1.0, t_kill - lead_in)
    
    clean_cstrike()
    shutil.copy2(demo_path, os.path.join(CSTRIKE_DIR, "render_v7.dem"))
    
    cycle_cmds = []
    for _ in range(cycle_count):
        cycle_cmds.extend(["+attack", *make_waits(5), "-attack", *make_waits(5)])
    cycle_cmds.extend(["spec_mode 4 0", *make_waits(5)])
    
    wait_jump = int(t_start * 2.2) + 120
    pfx = f"v7_c{clip_idx:02d}_frame"
    
    cfg = [
        "dem_forcehltv 1",
        "spec_autodirector 0",
        "hud_saytext 1",
        "hud_deathnotice_time 6",
        "viewdemo render_v7",
        *make_waits(100),
        "dem_pause 1",
        f"dem_jump {t_start:.1f}",
        *make_waits(wait_jump),
        "dem_pause 0",
        "dem_speed 1.0",
        *cycle_cmds,
        "host_framerate 0.03333333333",
        f"startmovie {pfx} 30",
        *make_waits(num_frames + 15),
        "endmovie",
        "host_framerate 0",
        "quit"
    ]
    with open(os.path.join(CSTRIKE_DIR, "exec_v7.cfg"), "w") as f:
        f.write("\n".join(cfg) + "\n")
        
    timeout = max(40, int(t_start * 0.12) + int(num_frames * 0.4) + 30)
    print(f"  [Render] Recording {num_frames} frames from {t_start:.1f}s...", flush=True)
    subprocess.run([
        HL_RECORDER, "-game", "cstrike", "-windowed", "-w", "1280", "-h", "720",
        "-novid", "+exec", "exec_v7.cfg"
    ], cwd=HL_DIR, timeout=timeout)
    
    frames = sorted([f for f in os.listdir(CSTRIKE_DIR) if f.startswith(pfx) and (f.endswith(".bmp") or f.endswith(".tga"))])
    print(f"  [Render] Captured {len(frames)} frames (target: {num_frames})", flush=True)
    if len(frames) < num_frames:
        print(f"  [ERROR] Not enough frames captured!", flush=True)
        return False, None
        
    # Check middle frame Quality Gate
    mid_p = os.path.join(CSTRIKE_DIR, frames[len(frames)//2])
    mid_img = cv2.imread(mid_p)
    if mid_img is not None:
        h, w = mid_img.shape[:2]
        crop = mid_img[int(h*0.91):int(h*0.98), int(w*0.35):int(w*0.65)]
        b, g, r = crop[:,:,0], crop[:,:,1], crop[:,:,2]
        ct_p = int(((b > 130) & (g > 130) & (r < 155)).sum())
        t_p = int(((r > 160) & (g < 80) & (b < 80)).sum())
        print(f"  [Quality Gate] Mid-frame: CT={ct_p}, T(Zombie)={t_p}", flush=True)
        
    out_mp4 = os.path.join(CLIPS_DIR, f"clip_{clip_idx:02d}.mp4")
    selected_frames = frames[:num_frames]
    temp_dir = os.path.join(CLIPS_DIR, f"temp_{clip_idx:02d}")
    os.makedirs(temp_dir, exist_ok=True)
    for idx_f, f_name in enumerate(selected_frames):
        shutil.move(os.path.join(CSTRIKE_DIR, f_name), os.path.join(temp_dir, f"frame_{idx_f:04d}.bmp"))
        
    cmd_ff = [
        "ffmpeg", "-y", "-framerate", "30",
        "-i", os.path.join(temp_dir, "frame_%04d.bmp"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
        out_mp4
    ]
    subprocess.run(cmd_ff, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(temp_dir, ignore_errors=True)
    clean_cstrike()
    
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 200000:
        size_mb = os.path.getsize(out_mp4) / (1024 * 1024)
        print(f"  [SUCCESS] Clip {clip_idx:02d}: {out_mp4} ({size_mb:.2f} MB, {num_frames} frames)", flush=True)
        return True, out_mp4
    return False, None

def assemble_montage():
    print("\n=======================================================", flush=True)
    print("ASSEMBLING FINAL VOLUME 7 MONTAGES (16:9 HD & 9:16 REELS)", flush=True)
    print("=======================================================", flush=True)
    
    concat_list = os.path.join(CLIPS_DIR, "concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for i in range(1, 17):
            p = os.path.join(CLIPS_DIR, f"clip_{i:02d}.mp4").replace("\\", "/")
            f.write(f"file '{p}'\n")
            
    raw_video = os.path.join(CLIPS_DIR, "raw_vol7.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy", raw_video
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    music_track = os.path.join(BASE_DIR, "tools", "phonk_house.opus")
    out_16x9 = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol7.mp4")
    out_9x16 = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol7_9x16.mp4")
    
    # 1. 16:9 HD (1280x720, 60.00s, 1800 frames, 30fps)
    cmd_16x9 = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-stream_loop", "-1", "-i", music_track,
        "-filter_complex", "[1:a]afade=t=out:st=59.5:d=0.5,volume=0.9[a]",
        "-map", "0:v:0", "-map", "[a]",
        "-t", "60.0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        out_16x9
    ]
    print(f"Encoding 16:9 HD: {out_16x9}...", flush=True)
    subprocess.run(cmd_16x9, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. 9:16 Vertical Reels (1080x1920)
    filter_9x16 = (
        "[0:v]split=2[bg_in][fg_in];"
        "[bg_in]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
        "[fg_in]scale=1080:608:flags=lanczos[fg];"
        "[bg][fg]overlay=0:(H-h)/2[v];"
        "[1:a]afade=t=out:st=59.5:d=0.5,volume=0.9[a]"
    )
    cmd_9x16 = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-stream_loop", "-1", "-i", music_track,
        "-filter_complex", filter_9x16,
        "-map", "[v]", "-map", "[a]",
        "-t", "60.0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        out_9x16
    ]
    print(f"Encoding 9:16 Reels: {out_9x16}...", flush=True)
    subprocess.run(cmd_9x16, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(out_16x9):
        print(f"SUCCESS 16:9: {out_16x9} ({os.path.getsize(out_16x9)/(1024*1024):.2f} MB)", flush=True)
    if os.path.exists(out_9x16):
        print(f"SUCCESS 9:16: {out_9x16} ({os.path.getsize(out_9x16)/(1024*1024):.2f} MB)", flush=True)
        
    shutil.copy2(out_16x9, os.path.join(BASE_DIR, "EvilShtrib_60s_Vol7.mp4"))
    shutil.copy2(out_9x16, os.path.join(BASE_DIR, "EvilShtrib_60s_Vol7_9x16.mp4"))
    print("Copied final videos to repo root!", flush=True)

def main():
    sys.path.insert(0, os.path.join(BASE_DIR, "tools"))
    from find_pure_ct_candidates import candidates
    
    print(f"Loaded {len(candidates)} candidates for Volume 7 montage.\n", flush=True)
    selected = candidates[:16]
    
    frame_alloc = [112]*12 + [114]*4
    verified_items = []
    
    for idx, cand in enumerate(selected, 1):
        num_f = frame_alloc[idx-1]
        print(f"\n=======================================================", flush=True)
        print(f"CLIP {idx:02d}/16: {cand['killer']} ({cand['wpn']}) on {cand['map']} @ {cand['time']:.1f}s", flush=True)
        print(f"=======================================================", flush=True)
        
        # 1. Probe cycle
        best_c, score = probe_killer_cycle(cand['full_path'], max(1.0, cand['time'] - 1.5), cand['killer'], max_cycles=14)
        
        # 2. Render clip
        ok, clip_path = render_clip(cand, idx, num_f, best_c)
        if not ok:
            print(f"Failed to render clip {idx:02d}, retrying...", flush=True)
            ok, clip_path = render_clip(cand, idx, num_f, 0)
            best_c = 0
            
        cand['rendered_clip'] = clip_path
        cand['exact_cycle'] = best_c
        cand['num_frames'] = num_f
        verified_items.append(cand)
        
    v_path = os.path.join(BASE_DIR, "tools", "verified_vol7.json")
    with open(v_path, "w", encoding="utf-8") as f:
        json.dump(verified_items, f, indent=2)
    print(f"\nAll 16 clips rendered and verified! Saved to {v_path}", flush=True)
    
    assemble_montage()

if __name__ == "__main__":
    main()
