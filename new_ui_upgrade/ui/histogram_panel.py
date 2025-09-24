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
    self.right_toolbox.addItem(histogram_widget, "Histogram")

