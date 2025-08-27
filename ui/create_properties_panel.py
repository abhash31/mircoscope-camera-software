from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,
    QLabel,QPushButton, QSlider, QHBoxLayout, QSpinBox,
    QCheckBox, QGroupBox, QComboBox
)
from PyQt5.QtCore import Qt

def create_properties_panel(self):
    """Create the main properties panel with camera controls"""
    properties_widget = QWidget()
    properties_layout = QVBoxLayout()

    record_group = QGroupBox("Live Record")
    record_layout = QVBoxLayout()

    record_row = QHBoxLayout()
    self.record_button = QPushButton("Start Record")
    self.record_button.setIcon(QIcon('../assets/play.png'))
    self.record_button.clicked.connect(self.start_recording)

    self.snap_button = QPushButton("Snapshot")
    self.snap_button.clicked.connect(self.save_current_frame)

    record_row.addWidget(self.record_button)
    record_row.addWidget(self.snap_button)
    record_layout.addLayout(record_row)

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

    self.exposure_spinbox = QSpinBox()
    self.exposure_spinbox.setRange(0, 100)
    self.exposure_spinbox.setValue(50)
    self.exposure_spinbox.valueChanged.connect(self.exposure_slider.setValue)
    self.exposure_slider.valueChanged.connect(self.exposure_spinbox.setValue)

    exposure_slider_row = QHBoxLayout()
    exposure_slider_row.addWidget(self.exposure_slider)
    exposure_slider_row.addWidget(self.exposure_spinbox)
    exposure_row.addLayout(exposure_slider_row)

    # Zoom
    zoom_row = QVBoxLayout()
    self.zoom_value = 10

    zoom_slider_row = QHBoxLayout()
    zoom_row.addLayout(zoom_slider_row)

    # Zoom Dropdown
    self.zoom_combo = QComboBox()
    self.zoom_combo.addItems(["25%", "50%", "100%", "150%", "200%", "400%"])
    self.zoom_combo.setCurrentText("100%")
    self.zoom_combo.currentTextChanged.connect(self.on_zoom_percent_changed)

    zoom_row.addWidget(QLabel("Zoom Preset:"))
    zoom_row.addWidget(self.zoom_combo)

    # Auto White Balance checkbox
    awb_row = QVBoxLayout()
    self.awb_checkbox = QCheckBox("Auto White Balance")
    self.awb_checkbox.setChecked(True)
    self.awb_checkbox.stateChanged.connect(self.update_awb_checkbox)
    awb_row.addWidget(self.awb_checkbox)

    # Add all to camera layout
    camera_layout.addLayout(brightness_row)
    camera_layout.addLayout(contrast_row)
    camera_layout.addLayout(exposure_row)
    camera_layout.addLayout(zoom_row)
    camera_layout.addLayout(awb_row)

    camera_group.setLayout(camera_layout)
    record_group.setLayout(record_layout)

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

    # save_row.addWidget(self.save_button)
    # save_row.addWidget(self.format_combo)
    # actions_layout.addLayout(save_row)
    #
    # actions_group.setLayout(actions_layout)

    # Add all groups to properties layout
    properties_layout.addWidget(record_group)
    properties_layout.addWidget(camera_group)
    properties_layout.addWidget(effects_group)
    # properties_layout.addWidget(actions_group)
    properties_layout.addStretch()
    properties_widget.setLayout(properties_layout)

    self.left_toolbox.addItem(properties_widget, "Properties")

    return self.record_button
