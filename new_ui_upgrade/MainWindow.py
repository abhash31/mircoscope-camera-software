import cv2
import datetime
import os
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtWidgets import (
    QMainWindow, QToolBox, QDockWidget,
    QSizePolicy, QFileDialog,
    QMessageBox, QScrollArea,
    QWidget, QVBoxLayout,
    QLabel, QPushButton, QSlider, QHBoxLayout, QSpinBox,
    QCheckBox, QGroupBox, QComboBox, QStackedLayout, QToolButton, QLayoutItem, QToolBar, QListWidget, QStyle, QLineEdit
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QRect
from CameraWorker import CameraWorkerThread
from RulerLabel import RulerLabel
from new_ui_upgrade.utils.style_sheet import active_colors, inactive_colors
from new_ui_upgrade.v_line import VLine
from ui.histogram_panel import histogram_panel
from ui.menu_bar import menu_bar

W = 10

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.camera = CameraWorkerThread()
        self.latest_frame = None
        self.current_image_path = None
        self.camera_active = False
        self.recording = False
        self.setWindowTitle("Microscope Camera Software")
        self.brightness_value = 50
        self.contrast_value = 50
        self.exposure_value = 50
        self.zoom_value = 2

        # Create output directory
        self.output_dir = "saved_frames"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        menu_bar(self) # create menu bar

        self.central_label = RulerLabel()
        self.central_label.setAlignment(Qt.AlignCenter)
        self.central_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.central_label.setScaledContents(False)

        self.logo_label = QLabel()

        svg_renderer = QSvgRenderer("assets/logo.svg")
        pixmap = QPixmap(400, 200)
        pixmap.fill(Qt.transparent)  # Transparent background
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()

        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        # Stack them
        stack = QWidget()
        self.stack_layout = QStackedLayout(stack)
        self.stack_layout.addWidget(self.logo_label)  # background
        self.stack_layout.addWidget(self.central_label)  # foreground

        self.stack_layout.setCurrentWidget(self.logo_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(stack)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)

        # Central camera display with ruler capabilities
        self.fixed_ruler_label = RulerLabel()  # Fixed ruler
        self.fixed_ruler_label.setAlignment(Qt.AlignCenter)
        self.fixed_ruler_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.fixed_ruler_label.setFixedHeight(W)

        # Create the toolbox
        self.top_toolbox = QToolBox()
        self.top_toolbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.top_toolbox.setMaximumHeight(200)
        self.top_toolbox.setVisible(False)  # hidden initially

        panel_layout = QToolBar()
        panel_layout.setMovable(False)
        panel_layout.setIconSize(QSize(23, 23))

        self.start_camera = QToolButton()
        self.start_camera.setIcon(QIcon("assets/video_inactive.svg"))
        self.start_camera.setIconSize(QSize(W, W))
        self.start_camera.setText("Start")
        self.start_camera.setCheckable(True)
        self.start_camera.clicked.connect(self.start_stop_camera_feed)

        self.camera_snap = QToolButton()
        self.camera_snap.setIcon(QIcon("assets/camera_inactive.svg"))
        self.camera_snap.setIconSize(QSize(W, W))
        self.camera_snap.setText("Snapshot")
        self.camera_snap.setCheckable(True)
        self.camera_snap.clicked.connect(self.save_current_frame)

        self.record_btn = QToolButton()
        self.record_btn.setIcon(QIcon("assets/record_inactive.svg"))
        self.record_btn.setIconSize(QSize(W, W))
        self.record_btn.setText("Record")
        self.record_btn.setCheckable(True)
        self.record_btn.clicked.connect(self.start_recording)

        self.stop_record_btn = QToolButton()
        self.stop_record_btn.setIcon(QIcon("assets/record_stop_inactive.svg"))
        self.stop_record_btn.setIconSize(QSize(W, W))
        self.stop_record_btn.setText("Stop-Record")
        self.stop_record_btn.setCheckable(True)
        self.stop_record_btn.clicked.connect(self.stop_recording)

        # Add buttons
        self.line_button = QToolButton()
        self.line_button.setIcon(QIcon("assets/line_inactive.svg"))
        self.line_button.setIconSize(QSize(W, W))
        self.line_button.setText("Line")
        self.line_button.setCheckable(True)
        self.line_button.clicked.connect(self.toggle_line_tool)

        self.circle_button = QToolButton()
        self.circle_button.setIcon(QIcon("assets/circle_inactive.svg"))
        self.circle_button.setIconSize(QSize(W, W))
        self.circle_button.setText("Circle")
        self.circle_button.setCheckable(True)
        self.circle_button.clicked.connect(self.toggle_circle_tool)

        self.angle_button = QToolButton()
        self.angle_button.setIcon(QIcon("assets/angle_inactive.svg"))
        self.angle_button.setIconSize(QSize(W, W))
        self.angle_button.setText("Angle")
        self.angle_button.setCheckable(True)
        self.angle_button.clicked.connect(self.toggle_angle_tool)

        self.zoom_in = QToolButton()
        self.zoom_in.setIcon(QIcon("assets/zoom_in.svg"))
        self.zoom_in.setIconSize(QSize(W, W))
        self.zoom_in.setText("Zoom in")
        self.zoom_in.clicked.connect(self.zoom_in_camera)

        self.zoom_out = QToolButton()
        self.zoom_out.setIcon(QIcon("assets/zoom_out.svg"))
        self.zoom_out.setIconSize(QSize(W, W))
        self.zoom_out.setText("Zoom out")
        self.zoom_out.clicked.connect(self.zoom_out_camera)

        panel_layout.addWidget(self.start_camera)
        panel_layout.addWidget(self.camera_snap)
        panel_layout.addWidget(self.record_btn)
        panel_layout.addWidget(self.stop_record_btn)
        panel_layout.addWidget(self.line_button)
        panel_layout.addWidget(self.circle_button)
        panel_layout.addWidget(self.angle_button)
        panel_layout.addWidget(self.zoom_in)
        panel_layout.addWidget(self.zoom_out)

        central_container = QWidget()
        layout = QVBoxLayout()

        self.addToolBar(panel_layout)

        central_container.setLayout(layout)
        self.setCentralWidget(central_container)

        # self.setup_top_toolbox_panel()

        # Toolbox
        self.left_toolbox = QToolBox()
        self.left_toolbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.right_toolbox = QToolBox()
        self.right_toolbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.bottom_toolbox = QToolBox()
        self.bottom_toolbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.left_bottom_toolbox = QToolBox()
        self.left_bottom_toolbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.right_bottom_toolbox = QToolBox()
        self.right_bottom_toolbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # TODO: camera controls panel
        self.create_left_properties_panel()
        self.create_right_properties_panel()
        self.create_bottom_properties_panel()
        self.create_left_bottom_properties_panel()

        histogram_panel(self)

        # Dock widget setup
        left_dock_content = QWidget()
        right_dock_content = QWidget()
        bottom_dock_content = QWidget()
        right_bottom_dock_content = QWidget()
        left_bottom_dock_content = QWidget()

        left_dock_layout = QVBoxLayout()
        right_dock_layout = QVBoxLayout()
        bottom_dock_layout = QHBoxLayout()
        right_bottom_dock_layout = QVBoxLayout()
        left_bottom_dock_layout = QVBoxLayout()

        left_dock_layout.setContentsMargins(1,1,1,1)
        right_dock_layout.setContentsMargins(1,1,1,1)
        bottom_dock_layout.setContentsMargins(1,1,1,1)
        right_bottom_dock_layout.setContentsMargins(1,1,1,1)
        left_bottom_dock_layout.setContentsMargins(1,1,1,1)

        left_dock_layout.addWidget(self.left_toolbox)
        right_dock_layout.addWidget(self.right_toolbox)
        bottom_dock_layout.addWidget(self.bottom_toolbox)
        right_bottom_dock_layout.addWidget(self.right_bottom_toolbox)
        left_bottom_dock_layout.addWidget(self.left_bottom_toolbox)

        left_dock_content.setLayout(left_dock_layout)
        right_dock_content.setLayout(right_dock_layout)
        bottom_dock_content.setLayout(bottom_dock_layout)
        right_bottom_dock_content.setLayout(right_bottom_dock_layout)
        left_bottom_dock_content.setLayout(left_bottom_dock_layout)

        self.left_dock = QDockWidget("Device", self)
        self.right_dock = QDockWidget("Properties", self)
        self.bottom_dock = QDockWidget("Features Overview", self)

        # self.right_bottom_dock = QDockWidget("Other Properties", self)
        self.left_bottom_dock = QDockWidget("Advanced Properties", self)

        self.left_dock.setWidget(left_dock_content)
        self.right_dock.setWidget(right_dock_content)
        self.bottom_dock.setWidget(bottom_dock_content)
        # self.right_bottom_dock.setWidget(right_bottom_dock_content)
        self.left_bottom_dock.setWidget(left_bottom_dock_content)

        self.left_dock.setMaximumWidth(250)
        self.right_dock.setMinimumWidth(350)
        self.bottom_dock.setMinimumHeight(200)
        # self.right_bottom_dock.setMinimumWidth(350)
        self.left_bottom_dock.setMinimumWidth(250)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.right_bottom_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_bottom_dock)

        self.left_dock.setFeatures(QDockWidget.DockWidgetMovable)
        self.right_dock.setFeatures(QDockWidget.DockWidgetMovable)
        self.bottom_dock.setFeatures(QDockWidget.DockWidgetMovable)
        # self.right_bottom_dock.setFeatures(QDockWidget.DockWidgetMovable)
        self.left_bottom_dock.setFeatures(QDockWidget.DockWidgetMovable)
        # Disable controls initially
        self.toggle_controls(False)

        layout.addWidget(self.scroll_area)  # main content

        self.showMaximized()

        # self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_ruler_position)

    def zoom_in_camera(self):
        zoom_value = self.zoom_slider.value()
        if zoom_value<100:
            zoom_value += 10
            self.zoom_slider.setValue(zoom_value)

    def zoom_out_camera(self):
        zoom_value = self.zoom_slider.value()
        if zoom_value > 40:
            zoom_value -= 10
            self.zoom_slider.setValue(zoom_value)

    def update_histogram(self):
        """Update the histogram and display it in the toolbox (and bottom label if present)."""
        if self.latest_frame is None:
            return

        # Convert QImage -> numpy RGB
        cv_image = self.latest_frame.convertToFormat(QImage.Format_RGB888)
        ptr = cv_image.bits()
        ptr.setsize(cv_image.byteCount())

        # Number of bytes per pixel in RGB888 format is 3 (1 byte for R, G, and B)
        # The image width and height should be correct for reshaping into a 3D array (height, width, 3)
        width = cv_image.width()
        height = cv_image.height()

        # Correct reshaping based on width and height (using 3 channels for RGB)
        # img = np.array(ptr, dtype=np.uint8).reshape((height, width, 3))
        bytes_per_line = cv_image.bytesPerLine()
        # Convert buffer to 1D array
        img_1d = np.frombuffer(ptr, dtype=np.uint8, count=bytes_per_line * height)
        # Reshape to (height, bytes_per_line)
        img_2d = img_1d.reshape((height, bytes_per_line))
        # Slice to width pixels (width * 3 because RGB888)
        img = img_2d[:, :width * 3].reshape((height, width, 3))

        # Draw hist image (H=200, W=256)
        H, W = 200, 256
        hist_img = np.zeros((H, W, 3), dtype=np.uint8)

        # Channels in img are RGB (0=R,1=G,2=B). Choose colors to draw in RGB space.
        channel_info = [
            (0, (255, 0, 0)),  # R channel drawn in red
            (1, (0, 255, 0)),  # G channel drawn in green
            (2, (0, 0, 255)),  # B channel drawn in blue
        ]

        for ch, color in channel_info:
            hist = cv2.calcHist([img], [ch], None, [256], [0, 256])
            cv2.normalize(hist, hist, 0, H - 1, cv2.NORM_MINMAX)
            hist = hist.flatten().astype(int)
            for x in range(1, 256):
                cv2.line(hist_img,
                         (x - 1, H - 1 - hist[x - 1]),
                         (x, H - 1 - hist[x]),
                         color, 1)

        # Convert numpy -> QPixmap (copy so QImage owns its data)
        qimg = QImage(hist_img.data, W, H, 3 * W, QImage.Format_RGB888).copy()
        pm = QPixmap.fromImage(qimg)

        # Show in toolbox panel
        if hasattr(self, "histogram_panel_label"):
            self.histogram_panel_label.setPixmap(pm)

        # If you also bring back the bottom histogram label:
        if hasattr(self, "histogram_label"):
            self.histogram_label.setPixmap(pm)

    def update_ruler_position(self):
        scroll_pos = self.scroll_area.verticalScrollBar().value()

        self.fixed_ruler_label.move(0, scroll_pos)  # Keep the ruler aligned with the scroll


    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.latest_frame:
            self.rescale_latest_frame()
            scaled_image = self.latest_frame.scaled(
                self.central_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.central_label.setPixmap(QPixmap.fromImage(scaled_image))

    def rescale_latest_frame(self):
        if self.latest_frame:
            label_size = self.central_label.size()
            scaled_image = self.latest_frame.scaled(
                label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.central_label.setPixmap(QPixmap.fromImage(scaled_image))

    def on_zoom_percent_changed(self, value):
        if self.latest_frame:
            percent = value
            scale_factor = percent / 10.0
            new_width = int(self.latest_frame.width() * scale_factor)
            new_height = int(self.latest_frame.height() * scale_factor)
            scaled_image = self.latest_frame.scaled(
                new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.central_label.setPixmap(QPixmap.fromImage(scaled_image))
            self.central_label.resize(new_width, new_height)  # ← must resize label explicitly
            self.central_label.set_zoom_factor(scale_factor)

    def create_section(self, title):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton(f"Action 1 in {title}"))
        layout.addWidget(QPushButton(f"Action 2 in {title}"))
        layout.addStretch()
        widget.setLayout(layout)
        return widget


    def open_image(self):
        """Open an image file"""
        # Stop camera if running
        if self.camera_active:
            self.stop_camera()

        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Image",
            "",
            "Image files (*.png *.jpg *.jpeg *.bmp *.tiff *.gif)"
        )

        if filename:
            self.current_image_path = filename
            # Load and display image
            pixmap = QPixmap(filename)
            self.reset_controls_to_default()

            if not pixmap.isNull():
                self.latest_frame = pixmap.toImage()
                self.on_zoom_percent_changed(self.zoom_slider.value())
                self.toggle_controls(True)
                self.update_zoom_factor_for_ruler()
                self.update_histogram()
                self.stack_layout.setCurrentWidget(self.central_label)
            else:
                QMessageBox.warning(self, "Error", "Could not load the selected image.")


    def toggle_controls(self, enable: bool):
        controls = [ # TODO: update these
            # self.slider, self.brightness_spinbox,
            # self.contrast_slider, self.contrast_spinbox,
            # self.exposure_slider, self.exposure_spinbox,
            # self.grayscale_checkbox,
            # self.zoom_slider, self.zoom_spinbox,
            # self.format_combo,
        ]
        for w in controls:
            w.setEnabled(enable)

    def update_brightness(self, value):
        self.brightness_value = value
        if self.camera:
            self.camera.set_brightness(value)
        elif self.current_image_path:
            self.apply_image_adjustments()

    def update_contrast(self, value):
        self.contrast_value = value
        if self.camera:
            self.camera.set_contrast(value)
        elif self.current_image_path:
            self.apply_image_adjustments()

    def update_exposure(self, value):
        self.exposure_value = value
        if self.camera:
            self.camera.set_exposure(value)
        elif self.current_image_path:
            self.apply_image_adjustments()

    def update_zoom(self, value):
        self.zoom_value = value
        zoom_factor = value / 10.0  # Convert to 1.0x - 3.0x range
        self.zoom_label.setText(f"{zoom_factor:.1f}x")

        if self.camera:
            self.camera.set_zoom(value)
        elif self.current_image_path:
            self.apply_image_adjustments()

        # Update ruler zoom factor
        self.update_zoom_factor_for_ruler()

    def update_zoom_factor_for_ruler(self):
        """Update the zoom factor for accurate ruler measurements"""
        zoom_factor = self.zoom_value / 10.0
        self.central_label.set_zoom_factor(zoom_factor)

    def apply_image_adjustments(self):
        """Apply adjustments to static image"""
        if not self.current_image_path:
            return

        # Load original image
        cv_image = cv2.imread(self.current_image_path)
        if cv_image is None:
            return

        # Apply brightness and contrast
        brightness_factor = (self.brightness_value - 50) * 2
        contrast_factor = (self.contrast_value - 50) / 50.0
        adjusted_image = cv2.convertScaleAbs(cv_image, alpha=1 + contrast_factor, beta=brightness_factor)

        # Apply exposure (simplified)
        exposure_factor = (self.exposure_value - 50) / 50.0
        adjusted_image = cv2.convertScaleAbs(adjusted_image, alpha=1.0, beta=exposure_factor * 50)

        # Apply grayscale if enabled
        if self.grayscale_checkbox.isChecked():
            adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)
            adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_GRAY2BGR)

        # Convert to QImage and update latest_frame
        color_swapped_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)
        qt_image = QImage(color_swapped_image.data,
                          color_swapped_image.shape[1],
                          color_swapped_image.shape[0],
                          color_swapped_image.strides[0],
                          QImage.Format_RGB888)

        self.latest_frame = qt_image

        # 🔥 Apply zoom after updating image
        self.on_zoom_percent_changed(self.zoom_slider.value())
        self.update_histogram()

    def update_awb_checkbox(self, state):
        if self.camera:
            self.camera.set_auto_awb(state == Qt.Checked)

    def update_grayscale(self, state):
        grayscale_enabled = state == Qt.Checked
        self.central_label.enable_grayscale(grayscale_enabled)
        if self.camera:
            self.camera.set_grayscale(grayscale_enabled)
        elif self.current_image_path:
            self.apply_image_adjustments()

    def toggle_ruler_from_menu(self, checked):
        """Toggle ruler from menu bar"""
        self.central_label.enable_ruler(checked)
        self.line_button.setChecked(False)
        self.circle_button.setChecked(False)
        self.angle_button.setChecked(False)

    def toggle_line_tool(self, checked):
        if not self.camera_active:
            self.line_button.setChecked(False)
            return
        if checked:
            self.central_label.enable_line_tool(checked)
            self.line_button.setIcon(QIcon("assets/line_active"))
        else:
            self.central_label.enable_line_tool(checked)
            self.line_button.setIcon(QIcon("assets/line_inactive"))

        self.circle_button.setIcon(QIcon("assets/circle_inactive"))
        self.angle_button.setIcon(QIcon("assets/angle_inactive"))
        self.circle_button.setChecked(False)
        self.angle_button.setChecked(False)
        self.central_label.enable_circle_tool(False)
        self.central_label.enable_angle_tool(False)

    def toggle_circle_tool(self, checked):
        if not self.camera_active:
            self.circle_button.setChecked(False)

            return

        if checked:
            self.central_label.enable_circle_tool(checked)
            self.circle_button.setIcon(QIcon("assets/circle_active"))
        else:
            self.central_label.enable_circle_tool(checked)
            self.circle_button.setIcon(QIcon("assets/circle_inactive"))

        self.line_button.setIcon(QIcon("assets/line_inactive"))
        self.angle_button.setIcon(QIcon("assets/angle_inactive"))
        self.angle_button.setChecked(False)
        self.line_button.setChecked(False)
        self.central_label.enable_line_tool(False)
        self.central_label.enable_angle_tool(False)

    def toggle_angle_tool(self, checked):
        if not self.camera_active:
            self.angle_button.setChecked(False)
            return

        if checked:
            self.central_label.enable_angle_tool(checked)
            self.angle_button.setIcon(QIcon("assets/angle_active"))
        else:
            self.central_label.enable_angle_tool(checked)
            self.angle_button.setIcon(QIcon("assets/angle_inactive"))

        self.line_button.setIcon(QIcon("assets/line_inactive"))
        self.circle_button.setIcon(QIcon("assets/circle_inactive"))
        self.circle_button.setChecked(False)
        self.line_button.setChecked(False)
        self.central_label.enable_line_tool(False)
        self.central_label.enable_circle_tool(False)

    def clear_all_rulers(self):
        self.central_label.clear_rulers()

    def save_current_frame(self):
        if self.latest_frame is None or self.camera_active==False:
            QMessageBox.warning(self, "Warning", "No frame to save!")
            return

        # Create a pixmap of the same size as the label
        pixmap = QPixmap(self.central_label.size())
        self.central_label.render(pixmap)  # Renders the widget (with overlays) onto the pixmap

        # Generate file path
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_format = self.format_combo.currentText().lower()
        filename = f"cryonano_{timestamp}.{file_format}"
        filepath = os.path.join(self.output_dir, filename)

        # Save the pixmap using Qt
        if file_format in ("png", "jpg", "jpeg", "bmp"):
            if pixmap.save(filepath):
                QMessageBox.information(self, "Success", f"Overlay saved as:\n{filepath}")
            else:
                QMessageBox.warning(self, "Error", "Failed to save overlay!")
        else:
            QMessageBox.warning(self, "Error", f"Unsupported format: {file_format}")

    def start_stop_camera_feed(self):
        if not self.camera_active:
            self.reset_controls_to_default()
            self.current_image_path = None
            self.camera = CameraWorkerThread()
            self.camera.change_pixmap_signal.connect(self.update_image)
            self.camera.set_brightness(self.brightness_value)
            self.camera.set_contrast(self.contrast_value)
            self.camera.set_exposure(self.exposure_value)
            self.camera.set_zoom(self.zoom_value)
            # self.camera.set_auto_awb(self.awb_checkbox.isChecked())
            self.camera.set_grayscale(self.grayscale_checkbox.isChecked())
            self.camera.start()
            self.camera_active = True
            self.toggle_controls(True)
            self.toggle_ruler_from_menu(False)
            self.line_button.setChecked(False)
            self.circle_button.setChecked(False)
            self.angle_button.setChecked(False)
            self.update_histogram()
            self.stack_layout.setCurrentWidget(self.central_label)
            self.start_camera.setIcon(QIcon("assets/video_active.svg"))
            # self.start_recording()  # Start recording when camera starts
        else:
            self.stop_camera()
            self.central_label.clear()
            self.toggle_controls(False)
            self.stack_layout.setCurrentWidget(self.logo_label)
            self.start_camera.setIcon(QIcon("assets/video_inactive.svg"))
            if self.recording:
                self.stop_recording()  # Stop recording when camera stops

    def start_recording(self):
        if self.camera_active and not self.recording:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"recording_{timestamp}.mp4"
            filepath = os.path.join(self.output_dir, filename)

            # Get frame dimensions from the camera
            frame_width = int(self.latest_frame.width())
            frame_height = int(self.latest_frame.height())
            self.video_writer = cv2.VideoWriter(filepath, fourcc, 30.0, (frame_width, frame_height))
            self.recording = True
            # self.record_btn.setIcon(QIcon('assets/record_active.svg'))
            self.stop_record_btn.setIcon('assets/record_stop_active.svg')
            print(f"Recording started: {filepath}")
            self.record_button.setText("Stop Record")
            self.record_button.setIcon(QIcon('assets/stop.png'))
            self.record_btn.setText("Stop")
        elif self.recording:
            self.stop_recording()
            self.record_button.setText("Start Record")
            self.record_button.setIcon(QIcon('assets/play.png'))
        else:
            QMessageBox.warning(self, "Failure", f"Start Camera to record")

    def stop_recording(self):
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            self.recording = False
            print("Recording stopped.")
            self.record_btn.setIcon(QIcon('assets/record_inactive.svg'))
            QMessageBox.information(self, "Success", f"Recording saved")

    def stop_camera(self):
        """Stop camera and clean up"""
        if self.camera and self.camera_active:
            self.camera.stop()
            self.camera.wait()
            self.camera.change_pixmap_signal.disconnect()
            self.camera = None
            self.camera_active = False

    def update_image(self, image):
        self.latest_frame = image
        image = image.convertToFormat(QImage.Format_RGB888)
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        img_data = np.array(ptr).reshape(image.height(), image.width(), 3)
        img_data_bgr = img_data[..., ::-1]

        if self.recording and self.video_writer:
            self.video_writer.write(img_data_bgr)

        # zoom_text = self.zoom_combo.currentText()
        # percent = int(zoom_text.strip('%'))
        scale_factor = self.zoom_slider.value() / 100.0
        new_width = int(image.width() * scale_factor)
        new_height = int(image.height() * scale_factor)

        scaled_image = image.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.central_label.setPixmap(QPixmap.fromImage(scaled_image))
        self.central_label.resize(new_width, new_height)
        self.central_label.set_zoom_factor(scale_factor)
        self.update_histogram()

    def closeEvent(self, event):
        """Clean up when closing application"""
        if self.camera_active:
            self.stop_camera()
        event.accept()

    def helper_reset_slider(self, slider, value):
        slider.blockSignals(True)
        slider.setValue(value)
        slider.setSliderPosition(value)  # directly set thumb
        slider.blockSignals(False)
        slider.update()
        slider.repaint()

    def reset_controls_to_default(self):
        """Reset all UI controls and internal values to default"""

        # Disconnect paired connections to prevent interference
        try:
            self.slider.valueChanged.disconnect(self.brightness_spinbox.setValue)
            self.brightness_spinbox.valueChanged.disconnect(self.slider.setValue)

            self.contrast_slider.valueChanged.disconnect(self.contrast_spinbox.setValue)
            self.contrast_spinbox.valueChanged.disconnect(self.contrast_slider.setValue)

            self.exposure_slider.valueChanged.disconnect(self.exposure_spinbox.setValue)
            self.exposure_spinbox.valueChanged.disconnect(self.exposure_slider.setValue)
        except TypeError:
            # Already disconnected
            pass

        # Set values directly
        self.helper_reset_slider(self.slider, 50)
        self.helper_reset_slider(self.contrast_slider, 50)
        self.helper_reset_slider(self.exposure_slider, 50)

        self.brightness_spinbox.setValue(50)
        self.contrast_spinbox.setValue(50)
        self.exposure_spinbox.setValue(50)

        # Reconnect signals
        self.slider.valueChanged.connect(self.brightness_spinbox.setValue)
        self.brightness_spinbox.valueChanged.connect(self.slider.setValue)

        self.contrast_slider.valueChanged.connect(self.contrast_spinbox.setValue)
        self.contrast_spinbox.valueChanged.connect(self.contrast_slider.setValue)

        self.exposure_slider.valueChanged.connect(self.exposure_spinbox.setValue)
        self.exposure_spinbox.valueChanged.connect(self.exposure_slider.setValue)

        # Repaint sliders to update visual thumb positions
        self.slider.repaint()
        self.contrast_slider.repaint()
        self.exposure_slider.repaint()

        # Reset internal values
        self.brightness_value = 50
        self.contrast_value = 50
        self.exposure_value = 50

        # self.zoom_combo.setCurrentText("100%")
        self.zoom_value = 2

        # self.awb_checkbox.setChecked(True)
        self.grayscale_checkbox.setChecked(False)
        self.format_combo.setCurrentText("PNG")

        self.central_label.clear_rulers()
        self.central_label.set_zoom_factor(1.0)

        self.toggle_ruler_from_menu(False)
        # self.toggle_top_toolbox(False)
        self.line_button.setChecked(False)
        self.circle_button.setChecked(False)
        self.angle_button.setChecked(False)

    def on_zoom_slider_changed(self, value):
        """ Update zoom and zoom factor in RulerLabel. """
        self.zoom_value = value
        scale = value / 100.0  # Convert zoom value to scale

        # Update zoom for the camera and the ruler
        if self.camera:
            self.camera.set_zoom(value)
        elif self.current_image_path:
            self.apply_image_adjustments()  # This will re-render the image with zoom

        # Apply scaling immediately to the display and ruler
        if self.latest_frame:
            new_w = int(self.latest_frame.width() * scale)
            new_h = int(self.latest_frame.height() * scale)
            scaled = self.latest_frame.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.central_label.setPixmap(QPixmap.fromImage(scaled))
            self.central_label.resize(new_w, new_h)
            self.central_label.set_zoom_factor(scale)

        # Update the ruler zoom factor (this will affect tick spacing)
        self.fixed_ruler_label.set_zoom_factor(scale)

    def set_camera_from_list(self, index):
        if 0 <= index < len(self.available_cameras):
            selected_camera_info = self.available_cameras[index]
            # call your camera setup here
            self.camera.set_camera(selected_camera_info)
            print(index)

    def create_left_properties_panel(self):
        properties_widget = QWidget()
        properties_layout = QVBoxLayout()

        # 1. Get available cameras
        self.available_cameras = QCameraInfo.availableCameras()

        # 2. Create a QListWidget instead of QComboBox
        self.camera_list = QListWidget()
        for camera in self.available_cameras:
            self.camera_list.addItem(camera.description())
            self.camera_list.addItem(camera.description())

        # 3. Connect signal to handle selection changes
        self.camera_list.currentRowChanged.connect(self.set_camera_from_list)

        # 4. Wrap in a group box
        camera_select_group = QGroupBox("Available Devices")
        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.camera_list)
        # camera_group.setLayout(camera_layout)
        camera_select_group.setLayout(controls_layout)

        properties_layout.addWidget(camera_select_group)
        # properties_layout.addWidget(camera_group)
        properties_layout.addStretch()
        properties_widget.setLayout(properties_layout)


        self.left_toolbox.addItem(properties_widget, "Device Selection")

    def create_right_properties_panel(self):
        """Create the main properties panel with camera controls"""
        properties_widget = QWidget()
        properties_layout = QVBoxLayout()

        # Camera Controls Group
        camera_group = QGroupBox("Camera Controls")
        camera_layout = QVBoxLayout()

        # Brightness
        brightness_row = QVBoxLayout()
        brightness_row.addWidget(QLabel("Brightness:"))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.brightness_value = 50
        self.slider.valueChanged.connect(self.update_brightness)
        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.brightness_value = 50
        self.slider.valueChanged.connect(self.update_brightness)

        self.brightness_spinbox = QSpinBox()
        self.brightness_spinbox.setRange(0, 100)
        self.brightness_spinbox.setValue(50)
        self.brightness_spinbox.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.brightness_spinbox.setValue)

        brightness_slider_row = QHBoxLayout()
        brightness_slider_row.addWidget(self.slider)
        brightness_slider_row.addWidget(self.brightness_spinbox)
        brightness_row.addLayout(brightness_slider_row)

        # Contrast
        contrast_row = QVBoxLayout()
        contrast_row.addWidget(QLabel("Contrast:"))
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 100)
        self.contrast_slider.setValue(50)
        self.contrast_value = 50
        self.contrast_slider.valueChanged.connect(self.update_contrast)

        self.contrast_slider.setStyleSheet(active_colors)

        self.contrast_spinbox = QSpinBox()
        self.contrast_spinbox.setRange(0, 100)
        self.contrast_spinbox.setValue(50)
        self.contrast_spinbox.valueChanged.connect(self.contrast_slider.setValue)
        self.contrast_slider.valueChanged.connect(self.contrast_spinbox.setValue)

        contrast_slider_row = QHBoxLayout()
        contrast_slider_row.addWidget(self.contrast_slider)
        contrast_slider_row.addWidget(self.contrast_spinbox)
        contrast_row.addLayout(contrast_slider_row)

        # Exposure
        exposure_row = QVBoxLayout()
        exposure_row.addWidget(QLabel("Exposure:"))
        self.exposure_slider = QSlider(Qt.Horizontal)
        self.exposure_slider.setRange(0, 100)
        self.exposure_slider.setValue(50)
        self.exposure_value = 50
        self.exposure_slider.valueChanged.connect(self.update_exposure)

        self.exposure_slider.setStyleSheet(active_colors)

        self.exposure_spinbox = QSpinBox()
        self.exposure_spinbox.setRange(0, 100)
        self.exposure_spinbox.setValue(50)
        self.exposure_spinbox.valueChanged.connect(self.exposure_slider.setValue)
        self.exposure_slider.valueChanged.connect(self.exposure_spinbox.setValue)

        exposure_slider_row = QHBoxLayout()
        exposure_slider_row.addWidget(self.exposure_slider)
        exposure_slider_row.addWidget(self.exposure_spinbox)
        exposure_row.addLayout(exposure_slider_row)

        # Zoom Label + Controls
        zoom_label = QLabel("Zoom (%):")
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(25, 400)
        self.zoom_slider.setSingleStep(5)
        self.zoom_slider.setValue(40)

        self.zoom_spinbox = QSpinBox()
        self.zoom_spinbox.setRange(25, 400)
        self.zoom_spinbox.setSingleStep(5)
        self.zoom_spinbox.setSuffix("%")
        self.zoom_spinbox.setValue(40)

        # Connect them
        self.zoom_spinbox.valueChanged.connect(self.zoom_slider.setValue)
        self.zoom_slider.valueChanged.connect(self.zoom_spinbox.setValue)
        self.zoom_slider.valueChanged.connect(self.on_zoom_slider_changed)

        # Layout it
        zoom_row = QVBoxLayout()
        zoom_row.addWidget(zoom_label)

        zoom_slider_row = QHBoxLayout()
        zoom_slider_row.addWidget(self.zoom_slider)
        zoom_slider_row.addWidget(self.zoom_spinbox)
        zoom_row.addLayout(zoom_slider_row)

        self.slider.setStyleSheet(active_colors)
        self.contrast_slider.setStyleSheet(active_colors)
        self.exposure_slider.setStyleSheet(active_colors)

        camera_layout.addLayout(brightness_row)
        camera_layout.addLayout(contrast_row)
        camera_layout.addLayout(exposure_row)

        camera_group.setLayout(camera_layout)

        # Image Effects Group
        effects_group = QGroupBox("Image Effects")
        effects_layout = QVBoxLayout()

        self.grayscale_checkbox = QCheckBox("Grayscale Mode")
        self.grayscale_checkbox.stateChanged.connect(self.update_grayscale)
        effects_layout.addWidget(self.grayscale_checkbox)
        effects_group.setLayout(effects_layout)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPG"])
        self.format_combo.setMaximumWidth(60)

        # 1. Get available cameras
        self.available_cameras = QCameraInfo.availableCameras()

        # 2. Create a QListWidget instead of QComboBox
        self.camera_list = QListWidget()
        for camera in self.available_cameras:
            self.camera_list.addItem(camera.description())

        # 3. Connect signal to handle selection changes
        self.camera_list.currentRowChanged.connect(self.set_camera_from_list)

        # 4. Wrap in a group box
        camera_select_group = QGroupBox("Cameras")
        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.camera_list)
        camera_select_group.setLayout(controls_layout)

        properties_layout.addWidget(camera_group)
        properties_layout.addWidget(effects_group)
        properties_layout.addStretch()
        properties_widget.setLayout(properties_layout)

        self.right_toolbox.addItem(properties_widget, "Image Properties")

    def create_bottom_properties_panel(self):
        properties_widget = QWidget()
        properties_layout = QVBoxLayout()

        # 1. Get available cameras
        self.available_cameras = QCameraInfo.availableCameras()

        # 2. Create a QListWidget instead of QComboBox
        self.camera_list = QListWidget()
        for camera in self.available_cameras:
            self.camera_list.addItem(camera.description())
            self.camera_list.addItem(camera.description())

        # 3. Connect signal to handle selection changes
        self.camera_list.currentRowChanged.connect(self.set_camera_from_list)

        # 4. Wrap in a group box
        camera_select_group = QGroupBox("Feature Documentation")
        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.camera_list)
        # camera_group.setLayout(camera_layout)
        # camera_select_group.setLayout(controls_layout)

        # properties_layout.addWidget(camera_select_group)
        # properties_layout.addWidget(camera_group)
        properties_layout.addStretch()
        properties_widget.setLayout(properties_layout)

        self.bottom_toolbox.addItem(properties_widget, "")

    def create_left_bottom_properties_panel(self):
        properties_widget = QWidget()
        properties_layout = QVBoxLayout()

        # Dummy Camera Properties
        # Camera Resolution (Height x Width) - Dropdown (QComboBox)
        resolution_label = QLabel("Camera Resolution (Height x Width):")
        self.resolution_combobox = QComboBox()
        # Add predefined resolutions to the combobox
        self.resolution_combobox.addItem("1920 x 1080")  # Full HD
        self.resolution_combobox.addItem("1280 x 720")  # HD
        self.resolution_combobox.addItem("640 x 480")  # VGA
        self.resolution_combobox.addItem("3840 x 2160")  # 4K
        self.resolution_combobox.addItem("2560 x 1440")  # QHD

        # Set default resolution
        self.resolution_combobox.setCurrentText("1920 x 1080")

        # Camera Gain
        gain_label = QLabel("Gain:")
        self.gain_spinbox = QSpinBox()
        self.gain_spinbox.setRange(0, 100)  # Set a range for gain
        self.gain_spinbox.setValue(50)  # Default gain value (editable)

        # Camera Exposure Time (in milliseconds)
        exposure_label = QLabel("Exposure Time (ms):")
        self.exposure_spinbox = QSpinBox()
        self.exposure_spinbox.setRange(0, 10000)  # Exposure time in milliseconds
        self.exposure_spinbox.setValue(100)  # Default exposure time (editable)

        # Camera ISO
        iso_label = QLabel("ISO:")
        self.iso_spinbox = QSpinBox()
        self.iso_spinbox.setRange(100, 3200)  # ISO range
        self.iso_spinbox.setValue(400)  # Default ISO value (editable)

        # Add all properties to the layout
        properties_layout.addWidget(resolution_label)
        properties_layout.addWidget(self.resolution_combobox)
        properties_layout.addWidget(gain_label)
        properties_layout.addWidget(self.gain_spinbox)
        properties_layout.addWidget(exposure_label)
        properties_layout.addWidget(self.exposure_spinbox)
        properties_layout.addWidget(iso_label)
        properties_layout.addWidget(self.iso_spinbox)

        # Add some space at the end
        properties_layout.addStretch()

        # Set the layout for the properties widget
        properties_widget.setLayout(properties_layout)

        # Add the properties widget to the left bottom toolbox
        self.left_bottom_toolbox.addItem(properties_widget, "Device Properties")


