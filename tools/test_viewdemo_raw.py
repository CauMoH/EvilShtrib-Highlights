import subprocess, time

p = subprocess.Popen([
    r'D:\SteamLibrary\steamapps\common\Half-Life\hl_recorder.exe',
    '-game', 'cstrike',
    '-windowed', '-w', '640', '-h', '480',
    '+viewdemo', 'render_clip'
])

t0 = time.time()
while time.time() - t0 < 8:
    if p.poll() is not None:
        print("Exited with code:", p.returncode)
        break
    time.sleep(1)
else:
    print("Still running after 8s")
    p.kill()
