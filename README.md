# EvilShtrib Highlights (CS 1.6)

Автоматическая система анализа HLTV-демозаписей сервера **EvilShtrib**, детекции ярких моментов уничтожения зомби и рендеринга 5–10 секундных клипов от **первого лица (`First-Person` / `In-Eye`)** с нормальной скоростью **1.0x**.

---

## 🎬 Топ-10 Моментов (First-Person, 1.0x)

| Клип | Игрок | Оружие | Карта | Длительность | Очки | Уничтоженные зомби |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **#01** | [Shadow-Death](clips/clip_01.mp4) | `SG550` | `bio_asalto_f` | 9.5s | 120 | Helios (sg550), Death Knight (sg550) |
| **#02** | [Death Knight](clips/clip_02.mp4) | `AWP` `HEADSHOT` | `bio_arena_fl` | 5.5s | 115 | thesofafox (awp) |
| **#03** | [thesofafox](clips/clip_03.mp4) | `AWP` `HEADSHOT` | `zm_colors_rb3` | 5.5s | 115 | Zombie_10 (awp) |
| **#04** | [shooterman](clips/clip_04.mp4) | `MP5NAVY` | `bio_$2000$_rbs_f2` | 9.5s | 110 | Shadow-Death (mp5navy), BDM-WhiteViper (mp5navy) |
| **#05** | [Death Knight](clips/clip_05.mp4) | `UMP45` | `bio_arena_fl` | 6.6s | 110 | shooterman (ump45), Helios (ump45) |
| **#06** | [blueguile](clips/clip_06.mp4) | `DEAGLE` `HEADSHOT` | `bio_arena_fl` | 5.5s | 105 | Zombie_10 (deagle) |
| **#07** | [BDM-WhiteViper](clips/clip_07.mp4) | `DEAGLE` `HEADSHOT` | `bio_blocks_pro` | 5.5s | 105 | Dk-Unknown (deagle) |
| **#08** | [blueguile](clips/clip_08.mp4) | `SCOUT` `HEADSHOT` | `bio_$2000$_rbs_f2` | 5.5s | 100 | Helios (scout) |
| **#09** | [Dk-Unknown](clips/clip_09.mp4) | `M3` `HEADSHOT` | `bio_$2000$_rbs_f2` | 5.5s | 100 | thesofafox (m3) |
| **#10** | [Helios](clips/clip_10.mp4) | `XM1014` `HEADSHOT` | `bio_2000_x_kizaki` | 5.5s | 100 | shooterman (xm1014) |

---

## ⚙️ Устраненные дефекты и улучшения

1. **Исправлена скорость воспроизведения (1.0x Normal Speed):**
   - Установлен `host_framerate 0.03333333` ($1/30$ сек на движковый кадр) перед стартом `startmovie`, что синхронизировало каждый отрендеренный кадр с внутренним временем движка CS 1.6. Видео больше не ускорено в 5–10 раз, а идет с естественной скоростью геймплея.
2. **Вид строго от первого лица (`OBS_IN_EYE`):**
   - Отключен авто-директор (`spec_autodirector 0`, `spec_autodirector_internal 0`), предотвращающий сброс в вид сверху.
   - Активирован режим `spec_mode 4 0` (In-Eye view).
   - Точное циклирование по слотам живых игроков переключает камеру непосредственно на стрелка (`killer_id`), отображая оружие в руках, прицел и сам момент выстрелов/убийства.
3. **Совместимость с Google Chrome и веб-плеерами:**
   - Кодирование в **H.264 (libx264)** с профилем `main`, цветовым пространством `yuv420p` и флагом `+faststart` (перемещение атома `moov` в начало файла). Все ролики мгновенно открываются и воспроизводятся в Chrome без задержек.
4. **Коррекция гаммы и яркости:**
   - На темных картах (`bio_asalto_f`, `bio_arena_fl`) применен фильтр цветокоррекции `eq=gamma=1.4:contrast=1.15:brightness=0.04`, делающий сцену четкой и контрастной.

---

## 🚀 Запуск и просмотр

1. **Просмотр клипов:**
   Откройте [index.html](index.html) в Google Chrome или любом современном браузере.
2. **Перегенерация клипов:**
   ```powershell
   python tools/render_clips.py
   ```
