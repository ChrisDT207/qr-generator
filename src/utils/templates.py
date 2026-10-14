"""Helper functions to format standard QR code payloads for Wi-Fi, vCard, Email, etc."""

from __future__ import annotations

import urllib.parse


def format_wifi(ssid: str, password: str = "", auth_type: str = "WPA", hidden: bool = False) -> str:
    """Format Wi-Fi configuration payload according to ZXing / standard Wi-Fi QR format."""
    ssid_safe = ssid.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace(":", "\\:")
    pass_safe = password.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace(":", "\\:")
    auth_str = "nopass" if auth_type.lower() in ("none", "open", "nopass") else auth_type.upper()
    hidden_str = "true" if hidden else "false"
    return f"WIFI:S:{ssid_safe};T:{auth_str};P:{pass_safe};H:{hidden_str};;"


def format_vcard(
    name: str,
    phone: str = "",
    email: str = "",
    org: str = "",
    title: str = "",
    url: str = "",
) -> str:
    """Format vCard 3.0 contact card payload."""
    lines = ["BEGIN:VCARD", "VERSION:3.0"]
    if name:
        lines.append(f"FN:{name}")
        lines.append(f"N:{name};;;;")
    if org:
        lines.append(f"ORG:{org}")
    if title:
        lines.append(f"TITLE:{title}")
    if phone:
        lines.append(f"TEL;TYPE=CELL:{phone}")
    if email:
        lines.append(f"EMAIL:{email}")
    if url:
        lines.append(f"URL:{url}")
    lines.append("END:VCARD")
    return "\n".join(lines)


def format_email(recipient: str, subject: str = "", body: str = "") -> str:
    """Format mailto: email payload with encoded parameters."""
    params = {}
    if subject:
        params["subject"] = subject
    if body:
        params["body"] = body

    query = urllib.parse.urlencode(params)
    if query:
        return f"mailto:{recipient}?{query}"
    return f"mailto:{recipient}"


def format_sms(phone: str, message: str = "") -> str:
    """Format SMS payload."""
    clean_phone = phone.strip()
    if message:
        return f"smsto:{clean_phone}:{message}"
    return f"smsto:{clean_phone}"


def format_tel(phone: str) -> str:
    """Format telephone call payload."""
    return f"tel:{phone.strip()}"
