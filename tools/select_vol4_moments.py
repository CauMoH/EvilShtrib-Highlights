import os, glob, sys
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban"
demo_files = sorted(glob.glob(os.path.join(DEMOS_DIR, "*.dem")))

used = [
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
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", 472.5),
    ("bio_asalto_f_2026-11-14_17-27-00.dem", 58.7),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 361.5),
    ("bio_evil_dust_fl_2026-11-15_07-01-00.dem", 337.4),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 16.3),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 249.5),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 509.1),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 15.5),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1156.9),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 1443.7),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1251.3),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1072.6),
]

all_moments = []
for df in demo_files:
    fname = os.path.basename(df)
    mname, pnames, kills = parse_demo_kills(df)
    moments = cluster_moments(kills)
    for m in moments:
        if m['num_kills'] >= 2:
            fk = m['kills'][0]['time']
            lk = m['kills'][-1]['time']
            span = lk - fk
            is_used = False
            for u_df, u_t in used:
                if u_df == fname and abs(fk - u_t) < 15.0:
                    is_used = True
                    break
            if not is_used and '`' not in m['killer_name'] and span <= 2.5:
                all_moments.append({
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

all_moments.sort(key=lambda x: x['span'])
print(f"Found {len(all_moments)} unused rapid moments:")
for i, m in enumerate(all_moments):
    wpns = ", ".join(m['weapons'])
    print(f"{i+1:02d}. {m['demo']} | {m['map']} | {m['killer']} | span={m['span']:.2f}s | t={m['start_time']:.1f}s | {m['num_kills']}k ({m['hs']}hs) | {wpns}")
