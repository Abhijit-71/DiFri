from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabBar, QLabel, QStackedWidget)
from PyQt6.QtGui import QIcon
from .browser import BrowserWindow
from browser.corebrowser import Browser
from .dropdown import DownloadTab, DownloadManager
from core.utils import resource_path


class TabManager(QWidget):
    def __init__(self):
        super().__init__()
        
        self.index = 1
        
        self.download_manager = DownloadManager()
        self.download_tab = DownloadTab(self.download_manager)
        self.browser_instance = Browser(self.download_manager)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create separate tab bar (without QTabWidget)
        self.tab_bar = QTabBar()
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.setDocumentMode(True)
        self.tab_bar.setStyleSheet("""
            QTabBar {
                background: transparent;
            }
            QTabBar::tab {
                background: #2e2e2e;
                color: #ffffff;
                padding: 6px 10px 6px 30px;
                margin-right: 4px;
                border-radius: 8px;
                width: 100px;
            }
            QTabBar::tab:selected {
                background:#3a2570;
            }
            QTabBar::tab:hover {
                border:1px solid #b4aaff;
            }
            QTabBar::tab:selected:hover {
                border:1px solid #d6c8ff;
            }
        """)
        
        close_icon = resource_path("svg/cross.svg").replace("\\", "/")
        self.tab_bar.setStyleSheet(self.tab_bar.styleSheet() + f"""
            QTabBar::close-button {{
                image: url({close_icon});
                subcontrol-position: right;
                width: 16px;
                height: 16px;
            }}
        """)

        self.tab_bar.setMinimumWidth(100)
        self.tab_bar.setMaximumWidth(1920)
        self.tab_bar.setUsesScrollButtons(False)

        # tab content
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background: transparent;
            }
        """)

        # Add tab bar to its own layout
        main_layout.addWidget(self.content_stack)
        
        self.setLayout(main_layout)
        
        #first browser window
        self.browser_window = BrowserWindow(self.browser_instance)
        #self.browser_window.toolbar.download.clicked.connect(self.add_download_tab)
        
        # Add first tab
        self.tab_bar.addTab("New Tab")
        self.content_stack.addWidget(self.browser_window)
        
        self.browser_window.browser.titleChanged.connect(
            lambda title: self.update_title_icon(self.browser_window, title=title)
        )
        self.browser_window.browser.iconChanged.connect(
            lambda icon: self.update_title_icon(self.browser_window, icon=icon)
        )
        
        # Connect signals
        self.tab_bar.currentChanged.connect(self.content_stack.setCurrentIndex)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        
        
        
    def add_tab(self, url=None):
        tab_content = BrowserWindow(self.browser_instance)
        #tab_content.toolbar.download.clicked.connect(self.add_download_tab)

        index = self.tab_bar.addTab("")
        self.content_stack.addWidget(tab_content)
        
        self.tab_bar.setCurrentIndex(index)
        self.index += 1
        
        tab_content.browser.titleChanged.connect(
            lambda title: self.update_title_icon(tab_content, title=title)
        )
        tab_content.browser.iconChanged.connect(
            lambda icon: self.update_title_icon(tab_content, icon=icon)
        )

        if url:
            from PyQt6.QtCore import QUrl
            tab_content.browser.setUrl(QUrl(url))
            
        return tab_content
    
    
    
    def add_download_tab(self):
        tab_content = self.download_tab
        index = self.tab_bar.addTab("Downloads")
        self.content_stack.addWidget(tab_content)
        self.tab_bar.setCurrentIndex(index)
        self.index += 1



    def close_tab(self, index):
        if self.tab_bar.count() <= 1:
            return
            
        widget = self.content_stack.widget(index)
        self.tab_bar.removeTab(index)
        self.content_stack.removeWidget(widget)
        
        if widget and widget != self.download_tab:
            widget.deleteLater()



    def update_title_icon(self, browser_window: BrowserWindow, icon=None, title=None):
        if icon is None:
            icon = browser_window.browser.icon()
        
        if title is None:
            title = browser_window.browser.title()

        for i in range(self.content_stack.count()):
            if self.content_stack.widget(i) == browser_window:
                self.tab_bar.setTabButton(
                    i, 
                    QTabBar.ButtonPosition.LeftSide, 
                    IconTextWidget(icon, title)
                )




class IconTextWidget(QWidget):
    def __init__(self, icon, text, max_text_width=80):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(6)

        icon_label = QLabel()
        pixmap = QIcon(icon).pixmap(14, 14)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(18, 18)

        text_label = QLabel(text)
        text_label.setFixedWidth(max_text_width)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        self.setStyleSheet("background-color: transparent;")
        self.setLayout(layout)