# NamePlate Studio Pro

**Professional 3D Name Plate Design Application**

A powerful desktop application for designing and generating 3D-printable name plates with real-time preview, bilingual interface (English/Finnish), and advanced customization options.

![NamePlate Studio Pro](./screenshot.png)
*Screenshot: Add your screenshot as `screenshot.png` in the project root*

## Features

### Core Functionality
- ✅ **Real-time 3D Preview** - See your design instantly with interactive 3D, Top, Front, and Side views
- ✅ **Bilingual Interface** - Full support for English and Finnish languages
- ✅ **Professional Templates** - Pre-configured templates for Library Signs, Door Plates, Desk Nameplates, and Wall Signs
- ✅ **Complete Customization** - Adjust dimensions, text, fonts, materials, and finishes
- ✅ **Project Management** - Save and load projects for reuse
- ✅ **Batch Processing** - Generate multiple name plates from CSV data
- ✅ **QR Code Integration** - Add QR codes with various data types (URL, WiFi, vCard, etc.)

### Design Controls
- **Text Content** - Dual-line text input with custom content
- **Dimensions** - Adjustable plate length, width, thickness, and letter depth (in millimeters)
- **Typography** - Multiple fonts (Quicksand family, Arial, Helvetica), text size, and line spacing
- **Materials** - PLA Standard, PETG Glossy, ABS, Wood Fill, Carbon Fiber
- **Finishes** - Smooth (post-processed), Standard (as-printed), Textured

### Advanced Features
- **Interactive 3D Visualization** - Zoom, pan, and rotate views
- **Design Validation** - Check designs before export
- **Multiple Export Formats** - STL and Blender (.blend) support
- **Recent Projects** - Quick access to your latest work
- **Professional Dark Theme** - Eye-friendly interface for extended use

## Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher (3.13 recommended)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Display**: 1400x800 minimum resolution

### Python Dependencies
```
PyQt6>=6.6.0
PyQt6-WebEngine>=6.6.0
matplotlib>=3.8.0
numpy>=1.24.0
Pillow>=10.0.0
qrcode[pil]>=7.4.2
segno>=1.6.0
pyyaml>=6.0
toml>=0.10.2
python-dateutil>=2.8.2
requests>=2.31.0
```

## Installation

### Quick Start

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd 7894
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**
   ```bash
   python launch_gui.py
   ```

   Or on Windows, double-click:
   ```
   launch_gui.bat
   ```

### Verify Installation

Test that all dependencies are installed correctly:
```bash
python test_imports.py
```

You should see all `[OK]` messages indicating successful installation.

## Usage

### Getting Started

1. **Launch the application**
   - Run `python launch_gui.py` or use the batch file on Windows

2. **Select a template** (optional)
   - Choose from Library Sign, Door Plate, Desk Nameplate, Wall Sign, or Custom
   - Templates provide optimized starting points

3. **Customize your design**
   - Enter your text in Line 1 and Line 2
   - Adjust dimensions using the sliders
   - Choose font, material, and finish options
   - Preview updates automatically

4. **View your design**
   - Switch between 3D, Top, Front, and Side views
   - Use zoom controls to inspect details
   - Reset view anytime with the Reset View button

5. **Save your project**
   - File → Save Project to keep your design
   - File → Open Project to load saved work
   - Recent Projects list for quick access

### Language Switching

Switch between English and Finnish:

1. Click **View** menu (or **Näytä** in Finnish)
2. Select **Language** (or **Kieli**)
3. Choose your preferred language:
   - **English** - Full English interface
   - **Suomi** - Complete Finnish interface
4. The interface updates immediately

### Templates

**Library Sign** (Kirjasto)
- Optimized for: Public signage
- Default size: 160×80×7mm
- Dual-language ready

**Door Plate**
- Optimized for: Office doors
- Default size: 120×60×7mm
- Professional finish

**Desk Nameplate**
- Optimized for: Desktop display
- Default size: 100×50×7mm
- Compact design

**Wall Sign**
- Optimized for: Wall mounting
- Default size: 200×100×7mm
- Large format

### Batch Processing

Process multiple name plates at once:

1. Go to **Tools** → **Batch Processing**
2. Import CSV file or add entries manually
3. Configure output format and settings
4. Set number of concurrent jobs
5. Start processing

CSV Format:
```csv
line1,line2,length,width,thickness
KIRJASTO,LIBRARY,160,80,7
OFFICE,TOIMISTO,120,60,7
```

### QR Codes

Add QR codes to your designs:

1. Go to **Tools** → **Add QR Code**
2. Choose QR code type:
   - URL
   - Plain Text
   - WiFi Credentials
   - vCard Contact
   - Email
3. Configure position and size
4. Select 3D style (embossed/recessed)
5. Generate and preview

## Keyboard Shortcuts

### File Operations
- `Ctrl+N` - New Project
- `Ctrl+O` - Open Project
- `Ctrl+S` - Save Project
- `Ctrl+Shift+S` - Save Project As
- `Ctrl+E` - Export to STL
- `Ctrl+Q` - Quit Application

### Edit
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+,` - Preferences

### View
- `Ctrl++` - Zoom In
- `Ctrl+-` - Zoom Out
- `Ctrl+0` - Fit to View

### Tools
- `Ctrl+B` - Batch Processing
- `Ctrl+Shift+V` - Validate Design

### Help
- `F1` - Help Contents

## Configuration

### Settings Dialog

Access via **Edit** → **Preferences** (`Ctrl+,`)

**General Tab**
- Language preference
- Auto-update preview
- Default save location

**Fonts Tab**
- Font file paths
- Custom font installation

**Output Tab**
- Default export directory
- File naming conventions
- Export quality settings

**Preview Tab**
- Rendering quality (Low/Medium/High)
- Anti-aliasing options
- View defaults

**Advanced Tab**
- Concurrent batch jobs
- Memory limits
- Debug options

## Project Structure

```
7894/
├── launch_gui.py              # Main application launcher
├── launch_gui.bat             # Windows launcher
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── screenshot.png             # UI screenshot
│
├── src/                       # Source code
│   ├── main.py               # Application entry point
│   │
│   ├── core/                 # Core functionality
│   │   ├── generator.py      # 3D model generation
│   │   ├── template_manager.py
│   │   ├── validator.py      # Design validation
│   │   ├── project_manager.py
│   │   └── translations.py   # Bilingual support
│   │
│   └── gui/                  # User interface
│       ├── main_window.py    # Main application window
│       ├── design_panel.py   # Design controls
│       ├── preview_panel.py  # 3D preview
│       ├── template_panel.py # Template selector
│       ├── settings_dialog.py
│       ├── batch_dialog.py
│       ├── qr_dialog.py
│       └── dashboard_panel.py
│
└── tests/                     # Test files
    ├── test_imports.py
    ├── test_suite.py
    └── validate_setup.py
```

## Troubleshooting

### Application Won't Launch

**Error**: Missing dependencies
```
Solution: pip install -r requirements.txt
```

**Error**: Python version too old
```
Solution: Install Python 3.8 or higher
```

### Preview Not Showing

1. Check that text is entered in both lines
2. Click "Generate Preview" button
3. Try "Reset View" button
4. Verify preview quality in settings

### Export Fails

1. Check output directory exists and is writable
2. Verify disk space available
3. Try different export location
4. Check file permissions

### Language Not Switching

1. Ensure you selected language from View → Language menu
2. Some labels update immediately, others require restart
3. Restart application to see all changes

### Performance Issues

1. Lower preview quality in settings
2. Reduce concurrent batch jobs
3. Close other applications
4. Check system resources

## Development

### Running from Source

```bash
# Clone repository
git clone <repository-url>
cd 7894

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python launch_gui.py
```

### Running Tests

```bash
# Test imports
python test_imports.py

# Run full test suite
python test_suite.py

# Validate setup
python validate_setup.py
```

## FAQ

**Q: Can I use custom fonts?**
A: Yes! Add font paths in Edit → Preferences → Fonts tab.

**Q: What export formats are supported?**
A: Currently STL and Blender (.blend) formats. More formats coming soon.

**Q: Can I print the name plates?**
A: Yes! Export to STL and import into your 3D printer slicer software.

**Q: How do I report bugs?**
A: Check the GitHub issues page or contact the development team.

**Q: Is this free to use?**
A: Yes, this application is provided for the Kirjasto Library project.

**Q: Can I use this for commercial projects?**
A: Please check the license file for usage terms.

## Tips & Best Practices

### Design Tips
- Keep text concise for better readability
- Use minimum 7mm plate thickness for durability
- Minimum 3-4mm letter depth recommended
- Test small prototypes before final print

### 3D Printing Recommendations
- **Material**: PLA or PETG for best results
- **Layer Height**: 0.2mm standard, 0.1mm for fine details
- **Infill**: 20-30% for most applications
- **Supports**: Usually not needed
- **Orientation**: Print with base flat on bed

### Performance
- Enable auto-update preview for live changes
- Use Medium quality for balanced performance
- Save projects regularly
- Close unused dialogs

## Version History

### Version 1.0.0
- Initial release
- Full GUI application with 3D preview
- Bilingual support (English/Finnish)
- Template system
- Project save/load
- Batch processing
- QR code integration
- Professional dark theme

## Credits

- **Font**: Quicksand (Google Fonts)
- **Framework**: PyQt6
- **3D Visualization**: Matplotlib
- **QR Codes**: qrcode, segno

## License

This application is provided for the Kirjasto Library name plate project.

## Support

For issues, questions, or feature requests:
1. Check this README and documentation
2. Review the Troubleshooting section
3. Run test_imports.py to verify setup
4. Check the FAQ section

---

**NamePlate Studio Pro** - Professional name plate design made simple.
