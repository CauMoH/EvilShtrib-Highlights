import os, sys
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

dirs = [
    r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban",
    r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_backup"
]

vol2_used = [
    ('bio_blocks_rb5_2026-11-15_05-44-00.dem', 'Dk-Unknown', 153.4),
    ('bio_dusty_2x2_fl_2026-11-15_06-35-00.dem', 'pyr0`', 176.2),
    ('bio_green_peaks_rb7_2026-11-15_07-52-00.dem', 'Galdalfus', 854.0),
    ('bio_heat_rb2_2026-11-15_08-17-00.dem', 'Dk-Unknown', 308.0),
    ('bio_blocks_rb5_2026-11-15_05-44-00.dem', 'aliendewd1', 1045.5),
    ('bio_green_peaks_rb7_2026-11-15_07-52-00.dem', 'kingkilla', 681.3),
    ('bio_cube_rb3_2026-11-15_06-10-00.dem', 'HappyKiD', 1253.6),
    ('bio_monument_2026-11-15_11-15-00.dem', 'HappyKiD', 40.3),
    ('bio_blocks_rb5_2026-11-15_05-44-00.dem', 'Player_9', 106.8),
    ('bio_blocks_rb5_2026-11-15_05-44-00.dem', 'Fat Matt', 172.9),
    ('bio_dusty_2x2_fl_2026-11-15_06-35-00.dem', 'Dk-Unknown', 387.2)
]

candidates = []
for d in dirs:
    if not os.path.exists(d): continue
    for fn in os.listdir(d):
        if not fn.endswith(".dem"): continue
        fp = os.path.join(d, fn)
        mname, pnames, kills = parse_demo_kills(fp)
        clusters = cluster_moments(kills)
        for c in clusters:
            kname = c['killer_name']
            if '`' in kname or kname == 'World' or kname == 'Trigger':
                continue
            if c['num_kills'] < 2:
                continue
            fk = c['kills'][0]['time']
            lk = c['kills'][-1]['time']
            span = lk - fk
            used = False
            for ufn, uk, ut in vol2_used:
                if ufn == fn and uk == kname and abs(ut - fk) < 5.0:
                    used = True
                    break
            if used: continue
            
            c['demo_file'] = fn
            c['map_name'] = mname
            c['first_kill'] = fk
            c['last_kill'] = lk
            c['span'] = span
            candidates.append(c)

candidates.sort(key=lambda x: (x['first_kill'] < 600, x['num_kills'], x['score'], -x['span']), reverse=True)
print(f"Total valid candidates: {len(candidates)}")
for i, c in enumerate(candidates[:25], 1):
    wpns = list(set(k.get('weapon') for k in c['kills']))
    hs = sum(1 for k in c['kills'] if k.get('headshot'))
    print(f"#{i:02d} [{c['map_name']:18s}] {c['killer_name']:12s} | {c['num_kills']}k ({hs}HS) in {c['span']:.1f}s | W: {wpns} | t={c['first_kill']:.1f}s | file: {c['demo_file']}")
