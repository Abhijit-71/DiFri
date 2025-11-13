from PyQt6.QtWidgets import QPushButton ,QProgressBar
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

class HoverButton(QPushButton):
    def __init__(self, normal:str, hover:str, pressed:str, size:int, parent=None):
        super().__init__(parent)
        self.icon_normal = QIcon(normal)
        self.icon_hover = QIcon(hover)
        self.icon_pressed = QIcon(pressed)

        self.setIcon(self.icon_normal)
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size,size)
        self.setFlat(True)  # Important: disables native style

    def enterEvent(self, event):
        self.setIcon(self.icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.icon_normal)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setIcon(self.icon_pressed)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.underMouse():
            self.setIcon(self.icon_hover)
        else:
            self.setIcon(self.icon_normal)
        super().mouseReleaseEvent(event)



class IconButton(QPushButton):
    def __init__(self, icon:str, size:int):
        super().__init__()
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size, size)
        self.setFlat(True)  # Now not used, only for testing buttons with one state icon

        

class ProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(2)
        self.setTextVisible(False)
        self.setRange(0, 100)
        self.hide()

    def on_load_started(self):
            self.show()
            self.setValue(0)

    def on_load_progress(self, progress):
            self.setValue(progress)

    def on_load_finished(self):
            self.hide()
