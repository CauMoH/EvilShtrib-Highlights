import cv2, os, numpy as np

CLIPS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\clips_evilzomb"
OUT_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\contact_sheets"
os.makedirs(OUT_DIR, exist_ok=True)

for i in range(1, 11):
    cap = cv2.VideoCapture(os.path.join(CLIPS_DIR, f"clip_{i:02d}.mp4"))
    frames = []
    # Grab 6 frames evenly spaced from frame 40 to 160 (step 24 = 0.8s)
    for f_idx in [45, 65, 75, 90, 115, 145]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
        ret, f = cap.read()
        if ret:
            # Resize to thumbnail 320x180
            thumb = cv2.resize(f, (320, 180))
            cv2.putText(thumb, f"F:{f_idx} ({(f_idx-75)/30:.1f}s)", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            frames.append(thumb)
    cap.release()
    if len(frames) == 6:
        # 2 rows of 3 columns
        row1 = np.hstack(frames[:3])
        row2 = np.hstack(frames[3:])
        sheet = np.vstack([row1, row2])
        cv2.imwrite(os.path.join(OUT_DIR, f"sheet_clip_{i:02d}.jpg"), sheet)
        print(f"Saved contact sheet for clip {i:02d}")
