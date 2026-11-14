import os, sys, glob
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos"
demos = sorted(glob.glob(os.path.join(DEMOS_DIR, "*.dem")))

dense_moments = []

for d in demos:
    mname, pnames, kills = parse_demo_kills(d)
    moments = cluster_moments(kills)
    for m in moments:
        if m['num_kills'] >= 2:
            fk = m['kills'][0]['time']
            lk = m['kills'][-1]['time']
            span = lk - fk
            # Density score: more kills in shorter time = higher density!
            # e.g. 3 kills in 2s = density 1.5 kills/sec
            density = m['num_kills'] / max(1.0, span)
            # Give bonus for headshots and grenade multi-kills
            hs_count = sum(1 for k in m['kills'] if k['headshot'])
            m['density'] = density
            m['span'] = span
            m['first_kill'] = fk
            m['last_kill'] = lk
            m['hs_count'] = hs_count
            m['demo_file'] = d
            dense_moments.append(m)

# Sort by (num_kills, hs_count, -span)
dense_moments.sort(key=lambda x: (x['num_kills'] >= 3, x['num_kills'], x['hs_count'], -x['span']), reverse=True)

print(f"Total multi-kill moments found: {len(dense_moments)}")
print("\nTOP 20 HYPER-DENSE MULTI-KILL HIGHLIGHTS:")
print("="*80)

seen_demos = {}
selected_pool = []

for m in dense_moments:
    demo_base = os.path.basename(m['demo_file'])
    # Don't pick more than 2 from the same demo so we keep variety
    if seen_demos.get(demo_base, 0) >= 2:
        continue
    seen_demos[demo_base] = seen_demos.get(demo_base, 0) + 1
    selected_pool.append(m)
    if len(selected_pool) >= 15:
        break

for i, m in enumerate(selected_pool, 1):
    w = ", ".join(set(k['weapon'] for k in m['kills'])).upper()
    print(f"#{i:02d} | Map: {m['map']:20s} | Killer: {m['killer_name']:18s} | {m['num_kills']} KILLS ({m['hs_count']} HS) with {w}")
    print(f"     Time: {m['first_kill']-0.8:.1f}s -> {m['last_kill']+0.8:.1f}s (Dur: {m['span']+1.6:.1f}s) in {os.path.basename(m['demo_file'])}")
    for k in m['kills']:
        print(f"       +{(k['time'] - m['first_kill']):.2f}s: {k['victim_name']} ({k['weapon']}) {'[HS]' if k['headshot'] else ''}")
