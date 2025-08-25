from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton


def create_measurement_panel(self):
    """Create the measurement and ruler panel"""
    measurement_widget = QWidget()
    measurement_layout = QVBoxLayout()

    # Ruler Controls Group
    ruler_group = QGroupBox("Ruler & Measurements")
    ruler_layout = QVBoxLayout()

    ruler_info = QLabel(
        "Click and drag to measure distances.\nMultiple measurements supported.\nMeasurements adjust with zoom level.")
    ruler_info.setWordWrap(True)
    ruler_info.setStyleSheet("color: gray; font-size: 9px;")
    ruler_layout.addWidget(ruler_info)

    self.clear_rulers_button = QPushButton("Clear All Measurements")
    self.clear_rulers_button.clicked.connect(self.clear_all_rulers)
    ruler_layout.addWidget(self.clear_rulers_button)

    ruler_group.setLayout(ruler_layout)

    # Scale Display Group
    scale_group = QGroupBox("Scale Display")
    scale_layout = QVBoxLayout()

    scale_info = QLabel(
        "Scale rulers are displayed on top and left edges showing actual pixel coordinates adjusted for zoom level.")
    scale_info.setWordWrap(True)
    scale_info.setStyleSheet("color: gray; font-size: 9px;")
    scale_layout.addWidget(scale_info)
    scale_group.setLayout(scale_layout)

    measurement_layout.addWidget(ruler_group)
    measurement_layout.addWidget(scale_group)
    measurement_layout.addStretch()
    measurement_widget.setLayout(measurement_layout)

    self.toolbox.addItem(measurement_widget, "Measurements")
