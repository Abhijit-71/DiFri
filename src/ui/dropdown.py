from PyQt6.QtWidgets import (QMenu,QWidget,QWidgetAction,QVBoxLayout,QLabel,QHBoxLayout,QPushButton,QProgressBar,QFileIconProvider)
from PyQt6.QtCore import QFileInfo
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
#from core.utils import resource_path

#https://www.thinkbroadband.com/download   === test url

class DownloadBar(QWidget):
    def __init__(self, download:QWebEngineDownloadRequest):
        super().__init__()
        self.setMaximumHeight(50)   
        self.setMinimumWidth(200)
        self.download = download
        
        file_info = QFileInfo(download.downloadFileName())
        provider = QFileIconProvider()
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QIcon(provider.icon(file_info)).pixmap(14, 14))
        self.name_label = QLabel(download.downloadFileName())
        self.name_label.setStyleSheet("font-size:12px;")
        self.size_label = QLabel("Unknown size")
        self.size_label.setStyleSheet("font-size:9px;")
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setValue(0)
        
        self.pause_btn = QPushButton("❙❙")
        self.pause_btn.setFixedWidth(20)
        self.pause_btn.setFixedHeight(20)
        self.pause_btn.setStyleSheet("font-size:10px;")
        self.pause_btn.clicked.connect(lambda: self.toggle_pause(download,self.pause_btn))
        self.cancel_btn = QPushButton("❌")
        self.cancel_btn.setFixedWidth(20)
        self.cancel_btn.setFixedHeight(20)
        self.cancel_btn.setStyleSheet("font-size:9px;")
        self.cancel_btn.clicked.connect(download.cancel)

        top = QHBoxLayout()
        top.setSpacing(5)
        top.addWidget(self.icon_label)
        top.addWidget(self.name_label)
        top.addStretch()
        top.addWidget(self.pause_btn)
        top.addWidget(self.cancel_btn)

        mid = QHBoxLayout()
        mid.addWidget(self.size_label)
        mid.addWidget(self.progress)

        vbox = QVBoxLayout()
        vbox.setSpacing(1)           
        vbox.addLayout(top)
        vbox.addLayout(mid)
        

        self.setLayout(vbox)
        
        #signal connection
        if download.totalBytes() != 0:
            download.receivedBytesChanged.connect(lambda: self.on_progress(download))
        download.isFinishedChanged.connect(lambda: self.on_finished(download))


    def on_progress(self,download):
        if download.totalBytes() > 0:
            pct = int((download.receivedBytes() / download.totalBytes()) * 100)
            self.size_label.setText(f"{(download.receivedBytes())/1024**2:.1f} MB/{(download.totalBytes())/1024**2:.1f} MB  | {pct}%")
            pct = int((download.receivedBytes() / download.totalBytes()) * 100)
            self.progress.setValue(pct)
        else:
            self.size_label.setText("Downloading…")
    
    def toggle_pause(self, download: QWebEngineDownloadRequest, button: QPushButton):
        if button.text() == "❙❙":
            download.pause()
            button.setText("▶")
        else:
            download.resume()
            button.setText("❙❙")
            
    def on_finished(self,download):
        if download.state() == download.DownloadState.DownloadCompleted:
            self.size_label.setText("Completed")
        elif download.state() == download.DownloadState.DownloadInterrupted:
            self.size_label.setText("Failed")
        elif download.state() == download.DownloadState.DownloadCancelled:
            self.size_label.setText("Cancelled")
        self.cancel_btn.hide()
        self.pause_btn.hide()
        self.progress.hide()





class DownloadMenu(QMenu):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(180)
        self.addAction("Downloads")
        self.addSeparator()
        self.setStyleSheet("""
            QMenu {
                background-color: #1e1e1e; 
                color: #f5f5f5;     
                border: 1px solid #444;
                padding: 10px;
                border-radius: 8px;
            }

            QMenu::item {
                padding: 6px 18px;
                border-radius: 4px;
            }

            QMenu::item:selected {
                background-color: #47327D; 
                color: white;
            }

            QMenu::separator {
                height: 1px;
                background: #555;
                margin: 4px 8px;
            }
        """)
        
        
    def add_download(self,download):
        print(download.downloadFileName())
        item = DownloadBar(download)
        action = QWidgetAction(self)
        action.setDefaultWidget(item)
        self.addAction(action)
        self.addSeparator()
    



class MenuDrop(QMenu):
    def __init__(self):
        super().__init__()

        #do include resource_path if icons required

        add_tab = QAction("Add New Tab",self)
        add_tab.setShortcut('Ctrl+T')
        self.addAction(add_tab)

        self.addSeparator()

        self.addAction("BookMark")
        self.addAction("History")
        self.addSeparator()
        
        print = QAction("Print",self)
        print.setShortcut('Ctrl+P')
        self.addAction(print)

        save = QAction("Save Page As      ",self)
        save.setShortcut('Ctrl+S')
        self.addAction(save)
        self.addSeparator()

        self.addAction("Settings")
        self.addAction("Help")
        self.addSeparator()
        
        exit = QAction("Exit",self)
        exit.setShortcut('Alt+F4')
        self.addAction(exit)

        self.setStyleSheet("""
            QMenu {
                background-color: #1e1e1e; 
                color: #f5f5f5;     
                border: 1px solid #444;
                padding: 10px;
                border-radius: 8px;
            }

            QMenu::item {
                padding: 6px 18px;
                border-radius: 4px;
            }

            QMenu::item:selected {
                background-color: #47327D; 
                color: white;
            }

            QMenu::separator {
                height: 1px;
                background: #555;
                margin: 4px 8px;
            }

            QMenu::icon {
                margin-right: 6px;
            }
        """)
        
