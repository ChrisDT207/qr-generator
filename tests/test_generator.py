"""Unit test suite verifying the QR code generator engine, customization, templates, and export."""

import os
import sys
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image

from src.engine.generator import QRCodeConfig, QRCodeGenerator
from src.utils.templates import format_email, format_sms, format_vcard, format_wifi


class TestQRCodeGenerator(unittest.TestCase):
    """Test QR code generation engine, styling, and exports."""

    def setUp(self):
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "output"))
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        # Clean test output files
        if os.path.isdir(self.output_dir):
            for f in os.listdir(self.output_dir):
                try:
                    os.remove(os.path.join(self.output_dir, f))
                except OSError:
                    pass

    def test_default_generation(self):
        config = QRCodeConfig(data="https://example.com")
        img = QRCodeGenerator.generate_pil_image(config)
        self.assertIsInstance(img, Image.Image)
        self.assertGreater(img.width, 100)
        self.assertGreater(img.height, 100)

    def test_custom_colors(self):
        config = QRCodeConfig(
            data="Color Test",
            fg_color="#10b981",
            bg_color="#0b0f19",
            box_size=8,
            border=2,
        )
        img = QRCodeGenerator.generate_pil_image(config)
        self.assertIsNotNone(img)
        self.assertEqual(img.mode, "RGBA")

    def test_error_correction_levels(self):
        for ec in ["L", "M", "Q", "H"]:
            config = QRCodeConfig(data="EC Test", error_correction=ec)
            img = QRCodeGenerator.generate_pil_image(config)
            self.assertIsNotNone(img)

    def test_logo_overlay(self):
        # Create a test logo image
        logo_path = os.path.join(self.output_dir, "test_logo.png")
        test_logo = Image.new("RGBA", (50, 50), (255, 0, 0, 255))
        test_logo.save(logo_path)

        config = QRCodeConfig(
            data="https://antigravity.google.com",
            error_correction="H",
            logo_path=logo_path,
            logo_scale=0.25,
            logo_pad=True,
        )
        img = QRCodeGenerator.generate_pil_image(config)
        self.assertIsNotNone(img)

    def test_svg_export(self):
        config = QRCodeConfig(data="https://antigravity.google.com", fg_color="#2563eb")
        svg_content = QRCodeGenerator.generate_svg_string(config)
        self.assertIn("<svg", svg_content)
        self.assertIn("</svg>", svg_content)

    def test_save_to_file_png_and_svg_and_jpg(self):
        config = QRCodeConfig(data="Export Test")

        png_path = os.path.join(self.output_dir, "test.png")
        self.assertTrue(QRCodeGenerator.save_to_file(config, png_path))
        self.assertTrue(os.path.isfile(png_path))

        svg_path = os.path.join(self.output_dir, "test.svg")
        self.assertTrue(QRCodeGenerator.save_to_file(config, svg_path))
        self.assertTrue(os.path.isfile(svg_path))

        jpg_path = os.path.join(self.output_dir, "test.jpg")
        self.assertTrue(QRCodeGenerator.save_to_file(config, jpg_path))
        self.assertTrue(os.path.isfile(jpg_path))


class TestTemplates(unittest.TestCase):
    """Test payload template generators."""

    def test_wifi_template(self):
        payload = format_wifi("MyOffice", "SecretPass123", "WPA", hidden=True)
        self.assertIn("WIFI:S:MyOffice;", payload)
        self.assertIn("P:SecretPass123;", payload)
        self.assertIn("H:true;;", payload)

    def test_vcard_template(self):
        payload = format_vcard("Alex Mercer", "+1 555-0100", "alex@corp.com", "Corp Inc")
        self.assertIn("BEGIN:VCARD", payload)
        self.assertIn("FN:Alex Mercer", payload)
        self.assertIn("TEL;TYPE=CELL:+1 555-0100", payload)
        self.assertIn("END:VCARD", payload)

    def test_email_template(self):
        payload = format_email("admin@test.com", "Hello", "How are you?")
        self.assertTrue(payload.startswith("mailto:admin@test.com?"))
        self.assertIn("subject=Hello", payload)


if __name__ == "__main__":
    unittest.main()
