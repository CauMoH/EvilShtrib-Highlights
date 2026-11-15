import cv2, os

for idx in range(1, 11):
    img = cv2.imread(rf"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\debug_frame_clip_{idx:02d}.jpg")
    if img is not None:
        h, w = img.shape[:2]
        # Crop bottom right (weapon model)
        weapon_crop = img[int(h*0.5):, int(w*0.5):]
        # Crop top right (death notices)
        death_crop = img[:int(h*0.25), int(w*0.6):]
        # Check standard deviation or brightness
        print(f"Clip {idx:02d}: weapon_std={weapon_crop.std():.1f}, death_std={death_crop.std():.1f}, mean={img.mean():.1f}")
