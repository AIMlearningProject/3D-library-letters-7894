"""
Test all imports to diagnose issues
"""

import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")
print()

# Test PyQt6
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QAction
    print("[OK] PyQt6 imports successful")
except ImportError as e:
    print(f"[FAIL] PyQt6 import failed: {e}")
    sys.exit(1)

# Test matplotlib
try:
    import matplotlib
    print("[OK] matplotlib imports successful")
except ImportError as e:
    print(f"[FAIL] matplotlib import failed: {e}")

# Test qrcode
try:
    import qrcode
    print("[OK] qrcode imports successful")
except ImportError as e:
    print(f"[FAIL] qrcode import failed: {e}")

# Test our modules
print()
print("Testing custom modules...")

sys.path.insert(0, 'src')

try:
    from gui.design_panel import DesignPanel
    print("[OK] design_panel import successful")
except Exception as e:
    print(f"[FAIL] design_panel import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from gui.preview_panel import PreviewPanel
    print("[OK] preview_panel import successful")
except Exception as e:
    print(f"[FAIL] preview_panel import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from gui.template_panel import TemplatePanel
    print("[OK] template_panel import successful")
except Exception as e:
    print(f"[FAIL] template_panel import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from gui.main_window import MainWindow
    print("[OK] main_window import successful")
except Exception as e:
    print(f"[FAIL] main_window import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from core.generator import NamePlateGenerator
    print("[OK] generator import successful")
except Exception as e:
    print(f"[FAIL] generator import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from core.template_manager import TemplateManager
    print("[OK] template_manager import successful")
except Exception as e:
    print(f"[FAIL] template_manager import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from core.validator import DesignValidator
    print("[OK] validator import successful")
except Exception as e:
    print(f"[FAIL] validator import failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("[SUCCESS] All imports successful! Ready to launch GUI.")
print()
print("To launch the application, run:")
print("  python launch_gui.py")
