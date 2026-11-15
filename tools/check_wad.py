import struct

with open(r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike_downloads\maps\zm_LB.bsp', 'rb') as f:
    version = struct.unpack('<I', f.read(4))[0]
    # lump 0 is entities
    ent_offset, ent_len = struct.unpack('<II', f.read(8))
    f.seek(ent_offset)
    ent_data = f.read(ent_len).decode('latin1', errors='ignore')
    
    for line in ent_data.split('\n'):
        if '"wad"' in line:
            print(line)
