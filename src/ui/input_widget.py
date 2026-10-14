"""Input widget for QR code content with templates for URL, Plain Text, Wi-Fi, vCard, and Email."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..utils.templates import format_email, format_sms, format_tel, format_vcard, format_wifi
from .icons import get_icon


class InputWidget(QFrame):
    """Data input card with multi-type template builder and character counter."""

    text_changed = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("InputCard")
        self.setProperty("class", "CardPanel")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self._current_payload = "https://github.com"
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # 1. Header Bar: Title + Badges
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        title_lbl = QLabel("1. Content & Data")
        title_lbl.setProperty("class", "SectionTitle")

        self.type_badge = QLabel("URL")
        self.type_badge.setProperty("class", "BadgeFormat")

        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.type_badge)
        layout.addLayout(header_layout)

        # 2. Template Selector Pills
        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(6)

        self.tab_buttons = []
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        templates = [
            ("URL / Text", "qr-code", 0),
            ("Wi-Fi", "wifi", 1),
            ("Contact", "user", 2),
            ("Email", "mail", 3),
        ]

        for label, icon_name, idx in templates:
            btn = QPushButton(label)
            btn.setCheckable(True)
            if idx == 0:
                btn.setChecked(True)
            self.btn_group.addButton(btn, idx)
            tabs_layout.addWidget(btn)

        self.btn_group.idClicked.connect(self._on_template_tab_changed)
        layout.addLayout(tabs_layout)

        # 3. Stacked Template Forms
        self.stack = QStackedWidget()

        # Page 0: Freeform / URL Plain Text Edit
        p0 = QWidget()
        p0_layout = QVBoxLayout(p0)
        p0_layout.setContentsMargins(0, 4, 0, 0)
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText("Enter URL, website link, or any plain text...")
        self.text_edit.setPlainText("https://github.com")
        self.text_edit.setMinimumHeight(85)
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_edit.setFont(font)
        self.text_edit.textChanged.connect(self._on_raw_text_edited)
        p0_layout.addWidget(self.text_edit)
        self.stack.addWidget(p0)

        # Page 1: Wi-Fi Configuration
        p1 = QWidget()
        p1_layout = QGridLayout(p1)
        p1_layout.setContentsMargins(0, 4, 0, 0)
        p1_layout.setSpacing(8)

        p1_layout.addWidget(QLabel("Network Name (SSID):"), 0, 0)
        self.wifi_ssid = QLineEdit()
        self.wifi_ssid.setPlaceholderText("e.g. Home_Network_5G")
        self.wifi_ssid.textChanged.connect(self._sync_wifi_template)
        p1_layout.addWidget(self.wifi_ssid, 0, 1)

        p1_layout.addWidget(QLabel("Password:"), 1, 0)
        self.wifi_pass = QLineEdit()
        self.wifi_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.wifi_pass.setPlaceholderText("Network password")
        self.wifi_pass.textChanged.connect(self._sync_wifi_template)
        p1_layout.addWidget(self.wifi_pass, 1, 1)

        p1_layout.addWidget(QLabel("Security:"), 2, 0)
        wifi_opts = QHBoxLayout()
        self.wifi_sec = QComboBox()
        self.wifi_sec.addItems(["WPA / WPA2 / WPA3", "WEP", "Open (No Password)"])
        self.wifi_sec.currentIndexChanged.connect(self._sync_wifi_template)
        self.wifi_hidden = QCheckBox("Hidden Network")
        self.wifi_hidden.stateChanged.connect(self._sync_wifi_template)
        wifi_opts.addWidget(self.wifi_sec, 1)
        wifi_opts.addWidget(self.wifi_hidden)
        p1_layout.addLayout(wifi_opts, 2, 1)

        self.stack.addWidget(p1)

        # Page 2: Contact Card (vCard)
        p2 = QWidget()
        p2_layout = QGridLayout(p2)
        p2_layout.setContentsMargins(0, 4, 0, 0)
        p2_layout.setSpacing(8)

        p2_layout.addWidget(QLabel("Full Name:"), 0, 0)
        self.vcard_name = QLineEdit()
        self.vcard_name.setPlaceholderText("e.g. Jane Doe")
        self.vcard_name.textChanged.connect(self._sync_vcard_template)
        p2_layout.addWidget(self.vcard_name, 0, 1)

        p2_layout.addWidget(QLabel("Phone:"), 1, 0)
        self.vcard_phone = QLineEdit()
        self.vcard_phone.setPlaceholderText("+1 555-0199")
        self.vcard_phone.textChanged.connect(self._sync_vcard_template)
        p2_layout.addWidget(self.vcard_phone, 1, 1)

        p2_layout.addWidget(QLabel("Email:"), 2, 0)
        self.vcard_email = QLineEdit()
        self.vcard_email.setPlaceholderText("jane.doe@example.com")
        self.vcard_email.textChanged.connect(self._sync_vcard_template)
        p2_layout.addWidget(self.vcard_email, 2, 1)

        p2_layout.addWidget(QLabel("Organization:"), 3, 0)
        self.vcard_org = QLineEdit()
        self.vcard_org.setPlaceholderText("Company or Institution")
        self.vcard_org.textChanged.connect(self._sync_vcard_template)
        p2_layout.addWidget(self.vcard_org, 3, 1)

        self.stack.addWidget(p2)

        # Page 3: Email
        p3 = QWidget()
        p3_layout = QGridLayout(p3)
        p3_layout.setContentsMargins(0, 4, 0, 0)
        p3_layout.setSpacing(8)

        p3_layout.addWidget(QLabel("Recipient:"), 0, 0)
        self.email_to = QLineEdit()
        self.email_to.setPlaceholderText("user@example.com")
        self.email_to.textChanged.connect(self._sync_email_template)
        p3_layout.addWidget(self.email_to, 0, 1)

        p3_layout.addWidget(QLabel("Subject:"), 1, 0)
        self.email_sub = QLineEdit()
        self.email_sub.setPlaceholderText("Email subject")
        self.email_sub.textChanged.connect(self._sync_email_template)
        p3_layout.addWidget(self.email_sub, 1, 1)

        p3_layout.addWidget(QLabel("Body:"), 2, 0)
        self.email_body = QLineEdit()
        self.email_body.setPlaceholderText("Message body")
        self.email_body.textChanged.connect(self._sync_email_template)
        p3_layout.addWidget(self.email_body, 2, 1)

        self.stack.addWidget(p3)

        layout.addWidget(self.stack)

        # 4. Meta Row: Character Count & Quick Clear Button
        meta_layout = QHBoxLayout()
        meta_layout.setContentsMargins(2, 0, 2, 0)

        self.chars_lbl = QLabel("18 characters")
        self.chars_lbl.setProperty("class", "SubTitle")

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setIcon(get_icon("trash", color="#94a3b8", size=14))
        self.clear_btn.setFixedHeight(26)
        self.clear_btn.clicked.connect(self.clear_content)

        meta_layout.addWidget(self.chars_lbl)
        meta_layout.addStretch()
        meta_layout.addWidget(self.clear_btn)
        layout.addLayout(meta_layout)

    def get_payload(self) -> str:
        """Return currently formatted QR payload."""
        return self._current_payload

    def set_payload(self, text: str) -> None:
        """Set raw text payload and update UI."""
        self.btn_group.button(0).setChecked(True)
        self.stack.setCurrentIndex(0)
        self.text_edit.setPlainText(text)

    def _on_template_tab_changed(self, idx: int) -> None:
        """Switch active template page."""
        self.stack.setCurrentIndex(idx)
        if idx == 0:
            self.type_badge.setText("URL / TEXT")
            self._on_raw_text_edited()
        elif idx == 1:
            self.type_badge.setText("WI-FI")
            self._sync_wifi_template()
        elif idx == 2:
            self.type_badge.setText("VCARD")
            self._sync_vcard_template()
        elif idx == 3:
            self.type_badge.setText("EMAIL")
            self._sync_email_template()

    def _on_raw_text_edited(self) -> None:
        text = self.text_edit.toPlainText()
        self._emit_payload(text)

    def _sync_wifi_template(self) -> None:
        ssid = self.wifi_ssid.text().strip()
        pwd = self.wifi_pass.text()
        sec_idx = self.wifi_sec.currentIndex()
        sec_type = "WPA" if sec_idx == 0 else ("WEP" if sec_idx == 1 else "nopass")
        hidden = self.wifi_hidden.isChecked()
        payload = format_wifi(ssid, pwd, sec_type, hidden)
        self._emit_payload(payload)

    def _sync_vcard_template(self) -> None:
        name = self.vcard_name.text().strip()
        phone = self.vcard_phone.text().strip()
        email = self.vcard_email.text().strip()
        org = self.vcard_org.text().strip()
        payload = format_vcard(name=name, phone=phone, email=email, org=org)
        self._emit_payload(payload)

    def _sync_email_template(self) -> None:
        to = self.email_to.text().strip()
        sub = self.email_sub.text().strip()
        body = self.email_body.text().strip()
        payload = format_email(recipient=to, subject=sub, body=body)
        self._emit_payload(payload)

    def _emit_payload(self, text: str) -> None:
        self._current_payload = text
        self.chars_lbl.setText(f"{len(text):,} characters")
        self.text_changed.emit(text)

    def clear_content(self) -> None:
        """Clear active inputs."""
        current_idx = self.stack.currentIndex()
        if current_idx == 0:
            self.text_edit.clear()
        elif current_idx == 1:
            self.wifi_ssid.clear()
            self.wifi_pass.clear()
        elif current_idx == 2:
            self.vcard_name.clear()
            self.vcard_phone.clear()
            self.vcard_email.clear()
            self.vcard_org.clear()
        elif current_idx == 3:
            self.email_to.clear()
            self.email_sub.clear()
            self.email_body.clear()
