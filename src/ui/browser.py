from PyQt6.QtWidgets import QWidget, QVBoxLayout , QFileDialog
from .toolbar import Toolbar, Navigation, URLTab
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from .coreui import ProgressBar
from browser.new_filter import FilterPage
from PyQt6.QtWebEngineCore import QWebEnginePage
from .dropdown import PermissionDialog 
from core.utils import resource_path
import os

class BrowserWindow(QWidget):
    
    _profile = None  # works as cache

    def __init__(self, browser_instance,tabmanager):
        super().__init__()

        if self._profile is None:
            self._profile = browser_instance.profile
        
        self.tab_manager = tabmanager
        self.browser = QWebEngineView(self)
        self.filtered_page = FilterPage(self._profile, self.browser)
        self.browser.setPage(self.filtered_page)
        
        if browser_instance._download_handler_connected == False: #from Browser class var.
            self.filtered_page.profile().downloadRequested.connect(self.handle_downloads) #type:ignore
            browser_instance._download_handler_connected = True
        
        self.filtered_page.fullScreenRequested.connect(self.handle_fullscreen)
        self.filtered_page.featurePermissionRequested.connect(self.handle_permission)
        self.browser.createWindow = self.create_window #type:ignore
        
        html_path =  resource_path("ui/index.html")
        file_url = QUrl.fromLocalFile(html_path)
        self.browser.setUrl(file_url)

        progress = ProgressBar() 
        self.browser.loadStarted.connect(progress.on_load_started)
        self.browser.loadProgress.connect(progress.on_load_progress)
        self.browser.loadFinished.connect(progress.on_load_finished)

        navbar = Navigation(self.browser)
        self.urlbar = URLTab(self.browser)
        self.toolbar = Toolbar(navbar, self.urlbar,self.tab_manager.download_menu)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.toolbar)
        layout.addWidget(progress)
        layout.addWidget(self.browser)

        self.browser.urlChanged.connect(self.update_urlbox)


    def update_urlbox(self, url:QUrl):
        url_string = url.toString()
        self.urlbar.urlbox.setText(url_string)

       
    def handle_downloads(self,download):
        suggested_name = download.downloadFileName()
        default_download_dir = os.path.join(os.environ["USERPROFILE"], "Downloads")
        suggested_path = os.path.join(default_download_dir, suggested_name)

        path,_ = QFileDialog.getSaveFileName(
            None,
            "DiFri Download Manager",
            suggested_path,
        )

        if path:
            download.setDownloadFileName(os.path.basename(path))
            download.setDownloadDirectory(os.path.dirname(path))
            download.accept()
            self.tab_manager.download_menu.add_download(download)
            self.toolbar.downloadbtn.showMenu()
        else:
            download.cancel()
   
            
    def handle_fullscreen(self, request):
        if request.toggleOn():
            self.showMaximized()
        else:
            self.showNormal()
        request.accept()
    
    
    def handle_permission(self, url, feature):
        origin = url.toString()
        dialog = PermissionDialog(feature, origin)
        result = dialog.exec()
        allowed = dialog.allowed
        if allowed:
            self.filtered_page.setFeaturePermission(
                url,
                feature,
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )
        else:
            self.filtered_page.setFeaturePermission(
                url,
                feature,
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser
            )
      
        
    def create_window(self, window_type):
        new_tab = self.tab_manager.add_tab() if self.tab_manager else None
        return new_tab.browser if new_tab else None
    
  