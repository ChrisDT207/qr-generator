"""URL and QR payload parsing and navigation utilities."""

from __future__ import annotations

import re
import urllib.parse
import webbrowser
from typing import Any, Dict

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

# Regex pattern for general URLs
URL_PATTERN = re.compile(
    r"^(?:(?:https?|ftp)://)"  # http://, https://, or ftp://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,63}\.?|"  # domain
    r"localhost|"  # localhost
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or IPv4
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

LOOSE_URL_PATTERN = re.compile(
    r"^(?:https?://)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^\s]*)?$",
    re.IGNORECASE,
)


def is_valid_url(text: str) -> bool:
    """Return True if text is a valid web URL."""
    if not text:
        return False
    text = text.strip()
    return bool(URL_PATTERN.match(text) or (text.startswith(("http://", "https://")) and len(text) > 8))


def normalize_url(text: str) -> str:
    """Ensure text has a standard scheme (http/https)."""
    text = text.strip()
    if text.startswith(("http://", "https://", "ftp://")):
        return text
    if LOOSE_URL_PATTERN.match(text):
        return f"https://{text}"
    return text


def open_url(url_text: str) -> bool:
    """Open a URL in the user's default web browser using Qt or Python webbrowser."""
    normalized = normalize_url(url_text)
    try:
        qurl = QUrl(normalized)
        if qurl.isValid():
            success = QDesktopServices.openUrl(qurl)
            if success:
                return True
    except Exception:
        pass

    # Fallback to Python's standard webbrowser module
    try:
        return webbrowser.open(normalized)
    except Exception:
        return False


def parse_qr_payload(raw_text: str) -> Dict[str, Any]:
    """Analyze and extract structured information from common QR code payload formats."""
    text = raw_text.strip()
    info: Dict[str, Any] = {
        "raw": text,
        "category": "Plain Text",
        "icon": "text",
        "details": {},
        "is_url": False,
        "url": "",
    }

    if not text:
        return info

    # 1. URL Detection
    if is_valid_url(text):
        info["category"] = "URL / Web Link"
        info["is_url"] = True
        info["url"] = normalize_url(text)
        info["icon"] = "globe"
        try:
            parsed = urllib.parse.urlparse(info["url"])
            info["details"] = {
                "Scheme": parsed.scheme.upper(),
                "Host / Domain": parsed.netloc,
                "Path": parsed.path or "/",
            }
        except Exception:
            pass
        return info

    # 2. Wi-Fi Configuration (WIFI:S:MySSID;T:WPA;P:MyPassword;;)
    if text.startswith("WIFI:"):
        info["category"] = "Wi-Fi Network"
        info["icon"] = "wifi"
        details: Dict[str, str] = {}
        # Parse key:value segments
        content = text[5:]
        tokens = content.split(";")
        for token in tokens:
            if ":" in token:
                k, v = token.split(":", 1)
                if k == "S":
                    details["Network Name (SSID)"] = v
                elif k == "T":
                    details["Security Type"] = v or "None (Open)"
                elif k == "P":
                    details["Password"] = v
                elif k == "H":
                    details["Hidden Network"] = "Yes" if v.lower() in ("true", "1") else "No"
        info["details"] = details
        return info

    # 3. vCard / Contact Card
    if text.startswith("BEGIN:VCARD"):
        info["category"] = "Contact Card (vCard)"
        info["icon"] = "user"
        details = {}
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("FN:"):
                details["Full Name"] = line[3:]
            elif line.startswith("TEL:") or line.startswith("TEL;"):
                details["Phone"] = line.split(":", 1)[-1]
            elif line.startswith("EMAIL:") or line.startswith("EMAIL;"):
                details["Email"] = line.split(":", 1)[-1]
            elif line.startswith("ORG:"):
                details["Organization"] = line[4:]
            elif line.startswith("TITLE:"):
                details["Title"] = line[6:]
        info["details"] = details
        return info

    # 4. Email (mailto: or raw email)
    if text.lower().startswith("mailto:") or re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", text):
        info["category"] = "Email Address"
        info["icon"] = "mail"
        email_str = text[7:] if text.lower().startswith("mailto:") else text
        if "?" in email_str:
            email_addr, query = email_str.split("?", 1)
            params = urllib.parse.parse_qs(query)
            info["details"] = {
                "Recipient": email_addr,
                "Subject": params.get("subject", [""])[0],
                "Body": params.get("body", [""])[0],
            }
        else:
            info["details"] = {"Recipient": email_str}
        return info

    # 5. Telephone (tel:)
    if text.lower().startswith("tel:") or (re.match(r"^\+?[0-9\s\-()]{7,20}$", text) and any(c.isdigit() for c in text)):
        info["category"] = "Telephone Number"
        info["icon"] = "phone"
        phone_num = text[4:] if text.lower().startswith("tel:") else text
        info["details"] = {"Phone Number": phone_num}
        return info

    # 6. SMS (smsto: or sms:)
    if text.lower().startswith(("smsto:", "sms:")):
        info["category"] = "SMS Message"
        info["icon"] = "message"
        body_part = text.split(":", 1)[1]
        parts = body_part.split(":", 1)
        info["details"] = {
            "Recipient": parts[0],
            "Message": parts[1] if len(parts) > 1 else "",
        }
        return info

    # 7. Geo Coordinates (geo:lat,lon)
    if text.lower().startswith("geo:"):
        info["category"] = "Geo Coordinates"
        info["icon"] = "map-pin"
        coords = text[4:].split("?")[0]
        info["details"] = {"Coordinates": coords}
        return info

    # Default: Plain Text
    return info
