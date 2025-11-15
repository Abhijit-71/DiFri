from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QPoint
from .coreui import HoverButton
from .tabbar import TabManager 
from core.utils import resource_path




class CustomTitleBar(QWidget):
    def __init__(self,tabbar,parent=None, height=45):
        super().__init__(parent)
        self.parent = parent # type: ignore
        self.setFixedHeight(height)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8,3,0,0)
        layout.setSpacing(5)

        # Tabbar
        layout.addWidget(tabbar.tab_bar)
        btn = HoverButton("svg/plus.svg","svg/plus.svg","svg/plus.svg",size=30)
        btn.clicked.connect(tabbar.add_tab)
        layout.addWidget(btn)
        layout.addStretch()

        # Minimize button
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(30,8,10,10)
        self.min_btn = HoverButton('svg/min-normal.svg','svg/min-hover.svg','svg/min-pressed.svg',16)
        self.min_btn.setStyleSheet("background: transparent; border: none;")
        self.min_btn.clicked.connect(self.parent.showMinimized) # type: ignore
        buttons_layout.addWidget(self.min_btn)

        # Maximize / Restore button
        self.max_btn = HoverButton('svg/max-normal.svg','svg/max-hover.svg','svg/max-pressed.svg',16)
        self.max_btn.setStyleSheet("background: transparent; border: none;")
        self.max_btn.clicked.connect(self.toggle_max_restore)
        buttons_layout.addWidget(self.max_btn)

        # Close button
        self.close_btn = HoverButton('svg/close-normal.svg','svg/close-hover.svg','svg/close-pressed.svg',16)
        self.close_btn.setStyleSheet("background: transparent; border: none;")
        self.close_btn.clicked.connect(self.parent.close) # type: ignore
        buttons_layout.addWidget(self.close_btn)
        
        layout.addLayout(buttons_layout)

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
    def __init__(self, widget,tab_manager:TabManager):
        super().__init__()
        self.setWindowTitle('DiFri')
        self.setWindowIcon(QIcon(resource_path('svg/dbrowser_logo.svg')))
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.setMinimumSize(800, 600)

        self.TabBar = tab_manager
        
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.titlebar = CustomTitleBar(self.TabBar,self)
        layout.addWidget(self.titlebar)
        layout.addWidget(widget)
        
        self.setCentralWidget(central)


class PaddedWindow(QWidget):
    def __init__(self, widget:QWidget, color):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {color};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 8)
        layout.setSpacing(0)

        layout.addWidget(widget)
        
        
    

