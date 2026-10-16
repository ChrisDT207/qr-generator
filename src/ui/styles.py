"""Modern Dark and Light styling stylesheets (QSS) for the QR Code Generator Pro application."""

DARK_THEME = """
/* Global Window & Font Defaults */
QWidget {
    background-color: #0b0f19;
    color: #f1f5f9;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Roboto", "Helvetica Neue", sans-serif;
    font-size: 13px;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
}

/* Card Containers & Panels */
QFrame.CardPanel {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
}

QFrame.SubCardPanel {
    background-color: #162032;
    border: 1px solid #243046;
    border-radius: 8px;
}

/* Section Header Titles */
QLabel.SectionTitle {
    color: #f8fafc;
    font-size: 15px;
    font-weight: 600;
}

QLabel.SubSectionTitle {
    color: #f8fafc;
    font-size: 13px;
    font-weight: 600;
}

QLabel.FieldLabel {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
}

QLabel.MutedNote {
    color: #94a3b8;
    font-size: 11px;
}

QLabel#AppTitle {
    color: #f8fafc;
    font-size: 16px;
    font-weight: 700;
}

QLabel#PresetLabel {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
}

QLabel#LogoThumbPlaceholder {
    background: #0f172a;
    border-radius: 4px;
    border: 1px dashed #334155;
}

QLabel.SubTitle {
    color: #94a3b8;
    font-size: 12px;
}

QLabel.BadgeLive {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid #10b981;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
}

QLabel.BadgeFile {
    background-color: rgba(59, 130, 246, 0.15);
    color: #3b82f6;
    border: 1px solid #3b82f6;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
}

QLabel.BadgeFormat {
    background-color: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 600;
}

/* Standard Buttons */
QPushButton {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #334155;
    border-color: #475569;
}

QPushButton:pressed {
    background-color: #0f172a;
}

QPushButton:disabled {
    background-color: #161f2e;
    color: #475569;
    border-color: #1f2937;
}

/* Primary Start Camera Button */
QPushButton#StartCamBtn {
    background-color: #059669;
    color: #ffffff;
    border: 1px solid #10b981;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 18px;
}

QPushButton#StartCamBtn:hover {
    background-color: #10b981;
    border-color: #34d399;
}

QPushButton#StartCamBtn:pressed {
    background-color: #047857;
}

/* Stop Camera Button */
QPushButton#StopCamBtn {
    background-color: #be123c;
    color: #ffffff;
    border: 1px solid #f43f5e;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 18px;
}

QPushButton#StopCamBtn:hover {
    background-color: #e11d48;
    border-color: #fb7185;
}

QPushButton#StopCamBtn:pressed {
    background-color: #9f1239;
}

/* Accent Action Button (Open Browser) */
QPushButton#OpenUrlBtn {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 16px;
}

QPushButton#OpenUrlBtn:hover {
    background-color: #3b82f6;
    border-color: #60a5fa;
}

/* Copy Button */
QPushButton#CopyBtn {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 16px;
}

QPushButton#CopyBtn:hover {
    background-color: #2563eb;
    color: #ffffff;
}

/* Tool Buttons & Icons */
QToolButton {
    background-color: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 6px;
}

QToolButton:hover {
    background-color: #334155;
    border-color: #475569;
}

QToolButton:pressed {
    background-color: #0f172a;
}

/* ComboBoxes */
QComboBox {
    background-color: #131b2e;
    color: #f8fafc;
    border: 1px solid #27354f;
    border-radius: 8px;
    padding: 6px 12px;
    min-height: 22px;
}

QComboBox:hover {
    border-color: #3b82f6;
}

QComboBox::drop-down {
    border: none;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #94a3b8;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #111827;
    color: #f8fafc;
    border: 1px solid #334155;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    border-radius: 6px;
    padding: 4px;
}

/* Text Fields and Result Viewers */
QPlainTextEdit, QTextEdit, QLineEdit {
    background-color: #080c14;
    color: #f8fafc;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 13px;
    line-height: 1.4;
}

QPlainTextEdit:focus, QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #3b82f6;
    background-color: #0b101c;
}

/* Table Widget for Scan History */
QTableWidget {
    background-color: #0d121f;
    border: 1px solid #1e293b;
    border-radius: 8px;
    gridline-color: #162032;
    color: #e2e8f0;
    selection-background-color: #1e3a5f;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #131b2e;
    color: #94a3b8;
    padding: 6px 8px;
    border: none;
    border-bottom: 1px solid #243046;
    font-weight: 600;
    font-size: 12px;
}

QTableWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #141d2d;
}

QTableWidget::item:selected {
    background-color: #1d3557;
    color: #f8fafc;
}

/* Custom Scrollbars */
QScrollBar:vertical {
    border: none;
    background-color: #0b0f19;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #334155;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #0b0f19;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #334155;
    min-width: 20px;
    border-radius: 4px;
}

/* Status Bar */
QStatusBar {
    background-color: #090d16;
    color: #94a3b8;
    border-top: 1px solid #1e293b;
    font-size: 12px;
}

QStatusBar QLabel {
    background: transparent;
    color: #94a3b8;
}

/* ToolTips */
QToolTip {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 12px;
}
"""

LIGHT_THEME = """
/* Global Window & Font Defaults */
QWidget {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Roboto", "Helvetica Neue", sans-serif;
    font-size: 13px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}

/* Card Containers & Panels */
QFrame.CardPanel {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}

QFrame.SubCardPanel {
    background-color: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

/* Section Header Titles */
QLabel.SectionTitle {
    color: #0f172a;
    font-size: 15px;
    font-weight: 600;
}

QLabel.SubSectionTitle {
    color: #0f172a;
    font-size: 13px;
    font-weight: 600;
}

QLabel.FieldLabel {
    color: #334155;
    font-size: 12px;
    font-weight: 600;
}

QLabel.MutedNote {
    color: #64748b;
    font-size: 11px;
}

QLabel#AppTitle {
    color: #0f172a;
    font-size: 16px;
    font-weight: 700;
}

QLabel#PresetLabel {
    color: #475569;
    font-size: 12px;
    font-weight: 600;
}

QLabel#LogoThumbPlaceholder {
    background: #f1f5f9;
    border-radius: 4px;
    border: 1px dashed #cbd5e1;
}

QLabel.SubTitle {
    color: #64748b;
    font-size: 12px;
}

QLabel.BadgeLive {
    background-color: rgba(16, 185, 129, 0.12);
    color: #059669;
    border: 1px solid #10b981;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
}

QLabel.BadgeFile {
    background-color: rgba(37, 99, 235, 0.12);
    color: #2563eb;
    border: 1px solid #3b82f6;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
}

QLabel.BadgeFormat {
    background-color: #e2e8f0;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 600;
}

/* Standard Buttons */
QPushButton {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #f1f5f9;
    border-color: #94a3b8;
}

QPushButton:pressed {
    background-color: #e2e8f0;
}

QPushButton:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}

/* Primary Start Camera Button */
QPushButton#StartCamBtn {
    background-color: #10b981;
    color: #ffffff;
    border: 1px solid #059669;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 18px;
}

QPushButton#StartCamBtn:hover {
    background-color: #059669;
}

QPushButton#StartCamBtn:pressed {
    background-color: #047857;
}

/* Stop Camera Button */
QPushButton#StopCamBtn {
    background-color: #e11d48;
    color: #ffffff;
    border: 1px solid #be123c;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 18px;
}

QPushButton#StopCamBtn:hover {
    background-color: #be123c;
}

QPushButton#StopCamBtn:pressed {
    background-color: #9f1239;
}

/* Accent Action Button (Open Browser) */
QPushButton#OpenUrlBtn {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #1d4ed8;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 16px;
}

QPushButton#OpenUrlBtn:hover {
    background-color: #1d4ed8;
}

/* Copy Button */
QPushButton#CopyBtn {
    background-color: #ffffff;
    color: #2563eb;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 16px;
}

QPushButton#CopyBtn:hover {
    background-color: #eff6ff;
}

/* Tool Buttons & Icons */
QToolButton {
    background-color: #ffffff;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 6px;
}

QToolButton:hover {
    background-color: #f1f5f9;
    border-color: #94a3b8;
}

QToolButton:pressed {
    background-color: #e2e8f0;
}

/* ComboBoxes */
QComboBox {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 6px 12px;
    min-height: 22px;
}

QComboBox:hover {
    border-color: #2563eb;
}

QComboBox::drop-down {
    border: none;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #64748b;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    border-radius: 6px;
    padding: 4px;
}

/* Text Fields and Result Viewers */
QPlainTextEdit, QTextEdit, QLineEdit {
    background-color: #f8fafc;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 13px;
    line-height: 1.4;
}

QPlainTextEdit:focus, QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #2563eb;
    background-color: #ffffff;
}

/* Table Widget for Scan History */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #f1f5f9;
    color: #0f172a;
    selection-background-color: #e0f2fe;
    selection-color: #0369a1;
}

QHeaderView::section {
    background-color: #f8fafc;
    color: #64748b;
    padding: 6px 8px;
    border: none;
    border-bottom: 1px solid #e2e8f0;
    font-weight: 600;
    font-size: 12px;
}

QTableWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #f1f5f9;
}

QTableWidget::item:selected {
    background-color: #e0e7ff;
    color: #1e1b4b;
}

/* Custom Scrollbars */
QScrollBar:vertical {
    border: none;
    background-color: #f8fafc;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #cbd5e1;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #f8fafc;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #cbd5e1;
    min-width: 20px;
    border-radius: 4px;
}

/* Status Bar */
QStatusBar {
    background-color: #f1f5f9;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    font-size: 12px;
}

QStatusBar QLabel {
    background: transparent;
    color: #64748b;
}

/* ToolTips */
QToolTip {
    background-color: #0f172a;
    color: #ffffff;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 12px;
}
"""
