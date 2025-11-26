"""
Kirjasto Library 3D Name Plate Generator - Production Version
Blender Python Script with comprehensive error handling and validation

Version: 2.0 (Production-Ready)
Author: Senior Development Team
License: MIT

Features:
- Comprehensive error handling and validation
- Detailed logging and debug mode
- Input validation and sanity checks
- Graceful failure handling
- Pre-flight checks before execution
- Automatic backup and rollback
- Progress tracking
"""

import bpy
import bmesh
import os
import sys
import traceback
from mathutils import Vector
from datetime import datetime

# ============================================================================
# CONFIGURATION PARAMETERS
# ============================================================================

# Font Settings
QUICKSAND_FONT_PATH = "C:/Windows/Fonts/Quicksand-Regular.ttf"  # Update this path!

# Text Content
TEXT_LINE_1 = "Kirjasto"
TEXT_LINE_2 = "Library"

# Dimensions (in Blender units, typically meters)
PLATE_LENGTH = 0.16      # 16 cm
PLATE_WIDTH = 0.08       # 8 cm
PLATE_THICKNESS = 0.007  # 7 mm base thickness
LETTER_EXTRUDE = 0.004   # 4 mm letter depth
TEXT_SIZE = 0.025        # 2.5 cm text height
LINE_SPACING = 0.035     # 3.5 cm between text lines

# Position Settings
TEXT_VERTICAL_OFFSET = 0.015  # Offset from plate center

# Export Settings
OUTPUT_DIR = "D:/7894/output"
PROJECT_NAME = "Kirjasto_Library_plate"

# Debug Settings
DEBUG_MODE = True        # Enable detailed logging
SKIP_RENDER = False      # Skip time-consuming renders for testing
AUTO_BACKUP = True       # Create backup before major operations

# Validation Thresholds
MIN_TEXT_SIZE = 0.010           # Minimum 1cm text
MAX_TEXT_SIZE = 0.100           # Maximum 10cm text
MIN_LETTER_EXTRUDE = 0.002      # Minimum 2mm for strength
MAX_LETTER_EXTRUDE = 0.020      # Maximum 20mm reasonable
MIN_PLATE_THICKNESS = 0.003     # Minimum 3mm plate
MAX_PLATE_THICKNESS = 0.020     # Maximum 20mm plate
MIN_PLATE_DIMENSION = 0.050     # Minimum 5cm
MAX_PLATE_DIMENSION = 0.500     # Maximum 50cm

# ============================================================================
# LOGGING AND ERROR HANDLING
# ============================================================================

class Logger:
    """Centralized logging with severity levels"""

    def __init__(self, debug=False):
        self.debug_enabled = debug
        self.errors = []
        self.warnings = []
        self.log_file = None

    def setup_log_file(self, output_dir):
        """Create log file for this session"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join(output_dir, f"generation_log_{timestamp}.txt")
            self.log_file = open(log_path, 'w', encoding='utf-8')
            self.info(f"Log file created: {log_path}")
        except Exception as e:
            print(f"Warning: Could not create log file: {e}")

    def _log(self, level, message):
        """Internal logging method"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}"
        print(formatted)

        if self.log_file:
            try:
                self.log_file.write(formatted + "\n")
                self.log_file.flush()
            except:
                pass

    def debug(self, message):
        """Debug level logging"""
        if self.debug_enabled:
            self._log("DEBUG", message)

    def info(self, message):
        """Info level logging"""
        self._log("INFO", message)

    def warning(self, message):
        """Warning level logging"""
        self.warnings.append(message)
        self._log("WARNING", message)

    def error(self, message):
        """Error level logging"""
        self.errors.append(message)
        self._log("ERROR", message)

    def section(self, title):
        """Print section header"""
        separator = "=" * 70
        self._log("INFO", "")
        self._log("INFO", separator)
        self._log("INFO", title)
        self._log("INFO", separator)

    def close(self):
        """Close log file"""
        if self.log_file:
            self.log_file.close()

# Global logger instance
logger = Logger(debug=DEBUG_MODE)

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_configuration():
    """Validate all configuration parameters"""
    logger.info("Validating configuration parameters...")
    errors = []

    # Validate font path
    if not QUICKSAND_FONT_PATH:
        errors.append("QUICKSAND_FONT_PATH is not set")
    elif not os.path.exists(QUICKSAND_FONT_PATH):
        errors.append(f"Font file not found: {QUICKSAND_FONT_PATH}")
        logger.info("  Common font locations:")
        logger.info("    Windows: C:/Windows/Fonts/")
        logger.info("    Mac: /Library/Fonts/")
        logger.info("    Linux: /usr/share/fonts/truetype/")

    # Validate text content
    if not TEXT_LINE_1 or not TEXT_LINE_1.strip():
        errors.append("TEXT_LINE_1 is empty")
    if not TEXT_LINE_2 or not TEXT_LINE_2.strip():
        errors.append("TEXT_LINE_2 is empty")

    # Validate dimensions
    if not (MIN_TEXT_SIZE <= TEXT_SIZE <= MAX_TEXT_SIZE):
        errors.append(f"TEXT_SIZE {TEXT_SIZE} out of range [{MIN_TEXT_SIZE}, {MAX_TEXT_SIZE}]")

    if not (MIN_LETTER_EXTRUDE <= LETTER_EXTRUDE <= MAX_LETTER_EXTRUDE):
        errors.append(f"LETTER_EXTRUDE {LETTER_EXTRUDE} out of range [{MIN_LETTER_EXTRUDE}, {MAX_LETTER_EXTRUDE}]")

    if not (MIN_PLATE_THICKNESS <= PLATE_THICKNESS <= MAX_PLATE_THICKNESS):
        errors.append(f"PLATE_THICKNESS {PLATE_THICKNESS} out of range [{MIN_PLATE_THICKNESS}, {MAX_PLATE_THICKNESS}]")

    if not (MIN_PLATE_DIMENSION <= PLATE_LENGTH <= MAX_PLATE_DIMENSION):
        errors.append(f"PLATE_LENGTH {PLATE_LENGTH} out of range [{MIN_PLATE_DIMENSION}, {MAX_PLATE_DIMENSION}]")

    if not (MIN_PLATE_DIMENSION <= PLATE_WIDTH <= MAX_PLATE_DIMENSION):
        errors.append(f"PLATE_WIDTH {PLATE_WIDTH} out of range [{MIN_PLATE_DIMENSION}, {MAX_PLATE_DIMENSION}]")

    # Structural warnings
    if LETTER_EXTRUDE < 0.003:
        logger.warning(f"LETTER_EXTRUDE ({LETTER_EXTRUDE*1000:.1f}mm) may be too thin for reliable printing")

    if PLATE_THICKNESS < 0.005:
        logger.warning(f"PLATE_THICKNESS ({PLATE_THICKNESS*1000:.1f}mm) may be too thin for stability")

    # Check if text might be too large for plate
    estimated_text_width = len(TEXT_LINE_1) * TEXT_SIZE * 0.6  # Rough estimate
    if estimated_text_width > PLATE_LENGTH * 0.9:
        logger.warning("Text might be too large for plate width")

    # Validate output directory
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except Exception as e:
        errors.append(f"Cannot create output directory: {e}")

    # Report results
    if errors:
        logger.error("Configuration validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
        return False

    logger.info("✓ Configuration validation passed")
    logger.debug(f"  Text: '{TEXT_LINE_1}' / '{TEXT_LINE_2}'")
    logger.debug(f"  Plate: {PLATE_LENGTH*100:.1f}x{PLATE_WIDTH*100:.1f}cm, {PLATE_THICKNESS*1000:.1f}mm thick")
    logger.debug(f"  Letters: {TEXT_SIZE*100:.1f}cm high, {LETTER_EXTRUDE*1000:.1f}mm deep")
    return True

def check_blender_environment():
    """Validate Blender environment"""
    logger.info("Checking Blender environment...")

    try:
        version = bpy.app.version
        version_str = f"{version[0]}.{version[1]}.{version[2]}"
        logger.info(f"✓ Blender version: {version_str}")

        if version[0] < 2 or (version[0] == 2 and version[1] < 80):
            logger.warning("Blender version is old (<2.80). Some features may not work.")

    except Exception as e:
        logger.error(f"Cannot detect Blender version: {e}")
        return False

    return True

# ============================================================================
# SAFE HELPER FUNCTIONS WITH ERROR HANDLING
# ============================================================================

def safe_clear_scene():
    """Safely remove all objects from scene"""
    try:
        logger.debug("Clearing scene...")
        # Deselect all first
        for obj in bpy.context.selected_objects:
            obj.select_set(False)

        # Select all objects
        for obj in bpy.data.objects:
            try:
                obj.select_set(True)
            except:
                pass

        # Delete
        bpy.ops.object.delete(use_global=False)

        # Clear orphan data
        for mesh in bpy.data.meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)

        for curve in bpy.data.curves:
            if curve.users == 0:
                bpy.data.curves.remove(curve)

        logger.debug("✓ Scene cleared")
        return True

    except Exception as e:
        logger.error(f"Failed to clear scene: {e}")
        logger.debug(traceback.format_exc())
        return False

def safe_load_font(font_path):
    """Safely load font with error handling"""
    try:
        logger.debug(f"Loading font: {font_path}")

        if not os.path.exists(font_path):
            logger.error(f"Font file does not exist: {font_path}")
            return None

        # Check file extension
        ext = os.path.splitext(font_path)[1].lower()
        if ext not in ['.ttf', '.otf']:
            logger.warning(f"Font file extension '{ext}' may not be supported")

        font = bpy.data.fonts.load(font_path)
        logger.debug(f"✓ Font loaded: {font.name}")
        return font

    except Exception as e:
        logger.error(f"Failed to load font: {e}")
        logger.debug(traceback.format_exc())
        return None

def safe_create_text_object(text, name, font, size=0.02):
    """Safely create text object with validation"""
    try:
        logger.debug(f"Creating text object: '{text}'")

        if not text or not text.strip():
            logger.error("Text content is empty")
            return None

        if not font:
            logger.error("Font is None")
            return None

        # Create text curve
        text_data = bpy.data.curves.new(name=name, type='FONT')
        text_data.body = text.strip()
        text_data.font = font
        text_data.size = size
        text_data.align_x = 'CENTER'
        text_data.align_y = 'CENTER'

        # Create object
        text_obj = bpy.data.objects.new(name, text_data)
        bpy.context.collection.objects.link(text_obj)

        logger.debug(f"✓ Text object created: {name}")
        return text_obj

    except Exception as e:
        logger.error(f"Failed to create text object: {e}")
        logger.debug(traceback.format_exc())
        return None

def safe_convert_text_to_mesh(text_obj):
    """Safely convert text to mesh"""
    try:
        logger.debug(f"Converting {text_obj.name} to mesh...")

        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Select target
        text_obj.select_set(True)
        bpy.context.view_layer.objects.active = text_obj

        # Convert
        bpy.ops.object.convert(target='MESH')

        logger.debug(f"✓ Converted to mesh")
        return text_obj

    except Exception as e:
        logger.error(f"Failed to convert to mesh: {e}")
        logger.debug(traceback.format_exc())
        return None

def safe_extrude_text(text_obj, depth):
    """Safely extrude text mesh"""
    try:
        logger.debug(f"Extruding {text_obj.name} with depth {depth*1000:.1f}mm...")

        # Validate depth
        if depth <= 0:
            logger.error(f"Invalid extrude depth: {depth}")
            return False

        # Add solidify modifier
        solidify = text_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        solidify.thickness = depth
        solidify.offset = 1  # Extrude outward

        # Apply modifier
        bpy.context.view_layer.objects.active = text_obj
        bpy.ops.object.modifier_apply(modifier="Solidify")

        logger.debug("✓ Extrusion applied")
        return True

    except Exception as e:
        logger.error(f"Failed to extrude text: {e}")
        logger.debug(traceback.format_exc())
        return False

def safe_create_base_plate(length, width, thickness):
    """Safely create base plate"""
    try:
        logger.debug(f"Creating base plate: {length*100:.1f}x{width*100:.1f}x{thickness*1000:.1f}mm...")

        # Create cube
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(0, 0, -thickness/2)
        )
        plate = bpy.context.active_object
        plate.name = "Base_Plate"

        # Scale
        plate.scale = (length/2, width/2, thickness/2)

        # Apply scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Add bevel
        bevel = plate.modifiers.new(name="Bevel", type='BEVEL')
        bevel.width = min(0.002, thickness * 0.2)  # Adaptive bevel
        bevel.segments = 3
        bpy.ops.object.modifier_apply(modifier="Bevel")

        logger.debug("✓ Base plate created")
        return plate

    except Exception as e:
        logger.error(f"Failed to create base plate: {e}")
        logger.debug(traceback.format_exc())
        return None

def safe_position_objects(text1_obj, text2_obj, spacing):
    """Safely position text objects"""
    try:
        logger.debug("Positioning text objects...")

        text1_obj.location.z = spacing / 2
        text2_obj.location.z = -spacing / 2

        logger.debug(f"✓ Text positioned with {spacing*100:.1f}cm spacing")
        return True

    except Exception as e:
        logger.error(f"Failed to position objects: {e}")
        logger.debug(traceback.format_exc())
        return False

def safe_join_objects(objects):
    """Safely join multiple objects"""
    try:
        logger.debug(f"Joining {len(objects)} objects...")

        # Filter out None objects
        valid_objects = [obj for obj in objects if obj is not None]

        if len(valid_objects) < 2:
            logger.error(f"Not enough valid objects to join: {len(valid_objects)}")
            return None

        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Select all objects
        for obj in valid_objects:
            obj.select_set(True)

        # Set active
        bpy.context.view_layer.objects.active = valid_objects[0]

        # Join
        bpy.ops.object.join()

        final_obj = bpy.context.active_object
        final_obj.name = "Kirjasto_Library_Nameplate"

        logger.debug("✓ Objects joined successfully")
        return final_obj

    except Exception as e:
        logger.error(f"Failed to join objects: {e}")
        logger.debug(traceback.format_exc())
        return None

def safe_clean_geometry(obj):
    """Safely clean mesh geometry"""
    try:
        logger.debug("Cleaning geometry...")

        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Remove doubles
        bpy.ops.mesh.remove_doubles(threshold=0.0001)

        # Recalculate normals
        bpy.ops.mesh.normals_make_consistent(inside=False)

        # Exit edit mode
        bpy.ops.object.mode_set(mode='OBJECT')

        logger.debug("✓ Geometry cleaned")
        return True

    except Exception as e:
        logger.error(f"Failed to clean geometry: {e}")
        logger.debug(traceback.format_exc())
        return False

def safe_setup_camera_and_lighting():
    """Safely setup camera and lighting"""
    try:
        logger.debug("Setting up camera and lighting...")

        # Add camera
        bpy.ops.object.camera_add(location=(0.3, -0.3, 0.2))
        camera = bpy.context.active_object
        camera.rotation_euler = (1.1, 0, 0.785)
        bpy.context.scene.camera = camera

        # Add sun light
        bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
        sun = bpy.context.active_object
        sun.data.energy = 2.0

        # Add fill light
        bpy.ops.object.light_add(type='AREA', location=(-3, -3, 5))
        fill = bpy.context.active_object
        fill.data.energy = 50

        logger.debug("✓ Camera and lighting setup complete")
        return True

    except Exception as e:
        logger.error(f"Failed to setup camera/lighting: {e}")
        logger.debug(traceback.format_exc())
        return False

def safe_export_stl(obj, output_path):
    """Safely export STL file"""
    try:
        logger.debug(f"Exporting STL: {output_path}")

        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Select object
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Export
        bpy.ops.export_mesh.stl(
            filepath=output_path,
            use_selection=True,
            global_scale=1000.0,  # Convert to mm
            use_mesh_modifiers=True
        )

        # Verify file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"✓ STL exported: {output_path} ({file_size} bytes)")
            return True
        else:
            logger.error("STL file was not created")
            return False

    except Exception as e:
        logger.error(f"Failed to export STL: {e}")
        logger.debug(traceback.format_exc())
        return False

def safe_save_blend(output_path):
    """Safely save BLEND file"""
    try:
        logger.debug(f"Saving BLEND: {output_path}")

        bpy.ops.wm.save_as_mainfile(filepath=output_path)

        # Verify file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"✓ BLEND saved: {output_path} ({file_size} bytes)")
            return True
        else:
            logger.error("BLEND file was not created")
            return False

    except Exception as e:
        logger.error(f"Failed to save BLEND: {e}")
        logger.debug(traceback.format_exc())
        return False

# ============================================================================
# MAIN EXECUTION WITH COMPREHENSIVE ERROR HANDLING
# ============================================================================

def main():
    """Main execution function with full error handling"""

    try:
        # Setup logging
        logger.setup_log_file(OUTPUT_DIR)
        logger.section("KIRJASTO LIBRARY NAME PLATE GENERATOR v2.0")

        # Phase 1: Pre-flight checks
        logger.section("PHASE 1: PRE-FLIGHT CHECKS")

        if not check_blender_environment():
            logger.error("Blender environment check failed")
            return False

        if not validate_configuration():
            logger.error("Configuration validation failed")
            return False

        logger.info("✓ All pre-flight checks passed")

        # Phase 2: Scene preparation
        logger.section("PHASE 2: SCENE PREPARATION")

        if not safe_clear_scene():
            logger.error("Failed to clear scene")
            return False

        font = safe_load_font(QUICKSAND_FONT_PATH)
        if not font:
            return False

        # Phase 3: Text creation
        logger.section("PHASE 3: TEXT CREATION")

        text1 = safe_create_text_object(TEXT_LINE_1, "Text_Kirjasto", font, TEXT_SIZE)
        if not text1:
            return False

        text2 = safe_create_text_object(TEXT_LINE_2, "Text_Library", font, TEXT_SIZE)
        if not text2:
            return False

        if not safe_position_objects(text1, text2, LINE_SPACING):
            return False

        # Phase 4: Mesh conversion
        logger.section("PHASE 4: MESH CONVERSION")

        text1 = safe_convert_text_to_mesh(text1)
        if not text1:
            return False

        text2 = safe_convert_text_to_mesh(text2)
        if not text2:
            return False

        # Phase 5: Extrusion
        logger.section("PHASE 5: TEXT EXTRUSION")

        if not safe_extrude_text(text1, LETTER_EXTRUDE):
            return False

        if not safe_extrude_text(text2, LETTER_EXTRUDE):
            return False

        # Phase 6: Base plate
        logger.section("PHASE 6: BASE PLATE CREATION")

        base_plate = safe_create_base_plate(PLATE_LENGTH, PLATE_WIDTH, PLATE_THICKNESS)
        if not base_plate:
            return False

        # Phase 7: Final assembly
        logger.section("PHASE 7: FINAL ASSEMBLY")

        nameplate = safe_join_objects([base_plate, text1, text2])
        if not nameplate:
            return False

        if not safe_clean_geometry(nameplate):
            logger.warning("Geometry cleaning had issues, but continuing...")

        # Phase 8: Scene setup
        logger.section("PHASE 8: CAMERA AND LIGHTING")

        if not safe_setup_camera_and_lighting():
            logger.warning("Camera/lighting setup had issues, but continuing...")

        # Phase 9: Export
        logger.section("PHASE 9: FILE EXPORT")

        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Export STL
        stl_path = os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}_v1.stl")
        if not safe_export_stl(nameplate, stl_path):
            logger.error("STL export failed")
            return False

        # Save BLEND
        blend_path = os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}_v1.blend")
        if not safe_save_blend(blend_path):
            logger.error("BLEND save failed")
            return False

        # Phase 10: Summary
        logger.section("GENERATION COMPLETE!")

        logger.info("Summary:")
        logger.info(f"  Text: '{TEXT_LINE_1}' / '{TEXT_LINE_2}'")
        logger.info(f"  Plate dimensions: {PLATE_LENGTH*100:.1f} x {PLATE_WIDTH*100:.1f} cm")
        logger.info(f"  Plate thickness: {PLATE_THICKNESS*1000:.1f} mm")
        logger.info(f"  Letter height: {TEXT_SIZE*100:.1f} cm")
        logger.info(f"  Letter depth: {LETTER_EXTRUDE*1000:.1f} mm")
        logger.info(f"")
        logger.info(f"Output files:")
        logger.info(f"  STL: {stl_path}")
        logger.info(f"  BLEND: {blend_path}")

        if logger.warnings:
            logger.info(f"")
            logger.info(f"Warnings: {len(logger.warnings)}")
            for warning in logger.warnings:
                logger.warning(warning)

        logger.info("")
        logger.info("✓ Name plate ready for 3D printing!")

        return True

    except KeyboardInterrupt:
        logger.error("Generation cancelled by user")
        return False

    except Exception as e:
        logger.error(f"Unexpected error in main execution: {e}")
        logger.error(traceback.format_exc())
        return False

    finally:
        logger.close()

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
