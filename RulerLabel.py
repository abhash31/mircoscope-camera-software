import numpy as np
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PyQt5.QtWidgets import QLabel

class RulerLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)

        self.setFocusPolicy(Qt.StrongFocus)  # Allow key events

        self.ruler_enabled = False
        self.line_tool = False
        self.grayscale_enabled = False
        self.ruler_start = None
        self.ruler_end = None
        self.drawing_ruler = False
        self.ruler_lines = []  # Stored in image coordinates (QPointF)
        self.zoom_factor = 1.0

        self.circle_tool = False
        self.circle_measurements = []  # (center: QPointF, edge: QPointF)

        self.angle_tool = False
        self.angle_points = []  # Temporarily holds points
        self.angle_measurements = []  # Stores list of (A, B, C)

        self.mouse_pos = None  # Used for dynamic third point preview

        self.line_redo_stack = []
        self.circle_redo_stack = []
        self.angle_redo_stack = []

    def set_zoom_factor(self, zoom_factor):
        self.zoom_factor = zoom_factor
        self.update()

    def enable_ruler(self, enabled):
        self.ruler_enabled = enabled
        # if not enabled:
        #     self.clear_rulers()
        self.update()

    def enable_line_tool(self, enabled):
        self.line_tool = enabled
        # if not enabled:
        #     self.clear_rulers()
        self.update()

    def enable_circle_tool(self, enabled):
        self.circle_tool = enabled
        self.update()

    def enable_angle_tool(self, enabled):
        self.angle_tool = enabled
        self.update()

    def enable_grayscale(self, enabled):
        self.grayscale_enabled = enabled

    def clear_rulers(self):
        self.ruler_start = None
        self.ruler_end = None
        self.ruler_lines = []
        self.circle_measurements = []
        self.angle_points = []
        self.angle_measurements = []
        self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        img_pos = event.pos() / self.zoom_factor

        if self.line_tool or self.circle_tool:
            self.ruler_start = img_pos
            self.ruler_end = img_pos
            self.drawing_ruler = True
            self.update()

    def mouseMoveEvent(self, event):
        if (self.line_tool or self.circle_tool) and self.drawing_ruler:
            self.ruler_end = event.pos() / self.zoom_factor
            self.update()

        if self.angle_tool:
            self.mouse_pos = event.pos() / self.zoom_factor
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        img_pos = event.pos() / self.zoom_factor

        if self.drawing_ruler:
            if self.ruler_start and img_pos:
                if self.line_tool:
                    self.ruler_lines.append((QPointF(self.ruler_start), QPointF(img_pos)))
                elif self.circle_tool:
                    self.circle_measurements.append((QPointF(self.ruler_start), QPointF(img_pos)))
            self.drawing_ruler = False
            self.update()

        elif self.angle_tool:
            self.angle_points.append(QPointF(img_pos))
            if len(self.angle_points) == 3:
                self.angle_measurements.append(tuple(self.angle_points))
                self.angle_points = []
            self.mouse_pos = None
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw rulers fixed to the window size
        # self.draw_scale_rulers(painter)

        # Draw saved measurements (lines, circles, angles)
        self.draw_measurement_rulers(painter)

        # --- Tool-specific previews ---
        # Preview active line or circle tool
        if self.drawing_ruler and self.ruler_start and self.ruler_end:
            if self.line_tool:
                self.draw_single_ruler(painter, self.ruler_start, self.ruler_end, QColor(255, 255, 0))
            elif self.circle_tool:
                self.draw_circle_measurement(painter, self.ruler_start, self.ruler_end, QColor(255, 255, 0))

        # Preview angle tool clicks (1 or 2 points placed)
        if self.angle_tool:
            pen = QPen(QColor(255, 255, 0), 2, Qt.DashLine)
            painter.setPen(pen)
            scaled_points = [pt * self.zoom_factor for pt in self.angle_points]

            if len(scaled_points) == 1:
                painter.drawEllipse(scaled_points[0], 3, 3)
            elif len(scaled_points) == 2:
                painter.drawLine(scaled_points[0], scaled_points[1])

            # Dynamic third-point preview for angle
            if len(self.angle_points) == 2 and self.mouse_pos:
                a, b = self.angle_points
                c = self.mouse_pos
                self.draw_angle_measurement(painter, a, b, c, QColor(200, 200, 0))

    def draw_scale_rulers(self, painter):
        pen = QPen(QColor(255, 255, 255, 200), 1)
        painter.setPen(pen)
        font = QFont()
        font.setPixelSize(8)
        painter.setFont(font)

        w, h = self.width(), self.height()  # Widget size
        tick_len = 8
        spacing = 50  # Default spacing for the ticks

        # Adjust spacing based on zoom factor
        adjusted_spacing = max(10, int(spacing / self.zoom_factor))  # Zoom effect on tick spacing
        small_spacing = max(5, int(10 / self.zoom_factor))  # Smaller spacing for detailed zoom

        # **Top Ruler (fixed to the window size)**
        painter.fillRect(0, 0, w, 20, QColor(0, 0, 0, 100))  # Background for the ruler

        for x in range(0, w, adjusted_spacing):
            painter.drawLine(x, 0, x, tick_len)
            if x > 0:  # Don't draw 0 at the edge
                actual_pixel = int(x)  # Actual pixel value considering zoom
                painter.setPen(QPen(Qt.white))
                painter.drawText(x + 2, 12, str(actual_pixel))  # Draw the tick value
                painter.setPen(pen)

        # Draw smaller ticks for zoomed-in view
        for x in range(0, w, small_spacing):
            painter.drawLine(x, 0, x, tick_len // 2)

        # **Left Ruler (fixed to the window size)**
        painter.fillRect(0, 0, 20, h, QColor(0, 0, 0, 100))  # Background for the left ruler

        for y in range(0, h, adjusted_spacing):
            painter.drawLine(0, y, tick_len, y)
            if y > 0:  # Don't draw 0 at the edge
                actual_pixel = int(y)  # Actual pixel value considering zoom
                painter.setPen(QPen(Qt.white))
                painter.save()
                painter.translate(15, y + 5)
                painter.rotate(-90)
                painter.drawText(0, 0, str(actual_pixel))
                painter.restore()
                painter.setPen(pen)

        for y in range(0, h, small_spacing):
            painter.drawLine(0, y, tick_len // 2, y)

    def draw_measurement_rulers(self, painter):
        if not self.ruler_enabled:
            return

        # Draw all lines
        for start, end in self.ruler_lines:
            self.draw_single_ruler(painter, start, end, QColor(0, 255, 0))

        # Draw all circles
        for center, edge in self.circle_measurements:
            self.draw_circle_measurement(painter, center, edge, QColor(0, 200, 255))

        # Draw angle measurements
        for a, b, c in self.angle_measurements:
            self.draw_angle_measurement(painter, a, b, c, QColor(255, 100, 0))

        # Draw current (active) tool
        if self.drawing_ruler and self.ruler_start and self.ruler_end:
            if self.line_tool:
                self.draw_single_ruler(painter, self.ruler_start, self.ruler_end, QColor(255, 255, 0))
            elif self.circle_tool:
                self.draw_circle_measurement(painter, self.ruler_start, self.ruler_end, QColor(255, 255, 0))

    def draw_single_ruler(self, painter, start_img, end_img, color):
        pen = QPen(color, 2)
        painter.setPen(pen)

        # Convert to widget coords
        start = start_img * self.zoom_factor
        end = end_img * self.zoom_factor

        # Draw main line
        painter.drawLine(start, end)

        # Draw end markers
        marker_size = 6
        painter.drawEllipse(start, marker_size, marker_size)
        painter.drawEllipse(end, marker_size, marker_size)

        # Calculate image-space distance
        dx = end_img.x() - start_img.x()
        dy = end_img.y() - start_img.y()
        distance = np.hypot(dx, dy)

        # Text at midpoint
        mid_x = (start.x() + end.x()) / 2
        mid_y = (start.y() + end.y()) / 2
        text = f"{distance:.1f}px"

        font = QFont()
        font.setPixelSize(10)
        font.setBold(True)
        painter.setFont(font)

        fm = painter.fontMetrics()
        text_rect = fm.boundingRect(text)
        text_rect = QRectF(text_rect).adjusted(-4, -2, 4, 2)
        text_rect.moveCenter(QPointF(mid_x, mid_y - 15))

        painter.fillRect(text_rect, QColor(0, 0, 0, 150))
        painter.setPen(Qt.white)
        painter.drawText(text_rect, Qt.AlignCenter, text)

    def draw_circle_measurement(self, painter, center_img, edge_img, color):
        pen = QPen(color, 2)
        painter.setPen(pen)

        center = center_img * self.zoom_factor
        edge = edge_img * self.zoom_factor

        # Radius in image space
        radius = np.hypot(edge_img.x() - center_img.x(), edge_img.y() - center_img.y())
        radius_scaled = radius * self.zoom_factor

        # Draw the circle
        painter.drawEllipse(center, radius_scaled, radius_scaled)

        # Draw center point
        painter.drawEllipse(center, 4, 4)

        # Label radius
        text = f"r = {radius:.1f}px"
        font = QFont()
        font.setPixelSize(10)
        font.setBold(True)
        painter.setFont(font)

        fm = painter.fontMetrics()
        text_rect = fm.boundingRect(text)
        text_rect = QRectF(text_rect).adjusted(-4, -2, 4, 2)
        text_rect.moveCenter(center + QPointF(radius_scaled + 20, 0))  # offset from edge

        painter.fillRect(text_rect, QColor(0, 0, 0, 150))
        painter.setPen(Qt.white)
        painter.drawText(text_rect, Qt.AlignCenter, text)

    def draw_angle_measurement(self, painter, a_img, b_img, c_img, color):
        pen = QPen(color, 2)
        painter.setPen(pen)

        a = a_img * self.zoom_factor
        b = b_img * self.zoom_factor
        c = c_img * self.zoom_factor

        # Draw lines AB and BC
        painter.drawLine(b, a)
        painter.drawLine(b, c)

        # Draw points
        marker_size = 5
        painter.drawEllipse(a, marker_size, marker_size)
        painter.drawEllipse(b, marker_size, marker_size)
        painter.drawEllipse(c, marker_size, marker_size)

        # Compute angle using dot product
        ba = np.array([a_img.x() - b_img.x(), a_img.y() - b_img.y()])
        bc = np.array([c_img.x() - b_img.x(), c_img.y() - b_img.y()])

        dot_product = np.dot(ba, bc)
        norm_ba = np.linalg.norm(ba)
        norm_bc = np.linalg.norm(bc)

        if norm_ba > 0 and norm_bc > 0:
            cosine_angle = np.clip(dot_product / (norm_ba * norm_bc), -1.0, 1.0)
            angle_rad = np.arccos(cosine_angle)
            angle_deg = np.degrees(angle_rad)
        else:
            angle_deg = 0.0

        # Show angle label
        text = f"{angle_deg:.1f}°"
        font = QFont()
        font.setPixelSize(10)
        font.setBold(True)
        painter.setFont(font)

        fm = painter.fontMetrics()
        text_rect = fm.boundingRect(text)
        text_rect = QRectF(text_rect).adjusted(-4, -2, 4, 2)
        text_rect.moveCenter(b + QPointF(15, -15))

        painter.fillRect(text_rect, QColor(0, 0, 0, 150))
        painter.setPen(Qt.white)
        painter.drawText(text_rect, Qt.AlignCenter, text)

    def keyPressEvent(self, event):
        is_undo = (
                event.key() == Qt.Key_Z and
                (event.modifiers() == Qt.ControlModifier or event.modifiers() == Qt.MetaModifier)
        )

        is_redo = (
                event.key() == Qt.Key_Y and
                (event.modifiers() == Qt.ControlModifier or event.modifiers() == Qt.MetaModifier)
        )

        if is_undo:
            if self.line_tool and self.ruler_lines:
                item = self.ruler_lines.pop()
                self.line_redo_stack.append(item)
            elif self.circle_tool and self.circle_measurements:
                item = self.circle_measurements.pop()
                self.circle_redo_stack.append(item)
            elif self.angle_tool and self.angle_measurements:
                item = self.angle_measurements.pop()
                self.angle_redo_stack.append(item)
            self.update()

        elif is_redo:
            if self.line_tool and self.line_redo_stack:
                item = self.line_redo_stack.pop()
                self.ruler_lines.append(item)
            elif self.circle_tool and self.circle_redo_stack:
                item = self.circle_redo_stack.pop()
                self.circle_measurements.append(item)
            elif self.angle_tool and self.angle_redo_stack:
                item = self.angle_redo_stack.pop()
                self.angle_measurements.append(item)
            self.update()
        else:
            super().keyPressEvent(event)