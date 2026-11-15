import os, sys, glob

sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban"
demos = sorted(glob.glob(os.path.join(DEMOS_DIR, "*.dem")))

used_keys = [
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
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 249.5),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 509.1),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 15.5),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1156.9),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 1443.7),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1251.3),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1072.6),
    # Vol 4
    ("bio_dusty_2x2_fl_2026-11-15_06-35-00.dem", 1334.4),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 854.4),
    ("bio_resident_beta_2026-11-15_12-57-00.dem", 1151.4),
    ("bio_horror_box_ff_2026-11-15_08-43-00.dem", 708.5),
    ("bio_horror_box_ff_2026-11-15_08-43-00.dem", 363.2),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 1399.5),
    ("bio_evil_dust_fl_2026-11-15_07-01-00.dem", 985.6),
    ("bio_resident_beta_2026-11-15_12-57-00.dem", 137.6),
    ("bio_horror_box_ff_2026-11-15_08-43-00.dem", 124.7),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", 1339.9),
    ("bio_cube_rb3_2026-11-15_06-10-00.dem", 779.9),
    ("bio_heat_rb2_2026-11-15_08-17-00.dem", 983.4),
    ("bio_resident_beta_2026-11-15_12-57-00.dem", 1090.5),
    ("bio_blocks_rb5_2026-11-15_05-44-00.dem", 908.2),
    ("bio_green_peaks_rb7_2026-11-15_07-52-00.dem", 741.3),
    ("bio_resident_beta_2026-11-15_12-57-00.dem", 1430.2),
]

def is_used(dem_file, t):
    for udem, ut in used_keys:
        if udem == dem_file and abs(ut - t) < 15.0:
            return True
    return False

all_candidates = []
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
            # Fast action & Early-mid time window (30s - 260s)
            if 30.0 <= fk <= 260.0 and span <= 2.2:
                if not is_used(dname, fk):
                    all_candidates.append({
                        'demo': dname,
                        'map': m['map'],
                        'killer': m['killer_name'],
                        'time': fk,
                        'span': span,
                        'kills': m['num_kills'],
                        'weapons': [k['weapon'] for k in m['kills']],
                        'hs': sum(1 for k in m['kills'] if k['headshot'])
                    })

print(f"Total action candidates found: {len(all_candidates)}")
# Sort by span ascending (fastest multi-kills first!)
all_candidates.sort(key=lambda x: x['span'])
for idx, c in enumerate(all_candidates[:40]):
    print(f"[{idx+1:02d}] {c['map']:18s} | {c['killer']:15s} | t={c['time']:5.1f}s | kills={c['kills']} (HS:{c['hs']}) | span={c['span']:.2f}s | {c['weapons']}")
