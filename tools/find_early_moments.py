import os, sys, glob
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban"

early_moments = []
for df in sorted(glob.glob(os.path.join(DEMOS_DIR, "*.dem"))):
    fname = os.path.basename(df)
    mname, pnames, kills = parse_demo_kills(df)
    moments = cluster_moments(kills)
    for m in moments:
        if m['num_kills'] >= 2 and '`' not in m['killer_name']:
            fk = m['kills'][0]['time']
            lk = m['kills'][-1]['time']
            span = lk - fk
            if fk <= 260.0 and span <= 3.5:
                early_moments.append({
                    'demo': fname,
                    'map': mname,
                    'killer': m['killer_name'],
                    'start_time': fk,
                    'end_time': lk,
                    'span': span,
                    'num_kills': m['num_kills'],
                    'weapons': list(set(k['weapon'] for k in m['kills'])),
                    'hs': sum(1 for k in m['kills'] if k.get('headshot', False))
                })

early_moments.sort(key=lambda x: (x['span'], -x['num_kills']))
print(f"Found {len(early_moments)} rapid moments in first 260s:")
for i, m in enumerate(early_moments):
    wpns = ", ".join(m['weapons'])
    print(f"{i+1:02d}. {m['demo']} | {m['map']} | {m['killer']} | span={m['span']:.2f}s | t={m['start_time']:.1f}s | {m['num_kills']}k ({m['hs']}hs) | {wpns}")
