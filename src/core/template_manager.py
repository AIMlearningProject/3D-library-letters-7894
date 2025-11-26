"""
Template Manager
Handles pre-configured design templates
"""

from typing import Dict, List
import json
from pathlib import Path


class TemplateManager:
    """Manages design templates"""

    def __init__(self):
        self.templates = self.load_default_templates()

    def load_default_templates(self) -> Dict:
        """Load built-in templates"""
        return {
            'Library Sign': {
                'name': 'Library Sign',
                'description': 'Bilingual library signage',
                'text_line_1': 'Kirjasto',
                'text_line_2': 'Library',
                'plate_length': 160,
                'plate_width': 80,
                'plate_thickness': 7,
                'letter_depth': 4,
                'font': 'Quicksand-Regular',
                'text_size': 25,
                'line_spacing': 35,
                'material': 'PLA Standard',
                'finish': 'Standard (as-printed)',
                'category': 'Signage'
            },
            'Door Plate': {
                'name': 'Door Plate',
                'description': 'Office door nameplate',
                'text_line_1': 'Office',
                'text_line_2': '201',
                'plate_length': 200,
                'plate_width': 50,
                'plate_thickness': 5,
                'letter_depth': 3,
                'font': 'Quicksand-Bold',
                'text_size': 20,
                'line_spacing': 25,
                'material': 'PETG Glossy',
                'finish': 'Smooth (post-processed)',
                'category': 'Office'
            },
            'Desk Nameplate': {
                'name': 'Desk Nameplate',
                'description': 'Professional desk sign',
                'text_line_1': 'John Doe',
                'text_line_2': 'Manager',
                'plate_length': 120,
                'plate_width': 30,
                'plate_thickness': 6,
                'letter_depth': 3,
                'font': 'Quicksand-Regular',
                'text_size': 15,
                'line_spacing': 18,
                'material': 'Wood Fill',
                'finish': 'Standard (as-printed)',
                'category': 'Professional'
            },
            'Room Number': {
                'name': 'Room Number',
                'description': 'Simple room identifier',
                'text_line_1': 'Room',
                'text_line_2': '101',
                'plate_length': 100,
                'plate_width': 40,
                'plate_thickness': 5,
                'letter_depth': 4,
                'font': 'Quicksand-Bold',
                'text_size': 18,
                'line_spacing': 22,
                'material': 'PLA Standard',
                'finish': 'Standard (as-printed)',
                'category': 'Signage'
            },
            'Welcome Sign': {
                'name': 'Welcome Sign',
                'description': 'Greeting sign',
                'text_line_1': 'Welcome',
                'text_line_2': 'Visitors',
                'plate_length': 180,
                'plate_width': 70,
                'plate_thickness': 7,
                'letter_depth': 5,
                'font': 'Quicksand-Bold',
                'text_size': 28,
                'line_spacing': 35,
                'material': 'PETG Glossy',
                'finish': 'Smooth (post-processed)',
                'category': 'Signage'
            }
        }

    def get_template(self, name: str) -> Dict:
        """Get a specific template by name"""
        return self.templates.get(name, {})

    def get_all_templates(self) -> Dict:
        """Get all available templates"""
        return self.templates

    def get_template_names(self) -> List[str]:
        """Get list of template names"""
        return list(self.templates.keys())

    def get_templates_by_category(self, category: str) -> Dict:
        """Get templates filtered by category"""
        return {
            name: template
            for name, template in self.templates.items()
            if template.get('category') == category
        }

    def add_custom_template(self, name: str, config: Dict) -> bool:
        """Add a custom template"""
        if name in self.templates:
            return False  # Template already exists

        self.templates[name] = {
            'name': name,
            'description': config.get('description', 'Custom template'),
            **config,
            'category': 'Custom'
        }
        return True

    def save_template_to_file(self, name: str, filepath: str) -> bool:
        """Save a template to a JSON file"""
        try:
            template = self.get_template(name)
            if not template:
                return False

            with open(filepath, 'w') as f:
                json.dump(template, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False

    def load_template_from_file(self, filepath: str) -> Dict:
        """Load a template from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                template = json.load(f)
            return template
        except Exception as e:
            print(f"Error loading template: {e}")
            return {}

    def export_all_templates(self, directory: str) -> bool:
        """Export all templates to JSON files"""
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)

            for name, template in self.templates.items():
                filename = f"{name.replace(' ', '_').lower()}.json"
                filepath = Path(directory) / filename
                with open(filepath, 'w') as f:
                    json.dump(template, f, indent=2)

            return True
        except Exception as e:
            print(f"Error exporting templates: {e}")
            return False
