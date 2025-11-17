from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest

class DownloadRouter:
   
    _instance = None
    _active_browsers = {}  # Maps page -> BrowserWindow
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
    
    def register_browser(self, browser_window):
        page = browser_window.browser.page()
        self._active_browsers[id(page)] = browser_window
        #print(f"[Router] browser tab (total: {len(self._active_browsers)})")
    
    def unregister_browser(self, browser_window):
        page = browser_window.browser.page()
        page_id = id(page)
        if page_id in self._active_browsers:
            del self._active_browsers[page_id]
            #print(f"[Router] Unregistered browser tab (remaining: {len(self._active_browsers)})")
    
    def handle_download(self, download:QWebEngineDownloadRequest):
        try:
            url = download.url().toString()
            mime = download.mimeType()
        except Exception:
            url = ''
            mime = ''
        
        # Check if it's a PDF
        is_pdf = (mime and 'pdf' in mime.lower()) or url.lower().endswith('.pdf')
        
        if is_pdf:
            print(f"[Router] PDF download intercepted: {url}")
            # Find which browser tab initiated this
            """try:
                page = download.page()
                if page:
                    page_id = id(page)
                    browser_window = self._active_browsers.get(page_id)
                    
                    if browser_window:
                        print(f"[Router] Routing PDF to originating tab")
                        browser_window.pdf_handler.show_pdf(browser_window.browser, url)
                    else:
                        print(f"[Router] Could not find originating tab (page_id: {page_id})")
                        print(f"[Router] Active tabs: {list(self._active_browsers.keys())}")
                    download.accept()
                else:
                    print(f"[Router] Download has no associated page")
            except Exception as e:
                print(f"[Router] Error routing PDF: {e}")"""
        else:
            # Allow non-PDF downloads
            try:
                download.accept()
            except Exception:
                pass
            
    