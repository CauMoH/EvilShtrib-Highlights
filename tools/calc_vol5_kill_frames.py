import os, sys

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments
from render_vol5_clips import VOL5_MOMENTS, DEMOS_DIR

for idx, item in enumerate(VOL5_MOMENTS, 1):
    demo_file, killer, approx_time, title, wpn_label, tag, fx_id, num_frames = item
    full_path = os.path.join(DEMOS_DIR, demo_file)
    mname, pnames, kills = parse_demo_kills(full_path)
    moments = cluster_moments(kills)
    match = None
    for m in moments:
        if m['num_kills'] >= 2 and m['killer_name'] == killer and abs(m['kills'][0]['time'] - approx_time) < 15.0:
            match = m
            break
            
    fk = match['kills'][0]['time']
    lk = match['kills'][-1]['time']
    mid_kill = (fk + lk) / 2.0
    half_dur = (num_frames / 30.0) / 2.0
    rec_start = max(1.0, mid_kill - half_dur)
    
    kill_frames = [int(round((k['time'] - rec_start) * 30.0)) for k in match['kills']]
    # Clamp to [0, num_frames-1]
    kill_frames = [max(0, min(num_frames-1, f)) for f in kill_frames]
    
    print(f"    {{'file': 'clip_{idx:02d}.mp4', 'start': 0, 'end': {num_frames}, 'kills': {kill_frames}, 'title': 'KILL STREAK {idx:02d} / 16', 'weapon': '{wpn_label}', 'tag': '{tag}', 'player': '{killer}', 'map': '{match['map']}', 'fx': {fx_id}}},")
