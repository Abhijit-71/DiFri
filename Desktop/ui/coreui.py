from PyQt6.QtWidgets import QPushButton, QProgressBar
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyQt6.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
import json

class HoverButton(QPushButton):
    def __init__(self, normal:str, hover:str, pressed:str, size:int, parent=None):
        super().__init__(parent)
        self.icon_normal = QIcon(normal)
        self.icon_hover = QIcon(hover)
        self.icon_pressed = QIcon(pressed)

        self.setIcon(self.icon_normal)
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size,size)
        self.setFlat(True)  # important: disables native style

    def enterEvent(self, event):
        self.setIcon(self.icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.icon_normal)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setIcon(self.icon_pressed)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.underMouse():
            self.setIcon(self.icon_hover)
        else:
            self.setIcon(self.icon_normal)
        super().mouseReleaseEvent(event)



class IconButton(QPushButton):
    def __init__(self, icon:str, size:int):
        super().__init__()
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size, size)
        self.setFlat(True)  # now not used , only for testing buttons with one stste icon

        

class ProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(2)
        self.setTextVisible(False)
        self.setRange(0, 100)
        self.hide()

    def on_load_started(self):
            self.show()
            self.setValue(0)

    def on_load_progress(self, progress):
            self.setValue(progress)

    def on_load_finished(self):
            self.hide()


def trigger_pdf_preview(webview: QWebEngineView, file_path: str):
    """
    Triggers the PDF viewer in the webview if the given file path points to a PDF.
    This function expects the webview's HTML to have a JavaScript function named
    `showPdfViewer(filePath)` which can handle displaying the PDF.

    Args:
        webview: The QWebEngineView instance displaying the HTML UI.
        file_path: The path to the file to be previewed.
    """
    if not file_path or not file_path.lower().endswith('.pdf'):
        # Not a PDF or invalid path, so we don't handle it here.
        return

    # Use pathlib for a modern and robust way to get an absolute path and convert to a file URI.
    # .resolve() gets the absolute path, and .as_uri() creates the 'file://...' URL.
    try:
        # The 'strict=True' argument ensures FileNotFoundError is raised if the path doesn't exist.
        file_uri = Path(file_path).resolve(strict=True).as_uri()
    except FileNotFoundError:
        # In a real app, you might want to log this or show a user-facing error.
        print(f"Error: PDF file not found at '{file_path}'")
        return

    # Safely inject the URI into a JavaScript string using json.dumps.
    # This is crucial to prevent issues with special characters (like quotes)
    # in the file path that could break the JavaScript string.
    js_command = f"showPdfViewer({json.dumps(file_uri)});"

    # Execute the JavaScript function in the webview.
    webview.page().runJavaScript(js_command)