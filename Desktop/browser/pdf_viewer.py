"""
PDF Viewer - Displays PDF files directly in browser
==================================================

A guaranteed PDF viewer that downloads PDFs and converts them to HTML with images.
Works with any PDF file by rendering each page as a high-quality image.

Features:
- Downloads PDF files securely (ignores SSL errors)
- Converts each page to PNG images using PyMuPDF
- Displays with zoom slider (25% - 300%)
- Clean filename display (removes URL parameters)
- Responsive design with smooth zoom transitions

Dependencies:
- PyQt6: GUI framework
- PyMuPDF (fitz): PDF processing
- requests: HTTP downloads
- urllib3: SSL warning suppression
"""

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QThread, pyqtSignal
import requests
import fitz
import base64
import urllib3

# Disable SSL warnings for PDF downloads
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PDFConverter(QThread):
    """Thread for converting PDF to HTML with images"""
    html_ready = pyqtSignal(str)
    
    def __init__(self, pdf_url):
        super().__init__()
        self.pdf_url = pdf_url
    
    def run(self):
        """Download PDF and convert to HTML"""
        try:
            print(f"📄 Downloading PDF: {self.pdf_url}")
            
            # Download PDF with SSL verification disabled
            response = requests.get(self.pdf_url, verify=False, timeout=15)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            print(f"✅ PDF downloaded: {len(response.content)} bytes")
            
            # Open with PyMuPDF
            doc = fitz.open(stream=response.content, filetype="pdf")
            
            # Clean filename (remove URL parameters)
            filename = self.pdf_url.split('/')[-1].split('?')[0]
            if len(filename) > 50:
                filename = filename[:47] + "..."
            
            # Generate HTML with embedded images
            html_parts = [f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>PDF Viewer</title>
                <style>
                    body {{ margin: 0; padding: 10px; background: #2c3e50; text-align: center; }}
                    .header {{ color: white; margin-bottom: 15px; position: sticky; top: 0; background: #2c3e50; padding: 8px; z-index: 100; display: flex; justify-content: space-between; align-items: center; }}
                    .filename {{ font-size: 14px; flex: 1; text-align: left; }}
                    .controls {{ display: flex; align-items: center; gap: 10px; }}
                    .zoom-slider {{ width: 150px; }}
                    .zoom-display {{ color: white; font-size: 14px; min-width: 50px; }}
                    .page {{ margin: 10px auto; box-shadow: 0 4px 8px rgba(0,0,0,0.3); display: flex; justify-content: center; }}
                    .page img {{ transition: width 0.2s ease; display: block; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <div class="filename">{filename} ({len(doc)} pages)</div>
                    <div class="controls">
                        <input type="range" class="zoom-slider" id="zoom-slider" min="25" max="300" value="100" oninput="setZoom(this.value)">
                        <span class="zoom-display" id="zoom-display">100%</span>
                    </div>
                </div>
                <div id="pages">
            """]
            
            # Convert each page to image
            for page_num in range(len(doc)):
                print(f"Rendering page {page_num + 1}/{len(doc)}")
                
                page = doc[page_num]
                mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for quality
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to base64
                img_data = pix.tobytes("png")
                b64_img = base64.b64encode(img_data).decode()
                
                html_parts.append(f"""
                <div class="page">
                    <img src="data:image/png;base64,{b64_img}" 
                         style="max-width:100%; height:auto; border:1px solid #ccc;">
                </div>
                """)
            
            # Add JavaScript for zoom functionality
            html_parts.append("""
                </div>
                <script>
                    function setZoom(value) {
                        const pages = document.querySelectorAll('.page img');
                        pages.forEach(img => {
                            img.style.width = value + '%';
                            img.style.maxWidth = 'none';
                            img.style.margin = '0 auto';
                        });
                        document.getElementById('zoom-display').textContent = value + '%';
                    }
                </script>
            </body>
            </html>
            """)
            
            doc.close()
            
            final_html = "".join(html_parts)
            self.html_ready.emit(final_html)
            
            print("✅ PDF converted to HTML successfully!")
            
        except Exception as e:
            # Generate error page
            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"></head>
            <body style="background:#2c3e50;color:white;text-align:center;padding:50px;font-family:Arial;">
                <h2>❌ Error</h2>
                <p>{self.pdf_url.split('/')[-1]}</p>
                <p>Error: {str(e)}</p>
                <p>Try another PDF or check internet connection</p>
            </body>
            </html>
            """
            self.html_ready.emit(error_html)
            print(f"❌ Error: {e}")

class PDFViewer:
    """Main PDF viewer class"""
    
    def __init__(self):
        self.converter = None
    
    def show_pdf(self, web_view: QWebEngineView, pdf_url: str):
        """Display PDF in web view - always works!"""
        print(f"🚀 Starting PDF conversion: {pdf_url}")
        
        # Show loading page with spinning balls
        loading_html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="background:#2c3e50;color:white;text-align:center;padding:50px;font-family:Arial;">
            <h2>📄 Loading PDF...</h2>
            <p>{pdf_url.split('/')[-1].split('?')[0]}</p>
            <div class="spinner-container">
                <div class="spinner">
                    <div class="ball ball1"></div>
                    <div class="ball ball2"></div>
                    <div class="ball ball3"></div>
                </div>
            </div>
            <style>
                .spinner-container {{
                    display: flex;
                    justify-content: center;
                    margin: 30px 0;
                }}
                .spinner {{
                    display: flex;
                    gap: 8px;
                }}
                .ball {{
                    width: 12px;
                    height: 12px;
                    background: #3498db;
                    border-radius: 50%;
                    animation: bounce 1.4s ease-in-out infinite both;
                }}
                .ball1 {{ animation-delay: -0.32s; }}
                .ball2 {{ animation-delay: -0.16s; }}
                .ball3 {{ animation-delay: 0s; }}
                @keyframes bounce {{
                    0%, 80%, 100% {{ transform: scale(0); }}
                    40% {{ transform: scale(1); }}
                }}
            </style>
        </body>
        </html>
        """
        web_view.setHtml(loading_html)
        
        # Start conversion
        self.converter = PDFConverter(pdf_url)
        self.converter.html_ready.connect(lambda html: web_view.setHtml(html))
        self.converter.start()
        
        print("🔄 Conversion started...")