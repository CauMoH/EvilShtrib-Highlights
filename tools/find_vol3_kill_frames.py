"""
Find the kill frame offsets in clips_vol3.
"""
import os, sys, cv2
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments
from render_vol3_clips import VOL3_MOMENTS, DEMOS_DIR, CLIPS_DIR

def inspect_vol3_clips():
    configs = []
    total_frames = 0
    for idx, item in enumerate(VOL3_MOMENTS, 1):
        demo_file, killer, approx_time, title, wpn_label, tag, fx_id, max_frames = item
        clip_file = f"clip_{idx:02d}.mp4"
        clip_path = os.path.join(CLIPS_DIR, clip_file)
        if not os.path.exists(clip_path):
            print(f"[{idx:02d}] Not ready: {clip_file}")
            continue
            
        cap = cv2.VideoCapture(clip_path)
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        
        full_path = os.path.join(DEMOS_DIR, demo_file)
        if not os.path.exists(full_path):
            full_path = os.path.join(r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_backup", demo_file)
        mname, pnames, kills = parse_demo_kills(full_path)
        moments = cluster_moments(kills)
        match = None
        for m in moments:
            if m['killer_name'] == killer and abs(m['kills'][0]['time'] - approx_time) < 10.0:
                match = m
                break
                
        fk = match['kills'][0]['time']
        lk = match['kills'][-1]['time']
        rec_start = max(1.0, fk - 0.9)
        
        # Kill frame offsets within the clip
        kill_frames = []
        for k in match['kills']:
            offset = int((k['time'] - rec_start) * 30.0)
            kill_frames.append(min(num_frames - 1, max(0, offset)))
            
        cfg = {
            "file": clip_file,
            "start": 0,
            "end": num_frames,
            "kills": kill_frames,
            "title": f"MOMENT {idx:02d} / 12",
            "weapon": wpn_label,
            "tag": tag,
            "player": killer,
            "map": match['map'],
            "fx": fx_id,
            "duration": num_frames / 30.0
        }
        configs.append(cfg)
        total_frames += num_frames
        print(f"[{idx:02d}] {clip_file} ({num_frames} frames, {num_frames/30.0:.2f}s) | Map: {match['map']} | Killer: {killer} | Kills: {kill_frames} | Wpn: {wpn_label}")
        
    print(f"\nTotal clips: {len(configs)} | Total frames: {total_frames} ({total_frames/30.0:.2f}s)")
    return configs

if __name__ == "__main__":
    inspect_vol3_clips()
