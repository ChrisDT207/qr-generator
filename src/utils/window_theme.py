"""Windows Desktop Window Manager (DWM) title bar theming helper."""

from __future__ import annotations

import ctypes
import logging
import sys

logger = logging.getLogger(__name__)

# DWM attribute constants
DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36


def update_window_titlebar_theme(hwnd: int, is_dark: bool) -> None:
    """Set the Windows 10/11 OS title bar, caption buttons (min/max/close), and colors to match the app theme.

    Args:
        hwnd: Native window handle (from QWidget.winId())
        is_dark: True for dark mode, False for light mode
    """
    if sys.platform != "win32" or not hwnd:
        return

    try:
        dwmapi = ctypes.windll.dwmapi
        user32 = ctypes.windll.user32

        # 1. DWMWA_USE_IMMERSIVE_DARK_MODE: Toggles dark/light caption buttons (minimize, maximize, close)
        # Windows 11 and Windows 10 build 19041+ use 20; build 17763-18363 use 19.
        dark_flag = ctypes.c_int(1 if is_dark else 0)
        hr = dwmapi.DwmSetWindowAttribute(
            ctypes.c_void_p(hwnd),
            ctypes.c_uint(DWMWA_USE_IMMERSIVE_DARK_MODE),
            ctypes.byref(dark_flag),
            ctypes.sizeof(dark_flag),
        )
        if hr != 0:
            dwmapi.DwmSetWindowAttribute(
                ctypes.c_void_p(hwnd),
                ctypes.c_uint(DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1),
                ctypes.byref(dark_flag),
                ctypes.sizeof(dark_flag),
            )

        # 2. Windows 11 (build 22000+): Set matching caption bar color and text color
        # COLORREF format in Win32 API is 0x00BBGGRR
        if is_dark:
            # Dark title bar background: #0b0f19 (BGR: 0x19, 0x0F, 0x0B)
            caption_color = ctypes.c_int(0x00190F0B)
            # Title text color: #f8fafc (BGR: 0xFC, 0xFA, 0xF8)
            text_color = ctypes.c_int(0x00FCFAF8)
        else:
            # Light title bar background: #f8fafc (BGR: 0xFC, 0xFA, 0xF8)
            caption_color = ctypes.c_int(0x00FCFAF8)
            # Title text color: #0f172a (BGR: 0x2A, 0x17, 0x0F)
            text_color = ctypes.c_int(0x002A170F)

        dwmapi.DwmSetWindowAttribute(
            ctypes.c_void_p(hwnd),
            ctypes.c_uint(DWMWA_CAPTION_COLOR),
            ctypes.byref(caption_color),
            ctypes.sizeof(caption_color),
        )
        dwmapi.DwmSetWindowAttribute(
            ctypes.c_void_p(hwnd),
            ctypes.c_uint(DWMWA_TEXT_COLOR),
            ctypes.byref(text_color),
            ctypes.sizeof(text_color),
        )

        # 3. Trigger immediate frame update on window
        # SWP_NOMOVE (0x2) | SWP_NOSIZE (0x1) | SWP_NOZORDER (0x4) | SWP_FRAMECHANGED (0x20) = 0x0027
        user32.SetWindowPos(ctypes.c_void_p(hwnd), 0, 0, 0, 0, 0, 0x0027)

    except Exception as e:
        logger.debug("Failed to set window titlebar theme: %s", e)
