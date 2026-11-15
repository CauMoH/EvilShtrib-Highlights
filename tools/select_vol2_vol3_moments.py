import os, sys
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

dirs = [
    r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban",
    r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_backup"
]

all_clusters = []
for d in dirs:
    if not os.path.exists(d): continue
    for fn in os.listdir(d):
        if not fn.endswith(".dem"): continue
        fp = os.path.join(d, fn)
        mname, pnames, kills = parse_demo_kills(fp)
        clusters = cluster_moments(kills)
        for c in clusters:
            c['demo_path'] = fp
            c['demo_file'] = fn
            c['map_name'] = mname
            fk = c['kills'][0]['time']
            lk = c['kills'][-1]['time']
            c['span'] = lk - fk
            c['first_kill'] = fk
            c['last_kill'] = lk
            all_clusters.append(c)

print(f"Total clusters: {len(all_clusters)}")

# Sort by num_kills desc, then score desc, then shortest span
multi_kills = [c for c in all_clusters if c['num_kills'] >= 2]
multi_kills.sort(key=lambda x: (x['num_kills'], x['score'], -x['span']), reverse=True)

print(f"\nFound {len(multi_kills)} multi-kill clusters (>= 2 kills).")
print("\nTop 30 multi-kill clusters:")
for i, c in enumerate(multi_kills[:30], 1):
    weapons = list(set(k.get('weapon') for k in c['kills']))
    v_hs = sum(1 for k in c['kills'] if k.get('headshot'))
    print(f"#{i:02d} [{c['map_name']:18s}] Killer: {c['killer_name']:14s} | {c['num_kills']} kills ({v_hs} HS) in {c['span']:.1f}s | Score: {c['score']:3d} | Wpns: {weapons} | t={c['first_kill']:.1f}s")
