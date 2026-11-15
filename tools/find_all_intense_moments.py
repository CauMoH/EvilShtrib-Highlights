import os, sys, glob
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos"
demos = sorted(glob.glob(os.path.join(DEMOS_DIR, "*.dem")))

all_clusters = []
for d in demos:
    mname, pnames, kills = parse_demo_kills(d)
    moments = cluster_moments(kills)
    for m in moments:
        # We only want moments with at least 2 kills, or 1 headshot sniper kill
        if m['num_kills'] >= 2 or m['has_headshot']:
            all_clusters.append(m)

# Sort by score (kill count, headshots, weapons)
all_clusters.sort(key=lambda x: -x['score'])

print(f"Total intense clusters found: {len(all_clusters)}")
print("Top 15 Most Intense Moments across all real demos:")
for i, m in enumerate(all_clusters[:15], 1):
    w = ", ".join(m['weapons']).upper()
    hs = "[HS]" if m['has_headshot'] else ""
    first_k = m['kills'][0]['time']
    last_k = m['kills'][-1]['time']
    span = last_k - first_k
    print(f"#{i:02d} | Map: {m['map']:22s} | Killer: {m['killer_name']:18s} | Kills: {m['num_kills']} ({w} {hs}) | Span: {span:.1f}s | Score: {m['score']}")
    for k in m['kills']:
        print(f"      +{(k['time'] - first_k):.2f}s: {k['victim_name']} ({k['weapon']}) {'[HS]' if k['headshot'] else ''}")
