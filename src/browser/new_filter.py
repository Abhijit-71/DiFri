from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl
from urllib.parse import urlparse, parse_qs , unquote
import requests , re , pickle
from core.utils import resource_path

html = """
<html>
    <head>
        <style>
            body {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Segoe UI', Roboto, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background-color: #1e1e1e;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
                padding: 40px 60px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            .card:hover {
                transform: scale(1.03);
            }
            h2 {
                color: #a398ff;
                font-size: 32px;
                margin-bottom: 20px;
                text-shadow: 0 0 8px rgba(163, 152, 255, 0.5);
            }
            p {
                color: #cccccc;
                font-size: 18px;
                line-height: 1;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>DiFri Content Filter</h2>
            <p>Check your network connection.
            <hr>
            Your search contains blocked keywords or Domain.<br>
            Please revise your query and url, then try again.
            <hr style="margin-top:10px;">
            Navigate back to solve the problem , if no search violations.<br>
            </p>
        </div>
    </body>
</html>
"""

path = resource_path("browser/keywords.dat")
with open(path, "rb") as file:
    KEYWORDS = pickle.load(file)


def full_url_parser(parsed):
    combined = "".join([
        parsed.netloc or "",
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or ""
    ]).lower()
    combined = unquote(combined)

    # Replace + with space (common in queries)
    combined = combined.replace("+", " ")
    # Remove all non-alphanumeric characters (keeps letters/numbers only)
    combined = re.sub(r"[^a-z0-9]", "", combined)
    return combined




class FilterPage(QWebEnginePage):

    def acceptNavigationRequest(self, url: QUrl, nav_type, isMainFrame: bool):
       
        if not isMainFrame:
            return super().acceptNavigationRequest(url, nav_type, isMainFrame)

        parsed = urlparse(url.toString())
        full_url = full_url_parser(parsed)


        # Block full domains
        if any(k in str(full_url) for k in KEYWORDS):
            self.setHtml(html)
            return False

        # otherwise allow navigation
        return super().acceptNavigationRequest(url, nav_type, isMainFrame)

