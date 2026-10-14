"""Core QR code generation engine using qrcode and Pillow with vector SVG support."""

from __future__ import annotations

import io
import logging
import os
from dataclasses import dataclass, field
from typing import Optional, Tuple

import qrcode
from PIL import Image, ImageColor, ImageDraw
from PyQt6.QtGui import QImage, QPixmap
from qrcode.image.svg import SvgPathImage

logger = logging.getLogger(__name__)

# Error correction mapping
ERROR_CORRECTIONS = {
    "L": qrcode.constants.ERROR_CORRECT_L,  # ~7% recovery
    "M": qrcode.constants.ERROR_CORRECT_M,  # ~15% recovery
    "Q": qrcode.constants.ERROR_CORRECT_Q,  # ~25% recovery
    "H": qrcode.constants.ERROR_CORRECT_H,  # ~30% recovery (ideal for center logos)
}


@dataclass
class QRCodeConfig:
    """Configuration settings for generating a QR code."""

    data: str = "https://github.com"
    error_correction: str = "M"  # "L", "M", "Q", "H"
    box_size: int = 10
    border: int = 4
    fg_color: str = "#000000"
    bg_color: str = "#ffffff"
    logo_path: Optional[str] = None
    logo_scale: float = 0.22  # 0.10 to 0.35
    logo_pad: bool = True  # Contrast background card behind logo


class QRCodeGenerator:
    """High-resolution QR code generator supporting custom palettes, logos, and vector exports."""

    @staticmethod
    def get_error_correction_constant(level: str) -> int:
        return ERROR_CORRECTIONS.get(level.upper(), qrcode.constants.ERROR_CORRECT_M)

    @classmethod
    def generate_pil_image(cls, config: QRCodeConfig, scale_multiplier: int = 1) -> Image.Image:
        """Generate a PIL RGBA Image of the QR code with optional center logo."""
        payload = config.data.strip() if config.data else " "
        ec_constant = cls.get_error_correction_constant(config.error_correction)

        # Force High error correction if a logo is attached to ensure scanability
        if config.logo_path and os.path.isfile(config.logo_path):
            if config.error_correction not in ("Q", "H"):
                ec_constant = qrcode.constants.ERROR_CORRECT_H

        effective_box_size = max(1, config.box_size * scale_multiplier)
        effective_border = max(0, config.border)

        qr = qrcode.QRCode(
            version=None,  # Auto-size
            error_correction=ec_constant,
            box_size=effective_box_size,
            border=effective_border,
        )
        qr.add_data(payload)
        qr.make(fit=True)

        # Render base image with colors
        base_img = qr.make_image(
            fill_color=config.fg_color,
            back_color=config.bg_color,
        ).convert("RGBA")

        # Overlay center logo if configured
        if config.logo_path and os.path.isfile(config.logo_path):
            base_img = cls._overlay_logo(base_img, config)

        return base_img

    @classmethod
    def _overlay_logo(cls, qr_img: Image.Image, config: QRCodeConfig) -> Image.Image:
        """Overlay a center logo image with contrast shielding onto the QR code."""
        try:
            logo = Image.open(config.logo_path).convert("RGBA")
        except Exception as e:
            logger.warning("Failed to open logo image '%s': %s", config.logo_path, e)
            return qr_img

        qr_w, qr_h = qr_img.size

        # Determine target logo bounding box
        target_max_size = int(min(qr_w, qr_h) * max(0.10, min(config.logo_scale, 0.35)))
        logo_w, logo_h = logo.size

        ratio = min(target_max_size / logo_w, target_max_size / logo_h)
        new_w = max(8, int(logo_w * ratio))
        new_h = max(8, int(logo_h * ratio))

        logo_resized = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)

        pos_x = (qr_w - new_w) // 2
        pos_y = (qr_h - new_h) // 2

        # Draw a clean contrast background shield behind the logo to prevent scanning issues
        if config.logo_pad:
            pad = max(4, int(new_w * 0.12))
            shield_w = new_w + (pad * 2)
            shield_h = new_h + (pad * 2)
            shield_x = (qr_w - shield_w) // 2
            shield_y = (qr_h - shield_h) // 2

            shield = Image.new("RGBA", (shield_w, shield_h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(shield)

            try:
                bg_rgb = ImageColor.getrgb(config.bg_color)
            except Exception:
                bg_rgb = (255, 255, 255)

            radius = max(4, int(pad * 1.2))
            draw.rounded_rectangle([0, 0, shield_w - 1, shield_h - 1], radius=radius, fill=(*bg_rgb, 255))
            qr_img.paste(shield, (shield_x, shield_y), mask=shield)

        # Paste the logo
        qr_img.paste(logo_resized, (pos_x, pos_y), mask=logo_resized)
        return qr_img

    @classmethod
    def generate_qpixmap(cls, config: QRCodeConfig, scale_multiplier: int = 1) -> QPixmap:
        """Generate a QPixmap for rendering directly on PyQt6 canvases."""
        pil_img = cls.generate_pil_image(config, scale_multiplier=scale_multiplier)
        data = pil_img.tobytes("raw", "RGBA")
        qimg = QImage(data, pil_img.width, pil_img.height, QImage.Format.Format_RGBA8888)
        return QPixmap.fromImage(qimg)

    @classmethod
    def generate_svg_string(cls, config: QRCodeConfig) -> str:
        """Generate a clean scalable vector SVG file format string."""
        payload = config.data.strip() if config.data else " "
        ec_constant = cls.get_error_correction_constant(config.error_correction)

        qr = qrcode.QRCode(
            version=None,
            error_correction=ec_constant,
            box_size=config.box_size,
            border=config.border,
            image_factory=SvgPathImage,
        )
        qr.add_data(payload)
        qr.make(fit=True)

        svg_img = qr.make_image(
            fill_color=config.fg_color,
            back_color=config.bg_color,
        )
        buf = io.BytesIO()
        svg_img.save(buf)
        return buf.getvalue().decode("utf-8")

    @classmethod
    def save_to_file(cls, config: QRCodeConfig, output_path: str, scale_multiplier: int = 1) -> bool:
        """Save generated QR code to PNG, JPG, or SVG."""
        ext = os.path.splitext(output_path)[1].lower()

        if ext == ".svg":
            svg_content = cls.generate_svg_string(config)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            return True

        pil_img = cls.generate_pil_image(config, scale_multiplier=scale_multiplier)

        if ext in (".jpg", ".jpeg"):
            # JPEG doesn't support alpha transparency; flatten onto background
            try:
                bg_rgb = ImageColor.getrgb(config.bg_color)
            except Exception:
                bg_rgb = (255, 255, 255)

            rgb_img = Image.new("RGB", pil_img.size, bg_rgb)
            rgb_img.paste(pil_img, mask=pil_img.split()[3])
            rgb_img.save(output_path, format="JPEG", quality=95)
            return True

        # Default PNG / WEBP / BMP
        pil_img.save(output_path)
        return True
