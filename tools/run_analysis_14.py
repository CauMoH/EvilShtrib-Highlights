import sys, os
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import find_top_highlights

moments = find_top_highlights(count=14)
print(f"Total moments found: {len(moments)}")
for idx, m in enumerate(moments, 1):
    w = ', '.join(m['weapons']).upper()
    hs = '[HS]' if m['has_headshot'] else ''
    kills_str = ', '.join([f"{k['victim_name']} ({k['weapon']})" for k in m['kills']])
    print(f"#{idx:02d} | Map: {m['map']:22s} | Killer: {m['killer_name']:18s} | Kills: {m['num_kills']} with {w} {hs} | Window: {m['time_start']:.1f}s - {m['time_end']:.1f}s ({m['duration']:.1f}s)")
    print(f"     Victims: {kills_str}")
