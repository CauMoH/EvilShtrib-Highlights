with open(r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike\cl_dlls\client.dll', 'rb') as f:
    data = f.read()

idx = data.find(b'trackplayer')
while idx != -1:
    context = data[max(0, idx-50):min(len(data), idx+150)]
    print(f"Match at {idx}: {repr(context)}")
    idx = data.find(b'trackplayer', idx+1)
