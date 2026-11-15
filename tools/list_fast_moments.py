import sys, os
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

d = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban"
results = []
for fn in os.listdir(d):
    if not fn.endswith('.dem'): continue
    mname, pnames, kills = parse_demo_kills(os.path.join(d, fn))
    clusters = cluster_moments(kills)
    for c in clusters:
        if c['num_kills'] >= 2 and c['kills'][0]['time'] < 500:
            c['demo'] = fn
            c['map'] = mname
            c['span'] = c['kills'][-1]['time'] - c['kills'][0]['time']
            results.append(c)

results.sort(key=lambda x: (x['num_kills'], x['score'], -x['span']), reverse=True)
print(f"Found {len(results)} multi-kills under 500s:")
for i, c in enumerate(results[:30], 1):
    wpns = list(set(k['weapon'] for k in c['kills']))
    hs = sum(1 for k in c['kills'] if k.get('headshot'))
    print(f"#{i:02d} [{c['map']:18s}] Killer: {c['killer_name']:12s} | {c['num_kills']}k ({hs}hs) in {c['span']:.1f}s | Wpns: {wpns} | t={c['kills'][0]['time']:.1f}s | {c['demo']}")
