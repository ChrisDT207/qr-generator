"""Automated production packaging pipeline for Windows QR Code Generator Pro using PyInstaller.

Includes UPX compression, bloat DLL stripping, and automated distribution archive generation.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
import zipfile


def print_step(message: str) -> None:
    print(f"\n\033[1;36m==>\033[0m \033[1m{message}\033[0m")


def print_success(message: str) -> None:
    print(f"\033[1;32m[OK]\033[0m {message}")


def print_warning(message: str) -> None:
    print(f"\033[1;33m[WARN]\033[0m {message}")


def print_error(message: str) -> None:
    print(f"\033[1;31m[ERROR]\033[0m {message}")


def check_prerequisites() -> bool:
    """Verify that Python and all required packaging libraries are available."""
    print_step("1. Verifying environment and build prerequisites...")

    packages = {
        "PyInstaller": "pyinstaller",
        "PyQt6": "PyQt6",
        "qrcode": "qrcode",
        "PIL": "pillow",
    }

    all_passed = True
    for mod_name, pip_pkg in packages.items():
        try:
            __import__(mod_name)
            print_success(f"Found {pip_pkg}")
        except ImportError:
            print_error(f"Missing required build dependency: {pip_pkg}")
            print(f"       Run: pip install {pip_pkg}")
            all_passed = False

    return all_passed


def ensure_assets(root_dir: str) -> None:
    """Ensure application icon and sample QR codes exist before building."""
    print_step("2. Checking application assets and samples...")

    # Icon check
    icon_path = os.path.join(root_dir, "assets", "icon.ico")
    if not os.path.isfile(icon_path):
        print_step("Generating application icon...")
        from PIL import Image, ImageDraw

        os.makedirs(os.path.join(root_dir, "assets"), exist_ok=True)
        img = Image.new("RGBA", (256, 256), (11, 15, 25, 255))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([16, 16, 240, 240], radius=40, fill=(17, 24, 39, 255), outline=(16, 185, 129, 255), width=10)
        for corner in [(44, 44), (148, 44), (44, 148)]:
            x, y = corner
            draw.rounded_rectangle([x, y, x + 64, y + 64], radius=12, outline=(16, 185, 129, 255), width=8)
            draw.rounded_rectangle([x + 16, y + 16, x + 48, y + 48], radius=6, fill=(16, 185, 129, 255))
        draw.line([30, 128, 226, 128], fill=(52, 211, 153, 255), width=6)
        img.save(icon_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        print_success("Created assets/icon.ico")
    else:
        print_success("Found assets/icon.ico")

    # Sample images check
    samples_dir = os.path.join(root_dir, "samples")
    if not os.path.isdir(samples_dir) or not os.listdir(samples_dir):
        print_step("Generating sample test QR codes...")
        try:
            from create_sample_codes import generate_samples
            generate_samples(samples_dir)
            print_success("Generated sample QR codes in samples/")
        except Exception as e:
            print_warning(f"Could not generate sample codes: {e}")
    else:
        print_success("Found sample QR codes in samples/")


def clean_build_artifacts(root_dir: str) -> None:
    """Remove stale PyInstaller cache, running binaries, and temporary build directories."""
    print_step("3. Cleaning previous build artifacts...")

    # Terminate any running QRGenerator processes on Windows to prevent WinError 5 Access Denied
    if sys.platform.startswith("win"):
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", "QRGenerator.exe", "/T"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except Exception:
            pass

    # Remove stale executable and zip packages in dist/
    dist_dir = os.path.join(root_dir, "dist")
    if os.path.isdir(dist_dir):
        for fname in os.listdir(dist_dir):
            if fname.startswith("QRGenerator") and (fname.endswith(".exe") or fname.endswith(".zip")):
                fpath = os.path.join(dist_dir, fname)
                try:
                    os.remove(fpath)
                    print_success(f"Removed previous dist/{fname}")
                except OSError as e:
                    print_warning(f"Could not remove old file {fname}: {e}")

    build_dir = os.path.join(root_dir, "build")
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir, ignore_errors=True)
        print_success("Removed old build/ directory")

    # Clean __pycache__
    for dirpath, dirnames, _ in os.walk(root_dir):
        for d in dirnames:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(dirpath, d), ignore_errors=True)


def run_pyinstaller(root_dir: str, spec_file: str) -> bool:
    """Invoke PyInstaller using the production spec file."""
    print_step(f"4. Executing PyInstaller with spec: {spec_file}...")
    start_time = time.time()

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
    ]

    upx_dir = os.path.join(root_dir, "tools", "upx")
    if os.path.isdir(upx_dir) and os.path.isfile(os.path.join(upx_dir, "upx.exe")):
        cmd.extend(["--upx-dir", upx_dir])
        print_success(f"Configured UPX compressor from {upx_dir}")

    cmd.append(spec_file)

    print(f"Running command: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, cwd=root_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    captured_lines = []
    for line in iter(process.stdout.readline, ""):
        cleaned = line.strip()
        captured_lines.append(cleaned)
        if any(keyword in cleaned for keyword in ["INFO:", "WARNING:", "ERROR:", "Building", "completed", "UPX"]):
            print(f"  [PyInstaller] {cleaned}")

    process.wait()
    duration = time.time() - start_time

    if process.returncode != 0:
        print_error(f"PyInstaller build failed with exit code {process.returncode}")
        print("\nLast 25 log lines from PyInstaller:")
        for log_line in captured_lines[-25:]:
            print(f"    {log_line}")
        return False

    print_success(f"PyInstaller packaging completed in {duration:.1f} seconds!")
    return True


def verify_executable(dist_dir: str) -> bool:
    """Verify final .exe artifact existence and size."""
    print_step("5. Validating output binary...")

    target_exe = os.path.join(dist_dir, "QRGenerator.exe")
    if not os.path.isfile(target_exe):
        print_error(f"Expected executable not found at: {target_exe}")
        return False

    size_bytes = os.path.getsize(target_exe)
    size_mb = size_bytes / (1024 * 1024)

    print_success(f"Executable successfully generated: {target_exe}")
    print_success(f"Binary Size: {size_mb:.2f} MB")
    print_success("Mode: Standalone Windows GUI Executable (No console window)")
    return True


def create_compressed_archive(root_dir: str, dist_dir: str) -> str:
    """Package the standalone executable into a maximum-compression zip archive."""
    print_step("6. Creating maximum-compression distribution zip...")

    exe_path = os.path.join(dist_dir, "QRGenerator.exe")
    zip_path = os.path.join(dist_dir, "QRGenerator-v2.0-win64.zip")

    if not os.path.isfile(exe_path):
        print_error(f"Cannot package archive: {exe_path} does not exist")
        return ""

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(exe_path, arcname="QRGenerator.exe")
        readme_path = os.path.join(root_dir, "README.md")
        if os.path.isfile(readme_path):
            zf.write(readme_path, arcname="README.md")

    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print_success(f"Created compressed distribution zip: {zip_path}")
    print_success(f"Zip Archive Size: {zip_size_mb:.2f} MB")
    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build production Windows .exe for QR Code Generator Pro")
    parser.add_argument("--clean-only", action="store_true", help="Only clean temporary build artifacts and exit")
    parser.add_argument("--spec", default="generator.spec", help="Spec file name (default: generator.spec)")
    args = parser.parse_args()

    root_dir = os.path.abspath(os.path.dirname(__file__))
    dist_dir = os.path.join(root_dir, "dist")

    if args.clean_only:
        clean_build_artifacts(root_dir)
        print_success("Clean completed.")
        return 0

    print("=" * 64)
    print("   QR Code Generator Pro - Windows Executable Build Pipeline    ")
    print("=" * 64)

    # Step 1: Prerequisites
    if not check_prerequisites():
        return 1

    # Step 2: Assets
    ensure_assets(root_dir)

    # Step 3: Clean
    clean_build_artifacts(root_dir)

    # Step 4: Build
    spec_path = os.path.join(root_dir, args.spec)
    if not os.path.isfile(spec_path):
        print_error(f"Spec file not found: {spec_path}")
        return 1

    if not run_pyinstaller(root_dir, args.spec):
        return 1

    # Step 5: Verify
    if not verify_executable(dist_dir):
        return 1

    # Place executable in outermost layer (project root) for easy access
    root_exe = os.path.join(root_dir, "QRGenerator.exe")
    dist_exe = os.path.join(dist_dir, "QRGenerator.exe")
    try:
        shutil.copy2(dist_exe, root_exe)
        print_success(f"Placed standalone executable in project root: {root_exe}")
    except Exception as e:
        print_warning(f"Could not copy executable to project root: {e}")

    # Step 6: Create compressed distribution archive
    create_compressed_archive(root_dir, dist_dir)

    print("\n" + "=" * 64)
    print("  BUILD SUCCESSFUL! Standalone application ready for use:")
    print(f"  ROOT EXE: {root_exe}")
    print(f"  DIST EXE: {dist_exe}")
    print(f"  ZIP:      {os.path.join(dist_dir, 'QRGenerator-v2.0-win64.zip')}")
    print("=" * 64 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
