import re

with open(r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike\cl_dlls\client.dll', 'rb') as f:
    data = f.read()

# Find all console command registrations: "AddCommand" or strings registered with gEngfuncs.pfnAddCommand
strings = [s.decode('latin1', errors='ignore') for s in re.findall(rb'[a-zA-Z0-9_+]{3,30}\x00', data)]
cmd_candidates = [s for s in set(strings) if any(w in s for w in ['spec', 'target', 'track', 'player', 'attack'])]
print("Found candidates:", sorted(cmd_candidates))
