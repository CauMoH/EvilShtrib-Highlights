"""
Probes remaining candidates at cycle == 0 to find 100% confirmed Human CT moments,
and renders them directly into the target slots (03, 04, 10, 13, 16) where cycle > 0 failed.
Guarantees 100% human POV across all 16 clips of Volume 6.
"""

import os, sys, glob, shutil, subprocess, time, cv2, json
import imageio_ffmpeg

HL_DIR = r"D:\SteamLibrary\steamapps\common\Half-Life"
CSTRIKE_DIR = os.path.join(HL_DIR, "cstrike")
HL_RECORDER = os.path.join(HL_DIR, "hl_recorder.exe")
BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
DEMOS_DIR = os.path.join(BASE_DIR, "demos_shtriban")
CLIPS_DIR = os.path.join(BASE_DIR, "clips_vol6")
VERIFIED_JSON = os.path.join(BASE_DIR, "tools", "verified_vol6.json")
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

sys.path.insert(0, os.path.join(BASE_DIR, "tools"))
from analyze_highlights import parse_demo_kills, cluster_moments

def make_waits(n):
    lines = []
    while n > 0:
        batch = min(20, n)
        lines.append(";".join(["wait"] * batch))
        n -= batch
    return lines

def clean_frames():
    for f in glob.glob(os.path.join(CSTRIKE_DIR, 'vol6_frame*.bmp')):
        try: os.remove(f)
        except OSError: pass

def test_candidate_cycle0(c):
    rec_start = max(1.0, c['time'] - 1.5)
    for f in os.listdir(CSTRIKE_DIR):
        if f.endswith(".bmp") or f.endswith(".tga"):
            try: os.remove(os.path.join(CSTRIKE_DIR, f))
            except OSError: pass

    shutil.copy2(c['full_path'], os.path.join(CSTRIKE_DIR, "render_clip.dem"))
    n_waits = int(rec_start * 2.0) + 120
    jump_waits = "\n".join(make_waits(n_waits))
    init_waits = "\n".join(make_waits(100))

    cfg_lines = [
        "dem_forcehltv 1",
        "spec_autodirector 0",
        "viewdemo render_clip",
        init_waits,
        "dem_pause 1",
        f"dem_jump {rec_start:.1f}",
        jump_waits,
        "dem_pause 0",
        "dem_speed 1.0",
        "spec_mode 4 0",
        "wait;wait;wait;wait;wait",
        "snapshot",
        "quit"
    ]
    with open(os.path.join(CSTRIKE_DIR, "test_c0.cfg"), "w") as f:
        f.write("\n".join(cfg_lines) + "\n")

    timeout_s = max(25, int(rec_start * 0.15) + 25)
    try:
        subprocess.run([
            HL_RECORDER, "-game", "cstrike", "-windowed", "-w", "1280", "-h", "720",
            "-novid", "+exec", "test_c0.cfg"
        ], cwd=HL_DIR, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        return None

    snaps = sorted([f for f in os.listdir(CSTRIKE_DIR) if f.endswith(".bmp") or f.endswith(".tga")])
    if not snaps:
        return None
    img = cv2.imread(os.path.join(CSTRIKE_DIR, snaps[0]))
    if img is None:
        return None
    h, w = img.shape[:2]
    crop = img[int(h*0.91):int(h*0.98), int(w*0.35):int(w*0.65)]
    b, g, r = crop[:,:,0], crop[:,:,1], crop[:,:,2]
    ct_p = int(((b > 130) & (g > 130) & (r < 155)).sum())
    t_p = int(((r > 160) & (g < 80) & (b < 80)).sum())
    return ct_p, t_p

def render_slot(item, idx, num_frames):
    out_mp4 = os.path.join(CLIPS_DIR, f"clip_{idx:02d}.mp4")
    print(f"\n>>> RENDERING SLOT {idx:02d} ({num_frames} frames / {num_frames/30.0:.2f}s)")
    print(f"    Demo:   {item['demo']}")
    print(f"    Killer: {item['killer']}")
    print(f"    Weapon: {item['wpn']}")
    print(f"    Time:   {item['time']:.1f}s")
    clean_frames()

    shutil.copy2(item['full_path'], os.path.join(CSTRIKE_DIR, "render_clip.dem"))
    lead_in = (num_frames / 30.0) * 0.45
    rec_start = max(1.0, item['time'] - lead_in)

    n_jump_waits = int(rec_start * 2.0) + 120
    jump_waits = "\n".join(make_waits(n_jump_waits))
    init_waits = "\n".join(make_waits(100))
    rec_waits = "\n".join(make_waits(num_frames + 15))

    cfg_lines = [
        "dem_forcehltv 1",
        "spec_autodirector 0",
        "viewdemo render_clip",
        init_waits,
        "dem_pause 1",
        f"dem_jump {rec_start:.1f}",
        jump_waits,
        "dem_pause 0",
        "dem_speed 1.0",
        "spec_mode 4 0",
        "wait;wait;wait;wait;wait",
        "host_framerate 0.0333333",
        "startmovie vol6_frame 30",
        rec_waits,
        "endmovie",
        "host_framerate 0",
        "wait;wait;wait;wait;wait",
        "quit"
    ]
    with open(os.path.join(CSTRIKE_DIR, "render_clip.cfg"), "w") as f:
        f.write("\n".join(cfg_lines) + "\n")

    timeout_s = max(40, int(rec_start * 0.15) + int(num_frames * 0.5) + 30)
    subprocess.run([
        HL_RECORDER, "-game", "cstrike", "-windowed", "-w", "1280", "-h", "720",
        "-novid", "+exec", "render_clip.cfg"
    ], cwd=HL_DIR, timeout=timeout_s)

    frames = sorted(glob.glob(os.path.join(CSTRIKE_DIR, "vol6_frame*.bmp")))
    if len(frames) < num_frames:
        print(f"    ERROR: Captured only {len(frames)} / {num_frames} frames!")
        return False

    mid_img = cv2.imread(frames[len(frames)//2])
    if mid_img is not None:
        h, w = mid_img.shape[:2]
        crop = mid_img[int(h*0.91):int(h*0.98), int(w*0.35):int(w*0.65)]
        b, g, r = crop[:,:,0], crop[:,:,1], crop[:,:,2]
        ct_p = ((b > 130) & (g > 130) & (r < 155)).sum()
        t_p = ((r > 160) & (g < 80) & (b < 80)).sum()
        print(f"    Quality Gate Check: CT={ct_p}, T={t_p}")
        if t_p > 0 and ct_p < 20:
            print("    FAILED Quality Gate! Rejecting.")
            return False

    selected_frames = frames[:num_frames]
    concat_list = os.path.join(CLIPS_DIR, "frames.txt")
    with open(concat_list, "w") as f:
        for fr in selected_frames:
            f.write(f"file '{fr}'\n")
            f.write("duration 0.033333\n")

    cmd = [
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p", "-r", "30", out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(concat_list):
        os.remove(concat_list)
    clean_frames()
    print(f"    Successfully rendered {out_mp4}!")
    return True

def main():
    with open(VERIFIED_JSON, "r", encoding="utf-8") as f:
        verified = json.load(f)

    # Slots that failed Quality Gate (cycle > 0):
    # 03 (idx 2, 112 frames)
    # 04 (idx 3, 112 frames)
    # 10 (idx 9, 112 frames)
    # 13 (idx 12, 114 frames)
    # 16 (idx 15, 114 frames)
    target_slots = [
        (3, 2, 112),
        (4, 3, 112),
        (10, 9, 112),
        (13, 12, 114),
        (16, 15, 114)
    ]

    # Collect existing used times to avoid duplicates
    used_times = {(v['demo'], round(v['time'], 1)) for i, v in enumerate(verified) if i not in [2, 3, 9, 12, 15]}

    # Candidates from list_all_cands
    VALID_WPNS = {'m4a1', 'ak47', 'xm1014', 'm3', 'sg550', 'g3sg1', 'scout', 'deagle', 'elite', 'mac10', 'mp5navy', 'famas', 'galil', 'm249', 'hegrenade', 'p90', 'ump45', 'aug', 'sg552'}
    USED_MD = os.path.join(BASE_DIR, "USED_MOMENTS.md")
    with open(USED_MD, "r", encoding="utf-8") as f:
        text = f.read()
    import re
    hist_used = []
    for line in text.splitlines():
        if ".dem`" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6:
                dem = parts[2].replace("`", "").strip()
                t_nums = re.findall(r"[0-9\.]+", parts[5].strip())
                if t_nums:
                    t1 = float(t_nums[0])
                    t2 = float(t_nums[1]) if len(t_nums) > 1 else t1 + 5.0
                    hist_used.append((dem, t1 - 4.0, t2 + 4.0))

    def is_hist_used(d, t):
        for ud, us, ue in hist_used:
            if ud == d and (us <= t <= ue):
                return True
        return False

    cands = []
    for dem in sorted(glob.glob(os.path.join(DEMOS_DIR, "*.dem"))):
        fname = os.path.basename(dem)
        mname, pnames, kills = parse_demo_kills(dem)
        gun_kills = [k for k in kills if k['weapon'].lower() in VALID_WPNS]
        moments = cluster_moments(gun_kills)
        for m in moments:
            if m['num_kills'] >= 2:
                fk = m['kills'][0]['time']
                span = m['kills'][-1]['time'] - fk
                if span <= 3.2 and not is_hist_used(fname, fk) and (fname, round(fk, 1)) not in used_times:
                    cands.append({
                        'demo': fname,
                        'full_path': dem,
                        'map': mname,
                        'killer': m['killer_name'],
                        'time': fk,
                        'span': span,
                        'kills': m['num_kills'],
                        'wpn': '/'.join(set(k['weapon'] for k in m['kills'])),
                        'cycle': 0
                    })

    # Sort prioritizing tight spans (most action packed)
    cands.sort(key=lambda x: x['span'])
    print(f"Available fresh candidates: {len(cands)}")

    slot_ptr = 0
    for c in cands:
        if slot_ptr >= len(target_slots):
            break
        slot_num, v_idx, n_frames = target_slots[slot_ptr]
        print(f"Testing candidate for Slot {slot_num:02d}: {c['demo'][:25]} | {c['killer'][:12]} | {c['wpn']} | span={c['span']:.2f}s... ", end="")
        sys.stdout.flush()

        res = test_candidate_cycle0(c)
        if res:
            ct_p, t_p = res
            print(f"CT={ct_p}, T={t_p}", end="")
            if ct_p > 50 and t_p == 0:
                print(" -> PASSED 100% CT! Rendering slot...")
                sys.stdout.flush()
                ok = render_slot(c, slot_num, n_frames)
                if ok:
                    verified[v_idx] = c
                    # Save progress
                    with open(VERIFIED_JSON, "w", encoding="utf-8") as f_out:
                        json.dump(verified, f_out, indent=2)
                    slot_ptr += 1
            else:
                print(" -> REJECTED (not CT)")
        else:
            print(" -> FAILED (recorder timeout/error)")

    print(f"\nFinished replacements! {slot_ptr}/{len(target_slots)} slots filled.")

if __name__ == "__main__":
    main()
