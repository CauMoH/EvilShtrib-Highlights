with open(r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike\cl_dlls\client.dll', 'rb') as f:
    data = f.read()

idx = data.find(b'playernext')
while idx != -1:
    context = data[max(0, idx-200):min(len(data), idx+300)]
    print(f"Match at {idx}: {repr(context)}")
    idx = data.find(b'playernext', idx+1)
