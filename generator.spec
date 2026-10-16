# -*- mode: python ; coding: utf-8 -*-
"""Production PyInstaller spec configuration for QR Code Generator Pro.

Optimized for maximum compression, minimal binary footprint, and fast startup
while maintaining 100% feature compatibility (SVG vector, PNG, JPEG, logos, palettes).
"""

import os
import sys

block_cipher = None

# Base workspace directory
project_dir = os.path.abspath(SPECPATH)

# 1. Collect Data Assets
datas = []

# Include application assets (icons, etc.)
assets_dir = os.path.join(project_dir, "assets")
if os.path.isdir(assets_dir):
    datas.append((assets_dir, "assets"))

# Include sample QR images for test scanning
samples_dir = os.path.join(project_dir, "samples")
if os.path.isdir(samples_dir):
    datas.append((samples_dir, "samples"))

# 2. Dynamic Binaries
binaries = []

# 3. Explicit Hidden Imports
hiddenimports = [
    # PyQt6 core and GUI modules
    "PyQt6",
    "PyQt6.QtCore",
    "PyQt6.QtGui",
    "PyQt6.QtWidgets",
    "PyQt6.QtSvg",
    # Imaging and QR code generation
    "PIL",
    "PIL.Image",
    "PIL.ImageColor",
    "PIL.ImageDraw",
    "PIL.PngImagePlugin",
    "PIL.JpegImagePlugin",
    "qrcode",
    "qrcode.image.svg",
    "qrcode.image.pil",
    # Internal project modules
    "src",
    "src.engine",
    "src.engine.generator",
    "src.ui",
    "src.ui.main_window",
    "src.ui.input_widget",
    "src.ui.customize_widget",
    "src.ui.preview_widget",
    "src.ui.styles",
    "src.ui.icons",
    "src.utils",
    "src.utils.resource_finder",
    "src.utils.templates",
    "src.utils.url_helper",
    "src.utils.window_theme",
]

# 4. Exclude unnecessary heavy packages to minimize binary size
excludes = [
    # Heavy scientific / unused libraries
    "cv2",
    "pyzbar",
    "numpy",
    "matplotlib",
    "scipy",
    "pandas",
    "tkinter",
    "IPython",
    "notebook",
    "jupyter",
    "tornado",
    "test",
    "unittest",
    "pydoc",
    "sqlite3",
    # Unused PyQt6 modules
    "PyQt6.QtMultimedia",
    "PyQt6.QtNetwork",
    "PyQt6.QtPdf",
    "PyQt6.QtQml",
    "PyQt6.QtQuick",
    "PyQt6.QtSql",
    "PyQt6.QtTest",
    "PyQt6.QtXml",
    "PyQt6.QtBluetooth",
    "PyQt6.QtPositioning",
    "PyQt6.QtNfc",
    "PyQt6.QtWebSockets",
    # Unused stdlib services
    "http.server",
    "xmlrpc",
    "asyncio",
    "multiprocessing",
]

# 5. Application Icon
icon_path = os.path.join(project_dir, "assets", "icon.ico")
if not os.path.isfile(icon_path):
    icon_path = None

a = Analysis(
    [os.path.join(project_dir, "main.py")],
    pathex=[project_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Strip unnecessary large DLLs and plugins to compress binary size
excluded_binaries = {
    "opengl32sw.dll",             # Mesa software OpenGL fallback (~20.6MB uncompressed)
    "qt6pdf.dll",                 # Qt6 PDF library (~4.4MB)
    "qpdf.dll",                   # Qt6 PDF image format plugin
    "_avif.cp313-win_amd64.pyd",  # AVIF decoder in Pillow (~7.5MB)
    "qtuiotouchplugin.dll",       # Unused touch input plugin
    "qtga.dll",                   # TGA image format plugin
    "qicns.dll",                  # Apple ICNS image format plugin
}

a.binaries = [
    b for b in a.binaries
    if os.path.basename(b[0]).lower() not in excluded_binaries
]

# Strip translation files (.qm) which take up several megabytes
a.datas = [
    d for d in a.datas
    if "translations" not in d[0].lower()
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="QRGenerator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # UPX compression enabled for maximum binary size reduction
    upx_exclude=[
        "vcruntime140.dll",
        "vcruntime140_1.dll",
        "msvcp140.dll",
        "qwindows.dll",
    ],
    runtime_tmpdir=None,
    console=False,  # No terminal window pops up behind the GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
