from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl
from ui.mwindow import MainWindow
import sys,os
from ui.tabbar import TabManager


# ======== starting point ==========

file_to_open = None
if len(sys.argv) > 1:
    file_to_open = sys.argv[1]

app = QApplication(sys.argv)


tab_manager = TabManager()

if file_to_open:
    tab_manager.browser_window.browser.setUrl(QUrl.fromLocalFile(os.path.abspath(file_to_open)))
    
    
# Create main window with custom title bar
window = MainWindow(tab_manager.content_stack,tab_manager)


window.show()
sys.exit(app.exec())
