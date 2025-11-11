from PyQt6.QtWidgets import QWidget , QVBoxLayout
from .toolbar import Toolbar , Navigation , URLTab
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from PyQt6.QtWebEngineCore import QWebEnginePage
from .coreui import ProgressBar
from browser.new_filter import FilterPage
from browser.local_pdfjs_viewer import LocalPDFJSViewer
import os


class BrowserWindow(QWidget):
    
    _profile = None # works as  cache

    def __init__(self,browser_instance):
        super().__init__()

        
        if self._profile is None:
            self._profile = browser_instance.profile  # browser_instance  is Browser class having all profile related configs
        
          
        self.browser = QWebEngineView()
        self.filtered_page = FilterPage(self._profile, self.browser)
        self.browser.setPage(self.filtered_page)
        self.pdf_handler = LocalPDFJSViewer()
        # intercept downloads (PDF links often trigger a download) and open viewer instead
        try:
            profile = self.browser.page().profile()
            profile.downloadRequested.connect(self.on_download_requested)
        except Exception:
            pass
        html_path = os.path.join(os.getcwd(),"ui/index.html") # gets location for html file
        file_url = QUrl.fromLocalFile(html_path) # converts loaction to url
        self.browser.setUrl(file_url)


        progress = ProgressBar() 
        self.browser.loadStarted.connect(progress.on_load_started)
        self.browser.loadProgress.connect(progress.on_load_progress)
        self.browser.loadFinished.connect(progress.on_load_finished)

        
        navbar = Navigation(self.browser)
        self.urlbar = URLTab(self.browser)
        self.toolbar = Toolbar(navbar,self.urlbar)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.toolbar)
        layout.addWidget(progress)
        layout.addWidget(self.browser)

        self.browser.urlChanged.connect(self.update_urlbox)

    def update_urlbox(self,url):
        url_string = url.toString()
        self.urlbar.urlbox.setText(url_string)
        
        # Check if it's a PDF and handle it
        if url_string.lower().endswith('.pdf'):
            self.pdf_handler.show_pdf(self.browser, url_string)

    def on_download_requested(self, download):
        """Intercept downloads and open PDFs in the viewer instead of saving."""
        try:
            url = download.url().toString()
            mime = download.mimeType()
        except Exception:
            url = ''
            mime = ''

        # if it's a PDF - show in viewer instead of downloading
        if (mime and 'pdf' in mime.lower()) or url.lower().endswith('.pdf'):
            print(f"[PDF] מציג PDF במקום הורדה: {url}")
            download.cancel()  # ביטול ההורדה
            self.pdf_handler.show_pdf(self.browser, url)  # הצגה בדפדפן
        else:
            # allow other downloads to proceed (default behavior)
            try:
                download.accept()
            except Exception:
                pass
    
