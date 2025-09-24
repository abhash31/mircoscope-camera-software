active_colors = """
            QSlider::groove:horizontal {
                border: 0px;
                height: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e6eaf0, stop:1 #dde2ea);
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #448aff, stop:1 #42a5f5);
                border-radius: 3px;
            }
            QSlider::add-page:horizontal {
                background: #e6eaf0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #90caf9);
                border: none;
                width: 16px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3f2fd, stop:1 #448aff);
            }
            """

inactive_colors = """
                        QSlider::groove:horizontal {
    border: 0px;
    height: 6px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #cccccc, stop:1 #dddddd);
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #999999, stop:1 #aaaaaa);
    border-radius: 3px;
}
QSlider::add-page:horizontal {
    background: #cccccc;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eeeeee, stop:1 #bbbbbb);
    border: none;
    width: 16px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #dddddd, stop:1 #999999);
}

                        """