# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton
#
#
# def create_measurement_panel(self):
#     """Create the measurement and ruler panel"""
#     measurement_widget = QWidget()
#     measurement_layout = QVBoxLayout()
#
#     # Ruler Controls Group
#     ruler_group = QGroupBox("Ruler & Measurements")
#     ruler_layout = QVBoxLayout()
#
#     ruler_info = QLabel(
#         "Click and drag to measure distances.\nMultiple measurements supported.\nMeasurements adjust with zoom level.")
#     ruler_info.setWordWrap(True)
#     ruler_info.setStyleSheet("color: gray; font-size: 9px;")
#     ruler_layout.addWidget(ruler_info)
#
#     self.clear_rulers_button = QPushButton("Clear All Measurements")
#     self.clear_rulers_button.clicked.connect(self.clear_all_rulers)
#     ruler_layout.addWidget(self.clear_rulers_button)
#
#     ruler_group.setLayout(ruler_layout)
#
#     # Scale Display Group
#     scale_group = QGroupBox("Scale Display")
#     scale_layout = QVBoxLayout()
#
#     scale_info = QLabel(
#         "Scale rulers are displayed on top and left edges showing actual pixel coordinates adjusted for zoom level.")
#     scale_info.setWordWrap(True)
#     scale_info.setStyleSheet("color: gray; font-size: 9px;")
#     scale_layout.addWidget(scale_info)
#     scale_group.setLayout(scale_layout)
#
#     measurement_layout.addWidget(ruler_group)
#     measurement_layout.addWidget(scale_group)
#     measurement_layout.addStretch()
#     measurement_widget.setLayout(measurement_layout)
#
#     self.toolbox.addItem(measurement_widget, "Measurements")

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton

def histogram_panel(self):
    """Create a Histogram panel inside the right-side toolbox."""
    histogram_widget = QWidget()
    histogram_layout = QVBoxLayout()

    # Histogram Group
    hist_group = QGroupBox("Histogram")
    hist_layout = QVBoxLayout()

    # Label that will display the histogram image
    # Keep a separate label for the toolbox panel so it doesn't clash with any bottom-area histogram
    self.histogram_panel_label = QLabel("Open an image or start the camera to see the histogram.")
    self.histogram_panel_label.setAlignment(Qt.AlignCenter)
    self.histogram_panel_label.setMinimumHeight(220)  # give it room so it won't crop
    self.histogram_panel_label.setStyleSheet("background-color:#111; border:1px solid #333;")
    self.histogram_panel_label.setScaledContents(True)

    # Optional: a manual refresh button
    refresh_btn = QPushButton("Refresh Histogram")
    refresh_btn.clicked.connect(self.update_histogram)

    hist_layout.addWidget(self.histogram_panel_label)
    hist_layout.addWidget(refresh_btn)
    hist_group.setLayout(hist_layout)

    histogram_layout.addWidget(hist_group)
    histogram_layout.addStretch()
    histogram_widget.setLayout(histogram_layout)

    # Put the panel into the toolbox (rename the tab to "Histogram")
    self.toolbox.addItem(histogram_widget, "Histogram")

