import sys, os, glob
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos"
demo_files = sorted(glob.glob(os.path.join(DEMOS_DIR, "*.dem")))

print(f"Scanning {len(demo_files)} downloaded real server demos...")
selected_moments = []

for df in demo_files:
    mname, pnames, kills = parse_demo_kills(df)
    candidates = cluster_moments(kills)
    if not candidates:
        print(f"  [WARNING] No kill moments found in {os.path.basename(df)}")
        continue
    candidates.sort(key=lambda x: -x['score'])
    best = candidates[0]
    selected_moments.append(best)
    w_str = ", ".join(best['weapons']).upper()
    hs_str = "[HEADSHOT]" if best['has_headshot'] else ""
    print(f"  [{mname:22s}]: Score={best['score']:3d} | Killer: {best['killer_name']:16s} ({best['num_kills']} kills with {w_str} {hs_str}) | Window: {best['time_start']:.1f}s - {best['time_end']:.1f}s ({best['duration']:.1f}s)")

# Sort selected moments by score
selected_moments.sort(key=lambda x: -x['score'])
print("\n" + "="*60)
print(f"FINAL 10 HIGHLIGHTS (1 per demo, for 60-second video):")
print("="*60)
for idx, m in enumerate(selected_moments, 1):
    w_str = ", ".join(m['weapons']).upper()
    hs_str = "[HS]" if m['has_headshot'] else ""
    v_str = ", ".join([f"{k['victim_name']} ({k['weapon']})" for k in m['kills']])
    print(f"#{idx:02d} | Map: {m['map']:22s} | Killer: {m['killer_name']:16s} | {m['num_kills']} kills with {w_str} {hs_str} | Score: {m['score']}")
    print(f"     Victims: {v_str}")
    print(f"     Window: {m['time_start']:.1f}s - {m['time_end']:.1f}s ({m['duration']:.1f}s) in {os.path.basename(m['demo_file'])}")
