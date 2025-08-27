from PyQt5.QtWidgets import QApplication

def apply_light_theme(app: QApplication):
    light_stylesheet = """
        QMainWindow {
            background-color: #f8f9fa;
        }
        QWidget {
            background-color: #ffffff;
            color: #000000;
            font-size: 11pt;
        }
        QToolBox {
            background-color: #f1f1f1;
            border: 1px solid #cccccc;
        }
        QGroupBox {
            background-color: #ffffff;
            border: 1px solid #aaaaaa;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            color: #333333;
        }
        QPushButton {
            background-color: #e9ecef;
            border: 1px solid #adb5bd;
            padding: 5px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #dee2e6;
        }
        QLabel {
            color: #212529;
        }
        QScrollArea {
            background-color: #ffffff;
        }
        QDockWidget {
            background-color: #f8f9fa;
            titlebar-close-icon: url(none);
            titlebar-normal-icon: url(none);
        }
    """
    app.setStyleSheet(light_stylesheet)
