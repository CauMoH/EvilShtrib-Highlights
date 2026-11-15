# Check kill frames for all 12 clips
clips_specs = [
    # (clip_file, start, end, kills_raw, title, weapon, tag, player, map, fx)
    ("clip_01.mp4", 0, 170, [27, 78, 140], "KILL STREAK 01", "FAMAS & HE GRENADE", "5X MULTI-KILL", "Player_21", "bio_ziger_azt", 1),
    ("clip_02.mp4", 0, 100, [27, 67, 91], "KILL STREAK 02", "UMP45 HEADSHOT RAPID", "3X HEADSHOT", "Player_10", "zm_biohazard_base_mx004", 2),
    ("clip_03.mp4", 0, 160, [27, 130], "KILL STREAK 03", "IDF GALIL HEADSHOTS", "TRIPLE KILL", "Player_21", "bio_talka", 3),
    ("clip_04.mp4", 0, 85, [27, 33, 72], "KILL STREAK 04", "M4A1 POINT-BLANK SPRAY", "TRIPLE KILL", "Player_22", "bio_snow_na2", 4),
    ("clip_05.mp4", 0, 70, [27, 47], "KILL STREAK 05", "M4A1 CARBINE DOUBLE", "DOUBLE HS", "Player_8", "bio_oldhouse", 5),
    ("clip_06.mp4", 0, 80, [27, 49], "KILL STREAK 06", "M4A1 SILENCED HEADSHOTS", "DOUBLE HS", "Player_21", "bio_arena_fl", 6),
    ("clip_07.mp4", 0, 125, [27, 114], "KILL STREAK 07", "HE GRENADE WIPEOUT", "3X GRENADE", "Player_15", "bio_snow_na2", 7),
    ("clip_08.mp4", 0, 165, [27, 93], "KILL STREAK 08", "HE GRENADE INVASION STOP", "4X GRENADE", "Player_2", "bio_ziger_azt", 8),
    ("clip_09.mp4", 0, 175, [27, 121], "KILL STREAK 09", "IDF GALIL HEADSHOT DEFENSE", "TRIPLE HS", "Player_6", "zm_biohazard_base_mx004", 9),
    ("clip_10.mp4", 0, 175, [27, 121], "KILL STREAK 10", "UMP45, GRENADE & USP", "TRIPLE KILL", "Player_21", "bio_valak", 10),
    ("clip_11.mp4", 0, 175, [27, 156], "KILL STREAK 11", "M4A1 CARVED HEADSHOTS", "TRIPLE KILL", "Player_12", "zm_restart_v3", 11),
    ("clip_12.mp4", 0, 100, [27], "KILL STREAK 12", "XM1014 AUTO-SHOTGUN PUMP", "DOUBLE HS", "Player_1", "zm_2day_rbt_f4", 12),
]

total = sum(c[2] - c[1] for c in clips_specs)
print("Total gameplay frames:", total)
