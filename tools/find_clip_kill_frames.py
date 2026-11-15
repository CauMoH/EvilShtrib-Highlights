import sys, os
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from select_10_demo_highlights import selected_moments

# For clip 4, we replaced zm_lb with zm_2day_rbt_f4
from analyze_highlights import parse_demo_kills, cluster_moments
_, _, k4 = parse_demo_kills(r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611142258-zm_2day_rbt_f4.dem")
c4 = cluster_moments(k4)
c4.sort(key=lambda x: -x['score'])
moment_04 = c4[0]

moments = list(selected_moments)
moments[3] = moment_04

for idx, m in enumerate(moments, 1):
    t_start = max(1.0, m['time_start'])
    first_kill_t = m['kills'][0]['time']
    rel_t = first_kill_t - t_start
    rel_frame = int(rel_t * 30.0)
    w_str = ", ".join(m['weapons']).upper()
    print(f"Clip {idx:02d} ({m['map']}): Start={t_start:.1f}s | 1st Kill={first_kill_t:.1f}s (rel: +{rel_t:.2f}s, frame #{rel_frame}) | Total Kills: {m['num_kills']} ({w_str})")
    for k in m['kills']:
        kt = k['time'] - t_start
        print(f"    -> Kill at +{kt:.2f}s (frame #{int(kt*30)}): {k['victim_name']} with {k['weapon']} {'[HS]' if k['headshot'] else ''}")
