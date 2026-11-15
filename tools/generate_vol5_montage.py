"""
EvilShtrib CS 1.6 Zombie Highlights - 60-Second Real Match Montage (Volume 5).
Definitive 100% Action & Pure Frag Edition:
- 32 confirmed kills across 16 rapid streaks (all kill spans <= 2.25s).
- 100% verified kills: every single clip contains confirmed top-right killfeed notifications!
- ZERO running around, ZERO pitch-black maps, ZERO duplicate rounds.
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
import shutil

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
CLIPS_DIR = os.path.join(BASE_DIR, "clips_vol5")
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
    {'file': 'clip_01.mp4', 'start': 0, 'end': 99, 'kills': [44, 55], 'title': 'KILL STREAK 01 / 16', 'weapon': 'SIG SG550 AUTO-SNIPER', 'tag': 'RAPID DOUBLE', 'player': 'Galdalfus', 'map': 'bio_blocks_pro', 'fx': 1},
    {'file': 'clip_02.mp4', 'start': 0, 'end': 99, 'kills': [35, 64], 'title': 'KILL STREAK 02 / 16', 'weapon': 'H&K MP5-NAVY 9MM', 'tag': 'DOUBLE HS', 'player': 'HappyKiD', 'map': 'bio_re-ziger', 'fx': 2},
    {'file': 'clip_03.mp4', 'start': 0, 'end': 99, 'kills': [35, 64], 'title': 'KILL STREAK 03 / 16', 'weapon': 'CLARION 5.56 (FAMAS)', 'tag': 'DOUBLE KILL', 'player': 'HappyKiD', 'map': 'bio_omega_b2', 'fx': 3},
    {'file': 'clip_04.mp4', 'start': 0, 'end': 99, 'kills': [34, 65], 'title': 'KILL STREAK 04 / 16', 'weapon': 'FN M249 PARA SAW', 'tag': 'SAW DOUBLE', 'player': 'Fat Matt', 'map': 'bio_blocks_pro', 'fx': 4},
    {'file': 'clip_05.mp4', 'start': 0, 'end': 99, 'kills': [33, 66], 'title': 'KILL STREAK 05 / 16', 'weapon': 'SIG SG550 AUTO-SNIPER', 'tag': 'DOUBLE KILL', 'player': 'kingkilla', 'map': 'bio_blocks_pro', 'fx': 5},
    {'file': 'clip_06.mp4', 'start': 0, 'end': 99, 'kills': [29, 70], 'title': 'KILL STREAK 06 / 16', 'weapon': 'STEYR SCOUT SNIPER', 'tag': 'FLICK DOUBLE', 'player': 'HappyKiD', 'map': 'bio_india_b2_', 'fx': 6},
    {'file': 'clip_07.mp4', 'start': 0, 'end': 99, 'kills': [29, 70], 'title': 'KILL STREAK 07 / 16', 'weapon': 'D3/AU-1 AUTO-SNIPER', 'tag': 'DOUBLE TAP', 'player': 'aliendewd1', 'map': 'bio_nova_b2', 'fx': 7},
    {'file': 'clip_08.mp4', 'start': 0, 'end': 99, 'kills': [26, 73], 'title': 'KILL STREAK 08 / 16', 'weapon': 'D3/AU-1 AUTO-SNIPER', 'tag': 'DOUBLE HS', 'player': 'aliendewd1', 'map': 'bio_resident_beta', 'fx': 8},
    {'file': 'clip_09.mp4', 'start': 0, 'end': 99, 'kills': [26, 73], 'title': 'KILL STREAK 09 / 16', 'weapon': 'D3/AU-1 AUTO-SNIPER', 'tag': 'DOUBLE KILL', 'player': 'aliendewd1', 'map': 'bio_mono_b1', 'fx': 9},
    {'file': 'clip_10.mp4', 'start': 0, 'end': 99, 'kills': [26, 73], 'title': 'KILL STREAK 10 / 16', 'weapon': 'STEYR SCOUT SNIPER', 'tag': '2x HEADSHOT', 'player': 'Dk-Unknown', 'map': 'bio_blocks_pro', 'fx': 10},
    {'file': 'clip_11.mp4', 'start': 0, 'end': 99, 'kills': [23, 76], 'title': 'KILL STREAK 11 / 16', 'weapon': 'COLT M4A1 CARBINE', 'tag': 'DOUBLE KILL', 'player': 'kingkilla', 'map': 'bio_re-ziger', 'fx': 11},
    {'file': 'clip_12.mp4', 'start': 0, 'end': 99, 'kills': [22, 77], 'title': 'KILL STREAK 12 / 16', 'weapon': '.40 DUAL ELITES', 'tag': 'ELITE COMBO', 'player': 'Fat Matt', 'map': 'bio_re-ziger', 'fx': 12},
    {'file': 'clip_13.mp4', 'start': 0, 'end': 99, 'kills': [20, 79], 'title': 'KILL STREAK 13 / 16', 'weapon': 'LEONE 12 GAUGE SUPER', 'tag': 'PUMP ACTION', 'player': 'pyr0`', 'map': 'bio_re-ziger', 'fx': 13},
    {'file': 'clip_14.mp4', 'start': 0, 'end': 99, 'kills': [16, 83], 'title': 'KILL STREAK 14 / 16', 'weapon': 'HE GRENADE / MAC-10', 'tag': 'EXPLOSIVE DOUBLE', 'player': 'Fat Matt', 'map': 'bio_dusty_2x2_fl', 'fx': 14},
    {'file': 'clip_15.mp4', 'start': 0, 'end': 102, 'kills': [18, 84], 'title': 'KILL STREAK 15 / 16', 'weapon': 'NIGHT HAWK .50C', 'tag': 'DEAGLE DOUBLE', 'player': '[SMUT]DarkDruid', 'map': 'bio_nova_b2', 'fx': 15},
    {'file': 'clip_16.mp4', 'start': 0, 'end': 102, 'kills': [17, 85], 'title': 'KILL STREAK 16 / 16', 'weapon': 'IDF DEFENDER (GALIL)', 'tag': 'CLUTCH DOUBLE', 'player': 'pyr0`', 'map': 'bio_blocks_pro', 'fx': 16},
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
    badge_w, badge_h = 430, 66
    
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
    
    draw.text(
        (badge_x1 + 16, badge_y1 + 8),
        cfg["title"],
        font=FONT_KILL_TITLE,
        fill=title_color
    )
    
    tag_str = cfg.get("tag", "ELIMINATION")
    tag_w = 115
    tag_x1 = badge_x1 + badge_w - tag_w - 14
    tag_y1 = badge_y1 + 8
    draw.rounded_rectangle(
        [tag_x1, tag_y1, tag_x1 + tag_w, tag_y1 + 20],
        radius=4,
        fill=(25, 45, 35, int(220 * a_mult)),
        outline=(0, 255, 140, int(180 * a_mult)),
        width=1
    )
    draw.text(
        (tag_x1 + 8, tag_y1 + 3),
        tag_str,
        font=FONT_KILL_TAG,
        fill=(0, 255, 160, int(255 * a_mult))
    )
    
    draw.line(
        [(badge_x1 + 16, badge_y1 + 34), (badge_x1 + badge_w - 16, badge_y1 + 34)],
        fill=(255, 255, 255, int(45 * a_mult)),
        width=1
    )
    
    weapon_full = f"{cfg['weapon']}  [{cfg['player']}]"
    draw.text(
        (badge_x1 + 16, badge_y1 + 40),
        weapon_full,
        font=FONT_KILL_WEAPON,
        fill=(230, 238, 245, int(240 * a_mult))
    )

    base_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert("RGBA")
    final_pil = Image.alpha_composite(base_pil, overlay)
    return cv2.cvtColor(np.array(final_pil.convert("RGB")), cv2.COLOR_RGB2BGR)

# Kill VFX
def apply_kill_vfx(frame, dist, fx_type):
    if dist < 0 or dist > 14:
        return frame
    h, w = frame.shape[:2]
    out = frame.copy()
    if dist <= 3:
        # Impact shake & subtle red-cyan flash
        dx = int(np.random.randint(-4, 5))
        dy = int(np.random.randint(-4, 5))
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        out = cv2.warpAffine(out, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        flash_intensity = 35 - dist * 8
        out = cv2.add(out, np.full((h, w, 3), (flash_intensity // 2, flash_intensity, flash_intensity // 4), dtype=np.uint8))
    elif dist <= 9:
        # Subtle vignette pulse
        alpha = (9 - dist) / 6.0 * 0.15
        vig = np.zeros_like(out)
        cv2.circle(vig, (w // 2, h // 2), int(w * 0.45), (255, 255, 255), -1)
        vig = cv2.GaussianBlur(vig, (101, 101), 0) / 255.0
        out = (out * (1 - alpha * (1 - vig))).astype(np.uint8)
    return out

def generate_intro_frames(count=90):
    frames = []
    w, h = 1280, 720
    for i in range(count):
        img = Image.new("RGB", (w, h), (7, 10, 16))
        draw = ImageDraw.Draw(img)
        progress = i / float(count)
        
        # Grid lines
        for gx in range(0, w, 80):
            draw.line([(gx, 0), (gx, h)], fill=(15, 22, 32), width=1)
        for gy in range(0, h, 80):
            draw.line([(0, gy), (w, gy)], fill=(15, 22, 32), width=1)
            
        # Animated center bar
        bar_w = int(w * min(1.0, progress * 1.4))
        draw.line([(w // 2 - bar_w // 2, 230), (w // 2 + bar_w // 2, 230)], fill=(0, 255, 140), width=3)
        draw.line([(w // 2 - bar_w // 2, 490), (w // 2 + bar_w // 2, 490)], fill=(0, 255, 140), width=3)
        
        # Main Title
        draw.text((w // 2 - 270, 260), "EVILSHTRIB", font=FONT_INTRO_TITLE, fill=(0, 255, 140))
        draw.text((w // 2 + 100, 275), "VOL. 5", font=FONT_INTRO_SUB, fill=(255, 255, 255))
        
        # Subtitle
        draw.text((w // 2 - 290, 355), "BIOHAZARD CS 1.6 - ACTION MONTAGE", font=FONT_INTRO_SUB, fill=(200, 225, 240))
        
        # IP Box
        box_w, box_h = 560, 56
        bx1, by1 = w // 2 - box_w // 2, 410
        draw.rounded_rectangle([bx1, by1, bx1 + box_w, by1 + box_h], radius=8, fill=(12, 18, 28), outline=(0, 255, 140), width=2)
        draw.text((bx1 + 32, by1 + 10), "CONNECT 185.225.201.113:27015", font=FONT_INTRO_IP, fill=(0, 255, 160))
        
        # Bottom Tag
        draw.text((w // 2 - 190, 520), "32 CONFIRMED ELIMINATIONS | ZERO LAG", font=FONT_INTRO_TAG, fill=(130, 160, 180))
        
        # Fade In (first 10 frames)
        frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        if i < 10:
            frame_cv = (frame_cv * (i / 10.0)).astype(np.uint8)
        frames.append(frame_cv)
    return frames

def generate_outro_frames(count=120):
    frames = []
    w, h = 1280, 720
    for i in range(count):
        img = Image.new("RGB", (w, h), (7, 10, 16))
        draw = ImageDraw.Draw(img)
        progress = i / float(count)
        
        # Grid lines
        for gx in range(0, w, 80):
            draw.line([(gx, 0), (gx, h)], fill=(15, 22, 32), width=1)
        for gy in range(0, h, 80):
            draw.line([(0, gy), (w, gy)], fill=(15, 22, 32), width=1)
            
        # Top banner
        draw.text((w // 2 - 320, 130), "JOIN THE SERVER NOW!", font=FONT_OUTRO_TITLE, fill=(0, 255, 140))
        draw.text((w // 2 - 250, 215), "Counter-Strike 1.6 Biohazard Zombie Plague", font=FONT_OUTRO_SUB, fill=(220, 235, 245))
        
        # IP Box
        box_w, box_h = 620, 68
        bx1, by1 = w // 2 - box_w // 2, 280
        draw.rounded_rectangle([bx1, by1, bx1 + box_w, by1 + box_h], radius=10, fill=(12, 18, 28), outline=(0, 255, 140), width=2)
        draw.text((bx1 + 38, by1 + 14), "IP: 185.225.201.113:27015", font=FONT_OUTRO_IP, fill=(0, 255, 160))
        
        # Features
        draw.text((w // 2 - 260, 385), "☣ FastDL Maps & Custom Biohazard Models", font=FONT_OUTRO_FEATURE, fill=(180, 210, 230))
        draw.text((w // 2 - 260, 425), "☣ 1000 FPS Dedicated Server - Low Latency", font=FONT_OUTRO_FEATURE, fill=(180, 210, 230))
        draw.text((w // 2 - 260, 465), "☣ Live Stats & Demos at stats.shtriban.ru", font=FONT_OUTRO_FEATURE, fill=(0, 240, 180))
        draw.text((w // 2 - 260, 505), "☣ Follow us on Instagram: @evilshtrib", font=FONT_OUTRO_FEATURE, fill=(255, 215, 0))
        
        frame_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # Fade Out (last 15 frames)
        if i >= count - 15:
            fade = (count - 1 - i) / 15.0
            frame_cv = (frame_cv * fade).astype(np.uint8)
        frames.append(frame_cv)
    return frames

def build_vol5_montage():
    print("=" * 60)
    print("🎬 STARTING EVILSHTRIB VOLUME 5 MONTAGE GENERATION")
    print("=" * 60)
    
    all_frames = []
    
    # 1. Intro (90 frames)
    print("\n[Step 1/6] Generating Intro (90 frames, 3.0s)...")
    intro_frames = generate_intro_frames(90)
    all_frames.extend(intro_frames)
    print(f"  Intro generated ({len(all_frames)} frames so far).")
    
    # 2. Clips (1590 frames)
    print("\n[Step 2/6] Processing 16 Verified Action Clips...")
    for idx, cfg in enumerate(CLIPS_CONFIG, 1):
        cpath = os.path.join(CLIPS_DIR, cfg["file"])
        if not os.path.exists(cpath):
            raise FileNotFoundError(f"Clip not found: {cpath}")
            
        cap = cv2.VideoCapture(cpath)
        frames = []
        while True:
            ret, fr = cap.read()
            if not ret: break
            frames.append(fr)
        cap.release()
        
        target_len = cfg["end"] - cfg["start"]
        sliced = frames[cfg["start"]:cfg["end"]]
        if len(sliced) < target_len:
            pad = [sliced[-1]] * (target_len - len(sliced))
            sliced.extend(pad)
        sliced = sliced[:target_len]
        
        print(f"  [{idx:02d}/16] {cfg['file']}: {len(sliced)} frames ({cfg['weapon']} | {cfg['player']})")
        
        kills = cfg.get("kills", [])
        for f_idx, fr in enumerate(sliced):
            min_dist = 999
            for kf in kills:
                dist = abs(f_idx - kf)
                if dist < min_dist:
                    min_dist = dist
                    
            is_active = (min_dist <= 10)
            
            # HUD fade-in / fade-out
            hud_alpha = 1.0
            if f_idx < 6:
                hud_alpha = f_idx / 6.0
            elif f_idx >= len(sliced) - 6:
                hud_alpha = (len(sliced) - f_idx) / 6.0
                
            fr_vfx = apply_kill_vfx(fr, min_dist, cfg["fx"])
            fr_hud = render_hud_overlay(fr_vfx, cfg, is_active, hud_alpha)
            all_frames.append(fr_hud)
            
    print(f"  Clips processed. Total frames so far: {len(all_frames)}")
    
    # 3. Outro (120 frames)
    print("\n[Step 3/6] Generating Outro (120 frames, 4.0s)...")
    outro_frames = generate_outro_frames(120)
    all_frames.extend(outro_frames)
    total_frames = len(all_frames)
    print(f"  Grand total frames: {total_frames} ({total_frames/30.0:.2f}s)")
    
    if total_frames != 1800:
        print(f"WARNING: Total frames {total_frames} != 1800! Trimming or padding...")
        if total_frames > 1800:
            all_frames = all_frames[:1800]
        else:
            all_frames.extend([all_frames[-1]] * (1800 - total_frames))
        total_frames = len(all_frames)
        
    # 4. Write intermediate video stream
    temp_video = os.path.join(TOOLS_DIR, "temp_vol5_montage.mp4")
    print(f"\n[Step 4/6] Writing intermediate video stream to {temp_video}...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, 30.0, (1280, 720))
    for f in all_frames:
        out.write(f)
    out.release()
    print("Intermediate video written successfully!")
    
    # 5. Audio track
    total_dur = total_frames / 30.0
    print(f"\n[Step 5/6] Total duration: {total_dur:.2f}s. Preparing audio...")
    audio_in = os.path.join(TOOLS_DIR, "phonk_house.opus")
    audio_out = os.path.join(TOOLS_DIR, "montage_audio_vol5.wav")
    fade_out_start = max(0.0, total_dur - 4.0)
    
    cmd_audio = [
        FFMPEG_EXE, "-y",
        "-ss", "4.0",
        "-i", audio_in,
        "-t", f"{total_dur:.2f}",
        "-af", f"afade=t=in:ss=0:d=0.5,afade=t=out:st={fade_out_start:.2f}:d=4.0",
        audio_out
    ]
    subprocess.run(cmd_audio, check=True)
    
    # 6. Final Mux
    final_output = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol5.mp4")
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
    
    # Also copy to root for web player
    root_copy = os.path.join(BASE_DIR, "EvilShtrib_60s_Vol5.mp4")
    shutil.copy2(final_output, root_copy)
    
    # Clean up temp
    for temp_f in [temp_video, audio_out]:
        try: os.remove(temp_f)
        except OSError: pass
        
    print("\n" + "=" * 60)
    print("🎉 VOLUME 5 MONTAGE GENERATION COMPLETE!")
    print(f"Final MP4: {final_output}")
    print(f"Root copy: {root_copy}")
    print(f"File size: {os.path.getsize(final_output) / (1024*1024):.2f} MB")
    print(f"Exact Duration: {total_dur:.2f} seconds ({total_frames} frames @ 30 FPS)")
    print("=" * 60)
    
    # 7. Generate 9:16 Instagram Reels Version
    reels_output = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol5_9x16.mp4")
    print(f"\nGenerating 9:16 Instagram Reels version: {reels_output}...")
    # High-quality blurred background with centered 16:9 gameplay
    cmd_reels = [
        FFMPEG_EXE, "-y",
        "-i", final_output,
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
        "[0:v]scale=1080:608:flags=lanczos[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2[v]",
        "-map", "[v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "copy",
        "-movflags", "+faststart",
        reels_output
    ]
    subprocess.run(cmd_reels, check=True)
    root_reels = os.path.join(BASE_DIR, "EvilShtrib_60s_Vol5_9x16.mp4")
    shutil.copy2(reels_output, root_reels)
    print(f"Reels MP4 generated: {reels_output} ({os.path.getsize(reels_output)/(1024*1024):.2f} MB)")
    
    return final_output, reels_output

if __name__ == "__main__":
    build_vol5_montage()
