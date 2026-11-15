import os, sys, glob

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban"
demos = sorted(glob.glob(os.path.join(DEMOS_DIR, "*.dem")))

used_moments = []
with open(r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\USED_MOMENTS.md", "r", encoding="utf-8") as f:
    for line in f:
        if ".dem" in line:
            parts = [p.strip().replace("`", "") for p in line.split("|")]
            if len(parts) >= 6:
                dem = parts[2]
                t_str = parts[5]
                try:
                    t_val = float(t_str.split("-")[0].strip())
                    used_moments.append((dem, t_val))
                except ValueError:
                    pass

print(f"Loaded {len(used_moments)} used moments from USED_MOMENTS.md")

def is_used(dem_file, t):
    for udem, ut in used_moments:
        if udem == dem_file and abs(ut - t) < 20.0:
            return True
    return False

candidates = []
for dpath in demos:
    dname = os.path.basename(dpath)
    if "horror_box" in dname:
        continue
    mname, pnames, kills = parse_demo_kills(dpath)
    moments = cluster_moments(kills)
    for m in moments:
        if m['num_kills'] >= 2:
            fk = m['kills'][0]['time']
            lk = m['kills'][-1]['time']
            span = lk - fk
            # Fast action & reasonable timestamp (under 600s)
            if 30.0 <= fk <= 600.0 and span <= 2.8:
                if not is_used(dname, fk):
                    # Check that killer is known
                    if not m['killer_name'].startswith("Player_"):
                        candidates.append({
                            'demo': dname,
                            'map': m['map'],
                            'killer': m['killer_name'],
                            'time': fk,
                            'end_time': lk,
                            'span': span,
                            'kills': m['num_kills'],
                            'weapons': [k['weapon'] for k in m['kills']],
                            'hs': sum(1 for k in m['kills'] if k['headshot'])
                        })

print(f"Found {len(candidates)} new intense action moments!")
candidates.sort(key=lambda x: (x['span'], -x['kills']))
for i, c in enumerate(candidates[:50]):
    print(f"[{i+1:02d}] {c['map']:18s} | {c['killer']:15s} | t={c['time']:5.1f}s | kills={c['kills']} (HS:{c['hs']}) | span={c['span']:.2f}s | {c['weapons']}")
