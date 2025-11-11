from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl
from urllib.parse import urlparse, parse_qs
import os

KEYWORDS = [
    "porn", "sex", "erotic", "nudity", "xxx", "adult", "hentai", "fetish", "webcam", "pornographic",
    "hardcore", "nsfw", "orgasm", "masturbation", "pornstar", "strip", "voyeurism", "bdsm", "fetishism", 
    "s&m", "breast", "butt", "genital", "penis", "vagina", "nipple", "anal", "hardcore", "amateur", 
    "milf", "cum", "gay", "lesbian", "blowjob", "dildo", "bukkake", "fisting", "dominatrix",
    "oral sex", "sex toys", "cuckold", "furry", "sex tape", "sex video", "adult film", "porn video",
    "nude", "sex cam", "camgirl", "camboy", "sex worker", "xxx videos", "adult streaming", "erotic story",
    "xxx webcam", "live porn", "nude model", "exotic dancer", "stripping", "escort", "hooker", "prostitute",
    "sex shop", "escort service", "sex services", "adult chat", "stripper", "masturbate", "oral", "hard-on",
    "shemale", "transgender", "intercourse", "orgy", "sex addict", "porn addiction", "cybersex", "kink", 
    "voyeur", "pornography", "pussy", "cumshot", "cock","suck", "buttplug", "dildo", "vibrator", "sex fantasy", "lube", "condom", "dirty talk", "pillow humping","tease", "striptease", "sexting", "dominant", "submissive", "anal play", 
    "slut", "whore", "bimbo", "horny", "sex tape leak", "sex scandal", "erotic roleplay","squirt","creampie","camel toe"
    "adult dating", "sexual harassment", "seduction", "flirting", "sex ad", "adult games", "porn blog", 
    "sexual content", "adult entertainment", "adult clips", "hardcore porn", "adult videos", "explicit","desi","mms","boobs", "naked","spank","gilf","hot girl","hot women","hot model","teen porn","girl showing","bikini","panty","bra"
]

BLOCKED_DOMAINS = [
    "pornhub.com", "xvideos.com", "xhamster.com", "youporn.com", "brazzers.com", "redtube.com", 
    "chaturbate.com", "onlyfans.com", "camsoda.com", "spankwire.com", "hentaifoundry.com", "fakku.net",
    "bdsm.com", "myfreecams.com", "livejasmin.com", "livecamgirls.com", "bongacams.com", "cam4.com", 
    "camgirl.com", "shemale.com", "gayporn.com", "amateurporn.com", "tnaflix.com", "tube8.com", 
    "pornostar.com", "sex.com", "pornstarplanet.com", "fapdu.com", "xtube.com", "meetyourheroes.com",
    "dirtyroulette.com", "eroticmature.com", "fetlife.com", "adultfriendfinder.com", "sexsearch.com",
    "adultmatchmaker.com", "adultsearch.com", "naked.com", "erotica.com", "sexchat.com", "nudeweb.com",
    "hentaimama.com", "porno.com", "sexcam.com", "sexkittens.com", "sexlovers.com", "playboy.com","eporner.com",
    "teenxy.com","kamababa.desi","nakedgirls.com", "nudeart.com", "xxxtentacion.com", "bustybabe.com", "camgirl.com", "tubepornclassic.com","spankbang.com","pornhat.com"
]

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
            print(f"[FILTER] acceptNavigationRequest called", flush=True)
            print(f"[FILTER] isMainFrame: {isMainFrame}", flush=True)
            
            if not isMainFrame:
                print(f"[FILTER] Not main frame, allowing", flush=True)
                return super().acceptNavigationRequest(url, nav_type, isMainFrame)

            print(f"[FILTER] Processing main frame navigation", flush=True)
            url_string = url.toString()
            print(f"[FILTER] URL string: {url_string}", flush=True)
            
            parsed = urlparse(url_string)
            print(f"[FILTER] URL parsed successfully", flush=True)
        except Exception as e:
            print(f"[FILTER] ERROR in initial processing: {e}", flush=True)
            return super().acceptNavigationRequest(url, nav_type, isMainFrame)
        
        # PDF זיהוי מושבת זמנית
        if url_string.lower().endswith('.pdf'):
            print(f"[PDF] PDF זוהה אך לא מטופל: {url_string}", flush=True)
            # נתן לדפדפן לטפל בזה רגיל
            pass

        # Regular filtering
        domain = registered_domain(parsed.hostname or "")
        qs = parse_qs(parsed.query)
        search_term = qs.get("q", [""])[0].lower()

        print(f"[FILTER] → Navigating to {domain}, search={search_term!r}", flush=True)
        print(f"[FILTER] Full URL: {url_string}", flush=True)
        print(f"[FILTER] Is main frame: {isMainFrame}", flush=True)

        if domain in BLOCKED_DOMAINS or any(k in str(domain) for k in KEYWORDS):
            self.setHtml(f"<h2>Blocked</h2><p>{domain} is restricted.</p>")
            return False

        if domain in ("google.com", "bing.com", "duckduckgo.com", "yahoo.com","brave.com"):
            if any(k in search_term for k in KEYWORDS):
                self.setHtml("<h2>Blocked Search</h2><p>Search contains blocked keywords.</p>")
                return False

        return super().acceptNavigationRequest(url, nav_type, isMainFrame)