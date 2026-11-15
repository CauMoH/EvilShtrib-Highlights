import cv2, os, glob

# Check where deathnotice appears: top-right corner: y: [20..120], x: [800..1260]
for idx in range(1, 11):
    cap = cv2.VideoCapture(rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\clips_evilzomb\clip_{idx:02d}.mp4")
    f_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"--- CLIP {idx:02d} ({f_count} frames) ---")
    cap.release()
