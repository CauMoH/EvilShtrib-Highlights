import cv2

img = cv2.imread(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\test_follow_60.jpg')
h, w = img.shape[:2]
# Center of screen (crosshair and zombies)
center = img[int(h*0.35):int(h*0.65), int(w*0.35):int(w*0.65)]
print(f"Center brightness: {center.mean():.1f}, center std: {center.std():.1f}")

# Check top right for killfeed (DeathMsg)
deathfeed = img[:int(h*0.25), int(w*0.65):]
print(f"Deathfeed std: {deathfeed.std():.1f}")
