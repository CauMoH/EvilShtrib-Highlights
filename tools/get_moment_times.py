import sys
sys.path.insert(0, r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools')
from analyze_highlights import parse_demo_kills, cluster_moments

_, _, k = parse_demo_kills(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611141907-zm_biohazard_base_mx004.dem')
moments = cluster_moments(k)
for m in moments:
    if m['killer_name'] == 'Player_10' and m['num_kills'] == 3:
        fk = m['kills'][0]['time']
        lk = m['kills'][-1]['time']
        print(f"Player_10 UMP45 triple: first_kill={fk:.2f}s, last_kill={lk:.2f}s, span={lk-fk:.2f}s")
