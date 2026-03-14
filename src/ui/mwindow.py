from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from .coreui import HoverButton
from .tabbar import TabManager 
from core.utils import resource_path




class CustomTitleBar(QWidget):
    def __init__(self,tabbar,parent=None, height=45):
        super().__init__(parent)
        self.parent = parent # type: ignore
        self.setFixedHeight(height)
        self.setStyleSheet("background:#2e2e2e")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8,0,0,0)
        layout.setSpacing(5)

        # Tabbar
        layout.addWidget(tabbar.tab_bar)
        btn = HoverButton("svg/plus.svg","svg/plus.svg","svg/plus.svg",size=30)
        btn.clicked.connect(tabbar.add_tab)
        layout.addWidget(btn)
        layout.addStretch()

    def toggle_tabs(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        
class MainWindow(QMainWindow):
    def __init__(self, widget,tab_manager:TabManager):
        super().__init__()
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon(resource_path('svg/icon_empty.png')))
        self.setWindowFlags(Qt.WindowType.NoTitleBarBackgroundHint)
        self.setStyleSheet("background:#202020")
        
        self.setMinimumSize(500, 500)
        
        self.TabBar = tab_manager
        
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.titlebar = CustomTitleBar(self.TabBar,self)
        self.TabBar.set_toggle_callback(self.titlebar.toggle_tabs)
        layout.addWidget(self.titlebar)
        self.titlebar.hide()
        layout.addWidget(widget)
        self.setCentralWidget(central)
    
    



        
        
    

