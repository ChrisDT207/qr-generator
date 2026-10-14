"""Live high-resolution preview canvas with image export and clipboard copy actions."""

from __future__ import annotations

import os
from typing import Optional

from PyQt6.QtCore import QRect, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..engine.generator import QRCodeConfig, QRCodeGenerator
from .icons import get_icon, get_pixmap


class QRCanvas(QWidget):
    """Viewport canvas rendering the generated QR code."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumSize(280, 280)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._pixmap: Optional[QPixmap] = None

    def set_pixmap(self, pixmap: Optional[QPixmap]) -> None:
        self._pixmap = pixmap
        self.update()

    def get_pixmap(self) -> Optional[QPixmap]:
        return self._pixmap

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        rect = self.rect()

        # Canvas container background
        painter.fillRect(rect, QColor("#080c14"))

        if self._pixmap and not self._pixmap.isNull():
            # Pad canvas
            avail_w = max(10, rect.width() - 32)
            avail_h = max(10, rect.height() - 32)
            scaled = self._pixmap.scaled(
                avail_w,
                avail_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            px = (rect.width() - scaled.width()) // 2
            py = (rect.height() - scaled.height()) // 2

            # Subtle white frame card around the QR code
            card_rect = QRect(px - 6, py - 6, scaled.width() + 12, scaled.height() + 12)
            painter.setPen(QColor(30, 41, 59, 180))
            painter.setBrush(QColor(15, 23, 42))
            painter.drawRoundedRect(card_rect, 10, 10)

            # Draw the QR code
            painter.drawPixmap(px, py, scaled)
        else:
            # Idle placeholder
            cx = rect.center().x()
            cy = rect.center().y()
            qr_icon = get_pixmap("qr-code", color="#334155", size=56)
            painter.drawPixmap(cx - 28, cy - 40, qr_icon)
            painter.setPen(QColor("#64748b"))
            painter.drawText(QRect(rect.left(), cy + 24, rect.width(), 20), Qt.AlignmentFlag.AlignCenter, "Enter content to generate QR code")

        painter.end()


class PreviewWidget(QFrame):
    """Preview card containing live QR canvas and export controls."""

    save_requested = pyqtSignal(str, int)  # (file_path, scale_factor)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("PreviewCard")
        self.setProperty("class", "CardPanel")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._current_config: Optional[QRCodeConfig] = None
        self._current_pixmap: Optional[QPixmap] = None

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # 1. Header Bar: Title + Dimensions Badge
        header = QHBoxLayout()
        title_lbl = QLabel("3. Live Preview & Export")
        title_lbl.setProperty("class", "SectionTitle")

        self.dims_badge = QLabel("0 × 0 px")
        self.dims_badge.setProperty("class", "BadgeFormat")

        header.addWidget(title_lbl)
        header.addStretch()
        header.addWidget(self.dims_badge)
        layout.addLayout(header)

        # 2. Canvas
        self.canvas = QRCanvas()
        layout.addWidget(self.canvas, 1)

        # 3. Export Options Bar
        export_frame = QFrame()
        export_frame.setProperty("class", "SubCardPanel")
        export_layout = QVBoxLayout(export_frame)
        export_layout.setContentsMargins(12, 10, 12, 10)
        export_layout.setSpacing(10)

        # Multiplier row
        scale_row = QHBoxLayout()
        scale_lbl = QLabel("Export Quality / Size:")
        scale_lbl.setStyleSheet("color: #94a3b8; font-weight: 600; font-size: 12px;")

        self.scale_combo = QComboBox()
        self.scale_combo.addItem("1× Standard (Screen / Web)", 1)
        self.scale_combo.addItem("2× High-Res (Documents)", 2)
        self.scale_combo.addItem("4× Ultra Print HD (Large Print)", 4)

        scale_row.addWidget(scale_lbl)
        scale_row.addWidget(self.scale_combo, 1)
        export_layout.addLayout(scale_row)

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        # Copy Image Button
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setObjectName("CopyBtn")
        self.copy_btn.setIcon(get_icon("copy", color="#3b82f6", size=16))
        self.copy_btn.clicked.connect(self._copy_image_to_clipboard)

        # Save Image Button
        self.save_btn = QPushButton("Save Image...")
        self.save_btn.setObjectName("OpenUrlBtn")  # Uses vibrant accent style
        self.save_btn.setIcon(get_icon("download", color="#ffffff", size=16))
        self.save_btn.clicked.connect(self._save_image)

        btn_row.addWidget(self.copy_btn, 1)
        btn_row.addWidget(self.save_btn, 1)
        export_layout.addLayout(btn_row)

        layout.addWidget(export_frame)

    def update_preview(self, config: QRCodeConfig) -> None:
        """Render high-resolution preview from config."""
        self._current_config = config

        if not config.data or not config.data.strip():
            self.canvas.set_pixmap(None)
            self.dims_badge.setText("0 × 0 px")
            self.copy_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            return

        pixmap = QRCodeGenerator.generate_qpixmap(config)
        self._current_pixmap = pixmap
        self.canvas.set_pixmap(pixmap)
        self.dims_badge.setText(f"{pixmap.width()} × {pixmap.height()} px")
        self.copy_btn.setEnabled(True)
        self.save_btn.setEnabled(True)

    def _copy_image_to_clipboard(self) -> None:
        """Copy generated QR code image to system clipboard."""
        if not self._current_config:
            return

        scale = self.scale_combo.currentData() or 1
        pixmap = QRCodeGenerator.generate_qpixmap(self._current_config, scale_multiplier=scale)

        clipboard = QApplication.clipboard()
        clipboard.setPixmap(pixmap)

        # Animated button feedback
        original_text = self.copy_btn.text()
        self.copy_btn.setText("✓ Copied Image!")
        self.copy_btn.setIcon(get_icon("check", color="#10b981", size=16))
        self.copy_btn.setStyleSheet("border-color: #10b981; color: #10b981;")

        def restore():
            self.copy_btn.setText(original_text)
            self.copy_btn.setIcon(get_icon("copy", color="#3b82f6", size=16))
            self.copy_btn.setStyleSheet("")

        QTimer.singleShot(1800, restore)

    def _save_image(self) -> None:
        """Prompt user for file path and save QR code."""
        if not self._current_config:
            return

        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save QR Code Image",
            "qrcode.png",
            "PNG Image (*.png);;SVG Vector (*.svg);;JPEG Image (*.jpg *.jpeg);;All Files (*)",
        )
        if not file_path:
            return

        scale = self.scale_combo.currentData() or 1
        try:
            success = QRCodeGenerator.save_to_file(self._current_config, file_path, scale_multiplier=scale)
            if success:
                QMessageBox.information(
                    self,
                    "Saved Successfully",
                    f"QR code successfully saved to:\n{file_path}",
                )
            else:
                QMessageBox.warning(self, "Save Failed", "Could not save QR code file.")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save image: {e}")
