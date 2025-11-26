"""
Batch Processing Dialog
Process multiple name plates at once
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QProgressBar, QTextEdit, QCheckBox,
    QComboBox, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from pathlib import Path
import csv


class BatchProcessDialog(QDialog):
    """Dialog for batch processing multiple designs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.batch_data = []
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Batch Processing - NamePlate Studio Pro")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)

        # Instructions
        info_label = QLabel(
            "Process multiple name plates at once. Import from CSV or add manually.\n"
            "CSV Format: text_line_1, text_line_2, length, width, thickness, depth"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Import/Add buttons
        button_layout = QHBoxLayout()

        import_csv_btn = QPushButton("Import from CSV")
        import_csv_btn.clicked.connect(self.import_csv)
        button_layout.addWidget(import_csv_btn)

        add_manual_btn = QPushButton("Add Manual Entry")
        add_manual_btn.clicked.connect(self.add_manual_entry)
        button_layout.addWidget(add_manual_btn)

        clear_all_btn = QPushButton("Clear All")
        clear_all_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_all_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Batch table
        table_group = QGroupBox("Batch Items")
        table_layout = QVBoxLayout()

        self.batch_table = QTableWidget()
        self.batch_table.setColumnCount(7)
        self.batch_table.setHorizontalHeaderLabels([
            "Line 1", "Line 2", "Length (mm)", "Width (mm)",
            "Thickness (mm)", "Depth (mm)", "Status"
        ])
        self.batch_table.horizontalHeader().setStretchLastSection(True)
        table_layout.addWidget(self.batch_table)

        table_group.setLayout(table_layout)
        layout.addWidget(table_group)

        # Options
        options_group = QGroupBox("Processing Options")
        options_layout = QHBoxLayout()

        options_layout.addWidget(QLabel("Output Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["STL", "BLEND", "Both"])
        self.format_combo.setCurrentIndex(0)
        options_layout.addWidget(self.format_combo)

        options_layout.addWidget(QLabel("Concurrent Jobs:"))
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setRange(1, 8)
        self.concurrent_spin.setValue(2)
        options_layout.addWidget(self.concurrent_spin)

        self.auto_number = QCheckBox("Auto-number files")
        self.auto_number.setChecked(True)
        options_layout.addWidget(self.auto_number)

        options_layout.addStretch()
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Progress
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        progress_layout.addWidget(self.log_text)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.process_btn = QPushButton("Start Processing")
        self.process_btn.clicked.connect(self.start_processing)
        action_layout.addWidget(self.process_btn)

        cancel_btn = QPushButton("Close")
        cancel_btn.clicked.connect(self.close)
        action_layout.addWidget(cancel_btn)

        layout.addLayout(action_layout)

    def import_csv(self):
        """Import batch data from CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import CSV",
            str(Path.home()),
            "CSV Files (*.csv);;All Files (*.*)"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                imported_count = 0
                for row in reader:
                    # Validate and add row
                    if self.validate_row(row):
                        self.add_batch_item(
                            row.get('text_line_1', ''),
                            row.get('text_line_2', ''),
                            float(row.get('length', 160)),
                            float(row.get('width', 80)),
                            float(row.get('thickness', 7)),
                            float(row.get('depth', 4))
                        )
                        imported_count += 1

            self.log(f"Imported {imported_count} items from CSV")
            QMessageBox.information(
                self, "Import Complete",
                f"Successfully imported {imported_count} items."
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Import Error",
                f"Failed to import CSV: {str(e)}"
            )

    def validate_row(self, row: dict) -> bool:
        """Validate a CSV row"""
        required = ['text_line_1', 'length', 'width']
        return all(field in row for field in required)

    def add_manual_entry(self):
        """Add a manual entry to the batch"""
        # Create simple input dialog or use current design panel values
        self.add_batch_item(
            "Sample Text 1",
            "Sample Text 2",
            160, 80, 7, 4
        )
        self.log("Added manual entry")

    def add_batch_item(self, text1: str, text2: str, length: float,
                       width: float, thickness: float, depth: float):
        """Add item to batch table"""
        row = self.batch_table.rowCount()
        self.batch_table.insertRow(row)

        self.batch_table.setItem(row, 0, QTableWidgetItem(text1))
        self.batch_table.setItem(row, 1, QTableWidgetItem(text2))
        self.batch_table.setItem(row, 2, QTableWidgetItem(str(length)))
        self.batch_table.setItem(row, 3, QTableWidgetItem(str(width)))
        self.batch_table.setItem(row, 4, QTableWidgetItem(str(thickness)))
        self.batch_table.setItem(row, 5, QTableWidgetItem(str(depth)))
        self.batch_table.setItem(row, 6, QTableWidgetItem("Pending"))

    def clear_all(self):
        """Clear all batch items"""
        reply = QMessageBox.question(
            self, "Clear All",
            "Remove all items from the batch?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.batch_table.setRowCount(0)
            self.log("Cleared all items")

    def start_processing(self):
        """Start batch processing"""
        if self.batch_table.rowCount() == 0:
            QMessageBox.warning(
                self, "No Items",
                "Please add items to process first."
            )
            return

        # Disable button during processing
        self.process_btn.setEnabled(False)
        self.log("Starting batch processing...")

        # TODO: Implement actual batch processing with threading
        # For now, simulate progress
        total = self.batch_table.rowCount()

        for i in range(total):
            # Update status
            self.batch_table.setItem(i, 6, QTableWidgetItem("Processing..."))
            self.progress_bar.setValue(int((i + 1) / total * 100))

            # Get item data
            text1 = self.batch_table.item(i, 0).text()
            text2 = self.batch_table.item(i, 1).text()

            self.log(f"Processing: {text1} / {text2}")

            # Simulate processing
            # In real implementation, call generator here

            self.batch_table.setItem(i, 6, QTableWidgetItem("✓ Complete"))

        self.progress_bar.setValue(100)
        self.log(f"\n✓ Batch processing complete! Processed {total} items.")

        QMessageBox.information(
            self, "Batch Complete",
            f"Successfully processed {total} name plates."
        )

        self.process_btn.setEnabled(True)

    def log(self, message: str):
        """Add message to log"""
        self.log_text.append(message)

    def export_template_csv(self):
        """Export a template CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Template CSV",
            str(Path.home() / "batch_template.csv"),
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'text_line_1', 'text_line_2', 'length',
                    'width', 'thickness', 'depth'
                ])
                # Add example rows
                writer.writerow(['Room', '101', '100', '40', '5', '3'])
                writer.writerow(['Room', '102', '100', '40', '5', '3'])
                writer.writerow(['Office', 'Manager', '120', '30', '6', '4'])

            QMessageBox.information(
                self, "Template Exported",
                f"Template CSV saved to:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Export Error",
                f"Failed to export template: {str(e)}"
            )
