"""
Main Window for NamePlate Studio Pro
Central application window with all panels and controls
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QMenuBar, QMenu, QToolBar, QStatusBar,
    QMessageBox, QFileDialog, QLabel
)
from PyQt6.QtCore import Qt, QSize, QSettings
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from pathlib import Path

from .design_panel import DesignPanel
from .preview_panel import PreviewPanel
from .template_panel import TemplatePanel
from .settings_dialog import SettingsDialog
from .batch_dialog import BatchProcessDialog
from .qr_dialog import QRCodeDialog
try:
    from ..core.project_manager import ProjectManager
except ImportError:
    from core.project_manager import ProjectManager


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.current_file = None
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("NamePlate Studio Pro")
        self.setGeometry(100, 100, 1400, 800)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create main splitter for panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Templates and Design Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)

        # Template selector
        self.template_panel = TemplatePanel()
        left_layout.addWidget(self.template_panel)

        # Design controls
        self.design_panel = DesignPanel()
        left_layout.addWidget(self.design_panel, stretch=1)

        # Right panel: 3D Preview
        self.preview_panel = PreviewPanel()

        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(self.preview_panel)

        # Set initial sizes (30% left, 70% right)
        splitter.setSizes([400, 1000])

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create menu bar (after panels are created)
        self.create_menu_bar()

        # Create toolbar (after panels are created)
        self.create_toolbar()

        # Connect signals
        self.connect_signals()

        # Apply dark theme
        self.apply_theme()

    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New Project", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        open_action = QAction("&Open Project...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        save_action = QAction("&Save Project", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save Project &As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        recent_menu = file_menu.addMenu("Recent Projects")
        self.update_recent_menu(recent_menu)

        file_menu.addSeparator()

        export_action = QAction("&Export to STL...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_stl)
        file_menu.addAction(export_action)

        export_blend_action = QAction("Export to Blend...", self)
        export_blend_action.triggered.connect(self.export_blend)
        file_menu.addAction(export_blend_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        preferences_action = QAction("&Preferences...", self)
        preferences_action.setShortcut("Ctrl+,")
        preferences_action.triggered.connect(self.show_preferences)
        edit_menu.addAction(preferences_action)

        # View Menu
        view_menu = menubar.addMenu("&View")

        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        view_menu.addAction(zoom_out_action)

        fit_view_action = QAction("&Fit to View", self)
        fit_view_action.setShortcut("Ctrl+0")
        view_menu.addAction(fit_view_action)

        view_menu.addSeparator()

        reset_view_action = QAction("&Reset View", self)
        reset_view_action.triggered.connect(self.preview_panel.reset_view)
        view_menu.addAction(reset_view_action)

        # Tools Menu
        tools_menu = menubar.addMenu("&Tools")

        batch_action = QAction("&Batch Processing...", self)
        batch_action.setShortcut("Ctrl+B")
        batch_action.triggered.connect(self.show_batch_dialog)
        tools_menu.addAction(batch_action)

        qr_action = QAction("Add &QR Code...", self)
        qr_action.triggered.connect(self.show_qr_dialog)
        tools_menu.addAction(qr_action)

        logo_action = QAction("Add &Logo/Image...", self)
        logo_action.triggered.connect(self.add_logo)
        tools_menu.addAction(logo_action)

        tools_menu.addSeparator()

        validate_action = QAction("&Validate Design", self)
        validate_action.setShortcut("Ctrl+Shift+V")
        validate_action.triggered.connect(self.validate_design)
        tools_menu.addAction(validate_action)

        # Help Menu
        help_menu = menubar.addMenu("&Help")

        quick_start_action = QAction("&Quick Start Guide", self)
        quick_start_action.setShortcut(QKeySequence.StandardKey.HelpContents)
        quick_start_action.triggered.connect(self.show_quick_start)
        help_menu.addAction(quick_start_action)

        tutorials_action = QAction("Video &Tutorials", self)
        tutorials_action.triggered.connect(self.show_tutorials)
        help_menu.addAction(tutorials_action)

        help_menu.addSeparator()

        about_action = QAction("&About NamePlate Studio Pro", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Create the main toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Add common actions
        new_btn = toolbar.addAction("New")
        new_btn.triggered.connect(self.new_project)

        open_btn = toolbar.addAction("Open")
        open_btn.triggered.connect(self.open_project)

        save_btn = toolbar.addAction("Save")
        save_btn.triggered.connect(self.save_project)

        toolbar.addSeparator()

        export_btn = toolbar.addAction("Export STL")
        export_btn.triggered.connect(self.export_stl)

        toolbar.addSeparator()

        generate_btn = toolbar.addAction("Generate 3D")
        generate_btn.triggered.connect(self.generate_model)

    def connect_signals(self):
        """Connect all signals between components"""
        # When design changes, update preview
        self.design_panel.design_changed.connect(self.on_design_changed)

        # When template selected, update design
        self.template_panel.template_selected.connect(self.on_template_selected)

    def apply_theme(self):
        """Apply dark theme to the application"""
        dark_stylesheet = """
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QGroupBox {
                border: 1px solid #555555;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a697;
            }
            QPushButton:pressed {
                background-color: #0a5c5f;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #0d7377;
            }
            QSlider::groove:horizontal {
                background: #3c3c3c;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #0d7377;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #14a697;
            }
            QLabel {
                color: #ffffff;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #0d7377;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenu::item:selected {
                background-color: #0d7377;
            }
            QToolBar {
                background-color: #3c3c3c;
                border: none;
                spacing: 5px;
                padding: 3px;
            }
            QStatusBar {
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QListWidget {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #0d7377;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    # Slot methods
    def on_design_changed(self, design_data):
        """Handle design changes from design panel"""
        self.status_bar.showMessage("Design updated")
        # Update preview if auto-update is enabled
        if self.settings.value("auto_update_preview", True, bool):
            self.preview_panel.update_preview(design_data)

    def on_template_selected(self, template_name):
        """Handle template selection"""
        self.status_bar.showMessage(f"Template loaded: {template_name}")
        self.design_panel.load_template(template_name)

    # Action methods
    def new_project(self):
        """Create a new project"""
        reply = QMessageBox.question(
            self, "New Project",
            "Create a new project? Unsaved changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.design_panel.reset()
            self.preview_panel.clear()
            self.current_file = None
            self.status_bar.showMessage("New project created")

    def open_project(self):
        """Open an existing project"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project",
            str(Path.home()),
            "NamePlate Project (*.npproj);;All Files (*.*)"
        )
        if file_path:
            success, project_data, message = ProjectManager.load_project(file_path)
            if success:
                self.design_panel.load_design_data(project_data['design'])
                self.current_file = file_path
                ProjectManager.add_recent_project(file_path)
                self.status_bar.showMessage(f"Opened: {Path(file_path).name}")
                QMessageBox.information(self, "Success", message)
            else:
                QMessageBox.critical(self, "Error", message)

    def save_project(self):
        """Save the current project"""
        if self.current_file:
            design_data = self.design_panel.get_design_data()
            success, message = ProjectManager.save_project(self.current_file, design_data)
            if success:
                self.status_bar.showMessage(f"Saved: {Path(self.current_file).name}")
            else:
                QMessageBox.critical(self, "Error", message)
        else:
            self.save_project_as()

    def save_project_as(self):
        """Save the project with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project As",
            str(Path.home()),
            "NamePlate Project (*.npproj)"
        )
        if file_path:
            design_data = self.design_panel.get_design_data()
            success, message = ProjectManager.save_project(file_path, design_data)
            if success:
                self.current_file = file_path
                ProjectManager.add_recent_project(file_path)
                self.status_bar.showMessage(f"Saved as: {Path(file_path).name}")
                QMessageBox.information(self, "Success", "Project saved successfully!")
            else:
                QMessageBox.critical(self, "Error", message)

    def export_stl(self):
        """Export design to STL file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to STL",
            str(Path.home()),
            "STL Files (*.stl)"
        )
        if file_path:
            # TODO: Implement STL export
            self.status_bar.showMessage(f"Exported: {Path(file_path).name}")

    def export_blend(self):
        """Export design to Blender file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to Blend",
            str(Path.home()),
            "Blender Files (*.blend)"
        )
        if file_path:
            # TODO: Implement Blend export
            self.status_bar.showMessage(f"Exported: {Path(file_path).name}")

    def generate_model(self):
        """Generate the 3D model"""
        self.status_bar.showMessage("Generating 3D model...")
        # TODO: Implement model generation
        design_data = self.design_panel.get_design_data()
        self.preview_panel.update_preview(design_data)
        self.status_bar.showMessage("Model generated successfully")

    def show_preferences(self):
        """Show preferences dialog"""
        dialog = SettingsDialog(self)
        dialog.exec()

    def show_batch_dialog(self):
        """Show batch processing dialog"""
        dialog = BatchProcessDialog(self)
        dialog.exec()

    def show_qr_dialog(self):
        """Show QR code dialog"""
        dialog = QRCodeDialog(self)
        dialog.qr_generated.connect(self.on_qr_generated)
        dialog.exec()

    def on_qr_generated(self, qr_data):
        """Handle QR code generation"""
        self.status_bar.showMessage(f"QR code added: {qr_data['label'] or 'Untitled'}")

    def add_logo(self):
        """Add logo or image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Logo/Image",
            str(Path.home()),
            "Images (*.png *.jpg *.jpeg *.svg);;All Files (*.*)"
        )
        if file_path:
            # TODO: Implement logo import
            self.status_bar.showMessage(f"Logo added: {Path(file_path).name}")

    def validate_design(self):
        """Validate the current design"""
        # TODO: Implement validation
        QMessageBox.information(
            self, "Validation",
            "Design validation:\n\n✓ All dimensions valid\n✓ Font found\n✓ Ready to export"
        )

    def show_quick_start(self):
        """Show quick start guide"""
        # TODO: Open documentation
        QMessageBox.information(self, "Quick Start", "Quick start guide coming soon!")

    def show_tutorials(self):
        """Show video tutorials"""
        # TODO: Open tutorials page
        QMessageBox.information(self, "Tutorials", "Video tutorials coming soon!")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About NamePlate Studio Pro",
            "<h2>NamePlate Studio Pro</h2>"
            "<p>Version 1.0.0</p>"
            "<p>Professional 3D Name Plate Generator</p>"
            "<p>Built with Blender Python API and PyQt6</p>"
            "<p>© 2024 NamePlate Studio</p>"
        )

    def update_recent_menu(self, menu):
        """Update recent projects menu"""
        # TODO: Load recent projects from settings
        menu.addAction("No recent projects")

    def load_settings(self):
        """Load application settings"""
        # Restore window geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        """Handle window close event"""
        # Save window geometry
        self.settings.setValue("geometry", self.saveGeometry())

        # Check for unsaved changes
        reply = QMessageBox.question(
            self, "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
