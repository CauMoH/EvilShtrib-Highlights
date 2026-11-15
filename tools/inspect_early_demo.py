import sys
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills

path = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos_shtriban\bio_blocks_pro_2026-11-15_05-19-00.dem"
mname, pnames, kills = parse_demo_kills(path)
print("Demo map:", mname)
print("Players count:", len(pnames))
for k in kills[:20]:
    print(f"{k['time']:6.1f}s | {k['killer']} ({k['weapon']}) -> {k['victim']}")
