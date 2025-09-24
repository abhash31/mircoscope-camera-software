import sys

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    palette = QPalette()

    # Background colors
    palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))  # Main window background
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))  # Input fields, text edit background
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))  # Alternate background for lists etc.

    # Text colors
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))  # Text on windows
    palette.setColor(QPalette.ColorRole.Text, QColor(33, 33, 33))  # General text
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))  # Tooltip text

    # Button colors
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))  # Button background
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))  # Button text

    # Highlight colors (selection)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))  # Selected background (blue)
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))  # Selected text (white)

    # Tooltips
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 225))  # Tooltip background

    # Auxiliary colors
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))  # For errors or important highlights
    palette.setColor(QPalette.ColorRole.Link, QColor(0, 102, 204))  # Hyperlink color

    # Optional: Light, Midlight, Dark shades for subtle UI elements
    palette.setColor(QPalette.ColorRole.Light, QColor(250, 250, 250))
    palette.setColor(QPalette.ColorRole.Midlight, QColor(224, 224, 224))
    palette.setColor(QPalette.ColorRole.Dark, QColor(190, 190, 190))
    palette.setColor(QPalette.ColorRole.Mid, QColor(160, 160, 160))
    palette.setColor(QPalette.ColorRole.Shadow, QColor(110, 110, 110))

    # Disabled state colors for clarity in disabled UI elements
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(130, 130, 130))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(130, 130, 130))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(130, 130, 130))

    app.setPalette(palette)
    app.setStyle('fusion')
    app.setStyleSheet("""
        * { font-family: 'Arial'; font-size: 12pt; }
    """)
    main_window = MainWindow()
    sys.exit(app.exec())