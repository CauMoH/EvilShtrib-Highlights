import sys, struct

with open(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611141954-zm_lb.dem', 'rb') as f:
    f.seek(540) # header is 540 bytes
    max_time = 0
    frames = 0
    while True:
        b = f.read(1)
        if not b: break
        cmd = b[0]
        if cmd == 5: # next section
            break
        time_sec = struct.unpack('<f', f.read(4))[0]
        frame = struct.unpack('<I', f.read(4))[0]
        if time_sec > max_time:
            max_time = time_sec
        frames = max(frames, frame)
        if cmd in (0, 1): # packet
            f.seek(464, 1) # lump / seq
            length = struct.unpack('<I', f.read(4))[0]
            f.seek(length, 1)
        elif cmd == 2: # sync
            pass
        elif cmd == 3: # client command
            f.seek(64, 1)
        elif cmd == 4: # unknown
            f.seek(32, 1)
        elif cmd == 8: # sound
            f.seek(4, 1)
            length = struct.unpack('<I', f.read(4))[0]
            f.seek(length, 1)
        elif cmd == 9: # user command
            f.seek(4, 1)
            length = struct.unpack('<I', f.read(4))[0]
            f.seek(length, 1)
        else:
            break

print(f"Demo max time: {max_time:.2f}s, total frames: {frames}")
