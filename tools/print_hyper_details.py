import os, sys
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

specs = [
    ("auto-2611142046-bio_ziger_azt.dem", "Player_21", 111.5, "KILL STREAK 01 / 12", "FAMAS BURST & GRENADE", "5X COMBO", "bio_ziger_azt"),
    ("auto-2611141907-zm_biohazard_base_mx004.dem", "Player_10", 298.8, "KILL STREAK 02 / 12", "UMP45 RAPID HEADSHOTS", "3X HEADSHOT", "zm_biohazard_base_mx004"),
    ("auto-2611142112-bio_talka.dem", "Player_21", 532.2, "KILL STREAK 03 / 12", "IDF GALIL HEADSHOTS", "TRIPLE KILL", "bio_talka"),
    ("auto-2611141820-bio_snow_na2.dem", "Player_22", 818.8, "KILL STREAK 04 / 12", "M4A1 POINT-BLANK SPRAY", "TRIPLE KILL", "bio_snow_na2"),
    ("auto-2611142343-bio_oldhouse.dem", "Player_8", 1127.5, "KILL STREAK 05 / 12", "M4A1 CARBINE DOUBLE", "DOUBLE HS", "bio_oldhouse"),
    ("auto-2611142138-bio_arena_fl.dem", "Player_21", 604.9, "KILL STREAK 06 / 12", "M4A1 SILENCED HEADSHOTS", "DOUBLE HS", "bio_arena_fl"),
    ("auto-2611141820-bio_snow_na2.dem", "Player_15", 1468.3, "KILL STREAK 07 / 12", "HE GRENADE WIPEOUT", "3X GRENADE", "bio_snow_na2"),
    ("auto-2611142046-bio_ziger_azt.dem", "Player_2", 194.1, "KILL STREAK 08 / 12", "HE GRENADE INVASION STOP", "4X GRENADE", "bio_ziger_azt"),
    ("auto-2611141907-zm_biohazard_base_mx004.dem", "Player_6", 1038.9, "KILL STREAK 09 / 12", "IDF GALIL HEADSHOT DEFENSE", "TRIPLE HS", "zm_biohazard_base_mx004"),
    ("auto-2611142020-bio_valak.dem", "Player_21", 996.9, "KILL STREAK 10 / 12", "UMP45, GRENADE & USP", "TRIPLE KILL", "bio_valak"),
    ("auto-2611142207-zm_restart_v3.dem", "Player_12", 753.5, "KILL STREAK 11 / 12", "M4A1 CARVED HEADSHOTS", "TRIPLE KILL", "zm_restart_v3"),
    ("auto-2611142258-zm_2day_rbt_f4.dem", "Player_1", 614.6, "KILL STREAK 12 / 12", "XM1014 AUTO-SHOTGUN PUMP", "DOUBLE HS", "zm_2day_rbt_f4"),
]

demos_dir = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos"
for idx, (dem, killer, approx_t, title, wpn, tag, map_name) in enumerate(specs, 1):
    fp = os.path.join(demos_dir, dem)
    mname, pnames, kills = parse_demo_kills(fp)
    clusters = cluster_moments(kills)
    match = None
    for c in clusters:
        if c['killer_name'] == killer and abs(c['kills'][0]['time'] - approx_t) < 10.0:
            match = c
            break
    if match:
        v_list = []
        for k in match['kills']:
            hs = " [HS]" if k.get("headshot") else ""
            v_list.append(f"{k['victim_name']}{hs} ({k.get('weapon','')})")
        print(f"CLIP {idx:02d} | {title} | {killer} on {map_name} | {len(match['kills'])} kills:")
        print(f"  Victims: {', '.join(v_list)}")
