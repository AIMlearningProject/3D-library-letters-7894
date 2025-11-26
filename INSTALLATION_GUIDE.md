# NamePlate Studio Pro - Installation & Testing Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Or install individually:**
```bash
pip install PyQt6 matplotlib qrcode[pil] pyyaml requests
```

### Step 2: Launch the Application

**Option A: Double-click (Windows)**
```
Double-click: launch_gui.bat
```

**Option B: Command Line**
```bash
python launch_gui.py
```

**Option C: From Blender (for full 3D generation)**
```bash
blender --python launch_gui.py
```

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 4 GB
- **Disk Space**: 500 MB

### Recommended
- **Python**: 3.10+
- **RAM**: 8 GB
- **Blender**: 3.0+ (for actual 3D model generation)

---

## 🧪 Testing Every Feature

### 1. GUI Launch Test
```bash
python launch_gui.py
```
✅ **Expected**: Application window opens with dark theme

### 2. Template Selection Test
**Steps:**
1. Click on "Library Sign" in the template list
2. Observe design panel updates

✅ **Expected**:
- Text changes to "Kirjasto" / "Library"
- Dimensions update to 160×80mm
- Preview shows updated design

### 3. Design Panel Test
**Test each control:**
- [ ] Text inputs (Line 1 & 2)
- [ ] Plate length slider (50-500mm)
- [ ] Plate width slider (30-300mm)
- [ ] Plate thickness slider (3-20mm)
- [ ] Letter depth slider (2-20mm)
- [ ] Font dropdown
- [ ] Text size spinner
- [ ] Line spacing spinner
- [ ] Material dropdown
- [ ] Finish dropdown

✅ **Expected**: All controls responsive, preview updates

### 4. Preview Panel Test
**Test view modes:**
- [ ] 3D view (isometric)
- [ ] Top view
- [ ] Front view
- [ ] Side view
- [ ] Zoom in (+)
- [ ] Zoom out (-)
- [ ] Reset view

✅ **Expected**: Different perspectives shown correctly

### 5. Menu Bar Test
**File Menu:**
- [ ] New Project
- [ ] Open Project
- [ ] Save Project
- [ ] Save Project As
- [ ] Export to STL
- [ ] Export to Blend
- [ ] Exit

**Edit Menu:**
- [ ] Undo (not yet implemented)
- [ ] Redo (not yet implemented)
- [ ] Preferences

**View Menu:**
- [ ] Zoom In (Ctrl++)
- [ ] Zoom Out (Ctrl+-)
- [ ] Fit to View (Ctrl+0)
- [ ] Reset View

**Tools Menu:**
- [ ] Batch Processing
- [ ] Add QR Code
- [ ] Add Logo/Image
- [ ] Validate Design

**Help Menu:**
- [ ] Quick Start Guide
- [ ] Video Tutorials
- [ ] About

### 6. Keyboard Shortcuts Test
- [ ] `Ctrl+N` - New Project
- [ ] `Ctrl+O` - Open
- [ ] `Ctrl+S` - Save
- [ ] `Ctrl+E` - Export STL
- [ ] `Ctrl+B` - Batch Processing
- [ ] `Ctrl+,` - Preferences
- [ ] `Ctrl++` - Zoom In
- [ ] `Ctrl+-` - Zoom Out
- [ ] `Ctrl+0` - Fit View

### 7. Validation Test
**Steps:**
1. Click Tools → Validate Design
2. Try invalid values (e.g., 1000mm length)
3. Check for error messages

✅ **Expected**: Validation dialog with checks

### 8. Export Test (GUI Only)
**Note**: Full export requires Blender

**Steps:**
1. Design a plate
2. Click File → Export to STL
3. Choose save location

✅ **Expected**: File dialog opens

### 9. Project Save/Load Test
**Steps:**
1. Create a design
2. File → Save Project As
3. Save as `test_project.npproj`
4. File → Open Project
5. Open the saved file

✅ **Expected**: Design restored (when implemented)

### 10. Theme Test
**Check:**
- [ ] Dark theme applied
- [ ] Buttons styled
- [ ] Inputs styled
- [ ] Sliders styled
- [ ] Readable text
- [ ] Proper contrast

---

## 🔍 Troubleshooting

### Issue: "PyQt6 not found"
**Solution:**
```bash
pip install PyQt6
```

### Issue: "Application won't start"
**Check:**
1. Python version: `python --version` (must be 3.8+)
2. Dependencies: `pip list | grep PyQt6`
3. Run with verbose: `python launch_gui.py`

### Issue: "Preview not showing"
**Solution:**
- Ensure you've entered text in both lines
- Click "Generate Preview" button
- Check zoom level (try Reset View)

### Issue: "Can't export STL"
**Explanation:**
- Full STL export requires Blender
- GUI shows export dialog but generation needs Blender API
- To fully test: Run from Blender

### Issue: "Font not found"
**Solution:**
1. Download Quicksand font from Google Fonts
2. Install on your system
3. Restart application

---

## 🧰 Advanced Testing

### Test with Blender Integration
```bash
# Launch from Blender
blender --python launch_gui.py

# Or run standalone generator
blender --background --python kirjasto_nameplate_generator_v2.py
```

### Test Template Manager
```python
from src.core.template_manager import TemplateManager

tm = TemplateManager()
print(tm.get_template_names())
print(tm.get_template('Library Sign'))
```

### Test Validator
```python
from src.core.validator import DesignValidator

config = {
    'text_line_1': 'Test',
    'text_line_2': 'Plate',
    'plate_length': 160,
    'plate_width': 80,
    'plate_thickness': 7,
    'letter_depth': 4,
    'text_size': 25,
    'line_spacing': 35
}

valid, errors = DesignValidator.validate(config)
print(f"Valid: {valid}")
print(f"Errors: {errors}")

score = DesignValidator.estimate_printability_score(config)
print(f"Printability Score: {score}/100")
```

---

## 📊 Feature Completion Status

### ✅ Phase 1: GUI Foundation (COMPLETE)
- [x] Main window with menu bar
- [x] Design panel with controls
- [x] Preview panel with 3D view
- [x] Template system
- [x] Dark theme
- [x] Keyboard shortcuts

### 🚧 Phase 2: Core Integration (IN PROGRESS)
- [x] Core module structure
- [x] Template manager
- [x] Design validator
- [ ] Full Blender integration
- [ ] Export functionality
- [ ] Settings dialog

### ⏳ Phase 3: Advanced Features (PENDING)
- [ ] Batch processing
- [ ] QR code generator
- [ ] Logo import
- [ ] Project save/load
- [ ] Undo/redo system

### ⏳ Phase 4: Web Version (PLANNED)
- [ ] Flask backend
- [ ] React frontend
- [ ] Three.js preview
- [ ] Cloud storage

### ⏳ Phase 5: Distribution (PLANNED)
- [ ] PyInstaller packaging
- [ ] Installers for all platforms
- [ ] Auto-update system
- [ ] Documentation site

---

## 🎯 Current Testing Priorities

### High Priority (Test Now)
1. ✅ GUI launches successfully
2. ✅ All controls are responsive
3. ✅ Templates load correctly
4. ✅ Preview updates in real-time
5. ✅ Validation works

### Medium Priority (Test Soon)
1. Export dialogs open
2. Keyboard shortcuts work
3. Window resizing behaves properly
4. Settings persist between sessions
5. Error handling is graceful

### Low Priority (Test Later)
1. Batch processing
2. QR codes
3. Logo import
4. Web version
5. Installers

---

## 📝 Testing Checklist

Copy this to track your testing:

```
Desktop GUI Application Testing
===============================

Basic Functionality:
[ ] Application launches
[ ] Window displays correctly
[ ] Dark theme applied
[ ] All panels visible

Design Panel:
[ ] Text inputs work
[ ] All sliders functional
[ ] Dropdowns populate
[ ] Spinners accept input
[ ] Values update preview

Preview Panel:
[ ] 3D view renders
[ ] Top view works
[ ] Front view works
[ ] Side view works
[ ] Zoom in/out works
[ ] Reset view works

Templates:
[ ] Library Sign loads
[ ] Door Plate loads
[ ] Desk Nameplate loads
[ ] Room Number loads
[ ] Welcome Sign loads

Menus:
[ ] File menu opens
[ ] Edit menu opens
[ ] View menu opens
[ ] Tools menu opens
[ ] Help menu opens

Dialogs:
[ ] New project dialog
[ ] Save/Open dialogs
[ ] Export dialogs
[ ] Validation dialog
[ ] About dialog

Validation:
[ ] Required fields checked
[ ] Dimensions validated
[ ] Proportions checked
[ ] Warnings displayed

Performance:
[ ] UI responsive
[ ] Preview updates quickly
[ ] No lag on slider movement
[ ] Memory usage reasonable
```

---

## 🚀 Next Steps After Testing

1. **Report Issues**: Note any bugs or unexpected behavior
2. **Request Features**: What would make it even better?
3. **Performance**: Any lag or slowness?
4. **UX Feedback**: Is it intuitive? Any confusion?

---

## 📞 Support

Having issues? Check:
1. This troubleshooting section
2. MASTER_PLAN.md for architecture
3. Run `python validate_setup.py` for system check

---

**Ready to test? Run:**
```bash
python launch_gui.py
```

**Let's make this 100/100! 🎉**
