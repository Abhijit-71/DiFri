from PyQt6.QtWebEngineCore import QWebEngineProfile , QWebEngineDownloadRequest 
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


        # Why this works: Earlier, profile was instantiated many times creating multiple profiles.
        # Now only one profile. Same name does not mean one profile - may create many instances.
        

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
        
        
        # Download is also connected once, for no repeated signal 

        if self._download_handler_connected == False:
            self.profile.downloadRequested.connect(self.download_req) #type:ignore
            self._download_handler_connected = True

        
    

    def download_req(self,download:QWebEngineDownloadRequest):
        
        suggested_name = download.downloadFileName()
        url = download.url().toString()
    
        print(f"Download triggered: {suggested_name}, URL: {url}")
        
        # Block PDF downloads - they should be handled by the PDF viewer
        if suggested_name.lower().endswith('.pdf') or url.lower().endswith('.pdf'):
            print("Blocking PDF download - should be handled by PDF viewer")
            download.cancel()
            return

        # Handle other downloads normally
        path,_ = QFileDialog.getSaveFileName(
            None,
            "dBrowser Download Manager",
            suggested_name,
        )

        if path:
            download.setDownloadFileName(os.path.basename(path))
            download.setDownloadDirectory(os.path.dirname(path))
            self.download_manager.add_download(download)
        else:
            download.cancel()
            print("cancelled")
    

