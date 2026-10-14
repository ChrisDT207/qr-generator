"""Main application window for QR Code Generator Pro."""

from __future__ import annotations

import logging
import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QSplitter,
    QStatusBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..engine.generator import QRCodeConfig
from .customize_widget import CustomizeWidget
from .icons import get_icon
from .input_widget import InputWidget
from .preview_widget import PreviewWidget
from .styles import DARK_THEME, LIGHT_THEME

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window coordinating inputs, customization, and live QR preview."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QR Code Generator Pro")
        self.setWindowIcon(get_icon("qr-code", color="#10b981", size=32))
        self.resize(1120, 760)
        self.setMinimumSize(880, 580)

        self._is_dark_theme = True

        # Debounce timer for smooth typing and responsive live updates
        self._debounce_timer = QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self._render_qr_code)

        self._init_ui()
        self._apply_theme()

        # Initial render
        self._render_qr_code()

    def _init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(12)

        # 1. Navbar Header
        navbar = self._create_navbar()
        main_layout.addWidget(navbar)

        # 2. Main Content Splitter (Left: Controls, Right: Live Preview)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)

        # --- Left Column: Controls (Scrollable) ---
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        # Input Section
        self.input_widget = InputWidget()
        self.input_widget.text_changed.connect(self._schedule_render)
        left_layout.addWidget(self.input_widget)

        # Customization Section (wrapped in scroll area)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.customize_widget = CustomizeWidget()
        self.customize_widget.settings_changed.connect(self._schedule_render)
        scroll_area.setWidget(self.customize_widget)
        left_layout.addWidget(scroll_area, 1)

        # --- Right Column: Live Preview & Export ---
        self.preview_widget = PreviewWidget()

        splitter.addWidget(left_container)
        splitter.addWidget(self.preview_widget)
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 6)

        main_layout.addWidget(splitter, 1)

        # 3. Status Bar
        self._setup_status_bar()

    def _create_navbar(self) -> QWidget:
        """Create header toolbar with brand title, presets, and theme toggle."""
        nav = QFrame()
        nav.setProperty("class", "CardPanel")
        layout = QHBoxLayout(nav)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(12)

        # Brand Title
        title_icon = QLabel()
        title_icon.setPixmap(get_icon("qr-code", color="#10b981", size=24).pixmap(24, 24))

        title_lbl = QLabel("QR Code Generator Pro")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 700; color: #f8fafc;")

        version_badge = QLabel("v2.0")
        version_badge.setProperty("class", "BadgeFormat")

        layout.addWidget(title_icon)
        layout.addWidget(title_lbl)
        layout.addWidget(version_badge)
        layout.addStretch()

        # Quick Samples Dropdown
        samples_lbl = QLabel("Load Preset:")
        samples_lbl.setStyleSheet("color: #94a3b8; font-weight: 600; font-size: 12px;")
        self.samples_combo = QComboBox()
        self.samples_combo.addItem("Select Example...", "")
        self.samples_combo.addItem("GitHub (URL)", "https://github.com/google")
        self.samples_combo.addItem("Office Wi-Fi", "WIFI:T:WPA;S:Office_WiFi_5G;P:SecurePass2026!;H:false;;")
        self.samples_combo.addItem("vCard Contact", "BEGIN:VCARD\nVERSION:3.0\nFN:Alex Mercer\nORG:Tech Dynamics\nTEL:+1-555-0199\nEMAIL:alex@example.com\nEND:VCARD")
        self.samples_combo.addItem("Email Feedback", "mailto:feedback@example.com?subject=Great%20App")
        self.samples_combo.currentIndexChanged.connect(self._on_preset_selected)

        layout.addWidget(samples_lbl)
        layout.addWidget(self.samples_combo)

        # Theme Switcher
        self.theme_btn = QToolButton()
        self.theme_btn.setToolTip("Switch Theme (Dark / Light)")
        self.theme_btn.setIcon(get_icon("sun", color="#94a3b8", size=18))
        self.theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_btn)

        # About Dialog Button
        self.about_btn = QToolButton()
        self.about_btn.setToolTip("About QR Code Generator Pro")
        self.about_btn.setIcon(get_icon("target", color="#94a3b8", size=18))
        self.about_btn.clicked.connect(self._show_about)
        layout.addWidget(self.about_btn)

        return nav

    def _setup_status_bar(self) -> None:
        """Setup status bar indicators."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_gen_lbl = QLabel("Ready")
        self.status_engine_lbl = QLabel("Engine: qrcode + Pillow")

        self.status_bar.addWidget(self.status_gen_lbl, 1)
        self.status_bar.addPermanentWidget(self.status_engine_lbl)

    def _schedule_render(self) -> None:
        """Trigger debounced QR code rendering to avoid UI stutter on fast keystrokes."""
        self._debounce_timer.start(50)

    def _render_qr_code(self) -> None:
        """Read active input and customization parameters and update the preview canvas."""
        t0 = time.time()
        payload = self.input_widget.get_payload()
        config = self.customize_widget.get_config(payload)

        try:
            self.preview_widget.update_preview(config)
            ms = (time.time() - t0) * 1000
            self.status_gen_lbl.setText(f"Generated live in {ms:.1f} ms · {len(payload)} chars")
        except Exception as e:
            logger.error("QR Code generation error: %s", e)
            self.status_gen_lbl.setText(f"Generation error: {e}")

    def _on_preset_selected(self, idx: int) -> None:
        payload = self.samples_combo.currentData()
        if payload:
            self.input_widget.set_payload(payload)

    def _apply_theme(self) -> None:
        theme_qss = DARK_THEME if self._is_dark_theme else LIGHT_THEME
        self.setStyleSheet(theme_qss)

        icon_name = "sun" if self._is_dark_theme else "moon"
        icon_color = "#94a3b8" if self._is_dark_theme else "#475569"
        self.theme_btn.setIcon(get_icon(icon_name, color=icon_color, size=18))

    def _toggle_theme(self) -> None:
        self._is_dark_theme = not self._is_dark_theme
        self._apply_theme()

    def _show_about(self) -> None:
        QMessageBox.information(
            self,
            "About QR Code Generator Pro",
            "<h3>QR Code Generator Pro v2.0</h3>"
            "<p>A modern desktop QR Code Generator built with <b>Python</b>, <b>PyQt6</b>, <b>qrcode</b>, and <b>Pillow</b>.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Live real-time preview rendering</li>"
            "<li>Templates for URLs, Wi-Fi networks, vCards, and Emails</li>"
            "<li>Custom color palettes and error correction controls</li>"
            "<li>Center logo/icon overlay support</li>"
            "<li>Export to PNG, JPG, and scalable vector SVG</li>"
            "<li>Direct Copy-to-Clipboard</li>"
            "</ul>",
        )
