"""
Core module for NamePlate Studio Pro
Contains the generator engine and business logic
"""

from .generator import NamePlateGenerator
from .template_manager import TemplateManager
from .validator import DesignValidator

__all__ = ['NamePlateGenerator', 'TemplateManager', 'DesignValidator']
