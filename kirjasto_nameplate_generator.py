"""
Kirjasto Library 3D Name Plate Generator
Blender Python Script for automating name plate creation

Usage:
1. Open Blender
2. Go to Scripting tab
3. Open this script
4. Update the QUICKSAND_FONT_PATH to your font location
5. Adjust configuration parameters as needed
6. Run the script (Alt+P or click Run Script button)

Requirements:
- Blender 2.8 or higher
- Quicksand font file (.ttf or .otf)
"""

import bpy
import bmesh
import os
from mathutils import Vector

# ============================================================================
# CONFIGURATION PARAMETERS
# ============================================================================

# Font Settings
QUICKSAND_FONT_PATH = "C:/Windows/Fonts/Quicksand-Regular.ttf"  # Update this path!

# Text Content
TEXT_LINE_1 = "Kirjasto"
TEXT_LINE_2 = "Library"

# Dimensions (in Blender units, typically meters - scale as needed)
PLATE_LENGTH = 0.16  # 16 cm
PLATE_WIDTH = 0.08   # 8 cm
PLATE_THICKNESS = 0.007  # 7 mm base thickness
LETTER_EXTRUDE = 0.004   # 4 mm letter depth
TEXT_SIZE = 0.025        # 2.5 cm text height
LINE_SPACING = 0.035     # 3.5 cm between text lines

# Position Settings
TEXT_VERTICAL_OFFSET = 0.015  # Offset from plate center

# Export Settings
OUTPUT_DIR = "D:/7894/output"  # Output directory for files
PROJECT_NAME = "Kirjasto_Library_plate"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clear_scene():
    """Remove all default objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def load_font(font_path):
    """Load the Quicksand font"""
    if not os.path.exists(font_path):
        print(f"ERROR: Font file not found at {font_path}")
        print("Please update QUICKSAND_FONT_PATH in the script")
        return None

    try:
        font = bpy.data.fonts.load(font_path)
        print(f"Successfully loaded font: {font_path}")
        return font
    except Exception as e:
        print(f"ERROR loading font: {e}")
        return None

def create_text_object(text, name, font, size=0.02):
    """Create a text object with specified parameters"""
    # Create text curve
    text_data = bpy.data.curves.new(name=name, type='FONT')
    text_data.body = text
    text_data.font = font
    text_data.size = size
    text_data.align_x = 'CENTER'
    text_data.align_y = 'CENTER'

    # Create object from curve
    text_obj = bpy.data.objects.new(name, text_data)
    bpy.context.collection.objects.link(text_obj)

    return text_obj

def convert_text_to_mesh(text_obj):
    """Convert text curve to mesh"""
    # Select and convert
    bpy.context.view_layer.objects.active = text_obj
    text_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    print(f"Converted {text_obj.name} to mesh")
    return text_obj

def extrude_text(text_obj, depth):
    """Extrude the text mesh to give it depth"""
    # Add solidify modifier
    solidify = text_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = depth
    solidify.offset = 1  # Extrude outward

    # Apply modifier
    bpy.context.view_layer.objects.active = text_obj
    bpy.ops.object.modifier_apply(modifier="Solidify")
    print(f"Extruded {text_obj.name} with depth {depth}")

def create_base_plate(length, width, thickness):
    """Create the base plate for the name plate"""
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, -thickness/2)
    )
    plate = bpy.context.active_object
    plate.name = "Base_Plate"

    # Scale to correct dimensions
    plate.scale = (length/2, width/2, thickness/2)

    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Add bevel for rounded edges (optional, makes it look nicer)
    bevel = plate.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.002  # 2mm bevel
    bevel.segments = 3
    bpy.ops.object.modifier_apply(modifier="Bevel")

    print(f"Created base plate: {length}x{width}x{thickness}")
    return plate

def position_text_objects(text1_obj, text2_obj, spacing):
    """Position two text objects vertically with specified spacing"""
    # Position first line (Kirjasto) above center
    text1_obj.location.z = spacing / 2

    # Position second line (Library) below center
    text2_obj.location.z = -spacing / 2

    print(f"Positioned text objects with {spacing} spacing")

def join_objects(objects):
    """Join multiple objects into one"""
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects to join
    for obj in objects:
        obj.select_set(True)

    # Set active object
    bpy.context.view_layer.objects.active = objects[0]

    # Join
    bpy.ops.object.join()

    final_obj = bpy.context.active_object
    final_obj.name = "Kirjasto_Library_Nameplate"

    print("Joined all objects into final nameplate")
    return final_obj

def clean_geometry(obj):
    """Clean up the mesh geometry"""
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

    print("Cleaned geometry")

def setup_camera_and_lighting():
    """Setup camera and lighting for preview renders"""
    # Add camera
    bpy.ops.object.camera_add(location=(0.3, -0.3, 0.2))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)  # 45-degree angle
    bpy.context.scene.camera = camera

    # Add sun light
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 2.0

    # Add fill light
    bpy.ops.object.light_add(type='AREA', location=(-3, -3, 5))
    fill = bpy.context.active_object
    fill.data.energy = 50

    print("Setup camera and lighting")

def export_files(obj, output_dir, project_name):
    """Export STL and BLEND files"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Select only the nameplate object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Export STL
    stl_path = os.path.join(output_dir, f"{project_name}_v1.stl")
    bpy.ops.export_mesh.stl(
        filepath=stl_path,
        use_selection=True,
        global_scale=1000.0,  # Convert to mm for 3D printing
        use_mesh_modifiers=True
    )
    print(f"Exported STL: {stl_path}")

    # Save BLEND file
    blend_path = os.path.join(output_dir, f"{project_name}_v1.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved BLEND: {blend_path}")

    return stl_path, blend_path

def render_preview(output_dir, project_name, angle_name="45deg"):
    """Render a preview image"""
    # Set render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    # Render
    render_path = os.path.join(output_dir, f"{project_name}_preview_{angle_name}.png")
    bpy.context.scene.render.filepath = render_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered preview: {render_path}")

    return render_path

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to generate the name plate"""
    print("\n" + "="*70)
    print("KIRJASTO LIBRARY NAME PLATE GENERATOR")
    print("="*70 + "\n")

    # Step 1: Clear scene
    print("Step 1: Clearing scene...")
    clear_scene()

    # Step 2: Load font
    print("\nStep 2: Loading Quicksand font...")
    font = load_font(QUICKSAND_FONT_PATH)
    if font is None:
        return False

    # Step 3: Create text objects
    print("\nStep 3: Creating text objects...")
    text1 = create_text_object(TEXT_LINE_1, "Text_Kirjasto", font, TEXT_SIZE)
    text2 = create_text_object(TEXT_LINE_2, "Text_Library", font, TEXT_SIZE)

    # Step 4: Position text objects
    print("\nStep 4: Positioning text objects...")
    position_text_objects(text1, text2, LINE_SPACING)

    # Step 5: Convert text to mesh
    print("\nStep 5: Converting text to mesh...")
    text1 = convert_text_to_mesh(text1)
    text2 = convert_text_to_mesh(text2)

    # Step 6: Extrude text
    print("\nStep 6: Extruding text...")
    extrude_text(text1, LETTER_EXTRUDE)
    extrude_text(text2, LETTER_EXTRUDE)

    # Step 7: Create base plate
    print("\nStep 7: Creating base plate...")
    base_plate = create_base_plate(PLATE_LENGTH, PLATE_WIDTH, PLATE_THICKNESS)

    # Step 8: Join all objects
    print("\nStep 8: Joining objects...")
    nameplate = join_objects([base_plate, text1, text2])

    # Step 9: Clean geometry
    print("\nStep 9: Cleaning geometry...")
    clean_geometry(nameplate)

    # Step 10: Setup camera and lighting
    print("\nStep 10: Setting up camera and lighting...")
    setup_camera_and_lighting()

    # Step 11: Export files
    print("\nStep 11: Exporting files...")
    stl_path, blend_path = export_files(nameplate, OUTPUT_DIR, PROJECT_NAME)

    # Step 12: Render preview (optional - can be slow)
    print("\nStep 12: Rendering preview...")
    try:
        render_preview(OUTPUT_DIR, PROJECT_NAME)
    except Exception as e:
        print(f"Note: Preview rendering skipped or failed: {e}")
        print("You can render manually from Blender UI")

    # Final summary
    print("\n" + "="*70)
    print("NAME PLATE GENERATION COMPLETE!")
    print("="*70)
    print(f"\nFiles saved to: {OUTPUT_DIR}")
    print(f"- STL file: {PROJECT_NAME}_v1.stl")
    print(f"- BLEND file: {PROJECT_NAME}_v1.blend")
    print(f"\nDimensions:")
    print(f"- Plate: {PLATE_LENGTH*100:.1f} x {PLATE_WIDTH*100:.1f} cm")
    print(f"- Thickness: {PLATE_THICKNESS*1000:.1f} mm")
    print(f"- Letter depth: {LETTER_EXTRUDE*1000:.1f} mm")
    print("\nReady for 3D printing!")
    print("="*70 + "\n")

    return True

# Run the script
if __name__ == "__main__":
    main()
