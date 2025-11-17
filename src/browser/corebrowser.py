from PyQt6.QtWebEngineCore import QWebEngineProfile , QWebEngineDownloadRequest , QWebEngineSettings
from PyQt6.QtWidgets import QFileDialog
from ui.dropdown import DownloadManager
import os


class Browser:

    _download_handler_connected = False

    def __init__(self,DownloadManager:DownloadManager):
        super().__init__()
        self.configure()
        self.download_manager = DownloadManager
    
    def configure(self):


        """why this works ?? ==> Earlier , profile was instanciated many times creating multiple profiles , now only one profile 
         same name does not mean one profile . May also create many instaces of a profile"""
        

        profile_path = os.path.join(os.getcwd(),"user_data")
        cache_path = os.path.join(os.getcwd(),"user_cache")
        os.makedirs(profile_path, exist_ok=True)
        os.makedirs(cache_path, exist_ok=True)
        self.profile = QWebEngineProfile("user_data")
        self.profile.setPersistentStoragePath(profile_path)
        self.profile.setCachePath(cache_path)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
            )
        
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled,True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        #settings.setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode, True) === forcing makes colors obselete
        
        
        # download is also connected once , for no repeated signal 

        if self._download_handler_connected == False:
            self.profile.downloadRequested.connect(self.download_req) #type:ignore
            self._download_handler_connected = True

        
    
    def download_req(self,download:QWebEngineDownloadRequest):
        
        suggested_name = download.downloadFileName()
    
        #print(f"trigerred {suggested_name}")

        path,_ = QFileDialog.getSaveFileName(
            None,
            "DiFri Download Manager",
            suggested_name,
        )

        if path:
            download.setDownloadFileName(os.path.basename(path))
            download.setDownloadDirectory(os.path.dirname(path))
            self.download_manager.add_download(download)
        else:
            download.cancel()
    

    

    