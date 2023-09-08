# Simulates actual physical action of pressing a keyboard key as opposed to programmatically
# simulating a keypress. TIP: For cleaner code, save as separate file and import it.

import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB = 0x09
VK_MENU = 0x12
VK_CONTROL = 0xA2
C_KEY = 0x43
V_KEY = 0x56
N_KEY = 0x4E
G_KEY = 0x47
VK_F4 = 0x73
I_KEY = 0x49
E_KEY = 0x45
VK_F2 = 0x71

VK_DOWN = 0x28
VK_UP = 0x26
# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    )


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    )

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    )


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT), ("mi", MOUSEINPUT), ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD), ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (
    wintypes.UINT,  # nInputs
    LPINPUT,  # pInputs
    ctypes.c_int,
)  # cbSize

# Functions


def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    x = INPUT(
        type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode, dwFlags=KEYEVENTF_KEYUP)
    )
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


# Mouse_Input?
def PressMouseKey(hexKeyCode):
    x = INPUT(type=INPUT_MOUSE, ki=MOUSEINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseMouseKey(hexKeyCode):
    x = INPUT(type=INPUT_MOUSE, ki=MOUSEINPUT(wVk=hexKeyCode, dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


""" def CtrlV():
    Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    PressKey(VK_CONTROL)  # Alt
    PressKey(C_KEY)  # Tab
    ReleaseKey(VK_TAB)  # Tab~
    time.sleep(0.1)
    ReleaseKey(C_KEY)  # Alt~
    time.sleep(0.2)
    ReleaseKey(VK_CONTROL) """


dict_associate = {
    "tab": 0x09,
    "alt": 0x12,
    "ctrl": 0xA2,
    "c": 0x43,
    "v": 0x56,
    "n": 0x4E,
    "g": 0x47,
    "f4": 0x73,
    "i": 0x49,
    "e": 0x45,
    "VK_DOWN": 0x28,
    "a": 0x41,
    "shift": 0xA0,
    "VK_LEFT": 0x25
}


def key_down(key_in):
    # An actual simulation
    PressKey(VK_CONTROL)  # Alt
    PressKey(C_KEY)  # Tab
    # ReleaseKey(VK_TAB)  # Tab~
    time.sleep(0.1)
    ReleaseKey(C_KEY)  # Alt~
    time.sleep(0.1)
    ReleaseKey(VK_CONTROL)


# 624x466


def single_Key(key):
    PressKey(key)
    time.sleep(0.01)
    ReleaseKey(key)


def get_3key_comb(key_comb):
    key_comb = key_comb.split("+")

    PressKey(dict_associate[key_comb[0]])
    PressKey(dict_associate[key_comb[1]])
    PressKey(dict_associate[key_comb[2]])
    time.sleep(0.1)
    ReleaseKey(dict_associate[key_comb[2]])
    time.sleep(0.1)
    ReleaseKey(dict_associate[key_comb[1]])
    time.sleep(0.1)
    ReleaseKey(dict_associate[key_comb[0]])


def get_key_comb(key_comb):
    key_comb = key_comb.split("+")

    PressKey(dict_associate[key_comb[0]])
    PressKey(dict_associate[key_comb[1]])
    time.sleep(0.1)
    ReleaseKey(dict_associate[key_comb[1]])
    time.sleep(0.1)
    ReleaseKey(dict_associate[key_comb[0]])


# Mouse portion:


if __name__ == "__main__":
    print("may remove")
