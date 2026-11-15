import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

def enum_cb(hwnd, lparam):
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    buf = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, buf, 256)
    cls = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, cls, 256)
    vis = user32.IsWindowVisible(hwnd)
    if vis and buf.value:
        print(f"PID: {pid.value:5d} | HWND: {hwnd:8d} | '{buf.value}' ({cls.value})")
    return True

user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
