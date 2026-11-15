import os, sys
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

# Read used moments
used = [
    # Vol 2
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 153.4),
    ("bio_dusty_2x2_fl_2026-11-15_06-35-00.dem", 176.2),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", 854.0),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 308.0),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1045.5),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", 681.3),
    ("bio_cube_rb3_2026-11-15_06-10-00.dem", 1253.6),
    ("bio_monument_2026-11-15_11-15-00.dem", 40.3),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", 301.9),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 106.8),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 172.9),
    ("bio_dusty_2x2_fl_2026-11-15_06-35-00.dem", 387.2),
    # Vol 3
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", 472.5),
    ("bio_asalto_f_2026-11-14_17-27-00.dem", 58.7),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 361.5),
    ("bio_evil_dust_fl_2026-11-15_07-01-00.dem", 337.4),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 16.3),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 15.5),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 249.5),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 509.1),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1156.9),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 1443.7),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1251.3),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1072.6),
]

dirs = [
    r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban",
    r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_backup"
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
            k = c['killer_name']
            if '`' in k or k in ('World', 'Trigger'):
                continue
            if c['num_kills'] < 2:
                continue
            fk = c['kills'][0]['time']
            lk = c['kills'][-1]['time']
            span = lk - fk
            
            # Check overlap with any used moment on this demo
            is_used = False
            for ufn, ut in used:
                if ufn == fn and abs(ut - fk) < 60.0:
                    is_used = True
                    break
            if is_used: continue
            
            c['demo_file'] = fn
            c['demo_path'] = fp
            c['map'] = mname
            c['first_kill'] = fk
            c['last_kill'] = lk
            c['span'] = span
            candidates.append(c)

# We want ULTRA-FAST multi-kills: shortest span first!
# Rapid kills: span <= 2.5s
rapid = [c for c in candidates if c['span'] <= 2.5]
rapid.sort(key=lambda x: (x['num_kills'], -x['span'], x['score']), reverse=True)

print(f"Total fresh rapid-fire candidates (span <= 2.5s): {len(rapid)}")
for i, c in enumerate(rapid[:30], 1):
    wpns = list(set(k.get('weapon') for k in c['kills']))
    hs = sum(1 for k in c['kills'] if k.get('headshot'))
    print(f"#{i:02d} [{c['map']:18s}] {c['killer_name']:12s} | {c['num_kills']}k ({hs}HS) in {c['span']:.2f}s | W: {wpns} | t={c['first_kill']:.1f}s | {c['demo_file']}")
