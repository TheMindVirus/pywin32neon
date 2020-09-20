import win32gui, win32con, ctypes, enum
from ctypes import wintypes
import time

class Policy(ctypes.Structure):
    _fields_ = \
    [
        ("accentState", ctypes.wintypes.DWORD),
        ("accentFlags", ctypes.wintypes.DWORD),
        ("gradientColour", ctypes.wintypes.DWORD),
        ("animationId", ctypes.wintypes.DWORD)
    ]

class Context(ctypes.Structure):
    _fields_ = \
    [
        ("attributes", ctypes.wintypes.DWORD),
        ("policyData", ctypes.POINTER(Policy)),
        ("policySize", ctypes.c_size_t)
    ]
    
class Neon:
    ACCENT_DISABLED = 0
    ACCENT_BLURBEHIND = 3
    ACCENT_POLICY = 19
    
    policyEnabled = Policy()
    policyEnabled.accentState = ACCENT_BLURBEHIND
    policyEnabled.accentFlags = 0
    policyEnabled.gradientColour = 0
    policyEnabled.animationId = 0
    
    policyDisabled = Policy()
    policyDisabled.accentState = ACCENT_DISABLED
    policyDisabled.accentFlags = 0
    policyDisabled.gradientColour = 0
    policyDisabled.animationId = 0

    contextEnabled = Context()
    contextEnabled.attributes = ACCENT_POLICY
    contextEnabled.policyData = ctypes.pointer(policyEnabled)
    contextEnabled.policySize = ctypes.sizeof(policyEnabled)

    contextDisabled = Context()
    contextDisabled.attributes = ACCENT_POLICY
    contextDisabled.policyData = ctypes.pointer(policyDisabled)
    contextDisabled.policySize = ctypes.sizeof(policyDisabled)
    
    def enable(window):
        user32 = ctypes.cdll.LoadLibrary("user32.dll")
        result = user32.SetWindowCompositionAttribute(window, ctypes.pointer(Neon.contextEnabled))
        print(result)
        return result
        
    def disable(window):
        user32 = ctypes.cdll.LoadLibrary("user32.dll")
        result = user32.SetWindowCompositionAttribute(window, ctypes.pointer(Neon.contextDisabled))
        return result

def testwndproc(hWnd, message, wParam, lParam):
    if message == win32con.WM_PAINT:
        hdc, ps = win32gui.BeginPaint(hWnd)
        client = win32gui.GetClientRect(hWnd)
        brush =  win32gui.CreateSolidBrush(0)
        win32gui.FillRect(hdc, client, brush)
        win32gui.EndPaint(hWnd, ps)
    return win32gui.DefWindowProc(hWnd, message, wParam, lParam)
    
def test():
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "NEON"
    wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wc.lpfnWndProc = testwndproc
    atom = win32gui.RegisterClass(wc)
    hWnd = win32gui.CreateWindow(wc.lpszClassName, None,
                                 win32con.WS_OVERLAPPEDWINDOW,
                                 win32con.CW_USEDEFAULT, 0, win32con.CW_USEDEFAULT, 0,
                                 None, None, None, None)
    Neon.enable(hWnd)
    win32gui.ShowWindow(hWnd, True)
    win32gui.UpdateWindow(hWnd)
    while True:
        try:
            win32gui.InvalidateRect(hWnd, None, True)
            win32gui.PumpWaitingMessages()
        except:
            pass
    win32gui.DestroyWindow(hWnd)
    win32gui.UnregisterClass(wc.lpszClassName, None)

test()
