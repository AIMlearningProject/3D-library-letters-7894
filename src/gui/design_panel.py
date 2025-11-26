"""
Design Panel - Text and dimension controls
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QLineEdit, QDoubleSpinBox, QSlider,
    QPushButton, QComboBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal


class DesignPanel(QWidget):
    """Panel for design configuration"""

    design_changed = pyqtSignal(dict)  # Emits design data

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Text Content Group
        text_group = QGroupBox("Text Content")
        text_layout = QFormLayout()

        self.line1_edit = QLineEdit("Kirjasto")
        self.line1_edit.textChanged.connect(self.emit_design_changed)
        text_layout.addRow("Line 1:", self.line1_edit)

        self.line2_edit = QLineEdit("Library")
        self.line2_edit.textChanged.connect(self.emit_design_changed)
        text_layout.addRow("Line 2:", self.line2_edit)

        text_group.setLayout(text_layout)
        layout.addWidget(text_group)

        # Dimensions Group
        dimensions_group = QGroupBox("Dimensions (mm)")
        dim_layout = QVBoxLayout()

        # Plate length
        self.plate_length = self.create_slider_control(
            "Plate Length:", 50, 500, 160, " mm"
        )
        dim_layout.addLayout(self.plate_length['layout'])

        # Plate width
        self.plate_width = self.create_slider_control(
            "Plate Width:", 30, 300, 80, " mm"
        )
        dim_layout.addLayout(self.plate_width['layout'])

        # Plate thickness
        self.plate_thickness = self.create_slider_control(
            "Plate Thickness:", 3, 20, 7, " mm"
        )
        dim_layout.addLayout(self.plate_thickness['layout'])

        # Letter depth
        self.letter_depth = self.create_slider_control(
            "Letter Depth:", 2, 20, 4, " mm"
        )
        dim_layout.addLayout(self.letter_depth['layout'])

        dimensions_group.setLayout(dim_layout)
        layout.addWidget(dimensions_group)

        # Typography Group
        typo_group = QGroupBox("Typography")
        typo_layout = QFormLayout()

        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Quicksand-Regular",
            "Quicksand-Bold",
            "Quicksand-Light",
            "Arial",
            "Helvetica"
        ])
        self.font_combo.currentTextChanged.connect(self.emit_design_changed)
        typo_layout.addRow("Font:", self.font_combo)

        self.text_size = QDoubleSpinBox()
        self.text_size.setRange(10, 100)
        self.text_size.setValue(25)
        self.text_size.setSuffix(" mm")
        self.text_size.valueChanged.connect(self.emit_design_changed)
        typo_layout.addRow("Text Size:", self.text_size)

        self.line_spacing = QDoubleSpinBox()
        self.line_spacing.setRange(10, 100)
        self.line_spacing.setValue(35)
        self.line_spacing.setSuffix(" mm")
        self.line_spacing.valueChanged.connect(self.emit_design_changed)
        typo_layout.addRow("Line Spacing:", self.line_spacing)

        typo_group.setLayout(typo_layout)
        layout.addWidget(typo_group)

        # Material Group
        material_group = QGroupBox("Material & Finish")
        material_layout = QFormLayout()

        self.material_combo = QComboBox()
        self.material_combo.addItems([
            "PLA Standard",
            "PETG Glossy",
            "ABS",
            "Wood Fill",
            "Carbon Fiber"
        ])
        material_layout.addRow("Material:", self.material_combo)

        self.finish_combo = QComboBox()
        self.finish_combo.addItems([
            "Smooth (post-processed)",
            "Standard (as-printed)",
            "Textured"
        ])
        material_layout.addRow("Finish:", self.finish_combo)

        material_group.setLayout(material_layout)
        layout.addWidget(material_group)

        # Action Buttons
        button_layout = QHBoxLayout()

        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset)
        button_layout.addWidget(reset_btn)

        generate_btn = QPushButton("Generate Preview")
        generate_btn.clicked.connect(self.emit_design_changed)
        button_layout.addWidget(generate_btn)

        layout.addLayout(button_layout)

        # Add stretch to push everything to top
        layout.addStretch()

    def create_slider_control(self, label, min_val, max_val, default, suffix):
        """Create a slider with spinbox control"""
        layout = QHBoxLayout()

        label_widget = QLabel(label)
        label_widget.setMinimumWidth(120)
        layout.addWidget(label_widget)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.valueChanged.connect(self.emit_design_changed)
        layout.addWidget(slider)

        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setValue(default)
        spinbox.setSuffix(suffix)
        spinbox.setMinimumWidth(80)
        spinbox.valueChanged.connect(slider.setValue)
        slider.valueChanged.connect(spinbox.setValue)
        layout.addWidget(spinbox)

        return {
            'layout': layout,
            'slider': slider,
            'spinbox': spinbox,
            'label': label_widget
        }

    def emit_design_changed(self):
        """Emit signal when design changes"""
        self.design_changed.emit(self.get_design_data())

    def get_design_data(self):
        """Get current design configuration"""
        return {
            'text_line_1': self.line1_edit.text(),
            'text_line_2': self.line2_edit.text(),
            'plate_length': self.plate_length['spinbox'].value(),
            'plate_width': self.plate_width['spinbox'].value(),
            'plate_thickness': self.plate_thickness['spinbox'].value(),
            'letter_depth': self.letter_depth['spinbox'].value(),
            'font': self.font_combo.currentText(),
            'text_size': self.text_size.value(),
            'line_spacing': self.line_spacing.value(),
            'material': self.material_combo.currentText(),
            'finish': self.finish_combo.currentText()
        }

    def reset(self):
        """Reset to default values"""
        self.line1_edit.setText("Kirjasto")
        self.line2_edit.setText("Library")
        self.plate_length['slider'].setValue(160)
        self.plate_width['slider'].setValue(80)
        self.plate_thickness['slider'].setValue(7)
        self.letter_depth['slider'].setValue(4)
        self.text_size.setValue(25)
        self.line_spacing.setValue(35)
        self.font_combo.setCurrentIndex(0)
        self.material_combo.setCurrentIndex(0)
        self.finish_combo.setCurrentIndex(0)
        self.emit_design_changed()

    def load_template(self, template_name):
        """Load a template configuration"""
        templates = {
            'Library Sign': {
                'text_line_1': 'Kirjasto',
                'text_line_2': 'Library',
                'plate_length': 160,
                'plate_width': 80,
                'text_size': 25
            },
            'Door Plate': {
                'text_line_1': 'Office',
                'text_line_2': '201',
                'plate_length': 200,
                'plate_width': 50,
                'text_size': 20
            },
            'Desk Nameplate': {
                'text_line_1': 'John Doe',
                'text_line_2': 'Manager',
                'plate_length': 120,
                'plate_width': 30,
                'text_size': 15
            }
        }

        if template_name in templates:
            template = templates[template_name]
            self.line1_edit.setText(template.get('text_line_1', ''))
            self.line2_edit.setText(template.get('text_line_2', ''))
            self.plate_length['slider'].setValue(template.get('plate_length', 160))
            self.plate_width['slider'].setValue(template.get('plate_width', 80))
            self.text_size.setValue(template.get('text_size', 25))
            self.emit_design_changed()

    def load_design_data(self, design_data: dict):
        """Load complete design data from saved project"""
        self.line1_edit.setText(design_data.get('text_line_1', ''))
        self.line2_edit.setText(design_data.get('text_line_2', ''))
        self.plate_length['slider'].setValue(design_data.get('plate_length', 160))
        self.plate_width['slider'].setValue(design_data.get('plate_width', 80))
        self.plate_thickness['slider'].setValue(design_data.get('plate_thickness', 7))
        self.letter_depth['slider'].setValue(design_data.get('letter_depth', 4))
        self.text_size.setValue(design_data.get('text_size', 25))
        self.line_spacing.setValue(design_data.get('line_spacing', 35))

        # Set comboboxes
        font = design_data.get('font', 'Quicksand-Regular')
        index = self.font_combo.findText(font)
        if index >= 0:
            self.font_combo.setCurrentIndex(index)

        material = design_data.get('material', 'PLA Standard')
        index = self.material_combo.findText(material)
        if index >= 0:
            self.material_combo.setCurrentIndex(index)

        finish = design_data.get('finish', 'Standard (as-printed)')
        index = self.finish_combo.findText(finish)
        if index >= 0:
            self.finish_combo.setCurrentIndex(index)

        self.emit_design_changed()
