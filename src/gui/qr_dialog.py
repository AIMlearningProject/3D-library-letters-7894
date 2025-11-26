"""
QR Code Generator Dialog
Add QR codes to name plates with advanced positioning
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QPushButton, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QTextEdit, QRadioButton,
    QButtonGroup, QCheckBox, QTabWidget, QWidget,
    QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
import qrcode
from io import BytesIO


class QRCodeDialog(QDialog):
    """Dialog for generating and positioning QR codes"""

    qr_generated = pyqtSignal(dict)  # Emits QR code data

    def __init__(self, parent=None):
        super().__init__(parent)
        self.qr_image = None
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("QR Code Generator - NamePlate Studio Pro")
        self.setMinimumSize(700, 600)

        layout = QVBoxLayout(self)

        # Create tabs
        tabs = QTabWidget()

        # Content tab
        content_tab = self.create_content_tab()
        tabs.addTab(content_tab, "Content")

        # Position tab
        position_tab = self.create_position_tab()
        tabs.addTab(position_tab, "Position & Size")

        # Style tab
        style_tab = self.create_style_tab()
        tabs.addTab(style_tab, "Style")

        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        tabs.addTab(advanced_tab, "Advanced")

        layout.addWidget(tabs)

        # Preview
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout()

        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(200, 200)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("border: 1px solid #555; background: white;")
        self.preview_label.setText("QR code preview will appear here")
        preview_layout.addWidget(self.preview_label)

        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        generate_btn = QPushButton("Generate Preview")
        generate_btn.clicked.connect(self.generate_qr)
        button_layout.addWidget(generate_btn)

        apply_btn = QPushButton("Add to Design")
        apply_btn.clicked.connect(self.apply_qr)
        button_layout.addWidget(apply_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def create_content_tab(self):
        """Create content input tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Content type
        type_group = QGroupBox("QR Code Type")
        type_layout = QVBoxLayout()

        self.type_group = QButtonGroup()

        self.url_radio = QRadioButton("Website URL")
        self.url_radio.setChecked(True)
        self.url_radio.toggled.connect(self.on_type_changed)
        self.type_group.addButton(self.url_radio)
        type_layout.addWidget(self.url_radio)

        self.text_radio = QRadioButton("Plain Text")
        self.text_radio.toggled.connect(self.on_type_changed)
        self.type_group.addButton(self.text_radio)
        type_layout.addWidget(self.text_radio)

        self.vcard_radio = QRadioButton("Contact (vCard)")
        self.vcard_radio.toggled.connect(self.on_type_changed)
        self.type_group.addButton(self.vcard_radio)
        type_layout.addWidget(self.vcard_radio)

        self.wifi_radio = QRadioButton("WiFi Credentials")
        self.wifi_radio.toggled.connect(self.on_type_changed)
        self.type_group.addButton(self.wifi_radio)
        type_layout.addWidget(self.wifi_radio)

        self.email_radio = QRadioButton("Email")
        self.email_radio.toggled.connect(self.on_type_changed)
        self.type_group.addButton(self.email_radio)
        type_layout.addWidget(self.email_radio)

        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # Content input (dynamic based on type)
        self.content_stack = QGroupBox("Content")
        self.content_layout = QVBoxLayout()
        self.content_stack.setLayout(self.content_layout)
        layout.addWidget(self.content_stack)

        # Initialize with URL input
        self.create_url_input()

        layout.addStretch()
        return widget

    def create_url_input(self):
        """Create URL input fields"""
        self.clear_content_layout()

        url_layout = QFormLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        url_layout.addRow("URL:", self.url_input)

        self.content_layout.addLayout(url_layout)

    def create_text_input(self):
        """Create text input field"""
        self.clear_content_layout()

        text_layout = QVBoxLayout()

        text_layout.addWidget(QLabel("Text Content:"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter any text...")
        self.text_input.setMaximumHeight(100)
        text_layout.addWidget(self.text_input)

        self.content_layout.addLayout(text_layout)

    def create_vcard_input(self):
        """Create vCard input fields"""
        self.clear_content_layout()

        vcard_layout = QFormLayout()

        self.vcard_name = QLineEdit()
        vcard_layout.addRow("Full Name:", self.vcard_name)

        self.vcard_org = QLineEdit()
        vcard_layout.addRow("Organization:", self.vcard_org)

        self.vcard_phone = QLineEdit()
        vcard_layout.addRow("Phone:", self.vcard_phone)

        self.vcard_email = QLineEdit()
        vcard_layout.addRow("Email:", self.vcard_email)

        self.vcard_url = QLineEdit()
        vcard_layout.addRow("Website:", self.vcard_url)

        self.content_layout.addLayout(vcard_layout)

    def create_wifi_input(self):
        """Create WiFi input fields"""
        self.clear_content_layout()

        wifi_layout = QFormLayout()

        self.wifi_ssid = QLineEdit()
        wifi_layout.addRow("Network Name (SSID):", self.wifi_ssid)

        self.wifi_password = QLineEdit()
        self.wifi_password.setEchoMode(QLineEdit.EchoMode.Password)
        wifi_layout.addRow("Password:", self.wifi_password)

        self.wifi_security = QComboBox()
        self.wifi_security.addItems(["WPA/WPA2", "WEP", "None"])
        wifi_layout.addRow("Security:", self.wifi_security)

        self.wifi_hidden = QCheckBox("Hidden network")
        wifi_layout.addRow("", self.wifi_hidden)

        self.content_layout.addLayout(wifi_layout)

    def create_email_input(self):
        """Create email input fields"""
        self.clear_content_layout()

        email_layout = QFormLayout()

        self.email_to = QLineEdit()
        email_layout.addRow("To:", self.email_to)

        self.email_subject = QLineEdit()
        email_layout.addRow("Subject:", self.email_subject)

        self.email_body = QTextEdit()
        self.email_body.setMaximumHeight(80)
        email_layout.addRow("Body:", self.email_body)

        self.content_layout.addLayout(email_layout)

    def clear_content_layout(self):
        """Clear content layout"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_layout(self, layout):
        """Recursively clear a layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def on_type_changed(self):
        """Handle content type change"""
        if self.url_radio.isChecked():
            self.create_url_input()
        elif self.text_radio.isChecked():
            self.create_text_input()
        elif self.vcard_radio.isChecked():
            self.create_vcard_input()
        elif self.wifi_radio.isChecked():
            self.create_wifi_input()
        elif self.email_radio.isChecked():
            self.create_email_input()

    def create_position_tab(self):
        """Create position settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Position
        pos_group = QGroupBox("Position on Plate")
        pos_layout = QFormLayout()

        self.position_combo = QComboBox()
        self.position_combo.addItems([
            "Bottom Right",
            "Bottom Left",
            "Top Right",
            "Top Left",
            "Center",
            "Custom"
        ])
        pos_layout.addRow("Position:", self.position_combo)

        self.offset_x = QDoubleSpinBox()
        self.offset_x.setRange(-100, 100)
        self.offset_x.setValue(0)
        self.offset_x.setSuffix(" mm")
        pos_layout.addRow("X Offset:", self.offset_x)

        self.offset_y = QDoubleSpinBox()
        self.offset_y.setRange(-100, 100)
        self.offset_y.setValue(0)
        self.offset_y.setSuffix(" mm")
        pos_layout.addRow("Y Offset:", self.offset_y)

        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)

        # Size
        size_group = QGroupBox("Size")
        size_layout = QFormLayout()

        self.qr_size = QSpinBox()
        self.qr_size.setRange(10, 100)
        self.qr_size.setValue(20)
        self.qr_size.setSuffix(" mm")
        size_layout.addRow("QR Code Size:", self.qr_size)

        self.scale_with_plate = QCheckBox("Scale with plate size")
        size_layout.addRow("Auto-scale:", self.scale_with_plate)

        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        # Depth
        depth_group = QGroupBox("3D Properties")
        depth_layout = QFormLayout()

        self.qr_style = QComboBox()
        self.qr_style.addItems(["Embossed (raised)", "Recessed (cut in)", "Flat"])
        depth_layout.addRow("Style:", self.qr_style)

        self.qr_depth = QDoubleSpinBox()
        self.qr_depth.setRange(0.5, 5)
        self.qr_depth.setValue(1.0)
        self.qr_depth.setSuffix(" mm")
        depth_layout.addRow("Depth:", self.qr_depth)

        depth_group.setLayout(depth_layout)
        layout.addWidget(depth_group)

        layout.addStretch()
        return widget

    def create_style_tab(self):
        """Create style settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Error correction
        error_group = QGroupBox("Error Correction")
        error_layout = QFormLayout()

        self.error_correction = QComboBox()
        self.error_correction.addItems([
            "Low (7%)",
            "Medium (15%)",
            "Quartile (25%)",
            "High (30%)"
        ])
        self.error_correction.setCurrentIndex(1)
        error_layout.addRow("Level:", self.error_correction)

        info_label = QLabel("Higher error correction allows damaged QR codes to still work")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #999;")
        error_layout.addRow("", info_label)

        error_group.setLayout(error_layout)
        layout.addWidget(error_group)

        # Border
        border_group = QGroupBox("Border")
        border_layout = QFormLayout()

        self.border_size = QSpinBox()
        self.border_size.setRange(0, 10)
        self.border_size.setValue(4)
        self.border_size.setSuffix(" modules")
        border_layout.addRow("Border Size:", self.border_size)

        border_group.setLayout(border_layout)
        layout.addWidget(border_group)

        layout.addStretch()
        return widget

    def create_advanced_tab(self):
        """Create advanced settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Module size
        module_group = QGroupBox("Module Settings")
        module_layout = QFormLayout()

        self.box_size = QSpinBox()
        self.box_size.setRange(1, 20)
        self.box_size.setValue(10)
        self.box_size.setSuffix(" pixels")
        module_layout.addRow("Module Size:", self.box_size)

        module_group.setLayout(module_layout)
        layout.addWidget(module_group)

        # Metadata
        meta_group = QGroupBox("Metadata")
        meta_layout = QFormLayout()

        self.qr_label = QLineEdit()
        self.qr_label.setPlaceholderText("Optional label for this QR code")
        meta_layout.addRow("Label:", self.qr_label)

        meta_group.setLayout(meta_layout)
        layout.addWidget(meta_group)

        layout.addStretch()
        return widget

    def generate_qr(self):
        """Generate QR code preview"""
        try:
            # Get content based on type
            content = self.get_qr_content()

            if not content:
                QMessageBox.warning(self, "No Content", "Please enter content for the QR code.")
                return

            # Get error correction level
            error_map = {
                "Low (7%)": qrcode.constants.ERROR_CORRECT_L,
                "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
                "Quartile (25%)": qrcode.constants.ERROR_CORRECT_Q,
                "High (30%)": qrcode.constants.ERROR_CORRECT_H
            }
            error_level = error_map[self.error_correction.currentText()]

            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=error_level,
                box_size=self.box_size.value(),
                border=self.border_size.value()
            )

            qr.add_data(content)
            qr.make(fit=True)

            # Create image
            img = qr.make_image(fill_color="black", back_color="white")

            # Convert to QPixmap for display
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)

            qimage = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimage)

            # Scale to fit preview
            scaled_pixmap = pixmap.scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.preview_label.setPixmap(scaled_pixmap)
            self.qr_image = img

            QMessageBox.information(self, "Success", "QR code generated successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate QR code: {str(e)}")

    def get_qr_content(self) -> str:
        """Get QR code content based on selected type"""
        if self.url_radio.isChecked():
            return self.url_input.text()

        elif self.text_radio.isChecked():
            return self.text_input.toPlainText()

        elif self.vcard_radio.isChecked():
            # Generate vCard format
            vcard = "BEGIN:VCARD\nVERSION:3.0\n"
            if self.vcard_name.text():
                vcard += f"FN:{self.vcard_name.text()}\n"
            if self.vcard_org.text():
                vcard += f"ORG:{self.vcard_org.text()}\n"
            if self.vcard_phone.text():
                vcard += f"TEL:{self.vcard_phone.text()}\n"
            if self.vcard_email.text():
                vcard += f"EMAIL:{self.vcard_email.text()}\n"
            if self.vcard_url.text():
                vcard += f"URL:{self.vcard_url.text()}\n"
            vcard += "END:VCARD"
            return vcard

        elif self.wifi_radio.isChecked():
            # Generate WiFi format
            security = self.wifi_security.currentText().split('/')[0]
            hidden = "true" if self.wifi_hidden.isChecked() else "false"
            return f"WIFI:T:{security};S:{self.wifi_ssid.text()};P:{self.wifi_password.text()};H:{hidden};;"

        elif self.email_radio.isChecked():
            # Generate mailto format
            content = f"mailto:{self.email_to.text()}"
            params = []
            if self.email_subject.text():
                params.append(f"subject={self.email_subject.text()}")
            if self.email_body.toPlainText():
                params.append(f"body={self.email_body.toPlainText()}")
            if params:
                content += "?" + "&".join(params)
            return content

        return ""

    def apply_qr(self):
        """Apply QR code to design"""
        if not self.qr_image:
            QMessageBox.warning(
                self, "No QR Code",
                "Please generate a QR code first."
            )
            return

        # Emit QR code data
        qr_data = {
            'content': self.get_qr_content(),
            'size': self.qr_size.value(),
            'position': self.position_combo.currentText(),
            'offset_x': self.offset_x.value(),
            'offset_y': self.offset_y.value(),
            'style': self.qr_style.currentText(),
            'depth': self.qr_depth.value(),
            'label': self.qr_label.text(),
            'image': self.qr_image
        }

        self.qr_generated.emit(qr_data)
        QMessageBox.information(
            self, "QR Code Added",
            "QR code has been added to your design!"
        )
        self.accept()
