"""
PDF.js Viewer - Full PDF functionality with text selection
==========================================================

Uses PDF.js CDN for complete PDF functionality:
- Text selection and copying
- Search within PDF
- Zoom controls
- Page navigation
- Requires internet connection for PDF.js library
"""

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QThread, pyqtSignal
import requests
import base64
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PDFDownloader(QThread):
    """Downloads PDF for PDF.js viewer"""
    pdf_ready = pyqtSignal(str)  # base64_data
    error = pyqtSignal(str)
    
    def __init__(self, pdf_url):
        super().__init__()
        self.pdf_url = pdf_url
    
    def run(self):
        try:
            response = requests.get(self.pdf_url, verify=False, timeout=15)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            pdf_base64 = base64.b64encode(response.content).decode()
            self.pdf_ready.emit(pdf_base64)
            
        except Exception as e:
            self.error.emit(str(e))

class PDFJSViewer:
    """PDF.js viewer with full functionality"""
    
    def __init__(self):
        self.downloader = None
    
    def show_pdf(self, web_view: QWebEngineView, pdf_url: str):
        """Display PDF with PDF.js"""
        print(f"📄 Loading PDF.js: {pdf_url}")
        
        self.show_loading(web_view, pdf_url)
        
        self.downloader = PDFDownloader(pdf_url)
        self.downloader.pdf_ready.connect(lambda data: self.display_pdfjs(web_view, data, pdf_url))
        self.downloader.error.connect(lambda err: self.show_error(web_view, pdf_url, err))
        self.downloader.start()
    
    def show_loading(self, web_view: QWebEngineView, pdf_url: str):
        """Show loading animation"""
        filename = pdf_url.split('/')[-1].split('?')[0]
        if len(filename) > 50:
            filename = filename[:47] + "..."
        
        loading_html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="background:#2c3e50;color:white;text-align:center;padding:50px;font-family:Arial;">
            <h2>📄 Loading PDF...</h2>
            <p>{filename}</p>
            <div style="margin:30px;">
                <div style="display:flex;justify-content:center;gap:8px;">
                    <div style="width:12px;height:12px;background:#3498db;border-radius:50%;animation:bounce 1.4s ease-in-out infinite both;animation-delay:-0.32s;"></div>
                    <div style="width:12px;height:12px;background:#3498db;border-radius:50%;animation:bounce 1.4s ease-in-out infinite both;animation-delay:-0.16s;"></div>
                    <div style="width:12px;height:12px;background:#3498db;border-radius:50%;animation:bounce 1.4s ease-in-out infinite both;animation-delay:0s;"></div>
                </div>
            </div>
            <style>
                @keyframes bounce {{ 0%, 80%, 100% {{ transform: scale(0); }} 40% {{ transform: scale(1); }} }}
            </style>
        </body>
        </html>
        """
        web_view.setHtml(loading_html)
    
    def display_pdfjs(self, web_view: QWebEngineView, pdf_base64: str, original_url: str):
        """Display PDF with PDF.js implementation"""
        filename = original_url.split('/')[-1].split('?')[0]
        if len(filename) > 50:
            filename = filename[:47] + "..."
        
        # Create complete PDF.js viewer HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>PDF Viewer</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: #2c3e50;
                    font-family: Arial, sans-serif;
                    color: white;
                    overflow: hidden;
                }}
                .header {{
                    background: #34495e;
                    padding: 10px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    position: sticky;
                    top: 0;
                    z-index: 100;
                    border-bottom: 1px solid #555;
                }}
                .filename {{
                    font-size: 14px;
                    flex: 1;
                }}
                .controls {{
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                .btn {{
                    background: #3498db;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    cursor: pointer;
                    font-size: 12px;
                }}
                .btn:hover {{
                    background: #2980b9;
                }}
                .search-box {{
                    padding: 5px;
                    border: 1px solid #555;
                    border-radius: 3px;
                    background: #34495e;
                    color: white;
                    width: 150px;
                }}
                .zoom-controls {{
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}
                .zoom-slider {{
                    width: 120px;
                }}
                .zoom-display {{
                    min-width: 50px;
                    text-align: center;
                    font-size: 12px;
                }}
                .viewer-container {{
                    width: 100%;
                    height: calc(100vh - 50px);
                    background: white;
                    position: relative;
                    overflow: auto;
                }}
                .pdf-canvas {{
                    display: block;
                    margin: 10px auto;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                    cursor: text;
                }}
                .page-info {{
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: rgba(0,0,0,0.7);
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 12px;
                }}
                .text-layer {{
                    position: absolute;
                    left: 0;
                    top: 0;
                    right: 0;
                    bottom: 0;
                    overflow: hidden;
                    opacity: 0.2;
                    line-height: 1.0;
                }}
                .text-layer > span {{
                    color: transparent;
                    position: absolute;
                    white-space: pre;
                    cursor: text;
                    transform-origin: 0% 0%;
                    font-family: sans-serif;
                }}

                .text-layer ::selection {{
                    background: rgba(0, 0, 255, 0.3);
                }}
            </style>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
        </head>
        <body>
            <div class="header">
                <div class="filename">{filename}</div>
                <div class="controls">
                    <input type="text" class="search-box" id="searchBox" placeholder="Search in PDF...">
                    <button class="btn" onclick="searchPDF()">Search</button>
                    <button class="btn" onclick="clearSearch()">Clear</button>
                    <div class="zoom-controls">
                        <input type="range" class="zoom-slider" id="zoomSlider" min="25" max="300" value="100" oninput="setZoom(this.value)">
                        <span class="zoom-display" id="zoomDisplay">100%</span>
                    </div>
                    <button class="btn" onclick="prevPage()">◀</button>
                    <button class="btn" onclick="nextPage()">▶</button>
                </div>
            </div>
            
            <div class="viewer-container" id="viewerContainer">
                <div class="page-info" id="pageInfo">Loading...</div>
            </div>

            <script>
                let pdfDoc = null;
                let currentPage = 1;
                let scale = 1.0;
                let searchResults = [];

                
                // Initialize PDF.js
                pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
                
                // Load PDF
                const pdfData = 'data:application/pdf;base64,{pdf_base64}';
                
                pdfjsLib.getDocument(pdfData).promise.then(function(pdf) {{
                    pdfDoc = pdf;
                    document.getElementById('pageInfo').textContent = `Page 1 of ${{pdf.numPages}}`;
                    renderAllPages();
                }}).catch(function(error) {{
                    console.error('Error loading PDF:', error);
                    document.getElementById('viewerContainer').innerHTML = '<div style="text-align:center;padding:50px;color:red;">Error loading PDF</div>';
                }});
                
                function renderAllPages() {{
                    const container = document.getElementById('viewerContainer');
                    container.innerHTML = '<div class="page-info" id="pageInfo">Page 1 of ' + pdfDoc.numPages + '</div>';
                    
                    for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {{
                        renderPage(pageNum);
                    }}
                }}
                
                function renderPage(pageNum) {{
                    pdfDoc.getPage(pageNum).then(function(page) {{
                        const viewport = page.getViewport({{scale: scale}});
                        
                        // Create page container
                        const pageDiv = document.createElement('div');
                        pageDiv.style.position = 'relative';
                        pageDiv.style.margin = '10px auto';
                        pageDiv.style.width = viewport.width + 'px';
                        pageDiv.style.height = viewport.height + 'px';
                        
                        // Create canvas
                        const canvas = document.createElement('canvas');
                        canvas.className = 'pdf-canvas';
                        canvas.width = viewport.width;
                        canvas.height = viewport.height;
                        
                        const context = canvas.getContext('2d');
                        
                        // Render PDF page
                        const renderContext = {{
                            canvasContext: context,
                            viewport: viewport
                        }};
                        
                        page.render(renderContext).promise.then(function() {{
                            // Add text layer for selection
                            return page.getTextContent();
                        }}).then(function(textContent) {{
                            const textLayerDiv = document.createElement('div');
                            textLayerDiv.className = 'text-layer';
                            textLayerDiv.style.width = viewport.width + 'px';
                            textLayerDiv.style.height = viewport.height + 'px';
                            
                            // Render text layer with scaled viewport
                            pdfjsLib.renderTextLayer({{
                                textContent: textContent,
                                container: textLayerDiv,
                                viewport: viewport,
                                textDivs: []
                            }}).promise.then(() => {{
                                // Scale text elements to match zoom
                                const textElements = textLayerDiv.querySelectorAll('span');
                                textElements.forEach(span => {{
                                    const fontSize = parseFloat(span.style.fontSize) || 12;
                                    span.style.fontSize = (fontSize * scale * 1.4) + 'px';
                                }});
                            }});
                            
                            pageDiv.appendChild(canvas);
                            pageDiv.appendChild(textLayerDiv);
                        }});
                        
                        document.getElementById('viewerContainer').appendChild(pageDiv);
                    }});
                }}
                
                function setZoom(value) {{
                    scale = value / 100;
                    document.getElementById('zoomDisplay').textContent = value + '%';
                    renderAllPages();
                }}
                
                function prevPage() {{
                    if (currentPage > 1) {{
                        currentPage--;
                        scrollToPage(currentPage);
                    }}
                }}
                
                function nextPage() {{
                    if (currentPage < pdfDoc.numPages) {{
                        currentPage++;
                        scrollToPage(currentPage);
                    }}
                }}
                
                function scrollToPage(pageNum) {{
                    const container = document.getElementById('viewerContainer');
                    const pages = container.querySelectorAll('.pdf-canvas');
                    if (pages[pageNum - 1]) {{
                        pages[pageNum - 1].scrollIntoView({{behavior: 'smooth'}});
                        document.getElementById('pageInfo').textContent = `Page ${{pageNum}} of ${{pdfDoc.numPages}}`;
                    }}
                }}
                
                function searchPDF() {{
                    const searchTerm = document.getElementById('searchBox').value.trim();
                    if (!searchTerm) return;
                    
                    clearSearch();
                    searchResults = [];
                    
                    setTimeout(() => {{
                        const textSpans = document.querySelectorAll('.text-layer > div, .text-layer > span');
                        textSpans.forEach(span => {{
                            const text = span.textContent || span.innerText;
                            if (text && text.toLowerCase().includes(searchTerm.toLowerCase())) {{
                                span.style.backgroundColor = '#FF8C00';
                                span.style.color = 'white';
                                span.style.fontWeight = 'bold';
                                searchResults.push(span);
                            }}
                        }});
                        
                        if (searchResults.length > 0) {{
                            searchResults[0].scrollIntoView({{behavior: 'smooth', block: 'center'}});
                        }}
                    }}, 500);
                }}
                
                function clearSearch() {{
                    document.querySelectorAll('.text-layer > div, .text-layer > span').forEach(el => {{
                        el.style.backgroundColor = '';
                        el.style.color = '';
                        el.style.fontWeight = '';
                    }});
                    searchResults = [];
                }}
                
                // Search on Enter key
                document.getElementById('searchBox').addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        searchPDF();
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        web_view.setHtml(html)
        print("✅ PDF.js viewer loaded with full functionality")
    
    def show_error(self, web_view: QWebEngineView, pdf_url: str, error: str):
        """Show error message"""
        filename = pdf_url.split('/')[-1].split('?')[0]
        
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="background:#2c3e50;color:white;text-align:center;padding:50px;font-family:Arial;">
            <h2>❌ Error Loading PDF</h2>
            <p>{filename}</p>
            <p>Error: {error}</p>
        </body>
        </html>
        """
        web_view.setHtml(error_html)