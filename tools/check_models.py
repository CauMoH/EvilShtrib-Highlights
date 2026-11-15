import struct, re

with open(r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike_downloads\maps\zm_LB.bsp', 'rb') as f:
    version = struct.unpack('<I', f.read(4))[0]
    ent_offset, ent_len = struct.unpack('<II', f.read(8))
    f.seek(ent_offset)
    ent_data = f.read(ent_len).decode('latin1', errors='ignore')
    
models = re.findall(r'"model"\s+"([^"]+)"', ent_data)
sounds = re.findall(r'"message"\s+"([^"]+)"', ent_data)
print("Models:", set(m for m in models if m.endswith('.mdl')))
print("Sounds:", set(s for s in sounds if s.endswith('.wav')))
