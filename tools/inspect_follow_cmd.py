with open(r'D:\SteamLibrary\steamapps\common\Half-Life\cstrike\cl_dlls\client.dll', 'rb') as f:
    data = f.read()

idx = data.find(b'follow "%s"')
print("Found at:", idx)
context = data[idx-50:idx+200]
print("Context:", repr(context))
