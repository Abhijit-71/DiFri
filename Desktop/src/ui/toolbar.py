from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout , QLineEdit , QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt,QUrl
from .coreui import HoverButton
from PyQt6.QtGui import  QPixmap
from urllib.parse import quote_plus
from .dropdown import MenuDrop
from core.utils import resource_path


class Navigation(QWidget):
    def __init__(self, browser:QWebEngineView):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(10)

        self.back = HoverButton('svg/back.svg','svg/back_pressed.svg','svg/back_pressed.svg', 20)
        self.back.clicked.connect(browser.back)
        layout.addWidget(self.back)

        self.forward = HoverButton('svg/forward.svg','svg/forward_pressed.svg','svg/forward_pressed.svg', 20)
        self.forward.clicked.connect(browser.forward)
        layout.addWidget(self.forward)

        self.reload = HoverButton('svg/reload.svg','svg/reload_pressed.svg','svg/reload_pressed.svg', 19)
        self.reload.clicked.connect(browser.reload)
        layout.addWidget(self.reload)

        self.setFixedHeight(45)




class URLTab(QWidget):
    def __init__(self,browser:QWebEngineView,color="#256eff"):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(6)
        layout.addStretch()

        self.sengine = QLabel()
        self.sengine.setPixmap(QPixmap(resource_path('svg/google_logo.svg')))
        self.sengine.setFixedSize(30,30)
        self.sengine.setScaledContents(True)
        self.sengine.setStyleSheet("background: transparent;")

        layout.addWidget(self.sengine)

        self.urlbox = QLineEdit()
        self.urlbox.setFixedHeight(35)
        self.urlbox.setMinimumWidth(400)
        self.urlbox.setPlaceholderText("Search with google or enter url .....")
        line_style = """
            QLineEdit {
                background: rgba(255,255,255,0.1);
                color: #ffffff;
                border: 1px solid rgba(255,255,255,0.06);
                padding: 4px 8px;
                border-radius: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #6aaaff;
                background: rgba(255,255,255,0.02);
            }
            QLineEdit::placeholder {
                color: rgba(255,255,255,0.6);
            }
        """
        self.urlbox.setStyleSheet(line_style)
        self.urlbox.setSizePolicy(QSizePolicy.Policy.Expanding , QSizePolicy.Policy.Fixed)
        layout.addWidget(self.urlbox,1)
        self.setStyleSheet(f"background-color: {color};")
        self.setFixedHeight(45)
        self.browser = browser
        self.urlbox.returnPressed.connect(lambda: self.change_src(self.urlbox.text()))


    def change_src(self,src:str):
        if '.' in src and ' ' not in src:
            if src.startswith('https://') or src.startswith('http://') or src.startswith('file:///'):
                self.browser.setUrl(QUrl(src))
            else:
                self.browser.setUrl(QUrl('https://'+src))
        else:
            query = quote_plus(src)
            url = f"https://www.google.com/search?q={query}"
            self.browser.setUrl(QUrl(url))
        
        




class Toolbar(QWidget):
    def __init__(self, navbar, urltab,downnload_man,color="#3a2570"):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.menu = HoverButton('svg/menu.svg','svg/menu_pressed.svg','svg/menu_pressed.svg', 24)
        self.menu.setMenu(MenuDrop()) #menu added
        self.menu.setStyleSheet("QPushButton::menu-indicator { image: none; }")

        menu_layout = QHBoxLayout()
        menu_layout.setContentsMargins(20,0,0,0)
        menu_layout.setSpacing(30)
        self.downloadbtn =HoverButton('svg/download.svg','svg/download_pressed.svg','svg/download_pressed.svg', 24)
        self.downloadbtn.setStyleSheet("QPushButton::menu-indicator { image: none; }")
        self.downloadbtn.setMenu(downnload_man)
        self.darkbtn =HoverButton('svg/light-mode.svg','svg/dark-mode.svg','svg/light-mode.svg', 20)
        menu_layout.addWidget(self.darkbtn)
        menu_layout.addWidget(self.downloadbtn)
        menu_layout.addWidget(self.menu)
        
        url_layout = QHBoxLayout()
        url_layout.setContentsMargins(0,0,0,0)
        url_layout.setSpacing(15)
        url_layout.addWidget(navbar)
        url_layout.addWidget(urltab)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20,0,20,0)
        layout.setSpacing(30)
        
        layout.addLayout(url_layout)
        layout.addLayout(menu_layout)
        
        self.setFixedHeight(45)
        self.setStyleSheet(f"background-color: {color};border-radius: 0px;border-top-right-radius: 8px;border-top-left-radius: 8px;")
        