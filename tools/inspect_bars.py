import cv2, os, numpy as np

# In CS 1.6 spectator mode, bottom center (x: 450..830, y: 670..710) contains the player name
# Let's inspect bottom center and weapon area (x: 800..1280, y: 400..720)
for idx in range(1, 11):
    cap = cv2.VideoCapture(rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\clips_evilzomb\clip_{idx:02d}.mp4")
    cap.set(cv2.CAP_PROP_POS_FRAMES, 75)
    ret, f = cap.read()
    if ret:
        h, w = f.shape[:2]
        # Crop spectator bar at bottom center
        bar = f[h-50:h-10, w//2-200:w//2+200]
        # Save crop for inspection
        cv2.imwrite(rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\contact_sheets\bar_{idx:02d}.jpg", bar)
        # Check weapon model (bottom right)
        wpn = f[h-250:, w-400:]
        cv2.imwrite(rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\contact_sheets\wpn_{idx:02d}.jpg", wpn)
        print(f"Clip {idx:02d}: bar shape={bar.shape}, mean={bar.mean():.1f}, wpn mean={wpn.mean():.1f}")
    cap.release()
