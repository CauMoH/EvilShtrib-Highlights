import os, cv2, glob

CLIPS_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\clips_evilzomb"

for i in range(1, 11):
    fn = os.path.join(CLIPS_DIR, f"clip_{i:02d}.mp4")
    cap = cv2.VideoCapture(fn)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    print(f"clip_{i:02d}.mp4: {n:3d} frames, {n/fps:4.2f}s, {w}x{h} @ {fps:.1f} fps")
