"""
Settings/Preferences Dialog
Configure application preferences and paths
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
    QSpinBox, QGroupBox, QFormLayout, QFileDialog,
    QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, QSettings
from pathlib import Path


class SettingsDialog(QDialog):
    """Application settings dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings()
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Settings - NamePlate Studio Pro")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout(self)

        # Create tabs
        tabs = QTabWidget()

        # General tab
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "General")

        # Paths tab
        paths_tab = self.create_paths_tab()
        tabs.addTab(paths_tab, "Paths")

        # Preview tab
        preview_tab = self.create_preview_tab()
        tabs.addTab(preview_tab, "Preview")

        # Export tab
        export_tab = self.create_export_tab()
        tabs.addTab(export_tab, "Export")

        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        tabs.addTab(advanced_tab, "Advanced")

        layout.addWidget(tabs)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self.save_and_close)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def create_general_tab(self):
        """Create general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Application settings
        app_group = QGroupBox("Application")
        app_layout = QFormLayout()

        self.auto_save_check = QCheckBox("Enable auto-save")
        app_layout.addRow("Auto-save:", self.auto_save_check)

        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(1, 60)
        self.auto_save_interval.setValue(5)
        self.auto_save_interval.setSuffix(" minutes")
        app_layout.addRow("Interval:", self.auto_save_interval)

        self.check_updates = QCheckBox("Check for updates on startup")
        app_layout.addRow("Updates:", self.check_updates)

        self.show_tips = QCheckBox("Show tips on startup")
        app_layout.addRow("Tips:", self.show_tips)

        app_group.setLayout(app_layout)
        layout.addWidget(app_group)

        # UI settings
        ui_group = QGroupBox("User Interface")
        ui_layout = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "System"])
        ui_layout.addRow("Theme:", self.theme_combo)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Finnish", "Swedish"])
        ui_layout.addRow("Language:", self.language_combo)

        self.show_statusbar = QCheckBox("Show status bar")
        self.show_statusbar.setChecked(True)
        ui_layout.addRow("Status bar:", self.show_statusbar)

        self.show_toolbar = QCheckBox("Show toolbar")
        self.show_toolbar.setChecked(True)
        ui_layout.addRow("Toolbar:", self.show_toolbar)

        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)

        layout.addStretch()
        return widget

    def create_paths_tab(self):
        """Create paths settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Font paths
        font_group = QGroupBox("Fonts")
        font_layout = QVBoxLayout()

        quicksand_layout = QHBoxLayout()
        quicksand_layout.addWidget(QLabel("Quicksand Font:"))
        self.quicksand_path = QLineEdit()
        self.quicksand_path.setText("C:/Windows/Fonts/Quicksand-Regular.ttf")
        quicksand_layout.addWidget(self.quicksand_path)
        browse_font_btn = QPushButton("Browse...")
        browse_font_btn.clicked.connect(lambda: self.browse_file(self.quicksand_path, "Font Files (*.ttf *.otf)"))
        quicksand_layout.addWidget(browse_font_btn)
        font_layout.addLayout(quicksand_layout)

        font_group.setLayout(font_layout)
        layout.addWidget(font_group)

        # Output paths
        output_group = QGroupBox("Output Directories")
        output_layout = QVBoxLayout()

        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(QLabel("Default Output:"))
        self.output_path = QLineEdit()
        self.output_path.setText("D:/7894/output")
        output_dir_layout.addWidget(self.output_path)
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(lambda: self.browse_directory(self.output_path))
        output_dir_layout.addWidget(browse_output_btn)
        output_layout.addLayout(output_dir_layout)

        project_dir_layout = QHBoxLayout()
        project_dir_layout.addWidget(QLabel("Projects:"))
        self.project_path = QLineEdit()
        self.project_path.setText(str(Path.home() / "Documents/NamePlateProjects"))
        project_dir_layout.addWidget(self.project_path)
        browse_project_btn = QPushButton("Browse...")
        browse_project_btn.clicked.connect(lambda: self.browse_directory(self.project_path))
        project_dir_layout.addWidget(browse_project_btn)
        output_layout.addLayout(project_dir_layout)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # Blender path
        blender_group = QGroupBox("Blender")
        blender_layout = QVBoxLayout()

        blender_path_layout = QHBoxLayout()
        blender_path_layout.addWidget(QLabel("Blender Executable:"))
        self.blender_path = QLineEdit()
        self.blender_path.setPlaceholderText("Auto-detect or specify path")
        blender_path_layout.addWidget(self.blender_path)
        browse_blender_btn = QPushButton("Browse...")
        browse_blender_btn.clicked.connect(lambda: self.browse_file(self.blender_path, "Blender (blender.exe)"))
        blender_path_layout.addWidget(browse_blender_btn)
        blender_layout.addLayout(blender_path_layout)

        blender_group.setLayout(blender_layout)
        layout.addWidget(blender_group)

        layout.addStretch()
        return widget

    def create_preview_tab(self):
        """Create preview settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Preview quality
        quality_group = QGroupBox("Preview Quality")
        quality_layout = QFormLayout()

        self.preview_quality = QComboBox()
        self.preview_quality.addItems(["Low (Fast)", "Medium", "High (Slow)"])
        self.preview_quality.setCurrentIndex(1)
        quality_layout.addRow("Quality:", self.preview_quality)

        self.auto_update_preview = QCheckBox("Auto-update on change")
        self.auto_update_preview.setChecked(True)
        quality_layout.addRow("Auto-update:", self.auto_update_preview)

        self.preview_fps = QSpinBox()
        self.preview_fps.setRange(10, 60)
        self.preview_fps.setValue(30)
        self.preview_fps.setSuffix(" FPS")
        quality_layout.addRow("Max FPS:", self.preview_fps)

        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)

        # View settings
        view_group = QGroupBox("View Settings")
        view_layout = QFormLayout()

        self.default_view = QComboBox()
        self.default_view.addItems(["3D", "Top", "Front", "Side"])
        view_layout.addRow("Default View:", self.default_view)

        self.show_grid = QCheckBox("Show grid")
        self.show_grid.setChecked(True)
        view_layout.addRow("Grid:", self.show_grid)

        self.show_axes = QCheckBox("Show axes")
        view_layout.addRow("Axes:", self.show_axes)

        self.show_dimensions = QCheckBox("Show dimensions")
        self.show_dimensions.setChecked(True)
        view_layout.addRow("Dimensions:", self.show_dimensions)

        view_group.setLayout(view_layout)
        layout.addWidget(view_group)

        layout.addStretch()
        return widget

    def create_export_tab(self):
        """Create export settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Export defaults
        export_group = QGroupBox("Export Defaults")
        export_layout = QFormLayout()

        self.stl_units = QComboBox()
        self.stl_units.addItems(["Millimeters", "Centimeters", "Inches"])
        export_layout.addRow("STL Units:", self.stl_units)

        self.stl_ascii = QCheckBox("ASCII format (larger file)")
        export_layout.addRow("STL Format:", self.stl_ascii)

        self.export_blend = QCheckBox("Also export .blend file")
        self.export_blend.setChecked(True)
        export_layout.addRow("Blend File:", self.export_blend)

        self.auto_open_folder = QCheckBox("Open folder after export")
        export_layout.addRow("Auto-open:", self.auto_open_folder)

        export_group.setLayout(export_layout)
        layout.addWidget(export_group)

        # File naming
        naming_group = QGroupBox("File Naming")
        naming_layout = QFormLayout()

        self.filename_pattern = QLineEdit()
        self.filename_pattern.setText("{project}_{date}_{time}")
        self.filename_pattern.setPlaceholderText("Use {project}, {date}, {time}, {text1}")
        naming_layout.addRow("Pattern:", self.filename_pattern)

        naming_layout.addRow(QLabel("Examples:"))
        naming_layout.addRow("", QLabel("nameplate_20231125_143022.stl"))
        naming_layout.addRow("", QLabel("Kirjasto_Library_v1.stl"))

        naming_group.setLayout(naming_layout)
        layout.addWidget(naming_group)

        layout.addStretch()
        return widget

    def create_advanced_tab(self):
        """Create advanced settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Performance
        perf_group = QGroupBox("Performance")
        perf_layout = QFormLayout()

        self.enable_multithreading = QCheckBox("Use multiple CPU cores")
        self.enable_multithreading.setChecked(True)
        perf_layout.addRow("Multithreading:", self.enable_multithreading)

        self.max_threads = QSpinBox()
        self.max_threads.setRange(1, 16)
        self.max_threads.setValue(4)
        perf_layout.addRow("Max Threads:", self.max_threads)

        self.cache_size = QSpinBox()
        self.cache_size.setRange(50, 1000)
        self.cache_size.setValue(200)
        self.cache_size.setSuffix(" MB")
        perf_layout.addRow("Cache Size:", self.cache_size)

        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)

        # Validation
        validation_group = QGroupBox("Validation")
        validation_layout = QFormLayout()

        self.strict_validation = QCheckBox("Strict validation mode")
        validation_layout.addRow("Mode:", self.strict_validation)

        self.min_printability_score = QSpinBox()
        self.min_printability_score.setRange(0, 100)
        self.min_printability_score.setValue(70)
        validation_layout.addRow("Min Score:", self.min_printability_score)

        validation_group.setLayout(validation_layout)
        layout.addWidget(validation_group)

        # Logging
        logging_group = QGroupBox("Logging")
        logging_layout = QFormLayout()

        self.enable_logging = QCheckBox("Enable detailed logging")
        self.enable_logging.setChecked(True)
        logging_layout.addRow("Logging:", self.enable_logging)

        self.log_level = QComboBox()
        self.log_level.addItems(["Debug", "Info", "Warning", "Error"])
        self.log_level.setCurrentIndex(1)
        logging_layout.addRow("Level:", self.log_level)

        logging_group.setLayout(logging_layout)
        layout.addWidget(logging_group)

        layout.addStretch()
        return widget

    def browse_file(self, line_edit, file_filter):
        """Browse for a file"""
        current = line_edit.text()
        path, _ = QFileDialog.getOpenFileName(
            self, "Select File",
            current if current else str(Path.home()),
            file_filter
        )
        if path:
            line_edit.setText(path)

    def browse_directory(self, line_edit):
        """Browse for a directory"""
        current = line_edit.text()
        path = QFileDialog.getExistingDirectory(
            self, "Select Directory",
            current if current else str(Path.home())
        )
        if path:
            line_edit.setText(path)

    def load_settings(self):
        """Load settings from QSettings"""
        # General
        self.auto_save_check.setChecked(self.settings.value("auto_save", True, bool))
        self.auto_save_interval.setValue(self.settings.value("auto_save_interval", 5, int))
        self.check_updates.setChecked(self.settings.value("check_updates", True, bool))
        self.show_tips.setChecked(self.settings.value("show_tips", True, bool))

        # UI
        theme = self.settings.value("theme", "Dark")
        self.theme_combo.setCurrentText(theme)
        self.show_statusbar.setChecked(self.settings.value("show_statusbar", True, bool))
        self.show_toolbar.setChecked(self.settings.value("show_toolbar", True, bool))

        # Paths
        self.quicksand_path.setText(self.settings.value("quicksand_font_path", "C:/Windows/Fonts/Quicksand-Regular.ttf"))
        self.output_path.setText(self.settings.value("output_path", "D:/7894/output"))
        self.project_path.setText(self.settings.value("project_path", str(Path.home() / "Documents/NamePlateProjects")))
        self.blender_path.setText(self.settings.value("blender_path", ""))

        # Preview
        self.auto_update_preview.setChecked(self.settings.value("auto_update_preview", True, bool))
        self.show_grid.setChecked(self.settings.value("show_grid", True, bool))
        self.show_dimensions.setChecked(self.settings.value("show_dimensions", True, bool))

        # Export
        self.export_blend.setChecked(self.settings.value("export_blend", True, bool))
        self.filename_pattern.setText(self.settings.value("filename_pattern", "{project}_{date}_{time}"))

    def save_settings(self):
        """Save settings to QSettings"""
        # General
        self.settings.setValue("auto_save", self.auto_save_check.isChecked())
        self.settings.setValue("auto_save_interval", self.auto_save_interval.value())
        self.settings.setValue("check_updates", self.check_updates.isChecked())
        self.settings.setValue("show_tips", self.show_tips.isChecked())

        # UI
        self.settings.setValue("theme", self.theme_combo.currentText())
        self.settings.setValue("show_statusbar", self.show_statusbar.isChecked())
        self.settings.setValue("show_toolbar", self.show_toolbar.isChecked())

        # Paths
        self.settings.setValue("quicksand_font_path", self.quicksand_path.text())
        self.settings.setValue("output_path", self.output_path.text())
        self.settings.setValue("project_path", self.project_path.text())
        self.settings.setValue("blender_path", self.blender_path.text())

        # Preview
        self.settings.setValue("auto_update_preview", self.auto_update_preview.isChecked())
        self.settings.setValue("show_grid", self.show_grid.isChecked())
        self.settings.setValue("show_dimensions", self.show_dimensions.isChecked())

        # Export
        self.settings.setValue("export_blend", self.export_blend.isChecked())
        self.settings.setValue("filename_pattern", self.filename_pattern.text())

    def save_and_close(self):
        """Save settings and close"""
        self.save_settings()
        QMessageBox.information(
            self, "Settings Saved",
            "Settings have been saved successfully.\n\n"
            "Some changes may require restarting the application."
        )
        self.accept()

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset to Defaults",
            "Reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.settings.clear()
            self.load_settings()
            QMessageBox.information(self, "Reset Complete", "All settings have been reset to defaults.")
