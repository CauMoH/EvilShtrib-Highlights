import sys
sys.path.insert(0, r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools')
from analyze_highlights import parse_demo_kills

m, p, k = parse_demo_kills(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611141954-zm_lb.dem')
print(f"Map: {m}")
print(f"Total kills: {len(k)}")
print(f"First kill: {k[0]['time']:.1f}s")
print(f"Last kill: {k[-1]['time']:.1f}s")
