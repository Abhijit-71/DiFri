from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QPoint
from .coreui import HoverButton



class CustomTitleBar(QWidget):
    def __init__(self,parent=None, height=35, padding=10):
        super().__init__(parent)
        self.parent = parent # type: ignore
        self.setFixedHeight(height)
        #self.setStyleSheet(f"background-color: {color}; color: white;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(padding, 5, padding, 5)
        layout.setSpacing(5)

        # Title label
        self.title = QLabel("DiFri")
        self.title.setStyleSheet("background: transparent;font-weight: bold;")
        layout.addWidget(self.title)
        layout.addStretch()

        # Minimize button
        self.min_btn = HoverButton('svg/min-normal.svg','svg/min-hover.svg','svg/min-pressed.svg',16)
        self.min_btn.setStyleSheet("background: transparent; border: none;")
        self.min_btn.clicked.connect(self.parent.showMinimized) # type: ignore
        layout.addWidget(self.min_btn)

        # Maximize / Restore button
        self.max_btn = HoverButton('svg/max-normal.svg','svg/max-hover.svg','svg/max-pressed.svg',16)
        self.max_btn.setStyleSheet("background: transparent; border: none;")
        self.max_btn.clicked.connect(self.toggle_max_restore)
        layout.addWidget(self.max_btn)

        # Close button
        self.close_btn = HoverButton('svg/close-normal.svg','svg/close-hover.svg','svg/close-pressed.svg',16)
        self.close_btn.setStyleSheet("background: transparent; border: none;")
        self.close_btn.clicked.connect(self.parent.close) # type: ignore
        layout.addWidget(self.close_btn)

        # Dragging
        self.start = QPoint(0, 0)

    def toggle_max_restore(self):
        if self.parent.isMaximized(): # type: ignore
            self.parent.showNormal() # type: ignore
        else:
            self.parent.showMaximized() # type: ignore
             

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.start
            self.parent.move(self.parent.pos() + delta) # type: ignore
            self.start = event.globalPosition().toPoint()


        
class MainWindow(QMainWindow):
    def __init__(self, widget,tab_manager):
        super().__init__()
        self.setWindowTitle('DiFri')
        self.setWindowIcon(QIcon('svg/logo.svg'))
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.setMinimumSize(800, 600)

        self.TabBar = tab_manager
        
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.titlebar = CustomTitleBar(self)
        layout.addWidget(self.titlebar)
        layout.addWidget(widget)
        
        self.setCentralWidget(central)
    
    # Resize event removed - was for adjusting tab width on maximize 

class PaddedWindow(QWidget):
    def __init__(self, widget, color):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {color}; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(0)
        
        #layout.addWidget(tab)
        #layout.addWidget(navbar)
        layout.addWidget(widget)
        
        
    

