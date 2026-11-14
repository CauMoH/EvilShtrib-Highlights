import os, sys, glob
sys.path.insert(0, r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools")
from analyze_highlights import parse_demo_kills, cluster_moments

# Let's inspect the 12 selected moments
selected_moments_spec = [
    # (demo_file, killer_name, approximate_first_kill_time, title, weapon_label, tag, fx_id)
    ("auto-2611142046-bio_ziger_azt.dem", "Player_21", 111.5, "5X MULTI-KILL SPREE", "FAMAS, GRENADE & DEAGLE", "5X COMBO", 1),
    ("auto-2611141907-zm_biohazard_base_mx004.dem", "Player_10", 298.8, "TRIPLE HEADSHOT", "UMP45 RAPID HEADSHOTS", "3X HEADSHOT", 2),
    ("auto-2611142112-bio_talka.dem", "Player_21", 532.2, "GALIL HEADSHOT STREAK", "IDF GALIL PRECISION SPRAY", "TRIPLE KILL", 3),
    ("auto-2611141820-bio_snow_na2.dem", "Player_22", 818.8, "M4A1 TRIPLE SPRAY", "M4A1 POINT-BLANK SPRAY", "TRIPLE KILL", 4),
    ("auto-2611142343-bio_oldhouse.dem", "Player_8", 1127.5, "DOUBLE TAP HEADSHOT", "M4A1 CARBINE DOUBLE", "DOUBLE HS", 5),
    ("auto-2611142138-bio_arena_fl.dem", "Player_21", 604.9, "INSTANT DOUBLE HEADSHOT", "M4A1 SILENCED HEADSHOTS", "DOUBLE HS", 6),
    ("auto-2611141820-bio_snow_na2.dem", "Player_15", 1468.3, "CLUSTER BOMB TRIPLE", "HE GRENADE WIPEOUT", "3X GRENADE", 7),
    ("auto-2611142046-bio_ziger_azt.dem", "Player_2", 194.1, "QUAD GRENADE BARRAGE", "HE GRENADES INVASION STOP", "4X GRENADE", 8),
    ("auto-2611141907-zm_biohazard_base_mx004.dem", "Player_6", 1038.9, "GALIL SURVIVOR DEFENSE", "IDF GALIL HEADSHOT DEFENSE", "TRIPLE HS", 9),
    ("auto-2611142020-bio_valak.dem", "Player_21", 996.9, "TACTICAL COMBO TRIPLE", "UMP45, GRENADE & USP", "TRIPLE KILL", 10),
    ("auto-2611142207-zm_restart_v3.dem", "Player_12", 753.5, "M4A1 ASSAULT DEFENSE", "M4A1 CARVED HEADSHOTS", "TRIPLE KILL", 11),
    ("auto-2611142258-zm_2day_rbt_f4.dem", "Player_1", 614.6, "XM1014 SHOTGUN DOUBLE", "XM1014 AUTO-SHOTGUN PUMP", "DOUBLE HS", 12),
]

DEMOS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos"

final_moments = []
for demo_file, killer, approx_time, title, wpn_label, tag, fx_id in selected_moments_spec:
    full_path = os.path.join(DEMOS_DIR, demo_file)
    mname, pnames, kills = parse_demo_kills(full_path)
    moments = cluster_moments(kills)
    # Find matching cluster
    best_match = None
    for m in moments:
        if m['killer_name'] == killer and abs(m['kills'][0]['time'] - approx_time) < 10.0:
            best_match = m
            break
    if best_match:
        fk = best_match['kills'][0]['time']
        lk = best_match['kills'][-1]['time']
        best_match['title'] = title
        best_match['weapon_label'] = wpn_label
        best_match['tag'] = tag
        best_match['fx_id'] = fx_id
        best_match['first_kill'] = fk
        best_match['last_kill'] = lk
        best_match['rec_start'] = max(1.0, fk - 0.8)
        best_match['rec_end'] = lk + 0.8
        best_match['rec_dur'] = best_match['rec_end'] - best_match['rec_start']
        best_match['demo_path'] = full_path
        final_moments.append(best_match)
        print(f"[{mname:20s}] Killer={killer:14s} | {best_match['num_kills']} Kills | {best_match['rec_start']:.1f}s -> {best_match['rec_end']:.1f}s ({best_match['rec_dur']:.1f}s)")
    else:
        print(f"FAILED to match {demo_file} for {killer} at ~{approx_time}s")

print(f"\nSuccessfully matched {len(final_moments)} / {len(selected_moments_spec)} moments!")
total_rec_dur = sum(m['rec_dur'] for m in final_moments)
print(f"Total gameplay duration: {total_rec_dur:.1f} seconds across {sum(m['num_kills'] for m in final_moments)} kills!")
