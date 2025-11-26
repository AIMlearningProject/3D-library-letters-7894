"""
Design Validator
Validates design configurations before generation
"""

from typing import Dict, List, Tuple


class DesignValidator:
    """Validates design parameters"""

    # Validation constraints (in mm)
    CONSTRAINTS = {
        'plate_length': {'min': 50, 'max': 500, 'unit': 'mm'},
        'plate_width': {'min': 30, 'max': 300, 'unit': 'mm'},
        'plate_thickness': {'min': 3, 'max': 20, 'unit': 'mm'},
        'letter_depth': {'min': 2, 'max': 20, 'unit': 'mm'},
        'text_size': {'min': 10, 'max': 100, 'unit': 'mm'},
        'line_spacing': {'min': 10, 'max': 100, 'unit': 'mm'},
    }

    @classmethod
    def validate(cls, config: Dict) -> Tuple[bool, List[str]]:
        """
        Validate complete design configuration

        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        errors = []

        # Check required fields
        required_fields = [
            'text_line_1', 'text_line_2', 'plate_length',
            'plate_width', 'plate_thickness', 'letter_depth'
        ]

        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")

        if errors:
            return False, errors

        # Validate dimensions
        for field, constraints in cls.CONSTRAINTS.items():
            if field in config:
                value = config[field]
                min_val = constraints['min']
                max_val = constraints['max']
                unit = constraints['unit']

                if value < min_val:
                    errors.append(
                        f"{field.replace('_', ' ').title()}: "
                        f"Must be at least {min_val}{unit} (got {value}{unit})"
                    )
                elif value > max_val:
                    errors.append(
                        f"{field.replace('_', ' ').title()}: "
                        f"Must be at most {max_val}{unit} (got {value}{unit})"
                    )

        # Validate text content
        if not config['text_line_1'].strip() and not config['text_line_2'].strip():
            errors.append("At least one text line must be non-empty")

        if len(config['text_line_1']) > 50:
            errors.append("Line 1: Text too long (max 50 characters)")

        if len(config['text_line_2']) > 50:
            errors.append("Line 2: Text too long (max 50 characters)")

        # Validate proportions
        if config['letter_depth'] > config['plate_thickness']:
            errors.append(
                "Letter depth cannot exceed plate thickness"
            )

        if config['text_size'] > config['plate_width'] * 0.8:
            errors.append(
                "Text size too large for plate width "
                "(should be max 80% of plate width)"
            )

        # Structural warnings (not blocking)
        warnings = cls.get_warnings(config)

        return len(errors) == 0, errors

    @classmethod
    def get_warnings(cls, config: Dict) -> List[str]:
        """
        Get non-critical warnings about the design

        Returns:
            List of warning messages
        """
        warnings = []

        # Check for thin letters
        if config.get('letter_depth', 0) < 3:
            warnings.append(
                "Warning: Letter depth < 3mm may be fragile when printing"
            )

        # Check for thin plate
        if config.get('plate_thickness', 0) < 5:
            warnings.append(
                "Warning: Plate thickness < 5mm may warp during printing"
            )

        # Check aspect ratio
        length = config.get('plate_length', 0)
        width = config.get('plate_width', 0)
        if length > 0 and width > 0:
            ratio = length / width
            if ratio > 5:
                warnings.append(
                    f"Warning: Aspect ratio ({ratio:.1f}:1) is very elongated. "
                    "Consider using supports or reducing length."
                )

        # Check text size relative to plate
        text_size = config.get('text_size', 0)
        plate_width = config.get('plate_width', 0)
        if plate_width > 0 and text_size > plate_width * 0.6:
            warnings.append(
                "Warning: Text size is very large relative to plate. "
                "May have poor readability or spacing issues."
            )

        return warnings

    @classmethod
    def validate_for_print(cls, config: Dict) -> Tuple[bool, List[str]]:
        """
        Validate design specifically for 3D printing feasibility

        Returns:
            Tuple of (is_printable: bool, issues: List[str])
        """
        issues = []

        # Minimum feature size for typical FDM printer (0.4mm nozzle)
        MIN_FEATURE_SIZE = 0.8  # mm

        letter_depth = config.get('letter_depth', 0)
        if letter_depth < MIN_FEATURE_SIZE * 3:
            issues.append(
                f"Letter depth ({letter_depth}mm) may be too small "
                f"for reliable printing. Recommended minimum: {MIN_FEATURE_SIZE * 3}mm"
            )

        # Check for overhangs
        if letter_depth > 10:
            issues.append(
                f"Letter depth ({letter_depth}mm) is very deep. "
                "May require supports or cause stringing."
            )

        # Check print bed size (assuming 220x220mm typical printer)
        MAX_PRINT_SIZE = 220  # mm
        length = config.get('plate_length', 0)
        width = config.get('plate_width', 0)

        if length > MAX_PRINT_SIZE or width > MAX_PRINT_SIZE:
            issues.append(
                f"Design ({length}x{width}mm) may not fit on standard "
                f"print bed ({MAX_PRINT_SIZE}x{MAX_PRINT_SIZE}mm)"
            )

        return len(issues) == 0, issues

    @classmethod
    def estimate_printability_score(cls, config: Dict) -> int:
        """
        Calculate printability score (0-100)

        Returns:
            Score from 0 (unprintable) to 100 (perfect)
        """
        score = 100

        # Deduct points for issues
        _, errors = cls.validate(config)
        score -= len(errors) * 20

        _, warnings = cls.validate_for_print(config)
        score -= len(warnings) * 10

        # Bonus points for ideal dimensions
        if 5 <= config.get('letter_depth', 0) <= 8:
            score += 5

        if 5 <= config.get('plate_thickness', 0) <= 10:
            score += 5

        return max(0, min(100, score))
