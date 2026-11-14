"""
EvilShtrib CS 1.6 Zombie Highlights - Montage Generator.
Creates a high-energy cinematic montage with custom kill FX, Phonk House music,
and server branding.
"""

import os
import sys
import glob
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
CLIPS_DIR = os.path.join(BASE_DIR, "clips")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
OUT_DIR = BASE_DIR
FFMPEG_EXE = r"C:\Users\CauMo\AppData\Roaming\Python\Python312\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 68)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
FONT_IP = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 36)
FONT_HUD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
FONT_HUD_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
FONT_FEATURE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)

# Clip configurations: (clip_filename, start_frame, end_frame, kill_frame_in_raw, title, weapon_label)
# Raw clips have their primary kill at frame 75 (2.50s)
# Trimming ensures >= 1.2s before kill and >= 1.6s after kill
CLIPS_CONFIG = [
    {
        "file": "clip_01.mp4",
        "start": 30,    # 1.00s (1.50s pre-kill)
        "end": 135,    # 4.50s (2.00s post-kill)
        "kill": 75,
        "title": "KILL 01 / 10",
        "weapon": "SG550 SNIPER HEADSHOT",
        "player": "Shadow-Death",
        "map": "bio_asalto_f",
        "fx": 1
    },
    {
        "file": "clip_02.mp4",
        "start": 35,    # 1.16s (1.33s pre-kill)
        "end": 135,    # 4.50s (2.00s post-kill)
        "kill": 75,
        "title": "KILL 02 / 10",
        "weapon": "AWP SNIPER FLICK",
        "player": "Death Knight",
        "map": "bio_arena_fl",
        "fx": 2
    },
    {
        "file": "clip_03.mp4",
        "start": 35,    # 1.16s (1.33s pre-kill)
        "end": 135,    # 4.50s (2.00s post-kill)
        "kill": 75,
        "title": "KILL 03 / 10",
        "weapon": "AWP BULLET-TIME HEADSHOT",
        "player": "thesofafox",
        "map": "zm_colors_rb3",
        "fx": 3
    },
    {
        "file": "clip_04.mp4",
        "start": 35,    # 1.16s (1.33s pre-kill)
        "end": 140,    # 4.66s (2.16s post-kill)
        "kill": 75,
        "title": "KILL 04 / 10",
        "weapon": "MP5 TACTICAL SPRAYDOWN",
        "player": "shooterman",
        "map": "bio_$2000$_rbs_f2",
        "fx": 4
    },
    {
        "file": "clip_05.mp4",
        "start": 30,    # 1.00s (1.50s pre-kill)
        "end": 150,    # 5.00s (double kill at 75 and 108)
        "kill": 75,
        "title": "KILL 05 / 10",
        "weapon": "UMP45 DOUBLE EXECUTION",
        "player": "Death Knight",
        "map": "bio_arena_fl",
        "fx": 5
    },
    {
        "file": "clip_06.mp4",
        "start": 35,    # 1.16s (1.33s pre-kill)
        "end": 135,    # 4.50s (2.00s post-kill)
        "kill": 75,
        "title": "KILL 06 / 10",
        "weapon": "DEAGLE ONE-TAP CRITICAL",
        "player": "blueguile",
        "map": "bio_arena_fl",
        "fx": 6
    },
    {
        "file": "clip_07.mp4",
        "start": 35,    # 1.16s (1.33s pre-kill)
        "end": 135,    # 4.50s (2.00s post-kill)
        "kill": 75,
        "title": "KILL 07 / 10",
        "weapon": "DEAGLE ROOF ELIMINATION",
        "player": "BDM-WhiteViper",
        "map": "bio_blocks_pro",
        "fx": 7
    },
    {
        "file": "clip_08.mp4",
        "start": 30,    # 1.00s (1.50s pre-kill)
        "end": 140,    # 4.66s (2.16s post-kill)
        "kill": 75,
        "title": "KILL 08 / 10",
        "weapon": "SCOUT EXPLOSIVE GIB",
        "player": "blueguile",
        "map": "bio_$2000$_rbs_f2",
        "fx": 8
    },
    {
        "file": "clip_09.mp4",
        "start": 35,    # 1.16s (1.33s pre-kill)
        "end": 135,    # 4.50s (2.00s post-kill)
        "kill": 75,
        "title": "KILL 09 / 10",
        "weapon": "12-GAUGE POINT-BLANK M3",
        "player": "Dk-Unknown",
        "map": "bio_$2000$_rbs_f2",
        "fx": 9
    },
    {
        "file": "clip_10.mp4",
        "start": 35,    # 1.16s (1.33s pre-kill)
        "end": 135,    # 4.50s (2.00s post-kill)
        "kill": 75,
        "title": "KILL 10 / 10",
        "weapon": "AUTO-SHOTGUN XM1014 FINALE",
        "player": "Helios",
        "map": "bio_2000_x_kizaki",
        "fx": 10
    }
]

def render_hud_overlay(frame, cfg, is_kill_active=False):
    """Draws sleek cyber HUD badges on the frame."""
    h, w = frame.shape[:2]
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img, "RGBA")
    
    # Top-Left: Server Branding Pill
    pill_x1, pill_y1 = 30, 25
    pill_w, pill_h = 490, 42
    draw.rounded_rectangle([pill_x1, pill_y1, pill_x1 + pill_w, pill_y1 + pill_h], radius=8, fill=(10, 15, 20, 190), outline=(0, 255, 120, 220), width=1)
    draw.text((pill_x1 + 14, pill_y1 + 9), "[☣ EVILSHTRIB BIOHAZARD]", font=FONT_HUD_BOLD, fill=(0, 255, 130))
    draw.text((pill_x1 + 270, pill_y1 + 10), "185.225.201.113:27015", font=FONT_HUD, fill=(240, 240, 240))
    
    # Bottom-Left: Kill Tracker Badge
    badge_x1, badge_y1 = 30, h - 75
    badge_w, badge_h = 390, 48
    bg_color = (25, 45, 25, 220) if is_kill_active else (10, 15, 20, 180)
    border_color = (0, 255, 180, 255) if is_kill_active else (80, 120, 100, 160)
    draw.rounded_rectangle([badge_x1, badge_y1, badge_x1 + badge_w, badge_y1 + badge_h], radius=6, fill=bg_color, outline=border_color, width=2 if is_kill_active else 1)
    
    # Kill Title and Weapon
    title_color = (0, 255, 200) if is_kill_active else (0, 220, 120)
    draw.text((badge_x1 + 14, badge_y1 + 6), cfg["title"], font=FONT_HUD_BOLD, fill=title_color)
    draw.text((badge_x1 + 14, badge_y1 + 26), cfg["weapon"], font=FONT_HUD, fill=(230, 230, 230))
    
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# --- Kill Visual Effects (FX 1 to 10) ---

def apply_fx_1(frame, d):
    """SG550: White Flash & High-Frequency Screen Shockwave."""
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 5:
        alpha = [0.85, 0.60, 0.40, 0.22, 0.10, 0.03][d]
        white = np.full_like(frame, 255)
        res = cv2.addWeighted(res, 1.0 - alpha, white, alpha, 0)
    if 0 <= d <= 8:
        dx = int(7 * np.sin(d * 3.7))
        dy = int(5 * np.cos(d * 4.1))
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        res = cv2.warpAffine(res, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    return res

def apply_fx_2(frame, d):
    """AWP: Fast Kinetic Zoom Punch."""
    h, w = frame.shape[:2]
    if -2 <= d <= 10:
        zoom_curve = [1.05, 1.14, 1.25, 1.22, 1.18, 1.14, 1.10, 1.06, 1.03, 1.01, 1.0, 1.0, 1.0]
        idx = d + 2
        z = zoom_curve[min(idx, len(zoom_curve)-1)]
        h_crop = int(h / z)
        w_crop = int(w / z)
        y1 = (h - h_crop) // 2
        x1 = (w - w_crop) // 2
        cropped = frame[y1:y1+h_crop, x1:x1+w_crop]
        res = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
        if 0 <= d <= 2:
            res = cv2.convertScaleAbs(res, alpha=1.15, beta=15)
        return res
    return frame

def apply_fx_3(frame, d):
    """AWP Headshot: Bullet-Time Slow-Mo & Chromatic Aberration."""
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 10:
        shifts = [14, 12, 10, 8, 6, 5, 4, 3, 2, 1, 0]
        s = shifts[d]
        if s > 0:
            b, g, r = cv2.split(res)
            # Blue shifted left, Red shifted right
            b_shifted = np.zeros_like(b)
            r_shifted = np.zeros_like(r)
            b_shifted[:, :-s] = b[:, s:]
            b_shifted[:, -s:] = b[:, -1:]
            r_shifted[:, s:] = r[:, :-s]
            r_shifted[:, :s] = r[:, :1]
            res = cv2.merge([b_shifted, g, r_shifted])
    return res

def apply_fx_4(frame, d):
    """MP5: Double Strobe Burst & Dark Pulsing Border Vignette."""
    h, w = frame.shape[:2]
    res = frame.copy()
    # Strobe pulses
    if d in [0, 1, 3, 4]:
        res = cv2.convertScaleAbs(res, alpha=1.35, beta=25)
    # Pulsing dark vignette
    if 0 <= d <= 12:
        Y, X = np.ogrid[:h, :w]
        dist = np.sqrt((X - w//2)**2 + (Y - h//2)**2)
        max_dist = np.sqrt((w//2)**2 + (h//2)**2)
        v = 1.0 - 0.45 * (dist / max_dist)
        for c in range(3):
            res[:, :, c] = np.clip(res[:, :, c] * v, 0, 255).astype(np.uint8)
    return res

def apply_fx_5(frame, d):
    """UMP45: Negative Flash, Blood Crimson Tint & Glitch Slices."""
    h, w = frame.shape[:2]
    res = frame.copy()
    if d == 0:
        return 255 - res
    elif 1 <= d <= 7:
        # Boost Red, mute Green/Blue
        b, g, r = cv2.split(res)
        r = np.clip(r.astype(np.float32) * 1.35 + 20, 0, 255).astype(np.uint8)
        g = np.clip(g.astype(np.float32) * 0.7, 0, 255).astype(np.uint8)
        b = np.clip(b.astype(np.float32) * 0.7, 0, 255).astype(np.uint8)
        res = cv2.merge([b, g, r])
        # Random horizontal slice glitch
        for y_start in [140, 360, 520]:
            slice_h = 35
            offset = int(25 * np.sin(d * 2.5))
            res[y_start:y_start+slice_h, :] = np.roll(res[y_start:y_start+slice_h, :], offset, axis=1)
    return res

def apply_fx_6(frame, d):
    """Deagle: 1-Tap Freeze Bloom & Radial Exposure."""
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 3:
        # High contrast exposure pop
        res = cv2.convertScaleAbs(res, alpha=1.28, beta=30)
        # Radial bloom blend
        blurred = cv2.GaussianBlur(res, (31, 31), 0)
        res = cv2.addWeighted(res, 0.7, blurred, 0.3, 0)
    return res

def apply_fx_7(frame, d):
    """Deagle Roof: Bio-Scanner Green Radar & CRT Scanlines."""
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 12:
        # Toxic green scanner tint
        b, g, r = cv2.split(res)
        g = np.clip(g.astype(np.float32) * 1.4 + 25, 0, 255).astype(np.uint8)
        r = np.clip(r.astype(np.float32) * 0.45, 0, 255).astype(np.uint8)
        b = np.clip(b.astype(np.float32) * 0.45, 0, 255).astype(np.uint8)
        res = cv2.merge([b, g, r])
        # CRT scanlines
        res[::3, :] = (res[::3, :].astype(np.float32) * 0.65).astype(np.uint8)
        # Expanding holographic targeting circle
        radius = int(25 + d * 9)
        cv2.circle(res, (w//2, h//2), radius, (0, 255, 120), 2, cv2.LINE_AA)
        cv2.drawMarker(res, (w//2, h//2), (0, 255, 200), cv2.MARKER_TILTED_CROSS, radius + 10, 1, cv2.LINE_AA)
    return res

def apply_fx_8(frame, d):
    """Scout: Blood Gib Burst & Hyper-Saturation Bloom."""
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 10:
        # Saturation boost in HSV
        hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.85, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.15, 0, 255)
        res = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        # Zoom punch 1.12x into blood splatter
        z = 1.12 - (d * 0.012)
        if z > 1.0:
            hc, wc = int(h / z), int(w / z)
            y1, x1 = (h - hc) // 2, (w - wc) // 2
            res = cv2.resize(res[y1:y1+hc, x1:x1+wc], (w, h), interpolation=cv2.INTER_LINEAR)
    return res

def apply_fx_9(frame, d):
    """M3 Shotgun: 12-Gauge Downward Recoil Kick & Noise Burst."""
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 7:
        kicks = [24, 18, 12, 6, -3, -2, 0, 0]
        dy = kicks[d]
        M = np.float32([[1, 0, 0], [0, 1, dy]])
        res = cv2.warpAffine(res, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        # Film grain / flash
        if d <= 3:
            noise = np.random.normal(0, 18, (h, w, 3)).astype(np.int16)
            res = np.clip(res.astype(np.int16) + noise + 20, 0, 255).astype(np.uint8)
    return res

def apply_fx_10(frame, d):
    """XM1014: Digital RGB Glitch Displacement & Outro Wipe."""
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 15:
        # Glitch RGB displacement
        b, g, r = cv2.split(res)
        shift = int(18 * np.sin(d * 1.5))
        b = np.roll(b, -shift, axis=1)
        r = np.roll(r, shift, axis=1)
        res = cv2.merge([b, g, r])
        # Digital artifact blocks
        for i in range(4):
            y_b = int((i * 160 + d * 25) % (h - 40))
            res[y_b:y_b+30, :] = np.roll(res[y_b:y_b+30, :], int(35 * np.cos(d + i)), axis=1)
    return res

FX_MAP = {
    1: apply_fx_1,
    2: apply_fx_2,
    3: apply_fx_3,
    4: apply_fx_4,
    5: apply_fx_5,
    6: apply_fx_6,
    7: apply_fx_7,
    8: apply_fx_8,
    9: apply_fx_9,
    10: apply_fx_10,
}

# --- Intro & Outro Generators ---

def generate_intro_frames(num_frames=90):
    """3.0s Animated Cyber Intro."""
    w, h = 1280, 720
    frames = []
    
    for f in range(num_frames):
        img = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Cyber dark background gradient
        for y in range(h):
            val = int(12 + 16 * (y / h))
            img[y, :] = [int(val * 0.7), int(val * 1.1), int(val * 0.8)]
            
        # Animated grid
        offset_y = int((f * 2) % 40)
        for x in range(0, w, 40):
            cv2.line(img, (x, 0), (x, h), (20, 35, 25), 1)
        for y in range(offset_y, h, 40):
            cv2.line(img, (0, y), (w, y), (20, 35, 25), 1)
            
        # Animated particles
        np.random.seed(42 + f)
        pts_x = np.random.randint(50, w - 50, 20)
        pts_y = np.random.randint(50, h - 50, 20)
        for px, py in zip(pts_x, pts_y):
            cv2.circle(img, (px, py), 2, (0, 200, 100), -1)
            
        # Draw with Pillow
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img, "RGBA")
        
        # Border frame
        draw.rounded_rectangle([100, 80, w - 100, h - 80], radius=16, outline=(0, 255, 120, 200), width=2)
        draw.rounded_rectangle([106, 86, w - 106, h - 86], radius=14, outline=(0, 180, 80, 120), width=1)
        
        # Glitch effect during first 15 frames
        glitch_x = int(6 * np.sin(f * 2.8)) if f < 18 else 0
        
        # Server Title
        draw.text((w // 2 - 180 + glitch_x, 140), "☣  EVILSHTRIB  ☣", font=FONT_TITLE, fill=(0, 255, 140))
        draw.text((w // 2 - 220 + glitch_x, 235), "CLASSIC BIOHAZARD", font=FONT_TITLE, fill=(255, 255, 255))
        draw.text((w // 2 - 200, 335), "TOP 10 ZOMBIE KILL HIGHLIGHTS", font=FONT_SUB, fill=(0, 220, 255))
        
        # IP Box
        ip_box = [w // 2 - 340, 410, w // 2 + 340, 500]
        pulse = int(25 * np.sin(f * 0.2))
        draw.rounded_rectangle(ip_box, radius=12, fill=(10, 40, 25, 220), outline=(0, 230 + pulse, 120), width=3)
        draw.text((w // 2 - 300, 435), "IP: 185.225.201.113:27015", font=FONT_IP, fill=(0, 255, 230))
        
        # Countdown/Drop teaser
        if f >= 60:
            draw.text((w // 2 - 110, 545), "DROP IN 3... 2... 1...", font=FONT_SUB, fill=(255, 180, 0))
        else:
            draw.text((w // 2 - 145, 545), "OFFICIAL SERVER PROMO", font=FONT_SUB, fill=(160, 200, 180))
            
        frame_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        # Glitch slice flash at frame 85..89
        if f >= 85:
            flash_alpha = (f - 85) / 5.0
            frame_bgr = cv2.addWeighted(frame_bgr, 1.0 - flash_alpha, np.full_like(frame_bgr, 255), flash_alpha, 0)
            
        frames.append(frame_bgr)
        
    return frames

def generate_outro_frames(num_frames=135):
    """4.5s Server Call to Action Outro."""
    w, h = 1280, 720
    frames = []
    
    for f in range(num_frames):
        img = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Dark green/cyan cyber background
        for y in range(h):
            val = int(10 + 18 * (y / h))
            img[y, :] = [int(val * 0.9), int(val * 1.2), int(val * 0.7)]
            
        # Grid
        for x in range(0, w, 40):
            cv2.line(img, (x, 0), (x, h), (20, 35, 25), 1)
        for y in range(0, h, 40):
            cv2.line(img, (0, y), (w, y), (20, 35, 25), 1)
            
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img, "RGBA")
        
        # Frame
        draw.rounded_rectangle([90, 60, w - 90, h - 60], radius=16, outline=(0, 255, 140, 220), width=2)
        
        # Header
        draw.text((w // 2 - 250, 100), "JOIN THE SURVIVORS", font=FONT_TITLE, fill=(0, 255, 140))
        draw.text((w // 2 - 220, 185), "EVILSHTRIB > CLASSIC BIOHAZARD", font=FONT_SUB, fill=(255, 255, 255))
        
        # Large IP Connect Box
        box = [w // 2 - 400, 240, w // 2 + 400, 345]
        draw.rounded_rectangle(box, radius=14, fill=(10, 45, 30, 240), outline=(0, 255, 200, 255), width=3)
        draw.text((w // 2 - 370, 260), "CONNECT 185.225.201.113:27015", font=FONT_IP, fill=(0, 255, 255))
        draw.text((w // 2 - 260, 305), "Open Console (~) and paste connect command", font=FONT_HUD, fill=(180, 240, 200))
        
        # Features list
        features = [
            "★  Classic CS 1.6 Zombie Plague Infection Mode",
            "★  Bio-Scanner & Early Infection Tactical Alerts",
            "★  Balanced Zombie Classes, Knockback & Weapons",
            "★  Low Ping, 24/7 Uptime, Dedicated Server & Fast DL"
        ]
        start_y = 375
        for i, feat in enumerate(features):
            draw.text((w // 2 - 330, start_y + i * 40), feat, font=FONT_FEATURE, fill=(220, 240, 230))
            
        # Bottom call
        draw.text((w // 2 - 165, 560), "SEE YOU ON THE BATTLEFIELD!", font=FONT_SUB, fill=(0, 255, 180))
        
        frame_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        # Fade out to black over last 35 frames
        if f >= num_frames - 35:
            alpha = (num_frames - f) / 35.0
            frame_bgr = (frame_bgr.astype(np.float32) * alpha).astype(np.uint8)
            
        frames.append(frame_bgr)
        
    return frames

def build_montage():
    print("=== STARTING EVILSHTRIB MONTAGE GENERATOR ===")
    
    all_frames = []
    
    # 1. Intro (3.0s = 90 frames)
    print("Generating Intro sequence (90 frames)...")
    intro_frames = generate_intro_frames(90)
    all_frames.extend(intro_frames)
    print(f"  Intro added. Total frames: {len(all_frames)}")
    
    # 2. Clips (10 clips)
    for idx, cfg in enumerate(CLIPS_CONFIG, 1):
        clip_path = os.path.join(CLIPS_DIR, cfg["file"])
        print(f"Processing Clip {idx:02d}: {cfg['file']} (start={cfg['start']}, end={cfg['end']}, kill={cfg['kill']})")
        
        cap = cv2.VideoCapture(clip_path)
        raw_frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            raw_frames.append(frame)
        cap.release()
        
        start = cfg["start"]
        end = min(cfg["end"], len(raw_frames))
        kill_raw = cfg["kill"]
        fx_fn = FX_MAP[cfg["fx"]]
        
        clip_processed = []
        for raw_idx in range(start, end):
            frame = raw_frames[raw_idx].copy()
            d = raw_idx - kill_raw  # relative distance to kill
            
            # Apply kill FX
            frame = fx_fn(frame, d)
            
            # Apply HUD overlay
            is_kill_active = (0 <= d <= 8)
            frame = render_hud_overlay(frame, cfg, is_kill_active=is_kill_active)
            
            clip_processed.append(frame)
            
        all_frames.extend(clip_processed)
        print(f"  Clip {idx:02d} added: {len(clip_processed)} frames ({len(clip_processed)/30.0:.2f}s). Total frames: {len(all_frames)}")
        
    # 3. Outro (4.5s = 135 frames)
    print("Generating Outro sequence (135 frames)...")
    outro_frames = generate_outro_frames(135)
    all_frames.extend(outro_frames)
    print(f"  Outro added. Total frames: {len(all_frames)} ({len(all_frames)/30.0:.2f}s)")
    
    # 4. Write intermediate video stream
    temp_video = os.path.join(TOOLS_DIR, "temp_montage_video.mp4")
    print(f"Writing intermediate video to {temp_video}...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, 30.0, (1280, 720))
    for f in all_frames:
        out.write(f)
    out.release()
    print("Intermediate video written successfully!")
    
    # 5. Prepare Audio
    # Total video duration:
    total_dur = len(all_frames) / 30.0
    print(f"Total video duration: {total_dur:.2f}s")
    
    # Cut audio from 3.3s to match video duration with smooth fade in and fade out
    audio_in = os.path.join(TOOLS_DIR, "phonk_house.wav")
    audio_out = os.path.join(TOOLS_DIR, "montage_audio_final.wav")
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
    
    # 6. Mux Final Video with Audio
    final_output = os.path.join(OUT_DIR, "EvilShtrib_Montage.mp4")
    print(f"Muxing final video to {final_output} with H.264 & AAC...")
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
        "-shortest",
        final_output
    ]
    subprocess.run(cmd_mux, check=True)
    print("=== MONTAGE GENERATION COMPLETE! ===")
    print(f"Final MP4: {final_output}")
    print(f"File size: {os.path.getsize(final_output) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    build_montage()
