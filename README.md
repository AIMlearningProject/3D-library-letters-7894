# Kirjasto Library 3D Name Plate Generator

Automated Blender Python script for generating 3D-printable name plates based on the project specifications.

## Features

- Automated text creation with Quicksand font
- Customizable dimensions and spacing
- Base plate generation with beveled edges
- Automatic mesh conversion and cleanup
- STL export for 3D printing (scaled to millimeters)
- BLEND file export for further editing
- Optional preview rendering
- Clean, maintainable code with extensive comments

## Requirements

- **Blender** 2.8 or higher (recommended: Blender 3.x or 4.x)
- **Quicksand Font** (TTF or OTF format)
  - Download from: https://fonts.google.com/specimen/Quicksand
  - Or use your existing installation

## Installation

1. Download the Quicksand font if you don't have it
2. Note the path to the font file (typically in `C:/Windows/Fonts/` on Windows)
3. Open `kirjasto_nameplate_generator.py` in a text editor
4. Update the `QUICKSAND_FONT_PATH` variable (line 24) with your font path

## Usage

### Method 1: Run from Blender UI (Recommended)

1. Open Blender
2. Switch to the **Scripting** workspace (top menu bar)
3. Click **Open** and select `kirjasto_nameplate_generator.py`
4. Click the **Run Script** button (or press `Alt+P`)
5. Monitor the console output for progress
6. Find your files in the `D:/7894/output` directory

### Method 2: Run from Command Line

```bash
blender --background --python kirjasto_nameplate_generator.py
```

### Method 3: Run with Custom Settings

Edit the configuration section in the script (lines 22-41) before running:

```python
# Text Content
TEXT_LINE_1 = "Kirjasto"
TEXT_LINE_2 = "Library"

# Dimensions (in Blender units)
PLATE_LENGTH = 0.16      # 16 cm
PLATE_WIDTH = 0.08       # 8 cm
PLATE_THICKNESS = 0.007  # 7 mm base thickness
LETTER_EXTRUDE = 0.004   # 4 mm letter depth
TEXT_SIZE = 0.025        # 2.5 cm text height
LINE_SPACING = 0.035     # 3.5 cm between lines
```

## Configuration Parameters

### Font Settings
- `QUICKSAND_FONT_PATH`: Path to Quicksand font file (REQUIRED)

### Text Content
- `TEXT_LINE_1`: First line of text (default: "Kirjasto")
- `TEXT_LINE_2`: Second line of text (default: "Library")

### Dimensions
All dimensions are in Blender units (typically meters). The script automatically converts to millimeters for STL export.

- `PLATE_LENGTH`: Overall length of base plate (0.16 = 16 cm)
- `PLATE_WIDTH`: Overall width of base plate (0.08 = 8 cm)
- `PLATE_THICKNESS`: Thickness of base plate (0.007 = 7 mm)
- `LETTER_EXTRUDE`: Depth/height of letters (0.004 = 4 mm)
- `TEXT_SIZE`: Height of text characters (0.025 = 2.5 cm)
- `LINE_SPACING`: Vertical distance between text lines (0.035 = 3.5 cm)

### Export Settings
- `OUTPUT_DIR`: Directory for output files (default: "D:/7894/output")
- `PROJECT_NAME`: Base name for exported files (default: "Kirjasto_Library_plate")

## Output Files

After running the script, you'll find these files in the output directory:

1. **`Kirjasto_Library_plate_v1.stl`**
   - 3D printable file in millimeters
   - Ready to import into your slicer software

2. **`Kirjasto_Library_plate_v1.blend`**
   - Blender project file
   - Can be opened for manual adjustments

3. **`Kirjasto_Library_plate_preview_45deg.png`** (optional)
   - Rendered preview image
   - May take time to render (can be skipped)

## Project Phases Automated

This script automates the following phases from the guide:

### Phase 2 - Modeling
- ✅ Import Quicksand font into Blender
- ✅ Create text and convert to mesh
- ✅ Align spacing between "Kirjasto" and "Library"
- ✅ Add base plate (Option 2 design)
- ✅ Add thickness (5-10 mm configurable)
- ✅ Check structural stability (no thin letters)
- ✅ Apply Solidify modifier
- ✅ Clean geometry

### Phase 4 - Export
- ✅ Export STL (with modifiers applied)
- ✅ Save BLEND file
- ✅ Generate preview renders (optional)
- ✅ Clean file naming

## Customization Tips

### Adjusting Text Size
If text is too large or small for the plate:
```python
TEXT_SIZE = 0.020  # Smaller text (2 cm)
TEXT_SIZE = 0.030  # Larger text (3 cm)
```

### Changing Plate Dimensions
For a larger or smaller plate:
```python
PLATE_LENGTH = 0.20  # 20 cm (larger)
PLATE_WIDTH = 0.10   # 10 cm (wider)
```

### Adjusting Letter Depth
For deeper or shallower letters:
```python
LETTER_EXTRUDE = 0.003  # 3 mm (shallower)
LETTER_EXTRUDE = 0.005  # 5 mm (deeper)
```

### Using Different Text
Change the text content:
```python
TEXT_LINE_1 = "Welcome"
TEXT_LINE_2 = "Center"
```

## Troubleshooting

### Font Not Found Error
```
ERROR: Font file not found at C:/Windows/Fonts/Quicksand-Regular.ttf
```
**Solution**:
1. Locate your Quicksand font file
2. Update `QUICKSAND_FONT_PATH` in the script
3. Use forward slashes (/) or double backslashes (\\\\) in path

### Output Directory Error
```
ERROR: Cannot create output directory
```
**Solution**:
1. Check if path exists and is writable
2. Update `OUTPUT_DIR` to a valid location
3. Create the directory manually first

### Preview Rendering Fails
**Solution**:
- This is optional and can be skipped
- You can render manually in Blender UI later
- The STL and BLEND files are still created successfully

### Letters Too Thin Warning
If letters break during printing:
1. Increase `LETTER_EXTRUDE` (minimum 3mm recommended)
2. Increase `TEXT_SIZE` for thicker letter strokes
3. Check your 3D printer's minimum feature size

## 3D Printing Tips

### Recommended Settings
- **Layer Height**: 0.2mm (or 0.1mm for higher quality)
- **Infill**: 20-40%
- **Supports**: Usually not needed (flat base)
- **Material**: PLA or PETG recommended
- **Orientation**: Print with base flat on bed

### Pre-Print Checklist
1. ✅ Import STL into your slicer
2. ✅ Check dimensions match requirements
3. ✅ Verify no thin features (minimum 3mm)
4. ✅ Preview layer-by-layer
5. ✅ Add brim if adhesion is concern

## Script Architecture

The script is organized into clear sections:

1. **Configuration** (lines 22-41): All user-adjustable parameters
2. **Helper Functions** (lines 44-235): Modular functions for each task
3. **Main Execution** (lines 238-306): Step-by-step workflow

### Key Functions
- `load_font()`: Imports the Quicksand font
- `create_text_object()`: Creates text curves
- `convert_text_to_mesh()`: Converts curves to meshes
- `extrude_text()`: Adds depth using Solidify modifier
- `create_base_plate()`: Generates base plate with bevels
- `position_text_objects()`: Aligns text spacing
- `join_objects()`: Combines all parts
- `clean_geometry()`: Removes duplicates and fixes normals
- `export_files()`: Saves STL and BLEND files

## Version History

### v1.0 (Current)
- Initial release
- Full automation of name plate generation
- Configurable parameters
- STL and BLEND export
- Optional preview rendering
- Comprehensive error handling

## License

This script is provided as-is for the Kirjasto Library name plate project.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review Blender console output for error messages
3. Verify all configuration parameters are correct
4. Test with default settings first

## Credits

- Font: Quicksand (Google Fonts)
- Created for: Kirjasto Library name plate project
- Based on: Project guide specifications (guide.md)
