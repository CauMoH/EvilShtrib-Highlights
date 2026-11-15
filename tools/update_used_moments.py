import json, os

with open(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\verified_vol6.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

lines = []
lines.append('\n---\n')
lines.append('## EvilShtrib Volume 6 (`final_videos/EvilShtrib_60s_Vol6.mp4`)\n')
lines.append('* **Длительность:** 60.00с (1800 кадров @ 30 FPS)')
lines.append('* **Количество фрагов:** 32 (100% экшен от первого лица, вид строго из глаз людей)')
lines.append('* **Музыка:** Andrew Codeman - "Run" (Breakbeat/Electronic, CC-BY 3.0)')
lines.append('* **Особенность:** 100% вид от лица Людей (Counter-Terrorists). Камера spectate строго от первого лица (spec_mode 4 0) с оружием в руках, перекрестием и синим HUD людей. Полное исключение ракурсов от лица зомби (0% зомби).\n')
lines.append('| # | Демка | Карта | Стрелок | Таймкод (сек) | Оружие | Кол-во фрагов |')
lines.append('|---|---|---|---|---|---|---|')

for i, v in enumerate(items, 1):
    t_start = max(1.0, v['time'] - 1.68)
    t_end = t_start + 3.73
    w = v['wpn'].upper()
    lines.append(f"| {i:02d} | `{v['demo']}` | {v['map']} | {v['killer']} | {t_start:.1f} - {t_end:.1f} | {w} | {v['kills']} (span {v['span']:.2f}s) |")

out_text = '\n'.join(lines) + '\n'

with open(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\USED_MOMENTS.md', 'a', encoding='utf-8') as f:
    f.write(out_text)

print('Appended Volume 6 to USED_MOMENTS.md successfully!')
