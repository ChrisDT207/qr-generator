# Windows Executable Packaging Guide

This document outlines how to build, customize, and troubleshoot the standalone Windows `.exe` (`QRGenerator.exe`) and compressed distribution zip for the QR Code Generator Pro desktop application.

---

## ⚡ Quick Start: Building the Binary

You can run the automated packaging pipeline using either Python or PowerShell:

### Option A: Using Python (Recommended)
```bash
python build.py
```

### Option B: Using PowerShell
```powershell
.\build.ps1
```

Once the build finishes, your artifacts will be located in `dist/`:
- **Standalone Executable:** `dist/QRGenerator.exe` (~24.6 MB)
- **Compressed Release Package:** `dist/QRGenerator-v2.0-win64.zip` (~24.4 MB)

---

## 🛠️ Pipeline Architecture & Compression Optimizations

The packaging pipeline is orchestrated by:
1. **[`build.py`](file:///c:/Users/chris/OneDrive/Desktop/Personal%20Projects/qr-code-generator/build.py):**
   - Verifies Python environment and dependencies (`PyQt6`, `qrcode`, `Pillow`, `PyInstaller`).
   - Automatically detects and configures UPX binary compressor from `tools/upx/`.
   - Ensures application icon (`assets/icon.ico`) and sample QR codes are generated.
   - Cleans stale `build/` caches and `__pycache__` artifacts.
   - Invokes PyInstaller using `generator.spec`.
   - Validates the resulting `.exe` (checks file size and exit code).
   - Automatically packages a maximum-compression release zip (`QRGenerator-v2.0-win64.zip`).
2. **[`generator.spec`](file:///c:/Users/chris/OneDrive/Desktop/Personal%20Projects/qr-code-generator/generator.spec):**
   - Configured with `console=False` (`--noconsole` / `--windowed`) so no command prompt pops up behind the GUI.
   - **Bloat Binary Stripping:** Excludes heavy unnecessary binaries such as Mesa software OpenGL (`opengl32sw.dll` ~20.6 MB), Qt6 PDF plugins (`Qt6Pdf.dll`, `qpdf.dll`), AVIF Pillow decoders (`_avif.cp313-win_amd64.pyd`), and Qt touch/unneeded format plugins.
   - **Language Translation Stripping:** Filters out international `.qm` translation catalogs to save multi-megabyte overhead.
   - **UPX Compression:** Enabled with sensitive runtime DLLs excluded (`vcruntime140.dll`, `vcruntime140_1.dll`, `msvcp140.dll`, `qwindows.dll`) to maximize compression while ensuring 100% crash-free runtime stability.
   - **Binary Footprint:** Reduced from ~43 MB down to ~24.6 MB (nearly 43% size reduction).
3. **[`src/utils/resource_finder.py`](file:///c:/Users/chris/OneDrive/Desktop/Personal%20Projects/qr-code-generator/src/utils/resource_finder.py):**
   - Automatically detects whether the app is running in standard Python or inside PyInstaller (`sys._MEIPASS`).
   - Registers `sys._MEIPASS` with Windows `os.add_dll_directory` upon startup before any native module loading.

---

## 🔍 Troubleshooting Common Packaging Issues

### 1. Windows SmartScreen or Antivirus False Positives
**Cause:** Freshly packaged executables created with PyInstaller lack a recognized digital certificate signature from a commercial Certificate Authority, which can trigger generic heuristic warnings.

**Solutions:**
- **SmartScreen Bypass:** During local testing, click **"More info"** on the Windows SmartScreen dialog, then click **"Run anyway"**.
- **Code Signing (Production):** If distributing to external users, sign the binary using `signtool.exe` with a code-signing certificate:
  ```powershell
  signtool sign /f mycert.pfx /p "password" /t http://timestamp.digicert.com dist\QRGenerator.exe
  ```

### 2. Missing C-Runtime / MSVCP DLLs
**Cause:** Systems without the Microsoft Visual C++ runtime may occasionally encounter DLL load errors when initializing Qt6 platform plugins.

**Solution:**
- Install the official [Microsoft Visual C++ Redistributable (2015–2022 x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe).

### 3. Vector SVG & High-DPI Rendering
**Behavior:**
- The application bundles `PyQt6.QtSvg` and `Pillow` to guarantee crisp rendering across 100%, 150%, and 200% Windows scaling displays.
- Vector SVG exports do not lose fidelity regardless of display resolution or print scaling.

### 4. Cleaning Build Caches
If you make code changes and want to force a completely clean build:
```bash
python build.py --clean-only
python build.py
```
