"""
EvilShtrib CS 1.6 Zombie Highlights - 60-Second Real Match Montage (Volume 3).
100% official server shtriban.ru & backup bot demos, 24 verified zombie kills across 12 streaks,
100% In-Eye first-person weapon camera tracking.
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
CLIPS_DIR = os.path.join(BASE_DIR, "clips_vol3")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
OUT_DIR = BASE_DIR
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# Fonts
FONT_INTRO_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 68)
FONT_INTRO_SUB = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 40)
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

# 12 clips configuration tailored to exactly 1590 frames (53.00s)
# 90 intro + 1590 clips + 120 outro = 1800 frames = exactly 60.00s
CLIPS_CONFIG = [
    {
        "file": "clip_01.mp4",
        "start": 0,
        "end": 110,    # 110 frames
        "kills": [26, 57],
        "title": "KILL STREAK 01 / 12",
        "weapon": "USP .45 DUAL HEADSHOTS",
        "tag": "DOUBLE HS",
        "player": "aliendewd1",
        "map": "bio_green_peaks_rb7",
        "fx": 1
    },
    {
        "file": "clip_02.mp4",
        "start": 0,
        "end": 177,    # 177 frames
        "kills": [26, 172],
        "title": "KILL STREAK 02 / 12",
        "weapon": "SG550 COMMANDO SNIPER",
        "tag": "DOUBLE KILL",
        "player": "Shadow-Death",
        "map": "bio_asalto_f",
        "fx": 2
    },
    {
        "file": "clip_03.mp4",
        "start": 0,
        "end": 124,    # 124 frames
        "kills": [26, 99],
        "title": "KILL STREAK 03 / 12",
        "weapon": "M249 5.56 PARA MACHINEGUN",
        "tag": "DOUBLE KILL",
        "player": "aliendewd1",
        "map": "bio_heat_rb2",
        "fx": 3
    },
    {
        "file": "clip_04.mp4",
        "start": 0,
        "end": 134,    # 134 frames
        "kills": [26, 111],
        "title": "KILL STREAK 04 / 12",
        "weapon": "SG550 COMMANDO SNIPER",
        "tag": "DOUBLE KILL",
        "player": "kingkilla",
        "map": "bio_evil_dust_fl",
        "fx": 4
    },
    {
        "file": "clip_05.mp4",
        "start": 0,
        "end": 170,    # 170 frames
        "kills": [27, 156],
        "title": "KILL STREAK 05 / 12",
        "weapon": "STEYR AUG & FIVESEVEN",
        "tag": "DOUBLE KILL",
        "player": "kingkilla",
        "map": "bio_heat_rb2",
        "fx": 5
    },
    {
        "file": "clip_06.mp4",
        "start": 0,
        "end": 185,    # 185 frames
        "kills": [27, 171],
        "title": "KILL STREAK 06 / 12",
        "weapon": "G3SG1 AUTO-SNIPER & GLOCK",
        "tag": "DOUBLE KILL",
        "player": "Player_9",
        "map": "bio_blocks_rb5",
        "fx": 6
    },
    {
        "file": "clip_07.mp4",
        "start": 0,
        "end": 118,    # 118 frames
        "kills": [26, 93],
        "title": "KILL STREAK 07 / 12",
        "weapon": "INGRAM MAC-10 BURST",
        "tag": "DOUBLE KILL",
        "player": "aliendewd1",
        "map": "bio_blocks_rb5",
        "fx": 7
    },
    {
        "file": "clip_08.mp4",
        "start": 0,
        "end": 195,    # 195 frames
        "kills": [27, 187],
        "title": "KILL STREAK 08 / 12",
        "weapon": "SIG SG552 COMMANDO",
        "tag": "DOUBLE KILL",
        "player": "Galdalfus",
        "map": "bio_heat_rb2",
        "fx": 8
    },
    {
        "file": "clip_09.mp4",
        "start": 0,
        "end": 86,     # 86 frames
        "kills": [27, 33],
        "title": "KILL STREAK 09 / 12",
        "weapon": "M249 HEAVY MACHINEGUN",
        "tag": "INSTA KILL",
        "player": "kingkilla",
        "map": "bio_blocks_rb5",
        "fx": 9
    },
    {
        "file": "clip_10.mp4",
        "start": 0,
        "end": 91,     # 91 frames
        "kills": [27, 38],
        "title": "KILL STREAK 10 / 12",
        "weapon": "SIG P228 FAST FIRE",
        "tag": "DOUBLE KILL",
        "player": "Player_9",
        "map": "bio_heat_rb2",
        "fx": 10
    },
    {
        "file": "clip_11.mp4",
        "start": 0,
        "end": 94,     # 94 frames
        "kills": [27, 41],
        "title": "KILL STREAK 11 / 12",
        "weapon": "DUAL .40 ELITES DOUBLE TAP",
        "tag": "DOUBLE KILL",
        "player": "kingkilla",
        "map": "bio_blocks_rb5",
        "fx": 1
    },
    {
        "file": "clip_12.mp4",
        "start": 0,
        "end": 106,    # 106 frames
        "kills": [27, 81],
        "title": "KILL STREAK 12 / 12",
        "weapon": "STEYR AUG RAPID BURST",
        "tag": "DOUBLE KILL",
        "player": "HappyKiD",
        "map": "bio_blocks_rb5",
        "fx": 4
    }
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
    
    draw.text(
        (badge_x1 + 16, badge_y1 + 8),
        cfg["title"],
        font=FONT_KILL_TITLE,
        fill=title_color
    )
    
    tag_str = cfg.get("tag", "ELIMINATION")
    tag_w = 110
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

# Kill VFX Functions
def apply_fx_1(frame, d):
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
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 10:
        shifts = [14, 12, 10, 8, 6, 5, 4, 3, 2, 1, 0]
        s = shifts[d]
        if s > 0:
            b, g, r = cv2.split(res)
            b_shifted = np.zeros_like(b)
            r_shifted = np.zeros_like(r)
            b_shifted[:, :-s] = b[:, s:]
            b_shifted[:, -s:] = b[:, -1:]
            r_shifted[:, s:] = r[:, :-s]
            r_shifted[:, :s] = r[:, :1]
            res = cv2.merge([b_shifted, g, r_shifted])
    return res

def apply_fx_4(frame, d):
    h, w = frame.shape[:2]
    res = frame.copy()
    if d in [0, 1, 3, 4]:
        res = cv2.convertScaleAbs(res, alpha=1.35, beta=25)
    if 0 <= d <= 12:
        Y, X = np.ogrid[:h, :w]
        dist = np.sqrt((X - w//2)**2 + (Y - h//2)**2)
        max_dist = np.sqrt((w//2)**2 + (h//2)**2)
        v = 1.0 - 0.45 * (dist / max_dist)
        for c in range(3):
            res[:, :, c] = np.clip(res[:, :, c] * v, 0, 255).astype(np.uint8)
    return res

def apply_fx_5(frame, d):
    h, w = frame.shape[:2]
    res = frame.copy()
    if d == 0:
        return 255 - res
    elif 1 <= d <= 7:
        b, g, r = cv2.split(res)
        r = np.clip(r.astype(np.float32) * 1.35 + 20, 0, 255).astype(np.uint8)
        g = np.clip(g.astype(np.float32) * 0.7, 0, 255).astype(np.uint8)
        b = np.clip(b.astype(np.float32) * 0.7, 0, 255).astype(np.uint8)
        res = cv2.merge([b, g, r])
        for y_start in [140, 360, 520]:
            slice_h = 35
            offset = int(25 * np.sin(d * 2.5))
            res[y_start:y_start+slice_h, :] = np.roll(res[y_start:y_start+slice_h, :], offset, axis=1)
    return res

def apply_fx_6(frame, d):
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 3:
        res = cv2.convertScaleAbs(res, alpha=1.28, beta=30)
        blurred = cv2.GaussianBlur(res, (31, 31), 0)
        res = cv2.addWeighted(res, 0.7, blurred, 0.3, 0)
    return res

def apply_fx_7(frame, d):
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 12:
        b, g, r = cv2.split(res)
        g = np.clip(g.astype(np.float32) * 1.4 + 25, 0, 255).astype(np.uint8)
        r = np.clip(r.astype(np.float32) * 0.45, 0, 255).astype(np.uint8)
        b = np.clip(b.astype(np.float32) * 0.45, 0, 255).astype(np.uint8)
        res = cv2.merge([b, g, r])
        res[::3, :] = (res[::3, :].astype(np.float32) * 0.65).astype(np.uint8)
        radius = int(25 + d * 9)
        cv2.circle(res, (w//2, h//2), radius, (0, 255, 120), 2, cv2.LINE_AA)
        cv2.drawMarker(res, (w//2, h//2), (0, 255, 200), cv2.MARKER_TILTED_CROSS, radius + 10, 1, cv2.LINE_AA)
    return res

def apply_fx_8(frame, d):
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 10:
        alpha = max(0.0, 1.0 - d / 10.0)
        red_tint = np.zeros_like(frame)
        red_tint[:, :, 2] = int(140 * alpha)
        res = cv2.addWeighted(res, 1.0, red_tint, 0.45 * alpha, 0)
        cv2.circle(res, (int(w*0.35), int(h*0.45)), int(18 + d*4), (0, 0, 180), -1)
        cv2.circle(res, (int(w*0.65), int(h*0.55)), int(12 + d*3), (0, 0, 160), -1)
    return res

def apply_fx_9(frame, d):
    h, w = frame.shape[:2]
    res = frame.copy()
    if d in [0, 1]:
        res = cv2.convertScaleAbs(res, alpha=1.45, beta=40)
    elif d == 2:
        res = 255 - res
    if 0 <= d <= 6:
        angle = (4 - d) * 1.2
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.04)
        res = cv2.warpAffine(res, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    return res

def apply_fx_10(frame, d):
    h, w = frame.shape[:2]
    res = frame.copy()
    if 0 <= d <= 8:
        shift = int(18 * np.sin(d * 1.5))
        b, g, r = cv2.split(res)
        g = np.roll(g, shift, axis=1)
        r = np.roll(r, -shift, axis=1)
        res = cv2.merge([b, g, r])
        if d in [0, 1]:
            cyan = np.full_like(frame, (255, 255, 0))
            res = cv2.addWeighted(res, 0.6, cyan, 0.4, 0)
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
    11: apply_fx_1,
    12: apply_fx_4,
}

def generate_transparent_intro_frames(bg_clip_path, num_frames=90):
    w, h = 1280, 720
    cap = cv2.VideoCapture(bg_clip_path)
    raw_bg_frames = []
    while len(raw_bg_frames) < 45:
        ret, f = cap.read()
        if not ret: break
        raw_bg_frames.append(f)
    cap.release()
    
    if not raw_bg_frames:
        raw_bg_frames = [np.zeros((h, w, 3), dtype=np.uint8)]
        
    intro_frames = []
    for f in range(num_frames):
        bg_idx = min(int(f * 0.5), len(raw_bg_frames) - 1)
        bg_frame = raw_bg_frames[bg_idx].copy()
        
        Y, X = np.ogrid[:h, :w]
        dist = np.sqrt((X - w//2)**2 + (Y - h//2)**2)
        max_dist = np.sqrt((w//2)**2 + (h//2)**2)
        vignette = 1.0 - 0.35 * (dist / max_dist)
        for c in range(3):
            bg_frame[:, :, c] = np.clip(bg_frame[:, :, c] * vignette * 0.85, 0, 255).astype(np.uint8)
            
        if f < 65:
            alpha = 1.0
        else:
            alpha = max(0.0, (num_frames - f) / 25.0)
            
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        if alpha > 0.01:
            box_w, box_h = 760, 310
            bx1 = (w - box_w) // 2
            by1 = (h - box_h) // 2 - 25
            bx2 = bx1 + box_w
            by2 = by1 + box_h
            
            glass_alpha = int(160 * alpha)
            border_alpha = int(220 * alpha)
            
            draw.rounded_rectangle(
                [bx1, by1, bx2, by2],
                radius=18,
                fill=(8, 14, 24, glass_alpha),
                outline=(0, 255, 140, border_alpha),
                width=2
            )
            draw.rounded_rectangle(
                [bx1 + 5, by1 + 5, bx2 - 5, by2 - 5],
                radius=14,
                outline=(0, 200, 100, int(70 * alpha)),
                width=1
            )
            
            glitch_x = int(5 * np.sin(f * 2.8)) if f < 15 else 0
            
            title_text = "☣  EVILSHTRIB  ☣"
            draw.text(((w - 480)//2 + glitch_x + 2, by1 + 25 + 2), title_text, font=FONT_INTRO_TITLE, fill=(0, 0, 0, int(180 * alpha)))
            draw.text(((w - 480)//2 + glitch_x, by1 + 25), title_text, font=FONT_INTRO_TITLE, fill=(0, 255, 140, int(255 * alpha)))
            
            sub_text = "VOL.3 HIGHLIGHTS"
            draw.text(((w - 365)//2 + 2, by1 + 110 + 2), sub_text, font=FONT_INTRO_SUB, fill=(0, 0, 0, int(180 * alpha)))
            draw.text(((w - 365)//2, by1 + 110), sub_text, font=FONT_INTRO_SUB, fill=(255, 255, 255, int(255 * alpha)))
            
            ip_w, ip_h = 560, 50
            ip_x1 = (w - ip_w) // 2
            ip_y1 = by1 + 175
            draw.rounded_rectangle(
                [ip_x1, ip_y1, ip_x1 + ip_w, ip_y1 + ip_h],
                radius=10,
                fill=(14, 38, 28, int(190 * alpha)),
                outline=(0, 255, 200, int(220 * alpha)),
                width=2
            )
            ip_text = "IP: 185.225.201.113:27015"
            draw.text(((w - 450)//2, ip_y1 + 9), ip_text, font=FONT_INTRO_IP, fill=(0, 255, 230, int(255 * alpha)))
            
            tag_text = "24 REAL SERVER KILLS // 100% NONSTOP COMBAT"
            draw.text(((w - 440)//2, by1 + 250), tag_text, font=FONT_INTRO_TAG, fill=(0, 255, 160, int(220 * alpha)))
            
        base_pil = Image.fromarray(cv2.cvtColor(bg_frame, cv2.COLOR_BGR2RGB)).convert("RGBA")
        comp_pil = Image.alpha_composite(base_pil, overlay)
        out_bgr = cv2.cvtColor(np.array(comp_pil.convert("RGB")), cv2.COLOR_RGB2BGR)
        
        if f >= 70:
            hud_fade_in = (f - 70) / 20.0
            out_bgr = render_hud_overlay(out_bgr, CLIPS_CONFIG[0], is_kill_active=False, hud_alpha=hud_fade_in)
            
        intro_frames.append(out_bgr)
        
    return intro_frames

def generate_outro_frames(num_frames=120):
    w, h = 1280, 720
    frames = []
    
    for f in range(num_frames):
        img = np.zeros((h, w, 3), dtype=np.uint8)
        
        for y in range(h):
            val = int(10 + 16 * (y / h))
            img[y, :] = [int(val * 0.9), int(val * 1.2), int(val * 0.75)]
            
        offset_y = int((f * 1.5) % 40)
        for x in range(0, w, 40):
            cv2.line(img, (x, 0), (x, h), (18, 32, 24), 1)
        for y in range(offset_y, h, 40):
            cv2.line(img, (0, y), (w, y), (18, 32, 24), 1)
            
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img, "RGBA")
        
        draw.rounded_rectangle([90, 60, w - 90, h - 60], radius=16, outline=(0, 255, 140, 220), width=2)
        
        draw.text(((w - 530) // 2, 95), "JOIN THE SURVIVORS", font=FONT_OUTRO_TITLE, fill=(0, 255, 140))
        draw.text(((w - 430) // 2, 175), "EVILSHTRIB > CLASSIC BIOHAZARD", font=FONT_OUTRO_SUB, fill=(255, 255, 255))
        
        box = [w // 2 - 400, 230, w // 2 + 400, 335]
        draw.rounded_rectangle(box, radius=14, fill=(10, 45, 30, 240), outline=(0, 255, 200, 255), width=3)
        draw.text(((w - 550) // 2, 250), "CONNECT 185.225.201.113:27015", font=FONT_OUTRO_IP, fill=(0, 255, 255))
        draw.text(((w - 390) // 2, 296), "Open Console (~) and paste connect command", font=FONT_KILL_WEAPON, fill=(180, 240, 200))
        
        features = [
            "★  Official shtriban.ru Server Highlights (Volume 3)",
            "★  24 Verified Zombie Kills Across 5 Battlefields",
            "★  Balanced Knockback, Zombie Classes & Custom Shop",
            "★  Low Ping, 24/7 Uptime, Dedicated Server & Fast DL"
        ]
        start_y = 365
        for i, feat in enumerate(features):
            draw.text(((w - 600) // 2, start_y + i * 42), feat, font=FONT_OUTRO_FEATURE, fill=(220, 240, 230))
            
        draw.text(((w - 340) // 2, 555), "SEE YOU ON THE BATTLEFIELD!", font=FONT_OUTRO_SUB, fill=(0, 255, 180))
        
        frame_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        if f >= num_frames - 35:
            alpha = (num_frames - f) / 35.0
            frame_bgr = (frame_bgr.astype(np.float32) * alpha).astype(np.uint8)
            
        frames.append(frame_bgr)
        
    return frames

def build_vol3_montage():
    print("=== STARTING EVILSHTRIB VOLUME 3 (60-SECOND) MONTAGE GENERATOR ===")
    
    all_frames = []
    
    # 1. Transparent Intro (90 frames = 3.00s)
    clip_01_path = os.path.join(CLIPS_DIR, "clip_01.mp4")
    print("Generating Transparent Intro sequence (90 frames)...")
    intro_frames = generate_transparent_intro_frames(clip_01_path, 90)
    all_frames.extend(intro_frames)
    print(f"  Intro added. Total frames: {len(all_frames)}")
    
    # 2. Process all 12 clips
    for idx, cfg in enumerate(CLIPS_CONFIG, 1):
        clip_path = os.path.join(CLIPS_DIR, cfg["file"])
        print(f"Processing Clip {idx:02d}: {cfg['file']} (frames {cfg['start']} -> {cfg['end']})")
        
        cap = cv2.VideoCapture(clip_path)
        raw_frames = []
        while True:
            ret, frame = cap.read()
            if not ret: break
            raw_frames.append(frame)
        cap.release()
        
        start = cfg["start"]
        end = min(cfg["end"], len(raw_frames))
        kills = cfg["kills"]
        fx_fn = FX_MAP[cfg["fx"]]
        
        clip_processed = []
        for raw_idx in range(start, end):
            frame = raw_frames[raw_idx].copy()
            
            dists = [raw_idx - k for k in kills]
            min_abs_d = min(abs(d) for d in dists)
            closest_d = [d for d in dists if abs(d) == min_abs_d][0]
            
            frame = fx_fn(frame, closest_d)
            is_kill_active = (0 <= closest_d <= 8)
            
            frame = render_hud_overlay(frame, cfg, is_kill_active=is_kill_active, hud_alpha=1.0)
            clip_processed.append(frame)
            
        all_frames.extend(clip_processed)
        print(f"  Clip {idx:02d} added: {len(clip_processed)} frames. Running total: {len(all_frames)}")
        
    # 3. Outro sequence (120 frames = 4.00s)
    print("Generating Outro sequence (120 frames)...")
    outro_frames = generate_outro_frames(120)
    all_frames.extend(outro_frames)
    total_frames = len(all_frames)
    print(f"  Outro added. Grand total frames: {total_frames} ({total_frames/30.0:.2f}s)")
    
    # 4. Write intermediate video stream
    temp_video = os.path.join(TOOLS_DIR, "temp_vol3_montage.mp4")
    print(f"Writing intermediate video stream to {temp_video}...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, 30.0, (1280, 720))
    for f in all_frames:
        out.write(f)
    out.release()
    print("Intermediate video written successfully!")
    
    # 5. Prepare Audio Track
    total_dur = total_frames / 30.0
    print(f"Total video duration: {total_dur:.2f}s")
    
    audio_in = os.path.join(TOOLS_DIR, "phonk_house.opus")
    audio_out = os.path.join(TOOLS_DIR, "montage_audio_vol3.wav")
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
    final_output = os.path.join(OUT_DIR, "EvilShtrib_60s_Vol3.mp4")
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
        "-movflags", "+faststart",
        "-shortest",
        final_output
    ]
    subprocess.run(cmd_mux, check=True)
    
    for temp_f in [temp_video, audio_out]:
        try: os.remove(temp_f)
        except OSError: pass
        
    print("=== VOLUME 3 MONTAGE GENERATION COMPLETE! ===")
    print(f"Final MP4: {final_output}")
    print(f"File size: {os.path.getsize(final_output) / (1024*1024):.2f} MB")
    print(f"Exact Duration: {total_dur:.2f} seconds")

if __name__ == "__main__":
    build_vol3_montage()
