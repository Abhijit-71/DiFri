from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl
from urllib.parse import urlparse, parse_qs
import requests , re , os , pickle


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
                color: #ff4c4c;
                font-size: 32px;
                margin-bottom: 20px;
                text-shadow: 0 0 8px rgba(255, 76, 76, 0.5);
            }
            p {
                color: #cccccc;
                font-size: 18px;
                line-height: 1.5;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🚫 Blocked Search</h2>
            <p>Your search contains blocked keywords or Domain.<br>
            Please revise your query and url, then try again.</p>
        </div>
    </body>
</html>
"""

path = os.path.join(os.getcwd(), "browser/keywords.dat")
with open(path, "rb") as file:
    KEYWORDS = pickle.load(file)


def safe_domain(domain:str) -> bool|None:
    if domain is None:
        return True
    domain_pattern = re.compile(
    r"^(?!-)([A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,}$"
    )
    if not domain_pattern.match(domain):
        return True
    
    url = "https://family.cloudflare-dns.com/dns-query"
    headers = {"accept": "application/dns-json"}
    params = {"name": domain, "type": "A"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        if data['Answer'][0]['data'] == '0.0.0.0':
            return False 
        else : 
            return True  
    except Exception as e:
        print(f"Error checking {domain}: {e}")


def registered_domain(hostname: str) -> str | None:
    if not hostname:
        return None
    parts = hostname.split('.')
    return '.'.join(parts[-2:]) if len(parts) >= 2 else hostname



class FilterPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.web_view = parent  # Store reference to the web view

    def acceptNavigationRequest(self, url: QUrl, nav_type, isMainFrame: bool):
        try:
            if not isMainFrame:
                return super().acceptNavigationRequest(url, nav_type, isMainFrame)

            url_string = url.toString()
            parsed = urlparse(url_string)
        except Exception as e:
            print(f"[FILTER] ERROR: {e}", flush=True)
            return super().acceptNavigationRequest(url, nav_type, isMainFrame)
        
        # Regular filtering
        domain = registered_domain(parsed.hostname or "") # takes the browser field and convert to domain format str
        qs = parse_qs(parsed.query)
        search_term = qs.get("q", [""])[0].lower()
        search_term = re.sub(r'[^a-z]+', '', search_term)

        if not safe_domain(domain): #type:ignore
            self.setHtml(html)
            return False

        if domain in ("google.com", "bing.com", "duckduckgo.com", "yahoo.com","brave.com"):
            if any(k in search_term for k in KEYWORDS):
                self.setHtml(html)
                return False

        return super().acceptNavigationRequest(url, nav_type, isMainFrame)