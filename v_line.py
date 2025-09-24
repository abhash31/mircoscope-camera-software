from PyQt5.QtWidgets import QFrame

class VLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        # self.setLineWidth(4)  # Main thickness
        self.setMidLineWidth(3)
        self.setFixedHeight(25)


