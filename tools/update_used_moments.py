import os

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
path = os.path.join(BASE_DIR, "USED_MOMENTS.md")

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

v7_marker = "## EvilShtrib Volume 7"
idx = text.find(v7_marker)
if idx != -1:
    new_v7 = """## EvilShtrib Volume 7 (`final_videos/EvilShtrib_60s_Vol7.mp4`) - Definitive Pure Action Edition

* **Длительность:** 60.00с (1800 кадров @ 30 FPS)
* **Графика:** Полное визуальное оформление восстановлено на всю длину ролика (анимированное интро 3.0с, постоянный бейдж сервера 185.225.201.113:27015 в левом верхнем углу, динамическая плашка KILL STREAK в левом нижнем углу с индикацией фрагов, анимированное оутро 4.0с).
* **Камера и качество:** 100% вид от первого лица Людей (CT, 0% зомби, 0% стен, 0% пустых коридоров). В каждом клипе нападающие зомби находятся непосредственно в прицеле игрока, видна вспышка выстрелов, кровь и подтвержденное уничтожение в киллфиде.
* **Музыка:** Alexi Action & Dedpled — "Negative" (Phonk House, CC-BY 3.0)

| # | Клип | Карта | Стрелок | Оружие | Серия / Тег |
|---|---|---|---|---|---|
| 01 | `clips/clip_01.mp4` | bio_colors | Shadow-Death | SIG SG550 AUTO-SNIPER | SNIPER HEADSHOT |
| 02 | `clips/clip_03.mp4` | bio_colors | thesofafox | H&K UMP-45 SMG | CORRIDOR HOLD |
| 03 | `clips/clip_05.mp4` | bio_colors | blueguile | H&K UMP-45 SMG | DOUBLE KILL |
| 04 | `clips/clip_06.mp4` | bio_colors | blueguile | H&K UMP-45 SMG | RAPID BURST |
| 05 | `clips/clip_08.mp4` | bio_colors | blueguile | SIG SG550 AUTO-SNIPER | ELITE HEADSHOT |
| 06 | `clips/clip_09.mp4` | bio_colors | BDM-WhiteViper | .40 DUAL ELITES | DUAL SPRAY |
| 07 | `clips_hyper/clip_01.mp4` | bio_crisis | [Zap Master] BSN | SIG SG550 AUTO-SNIPER | BUNKER DEFENSE |
| 08 | `clips_hyper/clip_09.mp4` | bio_crisis | solo | COLT M4A1 CARBINE | HEV EXECUTION |
| 09 | `clips_vol6/clip_06.mp4` | bio_india_b2_ | Dk-Unknown | STEYR AUG BULLPUP | RAPID BURST |
| 10 | `clips_vol6/clip_07.mp4` | bio_resident_beta | Dk-Unknown | SIG SG552 COMMANDO | DOUBLE TAP |
| 11 | `clips_vol6/clip_10.mp4` | bio_re-ziger | Dk-Unknown | H&K UMP-45 SMG | WALL PIN DOUBLE |
| 12 | `clips_vol6/clip_14.mp4` | bio_lego_ez | Dk-Unknown | .40 DUAL ELITES | CANAL BARRAGE |
| 13 | `clips_vol6/clip_15.mp4` | bio_re-ziger | Dk-Unknown | FN M249 PARA SAW | SAW SPRAYDOWN |
| 14 | `clips_vol5/clip_10.mp4` | bio_blocks_pro | Dk-Unknown | STEYR SCOUT SNIPER | 2x HEADSHOT |
| 15 | `clips_vol3/clip_05.mp4` | bio_dust2 | Dk-Unknown | STEYR SCOUT SNIPER | SNIPER FLICK |
| 16 | `clips_vol3/clip_08.mp4` | bio_dust2 | Dk-Unknown | D3/AU-1 AUTO-SNIPER | CLUTCH DOUBLE |
"""
    text = text[:idx] + new_v7
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("USED_MOMENTS.md updated successfully")
