"""Resource and runtime path resolution helper for development and PyInstaller bundles."""

from __future__ import annotations

import logging
import os
import sys

logger = logging.getLogger(__name__)


def is_frozen() -> bool:
    """Return True if running inside a PyInstaller frozen bundle."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def get_base_dir() -> str:
    """Get the root directory of the application (development root or PyInstaller _MEIPASS)."""
    if is_frozen():
        return sys._MEIPASS  # type: ignore[attr-defined]
    # In development: project root is 2 levels up from src/utils
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_resource_path(relative_path: str) -> str:
    """Resolve an asset or data file path relative to the application root.

    Works identically in both local source execution and PyInstaller onefile / onedir bundles.
    """
    base = get_base_dir()
    return os.path.normpath(os.path.join(base, relative_path))


def init_runtime_environment() -> None:
    """Configure search paths and environment for frozen Windows binaries."""
    if is_frozen() and sys.platform.startswith("win"):
        meipass = sys._MEIPASS  # type: ignore[attr-defined]

        # 1. Add _MEIPASS directory to Windows DLL search path (Python 3.8+)
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(meipass)
                logger.debug("Added DLL directory: %s", meipass)
            except Exception as e:
                logger.debug("Could not add meipass to DLL directory: %s", e)

        # 2. Prepend _MEIPASS to PATH environment variable
        current_path = os.environ.get("PATH", "")
        if meipass not in current_path:
            os.environ["PATH"] = f"{meipass};{current_path}"
