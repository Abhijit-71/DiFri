from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .toolbar import Toolbar, Navigation, URLTab
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from .coreui import ProgressBar
from browser.new_filter import FilterPage
from browser.downloadmanager import DownloadRouter
from PyQt6.QtWebEngineCore import QWebEnginePage
import os

class BrowserWindow(QWidget):
    
    _profile = None  # works as cache
    _download_connected = False  # Track if download handler is connected

    def __init__(self, browser_instance):
        super().__init__()

        if self._profile is None:
            self._profile = browser_instance.profile
        
        self.browser = QWebEngineView(self)
        self.filtered_page = FilterPage(self._profile, self.browser)
        self.browser.setPage(self.filtered_page)
        self.filtered_page.fullScreenRequested.connect(self.handle_fullscreen)
        self.filtered_page.featurePermissionRequested.connect(self.handle_permission)
        #self.pdf_handler = PDFJSViewer()
        
        
        # Register this browser with the router
        router = DownloadRouter()
        router.register_browser(self)
        # Connect download handler ONCE globally
        if not BrowserWindow._download_connected:
            try:
                profile = self.browser.page().profile() #type:ignore
                profile.downloadRequested.connect(router.handle_download) #type:ignore
                BrowserWindow._download_connected = True
                #print("[Browser] Download router connected")
            except Exception as e:
                print(f"[Browser] Error connecting downloads: {e}")
        
        
        
        html_path = os.path.join(os.getcwd(), "ui/index.html")
        file_url = QUrl.fromLocalFile(html_path)
        self.browser.setUrl(file_url)

        progress = ProgressBar() 
        self.browser.loadStarted.connect(progress.on_load_started)
        self.browser.loadProgress.connect(progress.on_load_progress)
        self.browser.loadFinished.connect(progress.on_load_finished)

        navbar = Navigation(self.browser)
        self.urlbar = URLTab(self.browser)
        self.toolbar = Toolbar(navbar, self.urlbar)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.toolbar)
        layout.addWidget(progress)
        layout.addWidget(self.browser)

        self.browser.urlChanged.connect(self.update_urlbox)

    def update_urlbox(self, url):
        url_string = url.toString()
        self.urlbar.urlbox.setText(url_string)
        
            
    def handle_fullscreen(self, request):
        if request.toggleOn():
            self.showFullScreen()
        else:
            self.showNormal()
        request.accept()
    
    def handle_permission(self, url, feature, callback):
        if feature == QWebEnginePage.Feature.Clipboard:
            callback(True)
        else:
            callback(True)
        
    def closeEvent(self, event):
        """Clean up when tab is closed"""
        router = DownloadRouter()
        router.unregister_browser(self)
        super().closeEvent(event)