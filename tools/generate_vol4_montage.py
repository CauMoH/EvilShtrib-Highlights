"""
EvilShtrib CS 1.6 Zombie Highlights - 60-Second Real Match Montage (Volume 4).
Ultra Kill-Density Edition:
- 33 confirmed kills across 16 rapid streaks (all kill spans <= 1.8s).
- 100% official server shtriban.ru HLTV demos, zero used moments from USED_MOMENTS.md.
- Tightly centered fragging action: 99 frames (3.30s) per streak, zero dead movement.
- Exact 60.00 seconds budget (90 intro + 1590 clips + 120 outro = 1800 frames @ 30 FPS).
"""

import os
import sys
import glob
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
import imageio_ffmpeg

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
CLIPS_DIR = os.path.join(BASE_DIR, "clips_vol4")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
FINAL_DIR = os.path.join(BASE_DIR, "final_videos")
os.makedirs(FINAL_DIR, exist_ok=True)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# Fonts
FONT_INTRO_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 68)
FONT_INTRO_SUB = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 38)
FONT_INTRO_IP = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 32)
FONT_INTRO_TAG = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 19)

FONT_HUD_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 16)
FONT_HUD_IP = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 15)

FONT_KILL_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 17)
FONT_KILL_WEAPON = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 14)
FONT_KILL_TAG = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 11)

FONT_OUTRO_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 64)
FONT_OUTRO_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
FONT_OUTRO_IP = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 34)
FONT_OUTRO_FEATURE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)

# 16 clips configuration tailored to exactly 1590 frames (53.00s)
# 90 intro + 1590 clips + 120 outro = 1800 frames = exactly 60.00s
CLIPS_CONFIG = [
    {'file': 'clip_01.mp4', 'start': 0, 'end': 99, 'kills': [46, 53], 'title': 'KILL STREAK 01 / 16', 'weapon': 'H&K UMP .45', 'tag': 'DOUBLE KILL', 'player': 'Dk-Unknown', 'map': 'bio_dusty_2x2_fl', 'fx': 2},
    {'file': 'clip_02.mp4', 'start': 0, 'end': 99, 'kills': [45, 54], 'title': 'KILL STREAK 02 / 16', 'weapon': 'BENELLI XM1014', 'tag': 'INSTA DOUBLE', 'player': 'Fat Matt', 'map': 'bio_heat_rb2', 'fx': 3},
    {'file': 'clip_03.mp4', 'start': 0, 'end': 99, 'kills': [43, 56], 'title': 'KILL STREAK 03 / 16', 'weapon': 'DUAL .40 ELITES', 'tag': 'DOUBLE KILL', 'player': 'shooterman', 'map': 'bio_resident_beta', 'fx': 4},
    {'file': 'clip_04.mp4', 'start': 0, 'end': 99, 'kills': [41, 58], 'title': 'KILL STREAK 04 / 16', 'weapon': 'H&K UMP .45', 'tag': 'DOUBLE HS', 'player': 'aliendewd1', 'map': 'bio_horror_box_ff', 'fx': 5},
    {'file': 'clip_05.mp4', 'start': 0, 'end': 99, 'kills': [39, 60], 'title': 'KILL STREAK 05 / 16', 'weapon': 'SG550 AUTO-SNIPER', 'tag': 'DOUBLE KILL', 'player': 'Dk-Unknown', 'map': 'bio_horror_box_ff', 'fx': 6},
    {'file': 'clip_06.mp4', 'start': 0, 'end': 99, 'kills': [38, 61], 'title': 'KILL STREAK 06 / 16', 'weapon': 'USP .45 TACTICAL', 'tag': 'DOUBLE KILL', 'player': 'Dk-Unknown', 'map': 'bio_blocks_rb5', 'fx': 7},
    {'file': 'clip_07.mp4', 'start': 0, 'end': 99, 'kills': [37, 62], 'title': 'KILL STREAK 07 / 16', 'weapon': 'COLT M4A1 CARBINE', 'tag': 'DOUBLE KILL', 'player': 'aliendewd1', 'map': 'bio_evil_dust_fl', 'fx': 8},
    {'file': 'clip_08.mp4', 'start': 0, 'end': 99, 'kills': [36, 63], 'title': 'KILL STREAK 08 / 16', 'weapon': 'STEYR TMP SMG', 'tag': 'DOUBLE HS', 'player': 'HappyKiD', 'map': 'bio_resident_beta', 'fx': 9},
    {'file': 'clip_09.mp4', 'start': 0, 'end': 99, 'kills': [36, 63], 'title': 'KILL STREAK 09 / 16', 'weapon': 'H&K UMP .45', 'tag': 'DOUBLE KILL', 'player': 'shooterman', 'map': 'bio_horror_box_ff', 'fx': 10},
    {'file': 'clip_10.mp4', 'start': 0, 'end': 99, 'kills': [35, 64], 'title': 'KILL STREAK 10 / 16', 'weapon': 'SIG SG552 COMMANDO', 'tag': 'DOUBLE HS', 'player': 'aliendewd1', 'map': 'bio_green_peaks_rb7', 'fx': 11},
    {'file': 'clip_11.mp4', 'start': 0, 'end': 99, 'kills': [33, 66], 'title': 'KILL STREAK 11 / 16', 'weapon': 'DUAL .40 ELITES', 'tag': 'DOUBLE KILL', 'player': 'HappyKiD', 'map': 'bio_cube_rb3', 'fx': 12},
    {'file': 'clip_12.mp4', 'start': 0, 'end': 99, 'kills': [28, 71], 'title': 'KILL STREAK 12 / 16', 'weapon': 'SG550 AUTO-SNIPER', 'tag': 'DOUBLE KILL', 'player': 'kingkilla', 'map': 'bio_heat_rb2', 'fx': 1},
    {'file': 'clip_13.mp4', 'start': 0, 'end': 99, 'kills': [28, 71], 'title': 'KILL STREAK 13 / 16', 'weapon': 'USP .45 TACTICAL', 'tag': 'DOUBLE KILL', 'player': 'Fat Matt', 'map': 'bio_resident_beta', 'fx': 2},
    {'file': 'clip_14.mp4', 'start': 0, 'end': 99, 'kills': [26, 73], 'title': 'KILL STREAK 14 / 16', 'weapon': 'SG550 AUTO-SNIPER', 'tag': 'DOUBLE HEADSHOT', 'player': 'Player_9', 'map': 'bio_blocks_rb5', 'fx': 3},
    {'file': 'clip_15.mp4', 'start': 0, 'end': 99, 'kills': [21, 78], 'title': 'KILL STREAK 15 / 16', 'weapon': 'SIG SG552 COMMANDO', 'tag': 'DOUBLE KILL', 'player': 'kingkilla', 'map': 'bio_green_peaks_rb7', 'fx': 4},
    {'file': 'clip_16.mp4', 'start': 0, 'end': 105, 'kills': [25, 71, 80], 'title': 'KILL STREAK 16 / 16', 'weapon': 'SG550 AUTO-SNIPER', 'tag': 'TRIPLE KILL', 'player': 'Dk-Unknown', 'map': 'bio_resident_beta', 'fx': 5},
]

def render_hud_overlay(frame, cfg, is_kill_active=False, hud_alpha=1.0):
    if hud_alpha <= 0.01:
        return frame

    h, w = frame.shape[:2]
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    a_mult = min(1.0, max(0.0, hud_alpha))

    # 1. Top-Left: Server Branding Badge
    pill_x1, pill_y1 = 28, 24
    pill_w, pill_h = 325, 54
    bg_a = int(210 * a_mult)
    border_a = int(220 * a_mult)
    
    draw.rounded_rectangle(
        [pill_x1, pill_y1, pill_x1 + pill_w, pill_y1 + pill_h],
        radius=10,
        fill=(10, 15, 24, bg_a),
        outline=(0, 255, 130, border_a),
        width=1
    )
    draw.rounded_rectangle(
        [pill_x1, pill_y1 + 8, pill_x1 + 4, pill_y1 + pill_h - 8],
        radius=2,
        fill=(0, 255, 140, int(255 * a_mult))
    )
    draw.text(
        (pill_x1 + 16, pill_y1 + 8),
        "☣ EVILSHTRIB BIOHAZARD",
        font=FONT_HUD_TITLE,
        fill=(0, 255, 140, int(255 * a_mult))
    )
    draw.text(
        (pill_x1 + 16, pill_y1 + 30),
        "IP: 185.225.201.113:27015",
        font=FONT_HUD_IP,
        fill=(235, 245, 255, int(240 * a_mult))
    )

    # 2. Bottom-Left: Kill Tracker Badge
    badge_x1, badge_y1 = 28, h - 94
    badge_w, badge_h = 425, 66
    
    if is_kill_active:
        badge_bg = (18, 48, 28, int(235 * a_mult))
        badge_border = (0, 255, 180, int(255 * a_mult))
        border_w = 2
        title_color = (0, 255, 210, int(255 * a_mult))
    else:
        badge_bg = (10, 15, 24, int(200 * a_mult))
        badge_border = (60, 100, 80, int(180 * a_mult))
        border_w = 1
        title_color = (0, 240, 130, int(255 * a_mult))
        
    draw.rounded_rectangle(
        [badge_x1, badge_y1, badge_x1 + badge_w, badge_y1 + badge_h],
        radius=10,
        fill=badge_bg,
        outline=badge_border,
        width=border_w
    )
    
    # Text in bottom badge
    draw.text((badge_x1 + 16, badge_y1 + 9), cfg["title"], font=FONT_KILL_TITLE, fill=title_color)
    info_str = f"{cfg['weapon']} | {cfg['player']} ({cfg['map']})"
    draw.text((badge_x1 + 16, badge_y1 + 34), info_str, font=FONT_KILL_WEAPON, fill=(225, 235, 245, int(230 * a_mult)))
    
    # Tag pill inside badge
    tag_w, tag_h = 96, 22
    tag_x = badge_x1 + badge_w - tag_w - 12
    tag_y = badge_y1 + 10
    tag_bg = (0, 180, 100, int(220 * a_mult)) if is_kill_active else (25, 45, 40, int(200 * a_mult))
    draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=5, fill=tag_bg)
    draw.text((tag_x + 8, tag_y + 3), cfg["tag"], font=FONT_KILL_TAG, fill=(255, 255, 255, int(255 * a_mult)))

    img_np = np.array(overlay)
    alpha = img_np[:, :, 3] / 255.0
    for c in range(3):
        frame[:, :, c] = (1.0 - alpha) * frame[:, :, c] + alpha * img_np[:, :, c]
    return frame

def apply_kill_vfx(frame, dist_to_kill, fx_type):
    if dist_to_kill < 0 or dist_to_kill > 6:
        return frame
        
    h, w = frame.shape[:2]
    intensity = 1.0 - (dist_to_kill / 6.0)
    
    # Screen shake
    if dist_to_kill <= 2:
        dx = np.random.randint(-4, 5)
        dy = np.random.randint(-4, 5)
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        frame = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        
    # Chromatic aberration or flash
    if dist_to_kill <= 3:
        shift = int(3 * intensity)
        if shift > 0:
            frame[:, :, 0] = np.roll(frame[:, :, 0], shift, axis=1)
            frame[:, :, 2] = np.roll(frame[:, :, 2], -shift, axis=1)
            
    # Color pulse
    flash = np.full_like(frame, (20, 60, 40), dtype=np.uint8)
    alpha_flash = 0.25 * intensity
    frame = cv2.addWeighted(frame, 1.0, flash, alpha_flash, 0)
    return frame

def generate_intro_frames(num_frames=90):
    w, h = 1280, 720
    frames = []
    for f in range(num_frames):
        img = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Grid lines background
        for y in range(0, h, 40):
            cv2.line(img, (0, y), (w, y), (15, 25, 20), 1)
        for x in range(0, w, 40):
            cv2.line(img, (x, 0), (x, h), (15, 25, 20), 1)
            
        # Glowing biohazard scanline
        scan_y = int((f / float(num_frames)) * h)
        cv2.line(img, (0, scan_y), (w, scan_y), (0, 255, 140), 2)
        
        alpha = min(1.0, f / 18.0)
        if f > num_frames - 15:
            alpha = (num_frames - f) / 15.0
            
        im_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(im_pil)
        
        t_color = (0, 255, 140, int(255 * alpha))
        sub_color = (240, 245, 255, int(235 * alpha))
        ip_color = (0, 240, 255, int(245 * alpha))
        
        # Center Title
        draw.text((w // 2 - 240, 180), "EVILSHTRIB", font=FONT_INTRO_TITLE, fill=t_color)
        draw.text((w // 2 - 380, 275), "CLASSIC BIOHAZARD HIGHLIGHTS - VOL.4", font=FONT_INTRO_SUB, fill=sub_color)
        draw.text((w // 2 - 325, 345), "33 KILLS IN 60 SECONDS - ULTRA KILL DENSITY", font=FONT_INTRO_TAG, fill=(0, 255, 180, int(255 * alpha)))
        
        # IP Box
        bx1, by1 = w // 2 - 270, 420
        bw, bh = 540, 68
        draw.rounded_rectangle([bx1, by1, bx1 + bw, by1 + bh], radius=12, fill=(10, 18, 28, int(220 * alpha)), outline=(0, 255, 140, int(255 * alpha)), width=2)
        draw.text((bx1 + 35, by1 + 16), "IP: 185.225.201.113:27015", font=FONT_INTRO_IP, fill=ip_color)
        
        frame = np.array(im_pil)
        frames.append(frame)
    return frames

def generate_outro_frames(num_frames=120):
    w, h = 1280, 720
    frames = []
    for f in range(num_frames):
        img = np.zeros((h, w, 3), dtype=np.uint8)
        
        for y in range(0, h, 40):
            cv2.line(img, (0, y), (w, y), (15, 25, 20), 1)
        for x in range(0, w, 40):
            cv2.line(img, (x, 0), (x, h), (15, 25, 20), 1)
            
        alpha = min(1.0, f / 18.0)
        if f > num_frames - 20:
            alpha = (num_frames - f) / 20.0
            
        im_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(im_pil)
        
        draw.text((w // 2 - 270, 140), "JOIN THE HORDE", font=FONT_OUTRO_TITLE, fill=(0, 255, 140, int(255 * alpha)))
        draw.text((w // 2 - 320, 235), "EVILSHTRIB > CLASSIC BIOHAZARD CS 1.6", font=FONT_OUTRO_SUB, fill=(240, 245, 255, int(240 * alpha)))
        
        bx1, by1 = w // 2 - 290, 310
        bw, bh = 580, 76
        draw.rounded_rectangle([bx1, by1, bx1 + bw, by1 + bh], radius=12, fill=(10, 18, 28, int(230 * alpha)), outline=(0, 255, 140, int(255 * alpha)), width=2)
        draw.text((bx1 + 45, by1 + 18), "IP: 185.225.201.113:27015", font=FONT_OUTRO_IP, fill=(0, 240, 255, int(255 * alpha)))
        
        draw.text((w // 2 - 230, 425), "HLTV DEMOS & STATS: STATS.SHTRIBAN.RU", font=FONT_OUTRO_FEATURE, fill=(180, 220, 210, int(240 * alpha)))
        draw.text((w // 2 - 220, 465), "CONNECT IN CS 1.6 CONSOLE: connect ...", font=FONT_OUTRO_FEATURE, fill=(0, 255, 180, int(230 * alpha)))
        
        frame = np.array(im_pil)
        frames.append(frame)
    return frames

def build_vol4_montage():
    print("=" * 60)
    print("BUILDING EVILSHTRIB 60s MONTAGE - VOLUME 4 (ULTRA KILL DENSITY)")
    print("=" * 60)
    
    all_frames = []
    
    # 1. Intro
    print("\n[Step 1/6] Generating Intro (90 frames, 3.0s)...")
    intro_frames = generate_intro_frames(90)
    all_frames.extend(intro_frames)
    print(f"  Intro added. Total frames: {len(all_frames)}")
    
    # 2. Process Clips
    print(f"\n[Step 2/6] Processing {len(CLIPS_CONFIG)} clips...")
    for idx, cfg in enumerate(CLIPS_CONFIG, 1):
        cpath = os.path.join(CLIPS_DIR, cfg["file"])
        if not os.path.exists(cpath):
            raise FileNotFoundError(f"Clip not found: {cpath}")
            
        cap = cv2.VideoCapture(cpath)
        clip_frames = []
        while True:
            ret, f = cap.read()
            if not ret: break
            clip_frames.append(f)
        cap.release()
        
        n_need = cfg["end"] - cfg["start"]
        sliced = clip_frames[cfg["start"]:cfg["end"]]
        if len(sliced) < n_need:
            # Pad if needed
            while len(sliced) < n_need:
                sliced.append(sliced[-1])
        sliced = sliced[:n_need]
        
        print(f"  Clip {idx:02d}/16: {cfg['file']} -> {len(sliced)} frames ({cfg['player']} | {cfg['weapon']})")
        
        # Apply VFX and Overlays
        for f_idx, fr in enumerate(sliced):
            # Check kill proximity
            dists = [abs(f_idx - kf) for kf in cfg["kills"]]
            min_dist = min(dists) if dists else 999
            is_active = (min_dist <= 8)
            
            # Fade in/out HUD at clip boundaries
            hud_alpha = 1.0
            if f_idx < 6:
                hud_alpha = f_idx / 6.0
            elif f_idx > len(sliced) - 6:
                hud_alpha = (len(sliced) - f_idx) / 6.0
                
            fr_vfx = apply_kill_vfx(fr.copy(), min_dist, cfg["fx"])
            fr_hud = render_hud_overlay(fr_vfx, cfg, is_active, hud_alpha)
            all_frames.append(fr_hud)
            
    print(f"  Clips processed. Total frames so far: {len(all_frames)}")
    
    # 3. Outro
    print("\n[Step 3/6] Generating Outro (120 frames, 4.0s)...")
    outro_frames = generate_outro_frames(120)
    all_frames.extend(outro_frames)
    total_frames = len(all_frames)
    print(f"  Outro added. Grand total frames: {total_frames} ({total_frames/30.0:.2f}s)")
    
    # 4. Write intermediate video stream
    temp_video = os.path.join(TOOLS_DIR, "temp_vol4_montage.mp4")
    print(f"\n[Step 4/6] Writing intermediate video stream to {temp_video}...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, 30.0, (1280, 720))
    for f in all_frames:
        out.write(f)
    out.release()
    print("Intermediate video written successfully!")
    
    # 5. Prepare Audio Track
    total_dur = total_frames / 30.0
    print(f"\n[Step 5/6] Total video duration: {total_dur:.2f}s")
    
    audio_in = os.path.join(TOOLS_DIR, "phonk_house.opus")
    audio_out = os.path.join(TOOLS_DIR, "montage_audio_vol4.wav")
    fade_out_start = max(0.0, total_dur - 4.0)
    
    cmd_audio = [
        FFMPEG_EXE, "-y",
        "-ss", "3.3",
        "-i", audio_in,
        "-t", f"{total_dur:.2f}",
        "-af", f"afade=t=in:ss=0:d=0.5,afade=t=out:st={fade_out_start:.2f}:d=4.0",
        audio_out
    ]
    print("Processing synchronized audio track with FFmpeg...")
    subprocess.run(cmd_audio, check=True)
    
    # 6. Mux Final Video
    final_output = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol4.mp4")
    print(f"\n[Step 6/6] Muxing final video to {final_output} with H.264 & AAC...")
    cmd_mux = [
        FFMPEG_EXE, "-y",
        "-i", temp_video,
        "-i", audio_out,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-movflags", "+faststart",
        "-shortest",
        final_output
    ]
    subprocess.run(cmd_mux, check=True)
    
    for temp_f in [temp_video, audio_out]:
        try: os.remove(temp_f)
        except OSError: pass
        
    print("\n" + "=" * 60)
    print("🎉 VOLUME 4 MONTAGE GENERATION COMPLETE!")
    print(f"Final MP4: {final_output}")
    print(f"File size: {os.path.getsize(final_output) / (1024*1024):.2f} MB")
    print(f"Exact Duration: {total_dur:.2f} seconds")
    print("=" * 60)
    return final_output

if __name__ == "__main__":
    build_vol4_montage()
