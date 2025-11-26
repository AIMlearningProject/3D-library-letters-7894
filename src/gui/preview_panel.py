"""
Preview Panel - 3D visualization of the name plate
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGroupBox, QButtonGroup, QRadioButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient
import math


class PreviewPanel(QWidget):
    """3D preview panel"""

    def __init__(self):
        super().__init__()
        self.design_data = None
        self.rotation_x = 30
        self.rotation_y = 45
        self.zoom = 1.0
        self.view_mode = '3D'
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)

        # View controls
        controls = QHBoxLayout()

        # View mode buttons
        view_group = QGroupBox("View Mode")
        view_layout = QHBoxLayout()
        self.view_button_group = QButtonGroup()

        view_3d = QRadioButton("3D")
        view_3d.setChecked(True)
        view_3d.toggled.connect(lambda: self.set_view_mode('3D'))
        self.view_button_group.addButton(view_3d)
        view_layout.addWidget(view_3d)

        view_top = QRadioButton("Top")
        view_top.toggled.connect(lambda: self.set_view_mode('Top'))
        self.view_button_group.addButton(view_top)
        view_layout.addWidget(view_top)

        view_front = QRadioButton("Front")
        view_front.toggled.connect(lambda: self.set_view_mode('Front'))
        self.view_button_group.addButton(view_front)
        view_layout.addWidget(view_front)

        view_side = QRadioButton("Side")
        view_side.toggled.connect(lambda: self.set_view_mode('Side'))
        self.view_button_group.addButton(view_side)
        view_layout.addWidget(view_side)

        view_group.setLayout(view_layout)
        controls.addWidget(view_group)

        controls.addStretch()

        # Zoom buttons
        zoom_label = QLabel("Zoom:")
        controls.addWidget(zoom_label)

        zoom_in = QPushButton("+")
        zoom_in.setMaximumWidth(40)
        zoom_in.clicked.connect(self.zoom_in)
        controls.addWidget(zoom_in)

        zoom_out = QPushButton("-")
        zoom_out.setMaximumWidth(40)
        zoom_out.clicked.connect(self.zoom_out)
        controls.addWidget(zoom_out)

        reset_btn = QPushButton("Reset View")
        reset_btn.clicked.connect(self.reset_view)
        controls.addWidget(reset_btn)

        layout.addLayout(controls)

        # Canvas for 3D preview
        self.canvas = PreviewCanvas()
        layout.addWidget(self.canvas, stretch=1)

        # Info label
        self.info_label = QLabel("No design loaded")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

    def update_preview(self, design_data):
        """Update the preview with new design data"""
        self.design_data = design_data
        self.canvas.set_design_data(design_data)
        self.canvas.set_view_mode(self.view_mode)
        self.canvas.set_zoom(self.zoom)
        self.canvas.update()
        self.update_info_label()

    def set_view_mode(self, mode):
        """Set the view mode"""
        self.view_mode = mode
        if self.design_data:
            self.canvas.set_view_mode(mode)
            self.canvas.update()

    def zoom_in(self):
        """Zoom in"""
        self.zoom = min(self.zoom * 1.2, 5.0)
        if self.design_data:
            self.canvas.set_zoom(self.zoom)
            self.canvas.update()

    def zoom_out(self):
        """Zoom out"""
        self.zoom = max(self.zoom / 1.2, 0.2)
        if self.design_data:
            self.canvas.set_zoom(self.zoom)
            self.canvas.update()

    def reset_view(self):
        """Reset view to default"""
        self.zoom = 1.0
        self.view_mode = '3D'
        self.view_button_group.buttons()[0].setChecked(True)
        if self.design_data:
            self.canvas.set_zoom(self.zoom)
            self.canvas.set_view_mode(self.view_mode)
            self.canvas.update()

    def clear(self):
        """Clear the preview"""
        self.design_data = None
        self.canvas.set_design_data(None)
        self.canvas.update()
        self.info_label.setText("No design loaded")

    def update_info_label(self):
        """Update the information label"""
        if self.design_data:
            length = self.design_data.get('plate_length', 0)
            width = self.design_data.get('plate_width', 0)
            thickness = self.design_data.get('plate_thickness', 0)
            self.info_label.setText(
                f"Dimensions: {length}×{width}×{thickness} mm | "
                f"Material: {self.design_data.get('material', 'N/A')}"
            )


class PreviewCanvas(QWidget):
    """Canvas widget for drawing the 3D preview"""

    def __init__(self):
        super().__init__()
        self.design_data = None
        self.view_mode = '3D'
        self.zoom = 1.0
        self.setMinimumSize(400, 400)

    def set_design_data(self, data):
        """Set design data"""
        self.design_data = data

    def set_view_mode(self, mode):
        """Set view mode"""
        self.view_mode = mode

    def set_zoom(self, zoom):
        """Set zoom level"""
        self.zoom = zoom

    def paintEvent(self, event):
        """Paint the preview"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor(40, 40, 40))

        if not self.design_data:
            # Draw placeholder
            painter.setPen(QPen(QColor(150, 150, 150), 2))
            font = QFont("Arial", 16)
            painter.setFont(font)
            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                "Preview will appear here\n\nModify design settings to see changes"
            )
            return

        # Get design parameters
        length = self.design_data.get('plate_length', 160)  # mm
        width = self.design_data.get('plate_width', 80)
        thickness = self.design_data.get('plate_thickness', 7)
        letter_depth = self.design_data.get('letter_depth', 4)
        text_1 = self.design_data.get('text_line_1', '')
        text_2 = self.design_data.get('text_line_2', '')

        # Calculate scaling
        center_x = self.width() / 2
        center_y = self.height() / 2
        scale = min(self.width(), self.height()) / max(length, width) * 0.7 * self.zoom

        # Draw based on view mode
        if self.view_mode == 'Top':
            self.draw_top_view(painter, center_x, center_y, scale, length, width, text_1, text_2)
        elif self.view_mode == 'Front':
            self.draw_front_view(painter, center_x, center_y, scale, length, thickness, letter_depth, text_1, text_2)
        elif self.view_mode == 'Side':
            self.draw_side_view(painter, center_x, center_y, scale, width, thickness, letter_depth)
        else:  # 3D view
            self.draw_3d_view(painter, center_x, center_y, scale, length, width, thickness, text_1, text_2)

    def draw_top_view(self, painter, cx, cy, scale, length, width, text1, text2):
        """Draw top-down view"""
        # Base plate
        rect_x = cx - (length * scale) / 2
        rect_y = cy - (width * scale) / 2
        rect_w = length * scale
        rect_h = width * scale

        # Draw plate with gradient
        gradient = QLinearGradient(rect_x, rect_y, rect_x + rect_w, rect_y + rect_h)
        gradient.setColorAt(0, QColor(180, 180, 180))
        gradient.setColorAt(1, QColor(220, 220, 220))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawRoundedRect(int(rect_x), int(rect_y), int(rect_w), int(rect_h), 5, 5)

        # Draw text
        painter.setPen(QColor(50, 50, 50))
        font = QFont("Arial", int(scale * 0.3))
        font.setBold(True)
        painter.setFont(font)

        text_y_offset = width * scale / 6
        painter.drawText(
            int(cx - rect_w / 2), int(cy - text_y_offset),
            int(rect_w), int(rect_h / 3),
            Qt.AlignmentFlag.AlignCenter, text1
        )
        painter.drawText(
            int(cx - rect_w / 2), int(cy + text_y_offset - rect_h / 3),
            int(rect_w), int(rect_h / 3),
            Qt.AlignmentFlag.AlignCenter, text2
        )

    def draw_front_view(self, painter, cx, cy, scale, length, thickness, letter_depth, text1, text2):
        """Draw front elevation view"""
        # Base plate
        plate_height = thickness * scale * 10  # Scale up for visibility
        rect_x = cx - (length * scale) / 2
        rect_y = cy - plate_height / 2
        rect_w = length * scale
        rect_h = plate_height

        # Draw base
        gradient = QLinearGradient(rect_x, rect_y, rect_x, rect_y + rect_h)
        gradient.setColorAt(0, QColor(180, 180, 180))
        gradient.setColorAt(1, QColor(140, 140, 140))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawRect(int(rect_x), int(rect_y), int(rect_w), int(rect_h))

        # Draw extruded letters
        letter_height = letter_depth * scale * 10
        letter_y = rect_y - letter_height
        painter.setBrush(QColor(200, 200, 200))
        painter.drawRect(int(rect_x + rect_w * 0.15), int(letter_y), int(rect_w * 0.7), int(letter_height))

        # Labels
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.drawText(int(rect_x), int(rect_y - letter_height - 20), f"{text1} / {text2}")

    def draw_side_view(self, painter, cx, cy, scale, width, thickness, letter_depth):
        """Draw side elevation view"""
        plate_height = thickness * scale * 10
        rect_x = cx - (width * scale) / 2
        rect_y = cy - plate_height / 2
        rect_w = width * scale
        rect_h = plate_height

        # Draw base
        gradient = QLinearGradient(rect_x, rect_y, rect_x, rect_y + rect_h)
        gradient.setColorAt(0, QColor(180, 180, 180))
        gradient.setColorAt(1, QColor(140, 140, 140))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawRect(int(rect_x), int(rect_y), int(rect_w), int(rect_h))

    def draw_3d_view(self, painter, cx, cy, scale, length, width, thickness, text1, text2):
        """Draw isometric 3D view"""
        # Isometric projection angles
        angle = math.radians(30)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # Scale dimensions
        l = length * scale
        w = width * scale
        h = thickness * scale * 5  # Exaggerate height for visibility

        # Define 3D corners
        corners = [
            (-l/2, -w/2, 0),   # 0: bottom-front-left
            ( l/2, -w/2, 0),   # 1: bottom-front-right
            ( l/2,  w/2, 0),   # 2: bottom-back-right
            (-l/2,  w/2, 0),   # 3: bottom-back-left
            (-l/2, -w/2, h),   # 4: top-front-left
            ( l/2, -w/2, h),   # 5: top-front-right
            ( l/2,  w/2, h),   # 6: top-back-right
            (-l/2,  w/2, h),   # 7: top-back-left
        ]

        # Project to 2D isometric
        def project(x, y, z):
            iso_x = cx + (x - y) * cos_a
            iso_y = cy + (x + y) * sin_a - z
            return (int(iso_x), int(iso_y))

        points_2d = [project(x, y, z) for x, y, z in corners]

        # Draw faces with gradients
        # Top face
        gradient = QLinearGradient(points_2d[4][0], points_2d[4][1],
                                  points_2d[6][0], points_2d[6][1])
        gradient.setColorAt(0, QColor(220, 220, 220))
        gradient.setColorAt(1, QColor(180, 180, 180))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        from PyQt6.QtCore import QPoint
        top_face = [QPoint(*points_2d[4]), QPoint(*points_2d[5]),
                   QPoint(*points_2d[6]), QPoint(*points_2d[7])]
        painter.drawPolygon(top_face)

        # Front face
        painter.setBrush(QColor(160, 160, 160))
        front_face = [QPoint(*points_2d[0]), QPoint(*points_2d[1]),
                     QPoint(*points_2d[5]), QPoint(*points_2d[4])]
        painter.drawPolygon(front_face)

        # Right face
        painter.setBrush(QColor(140, 140, 140))
        right_face = [QPoint(*points_2d[1]), QPoint(*points_2d[2]),
                     QPoint(*points_2d[6]), QPoint(*points_2d[5])]
        painter.drawPolygon(right_face)

        # Draw text on top face
        painter.setPen(QColor(50, 50, 50))
        font = QFont("Arial", int(scale * 0.25))
        font.setBold(True)
        painter.setFont(font)
        text_center_x = (points_2d[4][0] + points_2d[6][0]) // 2
        text_center_y = (points_2d[4][1] + points_2d[6][1]) // 2
        painter.drawText(text_center_x - 50, text_center_y - 20, 100, 20,
                        Qt.AlignmentFlag.AlignCenter, text1)
        painter.drawText(text_center_x - 50, text_center_y + 5, 100, 20,
                        Qt.AlignmentFlag.AlignCenter, text2)
