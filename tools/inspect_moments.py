import sys, os
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import find_top_highlights

moments = find_top_highlights(count=10)
for idx, m in enumerate(moments, 1):
    kills_rel = [round(k['time'] - m['time_start'], 2) for k in m['kills']]
    frames = [int(x*30) for x in kills_rel]
    print(f"Clip {idx:02d}: Killer={m['killer_name']} | Map={m['map']} | Weapons={m['weapons']} | Dur={m['duration']}s | KillsAt={kills_rel}s (frames={frames})")
