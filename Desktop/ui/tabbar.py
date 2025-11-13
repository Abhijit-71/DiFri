from PyQt6.QtWidgets import (QWidget, QTabWidget,QVBoxLayout, QHBoxLayout, QTabBar, QLabel)
from PyQt6.QtGui import QIcon
from .browser import BrowserWindow
from browser.corebrowser import Browser
from .dropdown import DownloadTab , DownloadManager

class TabManager(QWidget):
    def __init__(self):
        super().__init__()
        
        self.index = 1  # Index for tabs
        
        self.download_manager = DownloadManager()
        self.download_tab = DownloadTab(self.download_manager)
        self.browser_instance = Browser(self.download_manager)  # Called once for only one profile for each startup 

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(10)

        # Tab manager full 
        self.TabBar = QTabWidget()
        self.TabBar.setTabsClosable(True)
        self.TabBar.setMovable(True)
        self.TabBar.setDocumentMode(True)
        self.TabBar.setContentsMargins(0,0,0,0)
        self.TabBar.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
                
            }
            QTabBar {
                background: transparent;
            }
            QTabBar::tab {
                background: #2e2e2e;
                color: #ffffff;
                padding: 6px 10px 6px 30px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                width: 150px;
            }
            QTabBar::tab:selected {
                background:#47327D;
            }
            QTabBar::tab:hover {
                border:1px solid #b4aaff;
            }
            QTabBar::tab:selected:hover {
                border:1px solid #d6c8ff;
            }
            QTabBar::close-button {
                image: url("svg/cross.svg");
                subcontrol-position: right;
                width: 16px;
                height: 16px;
            }
        """)

        self.TabBar.tabBar().setMinimumWidth(200)# type: ignore 
        self.TabBar.tabBar().setMaximumWidth(1920)#type:ignore
        
        # for the tab changers button
        self.container = QWidget(self.TabBar.tabBar())
        h_layout = QHBoxLayout(self.container)
        h_layout.setContentsMargins(0,0,0,0)
        h_layout.addStretch() 
        self.container.setLayout(h_layout)
        self.container.show()
        self.container.move(self.TabBar.tabBar().width() - self.container.width(), 0) #type:ignore

        layout.addWidget(self.TabBar)
        
        self.setLayout(layout)
         
        
        # main browserwindow incl. toolbar
        self.browser_window = BrowserWindow(self.browser_instance)  # Passed profile (which was created once)
        self.browser_window.toolbar.home.clicked.connect(self.add_tab)
        self.browser_window.toolbar.download.clicked.connect(self.add_download_tab)
        self.TabBar.addTab(self.browser_window,"New Tab")

        self.browser_window.browser.titleChanged.connect(lambda title:self.update_title_icon(self.browser_window,title))
        self.browser_window.browser.iconChanged.connect(lambda icon:self.update_title_icon(self.browser_window,icon))
        
        self.TabBar.tabCloseRequested.connect(self.close_tab)
        
        
    def add_tab(self):
            tab_content = BrowserWindow(self.browser_instance)  # Passed profile (which was created once)
            tab_content.toolbar.home.clicked.connect(self.add_tab)
            tab_content.toolbar.download.clicked.connect(self.add_download_tab)

            index = self.TabBar.addTab(tab_content, f"")
            
            self.TabBar.setCurrentIndex(index)
            self.index += 1 
            
            tab_content.browser.titleChanged.connect(lambda title:self.update_title_icon(tab_content,title))
            tab_content.browser.iconChanged.connect(lambda icon:self.update_title_icon(tab_content,icon))
             
    
    def add_download_tab(self):
         tab_content = self.download_tab
         index = self.TabBar.addTab(tab_content, "Downloads")
         self.TabBar.setCurrentIndex(index)
         self.index += 1 


    def close_tab(self, index):
        widget = self.TabBar.widget(index)
        if self.TabBar.count() <= 1:
            return
        self.TabBar.removeTab(index)
        
        if widget and widget != self.download_tab :
            widget.deleteLater()



    def update_title_icon(self,browser_window:BrowserWindow,icon=None,title=None):
         if icon is None:
              icon = browser_window.browser.icon()
        
         if title is None:
              title = browser_window.browser.title()

         for i in range(self.TabBar.count()):
              if self.TabBar.widget(i) == browser_window:
                   self.TabBar.tabBar().setTabButton(i, QTabBar.ButtonPosition.LeftSide, IconTextWidget(icon,title,100)) #type:ignore
         
        

class IconTextWidget(QWidget):
    def __init__(self, icon, text, max_text_width=100):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(6)

        icon_label = QLabel()
        pixmap = QIcon(icon).pixmap(14,14)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(18, 18)

        text_label = QLabel(text)
        text_label.setFixedWidth(max_text_width)
        # Commented out: was for faded text in title of tabs but did not work

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        self.setStyleSheet("background-color: transparent;")
        self.setLayout(layout)

