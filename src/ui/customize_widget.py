"""Customization controls for error correction, sizing, color palettes, and center logo overlay."""

from __future__ import annotations

import os
from typing import Optional

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from ..engine.generator import QRCodeConfig
from .icons import get_icon


class ColorSwatchButton(QPushButton):
    """Button displaying a visual colored swatch."""

    def __init__(self, color_hex: str = "#000000", parent=None) -> None:
        super().__init__(parent)
        self.setFixedSize(32, 28)
        self._color_hex = color_hex
        self.update_color(color_hex)

    def update_color(self, hex_val: str) -> None:
        self._color_hex = hex_val
        self.setStyleSheet(
            f"background-color: {hex_val}; border: 2px solid #475569; border-radius: 6px;"
        )

    @property
    def color_hex(self) -> str:
        return self._color_hex


class CustomizeWidget(QFrame):
    """Card containing error correction, size sliders, color pickers, and logo overlay."""

    settings_changed = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("CustomizeCard")
        self.setProperty("class", "CardPanel")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self._fg_color = "#000000"
        self._bg_color = "#ffffff"
        self._logo_path: Optional[str] = None

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # 1. Header
        title_lbl = QLabel("2. Customization & Styling")
        title_lbl.setProperty("class", "SectionTitle")
        layout.addWidget(title_lbl)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)

        # 2. Error Correction Dropdown
        ec_lbl = QLabel("Error Correction:")
        ec_lbl.setStyleSheet("font-weight: 600; color: #94a3b8;")
        self.ec_combo = QComboBox()
        self.ec_combo.addItem("Medium (~15% Recovery)", "M")
        self.ec_combo.addItem("Low (~7% Recovery)", "L")
        self.ec_combo.addItem("Quartile (~25% Recovery)", "Q")
        self.ec_combo.addItem("High (~30% Recovery - Logo Safe)", "H")
        self.ec_combo.currentIndexChanged.connect(self._on_setting_changed)

        grid.addWidget(ec_lbl, 0, 0)
        grid.addWidget(self.ec_combo, 0, 1)

        # 3. Box Size Slider
        bs_lbl = QLabel("Module Box Size:")
        bs_lbl.setStyleSheet("font-weight: 600; color: #94a3b8;")
        bs_layout = QHBoxLayout()
        self.bs_slider = QSlider(Qt.Orientation.Horizontal)
        self.bs_slider.setRange(4, 24)
        self.bs_slider.setValue(10)
        self.bs_val_lbl = QLabel("10 px")
        self.bs_val_lbl.setMinimumWidth(40)
        self.bs_slider.valueChanged.connect(self._on_box_size_changed)

        bs_layout.addWidget(self.bs_slider, 1)
        bs_layout.addWidget(self.bs_val_lbl)
        grid.addWidget(bs_lbl, 1, 0)
        grid.addLayout(bs_layout, 1, 1)

        # 4. Border Margin Slider
        border_lbl = QLabel("Border Margin:")
        border_lbl.setStyleSheet("font-weight: 600; color: #94a3b8;")
        border_layout = QHBoxLayout()
        self.border_slider = QSlider(Qt.Orientation.Horizontal)
        self.border_slider.setRange(0, 8)
        self.border_slider.setValue(4)
        self.border_val_lbl = QLabel("4 boxes")
        self.border_val_lbl.setMinimumWidth(40)
        self.border_slider.valueChanged.connect(self._on_border_changed)

        border_layout.addWidget(self.border_slider, 1)
        border_layout.addWidget(self.border_val_lbl)
        grid.addWidget(border_lbl, 2, 0)
        grid.addLayout(border_layout, 2, 1)

        layout.addLayout(grid)

        # 5. Color Palette Card
        colors_frame = QFrame()
        colors_frame.setProperty("class", "SubCardPanel")
        colors_layout = QVBoxLayout(colors_frame)
        colors_layout.setContentsMargins(12, 10, 12, 10)
        colors_layout.setSpacing(8)

        colors_title = QLabel("Color Palette")
        colors_title.setStyleSheet("font-weight: 600; font-size: 13px; color: #f8fafc;")
        colors_layout.addWidget(colors_title)

        pickers_layout = QHBoxLayout()
        pickers_layout.setSpacing(12)

        # Foreground Color
        fg_col = QVBoxLayout()
        fg_lbl = QLabel("Code Modules:")
        fg_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        fg_picker_row = QHBoxLayout()
        self.fg_swatch = ColorSwatchButton(self._fg_color)
        self.fg_swatch.clicked.connect(self._pick_fg_color)
        self.fg_hex_input = QLineEdit(self._fg_color)
        self.fg_hex_input.setMaximumWidth(75)
        self.fg_hex_input.textChanged.connect(self._on_fg_hex_edited)
        fg_picker_row.addWidget(self.fg_swatch)
        fg_picker_row.addWidget(self.fg_hex_input)
        fg_col.addWidget(fg_lbl)
        fg_col.addLayout(fg_picker_row)

        # Background Color
        bg_col = QVBoxLayout()
        bg_lbl = QLabel("Background:")
        bg_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        bg_picker_row = QHBoxLayout()
        self.bg_swatch = ColorSwatchButton(self._bg_color)
        self.bg_swatch.clicked.connect(self._pick_bg_color)
        self.bg_hex_input = QLineEdit(self._bg_color)
        self.bg_hex_input.setMaximumWidth(75)
        self.bg_hex_input.textChanged.connect(self._on_bg_hex_edited)
        bg_picker_row.addWidget(self.bg_swatch)
        bg_picker_row.addWidget(self.bg_hex_input)
        bg_col.addWidget(bg_lbl)
        bg_col.addLayout(bg_picker_row)

        # Swap button
        self.swap_btn = QPushButton("⇄ Swap")
        self.swap_btn.setFixedHeight(28)
        self.swap_btn.setToolTip("Invert code and background colors")
        self.swap_btn.clicked.connect(self._swap_colors)

        pickers_layout.addLayout(fg_col)
        pickers_layout.addLayout(bg_col)
        pickers_layout.addWidget(self.swap_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        colors_layout.addLayout(pickers_layout)

        # Quick Palette Presets
        presets_layout = QHBoxLayout()
        presets_layout.setSpacing(6)
        presets_lbl = QLabel("Presets:")
        presets_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
        presets_layout.addWidget(presets_lbl)

        palette_presets = [
            ("Classic", "#000000", "#ffffff"),
            ("Cyber Emerald", "#10b981", "#0b0f19"),
            ("Royal Blue", "#2563eb", "#ffffff"),
            ("Crimson", "#e11d48", "#ffffff"),
            ("Sunset Dark", "#f59e0b", "#18181b"),
        ]

        for name, fg, bg in palette_presets:
            p_btn = QPushButton(name)
            p_btn.setStyleSheet("font-size: 11px; padding: 3px 8px;")
            p_btn.clicked.connect(lambda _, f=fg, b=bg: self._apply_color_preset(f, b))
            presets_layout.addWidget(p_btn)

        presets_layout.addStretch()
        colors_layout.addLayout(presets_layout)

        layout.addWidget(colors_frame)

        # 6. Center Logo Card
        logo_frame = QFrame()
        logo_frame.setProperty("class", "SubCardPanel")
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(12, 10, 12, 10)
        logo_layout.setSpacing(8)

        logo_header = QHBoxLayout()
        logo_title = QLabel("Center Logo Overlay (Optional)")
        logo_title.setStyleSheet("font-weight: 600; font-size: 13px; color: #f8fafc;")
        logo_header.addWidget(logo_title)
        logo_header.addStretch()

        self.remove_logo_btn = QPushButton("Remove")
        self.remove_logo_btn.setIcon(get_icon("trash", color="#f43f5e", size=14))
        self.remove_logo_btn.setFixedHeight(24)
        self.remove_logo_btn.clicked.connect(self._remove_logo)
        self.remove_logo_btn.setVisible(False)
        logo_header.addWidget(self.remove_logo_btn)

        logo_layout.addLayout(logo_header)

        logo_ctrl_row = QHBoxLayout()
        self.logo_thumb = QLabel()
        self.logo_thumb.setFixedSize(32, 32)
        self.logo_thumb.setStyleSheet("background: #0f172a; border-radius: 4px; border: 1px dashed #334155;")
        self.logo_thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_btn = QPushButton("Choose Logo Image...")
        self.logo_btn.setIcon(get_icon("image", color="#3b82f6", size=16))
        self.logo_btn.clicked.connect(self._browse_logo)

        self.logo_name_lbl = QLabel("No logo selected")
        self.logo_name_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")

        logo_ctrl_row.addWidget(self.logo_thumb)
        logo_ctrl_row.addWidget(self.logo_btn)
        logo_ctrl_row.addWidget(self.logo_name_lbl, 1)
        logo_layout.addLayout(logo_ctrl_row)

        layout.addWidget(logo_frame)

    def get_config(self, data: str) -> QRCodeConfig:
        """Construct QRCodeConfig object from current control values."""
        ec = self.ec_combo.currentData() or "M"
        return QRCodeConfig(
            data=data,
            error_correction=ec,
            box_size=self.bs_slider.value(),
            border=self.border_slider.value(),
            fg_color=self._fg_color,
            bg_color=self._bg_color,
            logo_path=self._logo_path,
            logo_scale=0.22,
            logo_pad=True,
        )

    def _on_box_size_changed(self, val: int) -> None:
        self.bs_val_lbl.setText(f"{val} px")
        self._on_setting_changed()

    def _on_border_changed(self, val: int) -> None:
        self.border_val_lbl.setText(f"{val} boxes")
        self._on_setting_changed()

    def _pick_fg_color(self) -> None:
        col = QColorDialog.getColor(QColor(self._fg_color), self, "Select QR Code Color")
        if col.isValid():
            self._fg_color = col.name()
            self.fg_swatch.update_color(self._fg_color)
            self.fg_hex_input.setText(self._fg_color)
            self._on_setting_changed()

    def _pick_bg_color(self) -> None:
        col = QColorDialog.getColor(QColor(self._bg_color), self, "Select Background Color")
        if col.isValid():
            self._bg_color = col.name()
            self.bg_swatch.update_color(self._bg_color)
            self.bg_hex_input.setText(self._bg_color)
            self._on_setting_changed()

    def _on_fg_hex_edited(self, hex_val: str) -> None:
        hex_val = hex_val.strip()
        if QColor.isValidColorName(hex_val):
            self._fg_color = hex_val
            self.fg_swatch.update_color(hex_val)
            self._on_setting_changed()

    def _on_bg_hex_edited(self, hex_val: str) -> None:
        hex_val = hex_val.strip()
        if QColor.isValidColorName(hex_val):
            self._bg_color = hex_val
            self.bg_swatch.update_color(hex_val)
            self._on_setting_changed()

    def _swap_colors(self) -> None:
        self._fg_color, self._bg_color = self._bg_color, self._fg_color
        self.fg_swatch.update_color(self._fg_color)
        self.bg_swatch.update_color(self._bg_color)
        self.fg_hex_input.setText(self._fg_color)
        self.bg_hex_input.setText(self._bg_color)
        self._on_setting_changed()

    def _apply_color_preset(self, fg: str, bg: str) -> None:
        self._fg_color = fg
        self._bg_color = bg
        self.fg_swatch.update_color(fg)
        self.bg_swatch.update_color(bg)
        self.fg_hex_input.setText(fg)
        self.bg_hex_input.setText(bg)
        self._on_setting_changed()

    def _browse_logo(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Logo Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.svg *.ico);;All Files (*)",
        )
        if path and os.path.isfile(path):
            self._logo_path = path
            self.logo_name_lbl.setText(os.path.basename(path))
            self.remove_logo_btn.setVisible(True)

            # Auto-switch to High error correction if currently lower to protect scanability
            if self.ec_combo.currentData() in ("L", "M"):
                self.ec_combo.setCurrentIndex(3)  # High

            # Set thumbnail
            pix = QPixmap(path)
            if not pix.isNull():
                self.logo_thumb.setPixmap(pix.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

            self._on_setting_changed()

    def _remove_logo(self) -> None:
        self._logo_path = None
        self.logo_name_lbl.setText("No logo selected")
        self.logo_thumb.clear()
        self.remove_logo_btn.setVisible(False)
        self._on_setting_changed()

    def _on_setting_changed(self) -> None:
        self.settings_changed.emit()
