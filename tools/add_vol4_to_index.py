import os, re

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

VOL4_HERO_HTML = """
    <!-- ==================== VOLUME 4 MONTAGE (ULTRA ACTION) ==================== -->
    <div class="montage-hero vol4">
        <div class="montage-header">
            <div class="montage-title">
                <span class="montage-badge vol4-badge">VOLUME 4</span>
                <span class="montage-badge kills">33 KILLS / 16 RAPID STREAKS</span>
                <span class="montage-badge ultra-badge">⚡ ULTRA KILL-DENSITY</span>
                <span>🔥 EvilShtrib 60s Promo — Volume 4 (Zero Dead Time Edition)</span>
            </div>
            <div class="montage-music">
                🎵 Alexi Action & Dedpled — <em>Negative (Phonk House)</em> [CC BY 3.0]
            </div>
        </div>
        <div class="montage-video-box">
            <video controls preload="metadata">
                <source src="final_videos/EvilShtrib_60s_Vol4.mp4" type="video/mp4">
                Ваш браузер не поддерживает встроенное воспроизведение видео.
            </video>
        </div>
        <div class="montage-footer">
            <div class="montage-spec">
                <strong>Длительность:</strong> ровно 60.0 сек (1800 кадров @ 30 FPS) | <strong>Разрешение:</strong> 1280x720 HD<br>
                <strong>Плотность экшена:</strong> 33 подтвержденных фрага в 16 сериях (все фраги происходят за &le;1.8 сек!)<br>
                <strong>Динамика:</strong> 0% беготни, 0% пустой стрельбы — фраги точно по центру каждого 3.3-секундного отрезка.<br>
                <strong>Форматы:</strong> Доступны горизонтальная 16:9 HD и вертикальная 9:16 Reels версии.<br>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <a class="download-btn" href="final_videos/EvilShtrib_60s_Vol4.mp4" download>📥 Скачать Volume 4 (16:9 HD)</a>
                    <a class="download-btn reels-btn" href="final_videos/EvilShtrib_60s_Vol4_9x16.mp4" download>📱 Скачать Volume 4 (9:16 Reels)</a>
                </div>
            </div>
            <div class="montage-spec">
                <strong>Карты, фраги и оружие (Volume 4):</strong><br>
                <span class="fx-tag">bio_dusty_2x2_fl: Dk-Unknown (UMP45, 0.21s)</span>
                <span class="fx-tag">bio_heat_rb2: Fat Matt (XM1014 Auto-Shotgun, 0.27s)</span>
                <span class="fx-tag">bio_resident_beta: shooterman (Dual Elites, 0.41s)</span>
                <span class="fx-tag">bio_horror_box_ff: aliendewd1 (UMP45 Double HS, 0.58s)</span>
                <span class="fx-tag">bio_horror_box_ff: Dk-Unknown (SG550 Sniper, 0.72s)</span>
                <span class="fx-tag">bio_blocks_rb5: Dk-Unknown (USP Tactical, 0.75s)</span>
                <span class="fx-tag">bio_evil_dust_fl: aliendewd1 (M4A1 Carbine, 0.81s)</span>
                <span class="fx-tag">bio_resident_beta: HappyKiD (TMP SMG Double HS, 0.89s)</span>
                <span class="fx-tag">bio_horror_box_ff: shooterman (UMP45, 0.90s)</span>
                <span class="fx-tag">bio_green_peaks_rb7: aliendewd1 (SG552 Commando HS, 0.96s)</span>
                <span class="fx-tag">bio_cube_rb3: HappyKiD (Dual Elites, 1.09s)</span>
                <span class="fx-tag">bio_heat_rb2: kingkilla (SG550 Sniper, 1.45s)</span>
                <span class="fx-tag">bio_resident_beta: Fat Matt (USP Tactical, 1.46s)</span>
                <span class="fx-tag">bio_blocks_rb5: Player_9 (SG550 Double HS, 1.57s)</span>
                <span class="fx-tag">bio_green_peaks_rb7: kingkilla (SG552 Commando, 1.91s)</span>
                <span class="fx-tag">bio_resident_beta: Dk-Unknown (SG550 Triple Kill, 1.81s)</span>
            </div>
        </div>
    </div>
"""

def update_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Add vol4 styles
    style_addition = """
        .montage-hero.vol4 {
            border-color: #ff0055;
            box-shadow: 0 0 35px rgba(255, 0, 85, 0.4);
        }
        .montage-hero.vol4 .montage-header {
            background: rgba(255, 0, 85, 0.12);
            border-bottom: 1px solid rgba(255, 0, 85, 0.3);
        }
        .montage-badge.vol4-badge {
            background: #ff0055;
        }
        .montage-badge.ultra-badge {
            background: #ffaa00;
            color: #000;
        }
        .download-btn.reels-btn:hover {
            border-color: #ff0055;
            color: #ff0055;
            box-shadow: 0 0 10px rgba(255, 0, 85, 0.5);
        }
    """
    
    if ".montage-hero.vol4" not in content:
        content = content.replace("</style>", style_addition + "\n    </style>")
        
    # Insert Volume 4 before Volume 2
    if "<!-- ==================== VOLUME 4 MONTAGE (ULTRA ACTION) ==================== -->" not in content:
        target = "<!-- ==================== VOLUME 2 MONTAGE ==================== -->"
        content = content.replace(target, VOL4_HERO_HTML + "\n    " + target)
        
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Successfully updated index.html with Volume 4!")

if __name__ == "__main__":
    update_index()
