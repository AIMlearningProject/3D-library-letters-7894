"""
Core Name Plate Generator
Integrates with Blender Python API to generate 3D models
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple


class NamePlateGenerator:
    """Main generator class for creating 3D name plates"""

    def __init__(self):
        self.blender_available = self.check_blender()
        self.default_config = self.get_default_config()

    def check_blender(self) -> bool:
        """Check if Blender Python API is available"""
        try:
            import bpy
            return True
        except ImportError:
            return False

    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'text_line_1': 'KIRJASTO',
            'text_line_2': 'LIBRARY',
            'plate_length': 160,  # mm
            'plate_width': 80,
            'plate_thickness': 7,
            'letter_depth': 4,
            'font': 'Quicksand-Regular',
            'text_size': 25,
            'line_spacing': 35,
            'material': 'PLA Standard',
            'finish': 'Standard (as-printed)'
        }

    def generate(self, config: Dict, output_path: str) -> Tuple[bool, str]:
        """
        Generate 3D model based on configuration

        Args:
            config: Design configuration dictionary
            output_path: Path where to save the output files

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.blender_available:
            return False, "Blender Python API not available. Please run from Blender."

        try:
            import bpy
            from mathutils import Vector

            # Clear scene
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()

            # Convert mm to Blender units (meters)
            scale_factor = 0.001

            # Create text objects
            success = self._create_text_objects(config, scale_factor)
            if not success:
                return False, "Failed to create text objects"

            # Create base plate
            success = self._create_base_plate(config, scale_factor)
            if not success:
                return False, "Failed to create base plate"

            # Export files
            success = self._export_files(config, output_path)
            if not success:
                return False, "Failed to export files"

            return True, f"Successfully generated model at {output_path}"

        except Exception as e:
            return False, f"Error during generation: {str(e)}"

    def _create_text_objects(self, config: Dict, scale: float) -> bool:
        """Create text objects in Blender"""
        try:
            import bpy

            # This is a simplified version
            # In production, you would copy the logic from kirjasto_nameplate_generator_v2.py

            text_1 = config['text_line_1']
            text_2 = config['text_line_2']

            # Create text curve
            bpy.ops.object.text_add()
            text_obj_1 = bpy.context.object
            text_obj_1.data.body = text_1

            # TODO: Apply font, extrusion, positioning from config
            # This would integrate the complete logic from your existing generator

            return True
        except Exception as e:
            print(f"Error creating text: {e}")
            return False

    def _create_base_plate(self, config: Dict, scale: float) -> bool:
        """Create base plate in Blender"""
        try:
            import bpy

            # Create cube and scale to plate dimensions
            length = config['plate_length'] * scale
            width = config['plate_width'] * scale
            thickness = config['plate_thickness'] * scale

            bpy.ops.mesh.primitive_cube_add()
            plate = bpy.context.object
            plate.scale = (length/2, width/2, thickness/2)
            bpy.ops.object.transform_apply(scale=True)

            return True
        except Exception as e:
            print(f"Error creating plate: {e}")
            return False

    def _export_files(self, config: Dict, output_path: str) -> bool:
        """Export STL and BLEND files"""
        try:
            import bpy

            os.makedirs(output_path, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"nameplate_{timestamp}"

            # Export STL
            stl_path = os.path.join(output_path, f"{base_name}.stl")
            bpy.ops.export_mesh.stl(filepath=stl_path)

            # Save BLEND
            blend_path = os.path.join(output_path, f"{base_name}.blend")
            bpy.ops.wm.save_as_mainfile(filepath=blend_path)

            return True
        except Exception as e:
            print(f"Error exporting: {e}")
            return False

    def validate_config(self, config: Dict) -> Tuple[bool, str]:
        """
        Validate configuration before generation

        Returns:
            Tuple of (valid: bool, message: str)
        """
        # Check required fields
        required = ['text_line_1', 'text_line_2', 'plate_length', 'plate_width']
        missing = [f for f in required if f not in config]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"

        # Check dimensions
        if config['plate_length'] < 50 or config['plate_length'] > 500:
            return False, "Plate length must be between 50-500mm"

        if config['plate_width'] < 30 or config['plate_width'] > 300:
            return False, "Plate width must be between 30-300mm"

        if config['plate_thickness'] < 3 or config['plate_thickness'] > 20:
            return False, "Plate thickness must be between 3-20mm"

        return True, "Configuration valid"

    def estimate_print_time(self, config: Dict) -> str:
        """Estimate 3D printing time"""
        volume = (config['plate_length'] * config['plate_width'] *
                 config['plate_thickness']) / 1000  # cm³

        # Rough estimate: 1 cm³ ≈ 10 minutes at 0.2mm layer height
        minutes = volume * 10

        hours = int(minutes // 60)
        mins = int(minutes % 60)

        return f"{hours}h {mins}m"

    def estimate_material_cost(self, config: Dict, material_price_per_kg: float = 20.0) -> float:
        """Estimate material cost"""
        volume_cm3 = (config['plate_length'] * config['plate_width'] *
                     config['plate_thickness']) / 1000

        # PLA density ≈ 1.24 g/cm³
        weight_g = volume_cm3 * 1.24

        cost = (weight_g / 1000) * material_price_per_kg

        return round(cost, 2)
