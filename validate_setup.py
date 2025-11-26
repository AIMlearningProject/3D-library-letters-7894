"""
Pre-Flight Validation Script for Kirjasto Name Plate Generator
Validates configuration and environment before running generation

Usage:
    python validate_setup.py

Or from Blender:
    blender --background --python validate_setup.py
"""

import os
import sys

# ============================================================================
# CONFIGURATION - Copy from your generator script
# ============================================================================

QUICKSAND_FONT_PATH = "C:/Windows/Fonts/Quicksand-Regular.ttf"
TEXT_LINE_1 = "Kirjasto"
TEXT_LINE_2 = "Library"
PLATE_LENGTH = 0.16
PLATE_WIDTH = 0.08
PLATE_THICKNESS = 0.007
LETTER_EXTRUDE = 0.004
TEXT_SIZE = 0.025
LINE_SPACING = 0.035
OUTPUT_DIR = "D:/7894/output"
PROJECT_NAME = "Kirjasto_Library_plate"

# Validation thresholds
MIN_TEXT_SIZE = 0.010
MAX_TEXT_SIZE = 0.100
MIN_LETTER_EXTRUDE = 0.002
MAX_LETTER_EXTRUDE = 0.020
MIN_PLATE_THICKNESS = 0.003
MAX_PLATE_THICKNESS = 0.020
MIN_PLATE_DIMENSION = 0.050
MAX_PLATE_DIMENSION = 0.500

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

class ValidationReport:
    """Track validation results"""
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.passed = 0
        self.failed = 0

    def error(self, msg):
        self.errors.append(msg)
        self.failed += 1

    def warning(self, msg):
        self.warnings.append(msg)

    def success(self, msg):
        self.info.append(msg)
        self.passed += 1

    def print_report(self):
        """Print final validation report"""
        print("\n" + "="*70)
        print("VALIDATION REPORT")
        print("="*70)

        print(f"\n[PASS] Passed: {self.passed}")
        print(f"[FAIL] Failed: {self.failed}")
        print(f"[WARN] Warnings: {len(self.warnings)}")

        if self.errors:
            print("\n" + "="*70)
            print("ERRORS (Must fix before running generator):")
            print("="*70)
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. {error}")

        if self.warnings:
            print("\n" + "="*70)
            print("WARNINGS (Recommended to review):")
            print("="*70)
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i}. {warning}")

        if not self.errors:
            print("\n" + "="*70)
            print("[PASS] VALIDATION PASSED")
            print("="*70)
            print("You can safely run the generator script.")
        else:
            print("\n" + "="*70)
            print("[FAIL] VALIDATION FAILED")
            print("="*70)
            print("Please fix the errors above before running the generator.")

        print()
        return len(self.errors) == 0

def validate_python_environment(report):
    """Validate Python environment"""
    print("\n[1/9] Checking Python environment...")

    try:
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        print(f"  Python version: {version_str}")

        if version.major < 3:
            report.error(f"Python 3.x required, found {version.major}.{version.minor}")
        else:
            report.success("Python version OK")

    except Exception as e:
        report.error(f"Cannot detect Python version: {e}")

def validate_blender_available(report):
    """Check if Blender Python API is available"""
    print("\n[2/9] Checking Blender availability...")

    try:
        import bpy
        version = bpy.app.version
        version_str = f"{version[0]}.{version[1]}.{version[2]}"
        print(f"  Blender version: {version_str}")

        if version[0] < 2 or (version[0] == 2 and version[1] < 80):
            report.warning(f"Blender {version_str} is old. Recommended: 3.0 or higher")
        else:
            report.success("Blender version OK")

        return True

    except ImportError:
        print("  Blender Python API not available")
        print("  Note: This is normal if running standalone Python")
        print("  The script will work when run from Blender")
        report.warning("Cannot verify Blender - run this script from Blender for full validation")
        return False

def validate_font_file(report):
    """Validate font file exists and is accessible"""
    print("\n[3/9] Checking font file...")

    if not QUICKSAND_FONT_PATH:
        report.error("QUICKSAND_FONT_PATH is not set")
        return

    print(f"  Font path: {QUICKSAND_FONT_PATH}")

    if not os.path.exists(QUICKSAND_FONT_PATH):
        report.error(f"Font file not found: {QUICKSAND_FONT_PATH}")
        print("\n  Common font locations:")
        print("    Windows: C:/Windows/Fonts/")
        print("    Mac: /Library/Fonts/")
        print("    Linux: /usr/share/fonts/truetype/")
        print("\n  To find Quicksand font:")
        print("    1. Download from https://fonts.google.com/specimen/Quicksand")
        print("    2. Install the font on your system")
        print("    3. Update QUICKSAND_FONT_PATH in the script")
        return

    # Check file extension
    ext = os.path.splitext(QUICKSAND_FONT_PATH)[1].lower()
    if ext not in ['.ttf', '.otf']:
        report.warning(f"Font extension '{ext}' may not be supported (expected .ttf or .otf)")

    # Check file size
    try:
        file_size = os.path.getsize(QUICKSAND_FONT_PATH)
        if file_size < 1000:
            report.warning(f"Font file seems unusually small ({file_size} bytes)")
        else:
            print(f"  Font file size: {file_size:,} bytes")
            report.success("Font file found and accessible")
    except Exception as e:
        report.error(f"Cannot read font file: {e}")

def validate_text_content(report):
    """Validate text content"""
    print("\n[4/9] Checking text content...")

    if not TEXT_LINE_1 or not TEXT_LINE_1.strip():
        report.error("TEXT_LINE_1 is empty")
    else:
        print(f"  Line 1: '{TEXT_LINE_1}'")
        if len(TEXT_LINE_1) > 20:
            report.warning(f"TEXT_LINE_1 is long ({len(TEXT_LINE_1)} chars) - may not fit on plate")

    if not TEXT_LINE_2 or not TEXT_LINE_2.strip():
        report.error("TEXT_LINE_2 is empty")
    else:
        print(f"  Line 2: '{TEXT_LINE_2}'")
        if len(TEXT_LINE_2) > 20:
            report.warning(f"TEXT_LINE_2 is long ({len(TEXT_LINE_2)} chars) - may not fit on plate")

    if TEXT_LINE_1 and TEXT_LINE_2:
        report.success("Text content is valid")

def validate_dimensions(report):
    """Validate all dimensions"""
    print("\n[5/9] Checking dimensions...")

    # Text size
    if not (MIN_TEXT_SIZE <= TEXT_SIZE <= MAX_TEXT_SIZE):
        report.error(f"TEXT_SIZE {TEXT_SIZE} out of range [{MIN_TEXT_SIZE}, {MAX_TEXT_SIZE}]")
    else:
        print(f"  [OK] Text size: {TEXT_SIZE*100:.1f} cm")

    # Letter extrude
    if not (MIN_LETTER_EXTRUDE <= LETTER_EXTRUDE <= MAX_LETTER_EXTRUDE):
        report.error(f"LETTER_EXTRUDE {LETTER_EXTRUDE} out of range [{MIN_LETTER_EXTRUDE}, {MAX_LETTER_EXTRUDE}]")
    else:
        print(f"  [OK] Letter depth: {LETTER_EXTRUDE*1000:.1f} mm")
        if LETTER_EXTRUDE < 0.003:
            report.warning(f"Letter depth ({LETTER_EXTRUDE*1000:.1f}mm) may be too thin for reliable printing (recommended: >=3mm)")

    # Plate thickness
    if not (MIN_PLATE_THICKNESS <= PLATE_THICKNESS <= MAX_PLATE_THICKNESS):
        report.error(f"PLATE_THICKNESS {PLATE_THICKNESS} out of range [{MIN_PLATE_THICKNESS}, {MAX_PLATE_THICKNESS}]")
    else:
        print(f"  [OK]Plate thickness: {PLATE_THICKNESS*1000:.1f} mm")
        if PLATE_THICKNESS < 0.005:
            report.warning(f"Plate thickness ({PLATE_THICKNESS*1000:.1f}mm) may be too thin (recommended: >=5mm)")

    # Plate length
    if not (MIN_PLATE_DIMENSION <= PLATE_LENGTH <= MAX_PLATE_DIMENSION):
        report.error(f"PLATE_LENGTH {PLATE_LENGTH} out of range [{MIN_PLATE_DIMENSION}, {MAX_PLATE_DIMENSION}]")
    else:
        print(f"  [OK]Plate length: {PLATE_LENGTH*100:.1f} cm")

    # Plate width
    if not (MIN_PLATE_DIMENSION <= PLATE_WIDTH <= MAX_PLATE_DIMENSION):
        report.error(f"PLATE_WIDTH {PLATE_WIDTH} out of range [{MIN_PLATE_DIMENSION}, {MAX_PLATE_DIMENSION}]")
    else:
        print(f"  [OK]Plate width: {PLATE_WIDTH*100:.1f} cm")

    if report.failed == 0:
        report.success("All dimensions are valid")

def validate_proportions(report):
    """Validate proportions and relationships"""
    print("\n[6/9] Checking proportions...")

    # Check if text might overflow plate
    estimated_text_width = max(len(TEXT_LINE_1), len(TEXT_LINE_2)) * TEXT_SIZE * 0.6
    if estimated_text_width > PLATE_LENGTH * 0.9:
        report.warning(f"Text might be too wide for plate (estimated {estimated_text_width*100:.1f}cm vs plate {PLATE_LENGTH*100:.1f}cm)")
    else:
        print(f"  [OK]Text width OK (estimated {estimated_text_width*100:.1f}cm fits in {PLATE_LENGTH*100:.1f}cm)")

    # Check text height vs plate width
    total_text_height = TEXT_SIZE * 2 + LINE_SPACING
    if total_text_height > PLATE_WIDTH * 0.9:
        report.warning(f"Text height might exceed plate width (estimated {total_text_height*100:.1f}cm vs plate {PLATE_WIDTH*100:.1f}cm)")
    else:
        print(f"  [OK]Text height OK (estimated {total_text_height*100:.1f}cm fits in {PLATE_WIDTH*100:.1f}cm)")

    # Check aspect ratio
    aspect_ratio = PLATE_LENGTH / PLATE_WIDTH
    if aspect_ratio < 1.5 or aspect_ratio > 3.0:
        report.warning(f"Unusual plate aspect ratio: {aspect_ratio:.1f}:1")
    else:
        print(f"  [OK]Plate aspect ratio OK: {aspect_ratio:.1f}:1")

    report.success("Proportions checked")

def validate_output_directory(report):
    """Validate output directory"""
    print("\n[7/9] Checking output directory...")

    print(f"  Output directory: {OUTPUT_DIR}")

    try:
        # Try to create directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        report.success("Output directory is accessible")

        # Check write permissions
        test_file = os.path.join(OUTPUT_DIR, ".test_write")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("  [OK]Write permissions OK")
        except Exception as e:
            report.error(f"Cannot write to output directory: {e}")

        # Check available space
        if sys.platform == 'win32':
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(OUTPUT_DIR),
                None,
                None,
                ctypes.pointer(free_bytes)
            )
            free_mb = free_bytes.value / 1024 / 1024
            print(f"  Available space: {free_mb:.0f} MB")
            if free_mb < 10:
                report.warning(f"Low disk space: {free_mb:.0f} MB available")

    except Exception as e:
        report.error(f"Cannot access output directory: {e}")

def validate_project_name(report):
    """Validate project name"""
    print("\n[8/9] Checking project name...")

    if not PROJECT_NAME or not PROJECT_NAME.strip():
        report.error("PROJECT_NAME is empty")
        return

    print(f"  Project name: {PROJECT_NAME}")

    # Check for invalid characters
    invalid_chars = '<>:"|?*'
    for char in invalid_chars:
        if char in PROJECT_NAME:
            report.error(f"PROJECT_NAME contains invalid character: '{char}'")

    if len(PROJECT_NAME) > 100:
        report.warning("PROJECT_NAME is very long (>100 chars)")

    if report.failed == 0:
        report.success("Project name is valid")

        # Show expected output files
        print(f"\n  Expected output files:")
        print(f"    - {PROJECT_NAME}_v1.stl")
        print(f"    - {PROJECT_NAME}_v1.blend")

def print_3d_printing_tips(report):
    """Print 3D printing recommendations"""
    print("\n[9/9] 3D Printing recommendations...")

    print(f"\n  Total plate dimensions: {PLATE_LENGTH*100:.1f} x {PLATE_WIDTH*100:.1f} x {(PLATE_THICKNESS + LETTER_EXTRUDE)*1000:.1f}mm")
    print(f"    Base: {PLATE_LENGTH*100:.1f} x {PLATE_WIDTH*100:.1f} x {PLATE_THICKNESS*1000:.1f}mm")
    print(f"    Letters: {LETTER_EXTRUDE*1000:.1f}mm raised")

    # Estimate print time (very rough)
    volume_cm3 = (PLATE_LENGTH * PLATE_WIDTH * PLATE_THICKNESS +
                  TEXT_SIZE * TEXT_SIZE * LETTER_EXTRUDE * len(TEXT_LINE_1 + TEXT_LINE_2) * 0.5) * 1000000
    print(f"\n  Estimated volume: {volume_cm3:.1f} cm³")

    # Printing tips
    print("\n  Recommended slicer settings:")
    print("    - Layer height: 0.2mm (or 0.1mm for better quality)")
    print("    - Infill: 20-40%")
    print("    - Supports: Not needed (flat base)")
    print("    - Material: PLA or PETG")
    print("    - Bed adhesion: Brim recommended")
    print("    - Print orientation: Base flat on bed")

    # Warnings based on dimensions
    if LETTER_EXTRUDE < 0.003:
        print("\n  [!] WARNING: Letter depth is below recommended 3mm")
        print("    - Letters may be fragile")
        print("    - Consider increasing LETTER_EXTRUDE to 0.004 or higher")

    if PLATE_THICKNESS < 0.005:
        print("\n  [!] WARNING: Plate thickness is below recommended 5mm")
        print("    - Plate may warp during printing")
        print("    - Consider increasing PLATE_THICKNESS to 0.006 or higher")

    report.success("Ready for 3D printing")

# ============================================================================
# MAIN VALIDATION
# ============================================================================

def main():
    """Run all validations"""
    print("="*70)
    print("KIRJASTO NAME PLATE GENERATOR - PRE-FLIGHT VALIDATION")
    print("="*70)

    report = ValidationReport()

    try:
        validate_python_environment(report)
        validate_blender_available(report)
        validate_font_file(report)
        validate_text_content(report)
        validate_dimensions(report)
        validate_proportions(report)
        validate_output_directory(report)
        validate_project_name(report)
        print_3d_printing_tips(report)

        # Print final report
        success = report.print_report()

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\nValidation cancelled by user")
        return 1

    except Exception as e:
        print(f"\n\nValidation failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
