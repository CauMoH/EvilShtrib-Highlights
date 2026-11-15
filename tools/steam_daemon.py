import subprocess, time

STEAM_EXE = r"C:\Program Files (x86)\Steam\steam.exe"

while True:
    try:
        proc = subprocess.run([STEAM_EXE, "-silent"])
        print(f"Steam exited with code {proc.returncode}, relaunching in 2s...")
    except Exception as e:
        print(f"Steam exception: {e}")
    time.sleep(2)
