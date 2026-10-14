"""Automated GUI test verifying PyQt6 widgets for QR Code Generator Pro."""

import os
import sys
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Run Qt headless for CI/test automation
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt6.QtWidgets import QApplication

from src.engine.generator import QRCodeConfig
from src.ui.customize_widget import CustomizeWidget
from src.ui.input_widget import InputWidget
from src.ui.main_window import MainWindow
from src.ui.preview_widget import PreviewWidget

app = QApplication.instance() or QApplication(sys.argv)


class TestGeneratorGUI(unittest.TestCase):
    """Test Qt widgets lifecycle, signal connections, and generator UI."""

    def setUp(self):
        self.window = MainWindow()

    def tearDown(self):
        self.window.close()

    def test_main_window_init(self):
        self.assertIsNotNone(self.window)
        self.assertIn("QR Code Generator Pro", self.window.windowTitle())

    def test_theme_toggle(self):
        self.assertTrue(self.window._is_dark_theme)
        self.window._toggle_theme()
        self.assertFalse(self.window._is_dark_theme)
        self.window._toggle_theme()
        self.assertTrue(self.window._is_dark_theme)

    def test_input_widget(self):
        iw = self.window.input_widget
        iw.set_payload("https://newsite.com")
        self.assertEqual(iw.get_payload(), "https://newsite.com")
        self.assertIn("19 characters", iw.chars_lbl.text())

    def test_customize_widget_config(self):
        cw = self.window.customize_widget
        cw._apply_color_preset("#10b981", "#0b0f19")
        cfg = cw.get_config("Test Data")
        self.assertEqual(cfg.fg_color, "#10b981")
        self.assertEqual(cfg.bg_color, "#0b0f19")
        self.assertEqual(cfg.data, "Test Data")

    def test_preview_widget_rendering(self):
        pw = self.window.preview_widget
        config = QRCodeConfig(data="https://antigravity.google.com")
        pw.update_preview(config)

        self.assertIsNotNone(pw.canvas.get_pixmap())
        self.assertTrue(pw.copy_btn.isEnabled())
        self.assertTrue(pw.save_btn.isEnabled())
        self.assertIn("px", pw.dims_badge.text())


if __name__ == "__main__":
    unittest.main()
