"""
Template Panel - Pre-configured design templates
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QListWidget,
    QListWidgetItem, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon


class TemplatePanel(QWidget):
    """Panel for selecting design templates"""

    template_selected = pyqtSignal(str)  # Emits template name

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Templates group
        group = QGroupBox("Design Templates")
        group_layout = QVBoxLayout()

        # Info label
        info = QLabel("Select a template to get started quickly:")
        info.setWordWrap(True)
        group_layout.addWidget(info)

        # Template list
        self.template_list = QListWidget()
        self.template_list.setMaximumHeight(150)

        templates = [
            ("Library Sign", "📚 Bilingual library signage (16×8 cm)"),
            ("Door Plate", "🚪 Office door nameplate (20×5 cm)"),
            ("Desk Nameplate", "💼 Professional desk sign (12×3 cm)"),
            ("Custom", "⚙️ Start from scratch")
        ]

        for name, description in templates:
            item = QListWidgetItem(f"{name}\n{description}")
            item.setData(Qt.ItemDataRole.UserRole, name)
            self.template_list.addItem(item)

        self.template_list.currentItemChanged.connect(self.on_template_selected)

        group_layout.addWidget(self.template_list)
        group.setLayout(group_layout)

        layout.addWidget(group)

    def on_template_selected(self, current, previous):
        """Handle template selection"""
        if current:
            template_name = current.data(Qt.ItemDataRole.UserRole)
            if template_name != "Custom":
                self.template_selected.emit(template_name)
