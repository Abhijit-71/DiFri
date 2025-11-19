from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
import os


class Browser:

    _download_handler_connected = False # to solve multiple connections


    def __init__(self):
        super().__init__()
        self.configure()
    
    
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
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
    
        
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled,True) #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)  #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)   #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)   #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)  #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)  #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)  #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)  #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)   #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)   #type:ignore
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)   #type:ignore
    
        
        
        # download is handled at browser window
        
    

    

    