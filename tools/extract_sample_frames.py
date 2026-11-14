import cv2, os

OUT_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\montage_samples_60s"
os.makedirs(OUT_DIR, exist_ok=True)
VIDEO_PATH = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\EvilShtrib_60s_Montage.mp4"

samples = [
    (45, "01_intro_transparent_1.5s.jpg"),
    (135, "02_kill01_drop_famas_4.5s.jpg"),
    (330, "03_kill02_galil_zoom_11.0s.jpg"),
    (490, "04_kill03_galil_bullet_time_16.3s.jpg"),
    (650, "05_kill04_xm1014_shotgun_21.6s.jpg"),
    (810, "06_kill05_ump45_negative_27.0s.jpg"),
    (970, "07_kill06_m4a1_bloom_32.3s.jpg"),
    (1130, "08_kill07_grenade_radar_37.6s.jpg"),
    (1290, "09_kill08_deagle_blood_43.0s.jpg"),
    (1450, "10_kill09_awp_recoil_48.3s.jpg"),
    (1600, "11_kill10_m4a1_glitch_53.3s.jpg"),
    (1720, "12_outro_cta_connect_57.3s.jpg"),
]

cap = cv2.VideoCapture(VIDEO_PATH)
for frame_idx, fname in samples:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(os.path.join(OUT_DIR, fname), frame)
        print(f"Saved {fname} (frame {frame_idx})")
cap.release()
print("All verification sample frames extracted!")
