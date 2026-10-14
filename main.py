"""Application entry point for QR Code Generator Pro."""

from __future__ import annotations

import argparse
import io
import logging
import os
import signal
import sys

# Ensure stdout/stderr are valid streams in frozen/windowed mode to prevent NoneType write crashes
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

# Initialize PyInstaller runtime DLL and search paths BEFORE importing Qt and engine
from src.utils.resource_finder import get_resource_path, init_runtime_environment
init_runtime_environment()

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow

# Allow Ctrl+C to terminate application from command line
signal.signal(signal.SIGINT, signal.SIG_DFL)


def setup_logging(verbose: bool = False) -> None:
    """Configure console logging level and format safely."""
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stderr) if sys.stderr else logging.NullHandler()
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
        datefmt="%H:%M:%S",
        handlers=[handler],
    )


def main() -> None:
    """Initialize and launch the QR Code Generator Pro desktop application."""
    parser = argparse.ArgumentParser(description="Desktop QR Code Generator Pro")
    parser.add_argument("text", nargs="?", help="Optional initial text or URL payload to generate immediately")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug logging")
    try:
        args, _ = parser.parse_known_args()
    except Exception:
        args = argparse.Namespace(text=None, verbose=False)

    setup_logging(args.verbose)

    # Enable smooth high-DPI scaling on modern displays
    if hasattr(Qt.HighDpiScaleFactorRoundingPolicy, "PassThrough"):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

    app = QApplication(sys.argv)
    app.setApplicationName("QR Code Generator Pro")
    app.setOrganizationName("Antigravity")
    app.setApplicationVersion("2.0.0")

    # Set application icon if assets/icon.ico is present
    icon_path = get_resource_path("assets/icon.ico")
    if os.path.exists(icon_path):
        from PyQt6.QtGui import QIcon
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    # If initial text/URL was supplied via CLI argument, load it right away
    if args.text:
        window.input_widget.set_payload(args.text)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
