import subprocess
import time
import os

STEAM_EXE = r"C:\Program Files (x86)\Steam\steam.exe"
STEAM_DIR = r"C:\Program Files (x86)\Steam"

def is_steam_running():
    try:
        out = subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq steam.exe"], text=True)
        return "steam.exe" in out.lower()
    except Exception:
        return False

def start_steam():
    if is_steam_running():
        print("Steam is already running!")
        return True

    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200

    print("Launching Steam...")
    for attempt in range(5):
        proc = subprocess.Popen(
            [STEAM_EXE, "-silent"],
            cwd=STEAM_DIR,
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
            close_fds=True
        )
        # Give it up to 6 seconds to see if it exits with 42
        t0 = time.time()
        exited = False
        while time.time() - t0 < 6:
            ret = proc.poll()
            if ret is not None:
                print(f"Steam exited with code {ret}")
                exited = True
                break
            time.sleep(0.5)

        if not exited:
            # It didn't exit, so it's running!
            print("Steam is running in background!")
            return True

        if ret == 42:
            print("Received magic restart code 42, relaunching Steam...")
            time.sleep(1)
            continue
        else:
            print(f"Unexpected exit code {ret}, retrying...")
            time.sleep(1)

    return is_steam_running()

if __name__ == "__main__":
    ok = start_steam()
    print("Final status: Steam running =", ok)
