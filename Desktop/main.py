from PyQt6.QtWebEngineCore import QWebEngineGlobalSettings
from PyQt6.QtWidgets import QApplication , QMainWindow , QVBoxLayout
from PyQt6.QtCore import QUrl
from ui.mwindow import MainWindow , PaddedWindow
from ui.toolbar import Navigation , Toolbar , URLTab
import sys
from ui.tabbar import TabManager
from ui.browser import BrowserWindow


"""app = QApplication(sys.argv)
browser = QWebEngineView()
browser.setUrl(QUrl('https://google.com'))

tools = Navigation(browser)
navbar = Toolbar(tools)
boom = PaddedWindow(browser,navbar)
window = MainWindow(boom)



window.show()
app.exec()"""

dns_config = [
    '--enable-features=DnsOverHttps',
    '--dns-over-https-servers=https://185.228.168.168/dns-query',
]

sys.argv.extend(dns_config)
# Apply the DNS mode globally

app = QApplication(sys.argv)

tab_manager = TabManager()
CentralWidget = PaddedWindow(tab_manager,"#181826")

# Create main window with blue title bar
window = MainWindow(CentralWidget,tab_manager)


window.show()
sys.exit(app.exec())
