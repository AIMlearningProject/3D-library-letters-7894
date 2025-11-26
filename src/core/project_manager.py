"""
Project Manager
Handles saving and loading project files
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple


class ProjectManager:
    """Manages project file operations"""

    PROJECT_VERSION = "1.0"
    PROJECT_EXTENSION = ".npproj"

    @classmethod
    def save_project(cls, filepath: str, design_data: Dict, metadata: Optional[Dict] = None) -> Tuple[bool, str]:
        """
        Save project to file

        Args:
            filepath: Path to save the project
            design_data: Design configuration dictionary
            metadata: Optional metadata (author, notes, etc.)

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Ensure .npproj extension
            if not filepath.endswith(cls.PROJECT_EXTENSION):
                filepath += cls.PROJECT_EXTENSION

            # Create project structure
            project = {
                "version": cls.PROJECT_VERSION,
                "created_date": datetime.now().isoformat(),
                "modified_date": datetime.now().isoformat(),
                "metadata": metadata or {},
                "design": design_data
            }

            # Create directory if needed
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            # Save as JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(project, f, indent=2, ensure_ascii=False)

            return True, f"Project saved to {filepath}"

        except Exception as e:
            return False, f"Failed to save project: {str(e)}"

    @classmethod
    def load_project(cls, filepath: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Load project from file

        Args:
            filepath: Path to the project file

        Returns:
            Tuple of (success: bool, project_data: Dict, message: str)
        """
        try:
            if not os.path.exists(filepath):
                return False, None, "Project file not found"

            with open(filepath, 'r', encoding='utf-8') as f:
                project = json.load(f)

            # Validate project structure
            if "version" not in project or "design" not in project:
                return False, None, "Invalid project file format"

            # Check version compatibility
            if project["version"] != cls.PROJECT_VERSION:
                # Could add migration logic here
                pass

            # Update modified date
            project["modified_date"] = datetime.now().isoformat()

            return True, project, "Project loaded successfully"

        except json.JSONDecodeError:
            return False, None, "Invalid JSON in project file"
        except Exception as e:
            return False, None, f"Failed to load project: {str(e)}"

    @classmethod
    def get_project_info(cls, filepath: str) -> Optional[Dict]:
        """
        Get project metadata without loading full project

        Args:
            filepath: Path to the project file

        Returns:
            Dictionary with project info or None if failed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                project = json.load(f)

            return {
                "version": project.get("version", "Unknown"),
                "created_date": project.get("created_date", "Unknown"),
                "modified_date": project.get("modified_date", "Unknown"),
                "metadata": project.get("metadata", {}),
                "has_design": "design" in project
            }

        except Exception:
            return None

    @classmethod
    def create_autosave(cls, design_data: Dict, autosave_dir: str) -> Tuple[bool, str]:
        """
        Create an autosave file

        Args:
            design_data: Current design configuration
            autosave_dir: Directory for autosave files

        Returns:
            Tuple of (success: bool, filepath: str)
        """
        try:
            os.makedirs(autosave_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"autosave_{timestamp}.npproj"
            filepath = os.path.join(autosave_dir, filename)

            metadata = {
                "autosave": True,
                "timestamp": timestamp
            }

            success, message = cls.save_project(filepath, design_data, metadata)

            # Clean up old autosaves (keep last 10)
            if success:
                cls.cleanup_autosaves(autosave_dir, keep=10)

            return success, filepath if success else message

        except Exception as e:
            return False, f"Autosave failed: {str(e)}"

    @classmethod
    def cleanup_autosaves(cls, autosave_dir: str, keep: int = 10):
        """Remove old autosave files, keeping only the most recent"""
        try:
            autosaves = []
            for file in Path(autosave_dir).glob("autosave_*.npproj"):
                autosaves.append(file)

            # Sort by modification time (newest first)
            autosaves.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            # Remove old ones
            for old_file in autosaves[keep:]:
                old_file.unlink()

        except Exception as e:
            print(f"Failed to clean up autosaves: {e}")

    @classmethod
    def export_to_json(cls, design_data: Dict, filepath: str) -> Tuple[bool, str]:
        """
        Export design configuration to JSON (without project wrapper)

        Args:
            design_data: Design configuration
            filepath: Path to save JSON file

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(design_data, f, indent=2, ensure_ascii=False)

            return True, f"Configuration exported to {filepath}"

        except Exception as e:
            return False, f"Export failed: {str(e)}"

    @classmethod
    def import_from_json(cls, filepath: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Import design configuration from JSON

        Args:
            filepath: Path to JSON file

        Returns:
            Tuple of (success: bool, design_data: Dict, message: str)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                design_data = json.load(f)

            # Basic validation
            required_fields = ['text_line_1', 'text_line_2', 'plate_length', 'plate_width']
            if not all(field in design_data for field in required_fields):
                return False, None, "Missing required fields in configuration"

            return True, design_data, "Configuration imported successfully"

        except json.JSONDecodeError:
            return False, None, "Invalid JSON file"
        except Exception as e:
            return False, None, f"Import failed: {str(e)}"

    @classmethod
    def get_recent_projects(cls, max_count: int = 10) -> list:
        """
        Get list of recently opened projects from settings

        Args:
            max_count: Maximum number of recent projects to return

        Returns:
            List of recent project file paths
        """
        from PyQt6.QtCore import QSettings
        settings = QSettings()
        recent = settings.value("recent_projects", [])

        if not isinstance(recent, list):
            recent = []

        # Filter out non-existent files
        recent = [p for p in recent if os.path.exists(p)]

        return recent[:max_count]

    @classmethod
    def add_recent_project(cls, filepath: str):
        """Add project to recent projects list"""
        from PyQt6.QtCore import QSettings
        settings = QSettings()

        recent = settings.value("recent_projects", [])
        if not isinstance(recent, list):
            recent = []

        # Remove if already in list
        if filepath in recent:
            recent.remove(filepath)

        # Add to front
        recent.insert(0, filepath)

        # Keep only last 10
        recent = recent[:10]

        settings.setValue("recent_projects", recent)
