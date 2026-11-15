import os, re

files = [
    r'D:\SteamLibrary\steamapps\common\Half-Life\hl.exe',
    r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike\cl_dlls\client.dll',
    r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike\dlls\mp.dll',
]

patterns = [rb'\bspec_[a-zA-Z0-9_]+', rb'\bdem_[a-zA-Z0-9_]+', rb'\bhltv_[a-zA-Z0-9_]+']

found = set()
for path in files:
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = f.read()
            for p in patterns:
                for match in re.findall(p, data):
                    found.add(match.decode('latin1'))

for cmd in sorted(found):
    print(cmd)
