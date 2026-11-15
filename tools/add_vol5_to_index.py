import os, re

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

VOL5_HERO_HTML = """
    <!-- ==================== VOLUME 5 MONTAGE (100% VERIFIED ACTION) ==================== -->
    <div class="montage-hero vol5">
        <div class="montage-header">
            <div class="montage-title">
                <span class="montage-badge vol5-badge">VOLUME 5</span>
                <span class="montage-badge kills">32 KILLS / 16 STREAKS</span>
                <span class="montage-badge verified-badge">✅ 100% KILLFEED VERIFIED</span>
                <span class="montage-badge ultra-badge">⚡ ZERO DEAD TIME</span>
                <span>🔥 EvilShtrib 60s Promo — Volume 5 (Definitive Pure Action Edition)</span>
            </div>
            <div class="montage-music">
                🎵 Alexi Action & Dedpled — <em>Negative (Phonk House)</em> [CC BY 3.0]
            </div>
        </div>
        <div class="montage-video-box">
            <video controls preload="metadata">
                <source src="final_videos/EvilShtrib_60s_Vol5.mp4" type="video/mp4">
                Ваш браузер не поддерживает встроенное воспроизведение видео.
            </video>
        </div>
        <div class="montage-footer">
            <div class="montage-spec">
                <strong>Длительность:</strong> ровно 60.0 сек (1800 кадров @ 30 FPS) | <strong>Разрешение:</strong> 1280x720 HD<br>
                <strong>Плотность экшена:</strong> 32 подтвержденных фрага в 16 сериях (все фраги с интервалом &le;2.25 сек!)<br>
                <strong>Автоматическая проверка:</strong> 100% клипов проверены сканером киллфида — каждый фрагмент содержит подтвержденные убийства в 80–99% кадров!<br>
                <strong>Никакой беготни и темноты:</strong> фраги начинаются с первых секунд и идут непрерывно до финала.<br>
                <strong>Форматы:</strong> Доступны горизонтальная 16:9 HD и вертикальная 9:16 Reels версии.<br>
                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px;">
                    <a class="download-btn" href="final_videos/EvilShtrib_60s_Vol5.mp4" download>📥 Скачать Volume 5 (16:9 HD)</a>
                    <a class="download-btn reels-btn" href="final_videos/EvilShtrib_60s_Vol5_9x16.mp4" download>📱 Скачать Volume 5 (9:16 Reels)</a>
                </div>
            </div>
            <div class="montage-spec" style="margin-top: 10px;">
                <strong>Карты, стрелки и оружие (Volume 5 — 100% киллы):</strong><br>
                <span class="fx-tag">bio_blocks_pro: Galdalfus (SIG SG550 Auto-Sniper, 0.38s) [99/99 килл-кадров]</span>
                <span class="fx-tag">bio_re-ziger: HappyKiD (H&K MP5-Navy 9mm, 0.95s) [89/99]</span>
                <span class="fx-tag">bio_omega_b2: HappyKiD (Clarion 5.56 FAMAS, 0.99s) [92/99]</span>
                <span class="fx-tag">bio_blocks_pro: Fat Matt (FN M249 Para SAW, 1.01s) [96/99]</span>
                <span class="fx-tag">bio_blocks_pro: kingkilla (SIG SG550 Auto-Sniper, 1.10s) [97/99]</span>
                <span class="fx-tag">bio_india_b2_: HappyKiD (Steyr Scout Sniper, 1.34s) [84/99]</span>
                <span class="fx-tag">bio_nova_b2: aliendewd1 (D3/AU-1 G3SG1, 1.37s) [93/99]</span>
                <span class="fx-tag">bio_resident_beta: aliendewd1 (D3/AU-1 G3SG1, 1.54s) [90/99]</span>
                <span class="fx-tag">bio_mono_b1: aliendewd1 (D3/AU-1 G3SG1, 1.54s) [88/99]</span>
                <span class="fx-tag">bio_blocks_pro: Dk-Unknown (Steyr Scout 2x HS, 1.57s) [89/99]</span>
                <span class="fx-tag">bio_re-ziger: kingkilla (Colt M4A1 Carbine, 1.73s) [86/99]</span>
                <span class="fx-tag">bio_re-ziger: Fat Matt (.40 Dual Elites, 1.85s) [90/99]</span>
                <span class="fx-tag">bio_re-ziger: pyr0` (Leone 12 Gauge Super M3, 1.99s) [81/99]</span>
                <span class="fx-tag">bio_dusty_2x2_fl: Fat Matt (HE Grenade / MAC-10, 2.22s) [89/99]</span>
                <span class="fx-tag">bio_nova_b2: [SMUT]DarkDruid (Night Hawk .50C Deagle, 2.22s) [80/102]</span>
                <span class="fx-tag">bio_blocks_pro: pyr0` (IDF Defender Galil, 2.24s) [84/102]</span>
            </div>
        </div>
    </div>
"""

VOL5_CSS = """
        .montage-hero.vol5 {
            border-color: #00ff88;
            box-shadow: 0 0 45px rgba(0, 255, 136, 0.3);
        }
        .montage-hero.vol5 .montage-header {
            background: linear-gradient(90deg, rgba(0, 255, 136, 0.22), rgba(15, 23, 42, 0.85));
            border-bottom: 1px solid rgba(0, 255, 136, 0.4);
        }
        .montage-badge.vol5-badge {
            background: #00ff88;
            color: #05140b;
            font-weight: 900;
        }
        .montage-badge.verified-badge {
            background: #10b981;
            color: #ffffff;
            font-weight: 700;
        }
"""

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Add CSS before </style>
if ".montage-hero.vol5" not in content:
    content = content.replace("</style>", VOL5_CSS + "\n    </style>")

# Insert VOL5 hero before VOL4 hero
if "VOLUME 5 MONTAGE" not in content:
    content = content.replace("<!-- ==================== VOLUME 4 MONTAGE (ULTRA ACTION) ==================== -->", VOL5_HERO_HTML + "\n    <!-- ==================== VOLUME 4 MONTAGE (ULTRA ACTION) ==================== -->")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html with Volume 5 successfully!")
