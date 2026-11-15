import cv2, os

for idx in range(1, 11):
    path = rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\clips_evilzomb\clip_{idx:02d}.mp4"
    cap = cv2.VideoCapture(path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 75)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\debug_frame_clip_{idx:02d}.jpg", frame)
    cap.release()
print("Saved debug frames at frame 75 for all 10 clips!")
