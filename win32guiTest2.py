import win32gui

hoi3_hwnd = win32gui.FindWindow(None, "Windows Task-Manager")
win32gui.CloseWindow(hoi3_hwnd)