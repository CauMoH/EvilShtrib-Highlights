import cv2, os, glob

for idx in range(1, 13):
    path = rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\clips_hyper\clip_{idx:02d}.mp4"
    cap = cv2.VideoCapture(path)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, min(30, count-1))
    ret, f = cap.read()
    if ret:
        h, w = f.shape[:2]
        wpn = f[int(h*0.5):, int(w*0.5):]
        center = f[int(h*0.35):int(h*0.65), int(w*0.35):int(w*0.65)]
        print(f"Clip {idx:02d}: {count} frames ({count/30:.2f}s) | wpn_mean={wpn.mean():.1f}, wpn_std={wpn.std():.1f} | center_std={center.std():.1f}")
    cap.release()
