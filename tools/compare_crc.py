import binascii, struct

with open(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611141954-zm_lb.dem', 'rb') as f:
    f.seek(8 + 4 + 4 + 260 + 260)
    demo_map_crc = struct.unpack('<I', f.read(4))[0]

with open(r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike_downloads\maps\zm_LB.bsp', 'rb') as f:
    bsp_data = f.read()
    bsp_crc = binascii.crc32(bsp_data) & 0xffffffff

print(f"Demo map CRC: {demo_map_crc} (0x{demo_map_crc:08X})")
print(f"File map CRC: {bsp_crc} (0x{bsp_crc:08X})")
