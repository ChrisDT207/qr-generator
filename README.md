# QR Code Generator Pro

A modern, fast, cross-platform desktop **QR Code Generator** built with **Python**, **PyQt6**, **qrcode**, and **Pillow**.

---

## Key Features

### 1. Flexible Input Section
- **Multi-Type Templates:** Seamlessly switch between structured templates:
  - **URL & Plain Text:** Direct text input with auto-detection.
  - **Wi-Fi Configuration:** Network Name (SSID), Password, Encryption (WPA/WPA2/WPA3, WEP, Open), and Hidden Network option.
  - **Contact Card (vCard 3.0):** Full Name, Phone, Email, and Organization.
  - **Email:** Recipient, Subject, and Body (`mailto:`).
- **Character Count Indicator:** Live counter showing exact payload size and UTF-8 characters.
- **Preset Examples:** Quick dropdown to test Wi-Fi, vCard, GitHub, or Email payloads with a single click.

### 2. Deep Customization Controls
- **Error Correction Levels:**
  - `Low (L)`: ~7% data recovery.
  - `Medium (M)`: ~15% data recovery (default).
  - `Quartile (Q)`: ~25% data recovery.
  - `High (H)`: ~30% data recovery (recommended for center logos).
- **Sizing & Spacing Sliders:**
  - **Module Box Size:** Adjustable from 4 px to 24 px with live numeric feedback.
  - **Border Margin:** Adjustable quiet zone from 0 to 8 module units.
- **Color Palettes:**
  - **Custom Pickers:** Full color picker dialog (`QColorDialog`) and hexadecimal inputs for both code modules and background.
  - **Quick Palettes:** One-click presets (Classic, Cyber Emerald, Royal Blue, Crimson, Sunset Dark).
  - **Color Inversion:** Instant "⇄ Swap" button to invert foreground and background colors.
- **Center Logo Overlay:**
  - Upload custom logo/icon images (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.ico`).
  - Automatic contrast shield behind the logo to prevent scanning issues.
  - Auto-switches to High (H) error correction to maintain 100% scan reliability.
  - Thumbnail preview and one-click "Remove Logo" button.

### 3. Live Preview & Real-Time Output
- **Real-Time Generation:** Debounced live rendering (50ms) updates the preview canvas instantly as you type or adjust sliders.
- **High-Resolution Canvas:** Antialiased rendering displaying exact pixel dimensions (e.g. `370 × 370 px`).
- **Dark & Light Themes:** Modern theme toggleable from the navbar anytime.

### 4. Versatile Export Options
- **"Save Image..." File Dialog:**
  - **PNG (`.png`)**: Standard raster format.
  - **JPEG (`.jpg`, `.jpeg`)**: Flattened high-quality image.
  - **SVG Vector (`.svg`)**: Infinite scalability for professional printing.
- **"Copy to Clipboard":**
  - Copies the high-resolution QR code directly into the system clipboard (`QApplication.clipboard().setPixmap(...)`).
  - Animated visual feedback (`✓ Copied Image!`).
- **Resolution Scale Multiplier:**
  - `1× Standard` (Screen / Web)
  - `2× High-Res` (Documents)
  - `4× Ultra Print HD` (Large format print)

---

## Project Structure

```text
qr-code-generator/
├── main.py                     # Application entry point and CLI runner
├── build.py                    # Automated Windows .exe packaging pipeline
├── build.ps1                   # One-click PowerShell build script
├── generator.spec              # PyInstaller specification & binary bundling rules
├── create_sample_codes.py      # Utility generating test QR codes
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation
├── BUILD.md                    # Windows packaging & troubleshooting guide
├── assets/                     # High-DPI icons and branding assets
│   └── icon.ico
├── samples/                    # Pre-generated sample QR codes
│   ├── sample_url.png
│   ├── sample_wifi.png
│   ├── sample_vcard.png
│   └── sample_text.png
├── src/
│   ├── __init__.py
│   ├── engine/
│   │   ├── __init__.py
│   │   └── generator.py        # Core QR generation engine (qrcode + Pillow + SVG)
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Main window coordinator
│   │   ├── input_widget.py     # Content text area & template builder
│   │   ├── customize_widget.py # Error correction, sizing, colors, and logo
│   │   ├── preview_widget.py   # Live high-res preview canvas & export toolbar
│   │   ├── icons.py            # Resolution-independent vector SVG icons
│   │   └── styles.py           # Modern Dark & Light QSS theme stylesheets
│   └── utils/
│       ├── __init__.py
│       ├── templates.py        # Wi-Fi, vCard, Email payload formatters
│       ├── resource_finder.py  # Runtime bundle path and asset locator
│       └── url_helper.py       # URL validation and parser
└── tests/
    ├── test_generator.py       # Engine, customization, and export tests
    └── test_gui.py             # PyQt6 GUI and headless widget tests
```

---

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
python main.py
```

### Optional: Pass Initial Content via CLI
```bash
python main.py "https://github.com"
```

---

## Running Automated Tests

Run the full automated test suite:
```bash
python -m unittest discover tests
```
*All 24 automated tests validate QR code generation, Pillow logo blending, SVG vector output, payload templates, and PyQt6 GUI components.*

---

## Building Standalone Windows Executable (.exe)

Compile the application into an optimized, highly-compressed standalone Windows executable with no terminal pop-up (`dist/QRGenerator.exe` ~24.6 MB) and portable distribution package (`dist/QRGenerator-v2.0-win64.zip`):

```bash
# Using Python
python build.py

# Or using PowerShell
.\build.ps1
```

See [BUILD.md](file:///c:/Users/chris/OneDrive/Desktop/Personal%20Projects/qr-code-generator/BUILD.md) for advanced build configurations, UPX compression settings, and code signing details.
