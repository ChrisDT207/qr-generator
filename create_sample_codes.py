"""Helper utility to generate sample QR codes for testing file scanning and drag-and-drop."""

import os
import qrcode

SAMPLES = [
    (
        "sample_url.png",
        "https://github.com/google",
        "URL Sample (GitHub)",
    ),
    (
        "sample_wifi.png",
        "WIFI:T:WPA;S:FastOffice_WiFi;P:Welcome2026!;H:false;;",
        "Wi-Fi Network Configuration",
    ),
    (
        "sample_vcard.png",
        "BEGIN:VCARD\nVERSION:3.0\nFN:Dr. Jane Hopper\nORG:Hawkins Lab\nTITLE:Lead Researcher\nTEL:+1-555-0142\nEMAIL:jane.hopper@hawkinslab.org\nEND:VCARD",
        "vCard Contact Card",
    ),
    (
        "sample_text.png",
        "Clean, cross-platform desktop QR Code Generator built with Python, PyQt6, and Pillow.",
        "Plain Text Message",
    ),
]


def generate_samples(output_dir: str = "samples") -> None:
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating sample QR codes in '{output_dir}/'...")

    for filename, payload, label in SAMPLES:
        file_path = os.path.join(output_dir, filename)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(payload)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_path)
        print(f"  [OK] Created {filename} ({label})")

    print("\nAll sample QR codes generated successfully!")


if __name__ == "__main__":
    generate_samples()
