"""
NamePlate Studio Pro - Main Entry Point
Professional 3D Name Plate Generator Application
"""

import sys
import os
from pathlib import Path

# Ensure the src directory is in the Python path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing = []

    try:
        from PyQt6 import QtWidgets, QtCore, QtGui
    except ImportError:
        missing.append("PyQt6")

    try:
        import matplotlib
    except ImportError:
        missing.append("matplotlib")

    try:
        import qrcode
    except ImportError:
        missing.append("qrcode")

    if missing:
        print("=" * 60)
        print("MISSING DEPENDENCIES")
        print("=" * 60)
        print("\nThe following required packages are not installed:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nPlease install them using:")
        print(f"  pip install -r requirements.txt")
        print("\nOr install individually:")
        for pkg in missing:
            print(f"  pip install {pkg}")
        print("=" * 60)
        return False
    return True

def main():
    """Main application entry point"""

    # Check dependencies first
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return 1

    # Import after dependency check
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from gui.main_window import MainWindow

    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("NamePlate Studio Pro")
    app.setOrganizationName("NamePlate Studio")
    app.setApplicationVersion("1.0.0")

    # Set application style
    app.setStyle("Fusion")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run application
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
