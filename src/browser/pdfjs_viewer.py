
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QThread, pyqtSignal
import requests , base64 , urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PDFDownloader(QThread):
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
  
        #print(f"Loading PDF.js: {pdf_url}")
        
        self.show_loading(web_view, pdf_url)
        
        self.downloader = PDFDownloader(pdf_url)
        self.downloader.pdf_ready.connect(lambda data: self.display_pdfjs(web_view, data, pdf_url))
        #self.downloader.error.connect(lambda err: self.show_error(web_view, pdf_url))
        self.downloader.start()
    
    def show_loading(self, web_view: QWebEngineView, pdf_url: str):
        """Show loading animation"""
        filename = pdf_url.split('/')[-1].split('?')[0]
        if len(filename) > 50:
            filename = filename[:47] + "..."
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f1419 100%);
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
        }}
        
        /* Animated background gradient */
        body::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(138, 43, 226, 0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }}
        
        @keyframes rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .container {{
            position: relative;
            z-index: 1;
            text-align: center;
            padding: 40px;
            background: rgba(30, 30, 46, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(138, 43, 226, 0.2);
            box-shadow: 0 8px 32px rgba(138, 43, 226, 0.15);
            max-width: 500px;
        }}
        
        .icon {{
            font-size: 64px;
            margin-bottom: 20px;
            animation: float 3s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        h2 {{
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 50%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .filename {{
            color: #9ca3af;
            font-size: 14px;
            margin-bottom: 40px;
            word-break: break-all;
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }}
        
        .loader-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            margin-top: 30px;
        }}
        
        .dot {{
            width: 14px;
            height: 14px;
            background: linear-gradient(135deg, #a78bfa, #8b5cf6);
            border-radius: 50%;
            animation: bounce 1.4s ease-in-out infinite both;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
        }}
        
        .dot:nth-child(1) {{
            animation-delay: -0.32s;
        }}
        
        .dot:nth-child(2) {{
            animation-delay: -0.16s;
        }}
        
        .dot:nth-child(3) {{
            animation-delay: 0s;
        }}
        
        @keyframes bounce {{
            0%, 80%, 100% {{
                transform: scale(0);
                opacity: 0.5;
            }}
            40% {{
                transform: scale(1.2);
                opacity: 1;
            }}
        }}
        
        .progress-bar {{
            width: 100%;
            height: 3px;
            background: rgba(138, 43, 226, 0.2);
            border-radius: 10px;
            margin-top: 30px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #a78bfa, #8b5cf6, #7c3aed);
            border-radius: 10px;
            animation: progress 2s ease-in-out infinite;
        }}
        
        @keyframes progress {{
            0% {{
                width: 0%;
                opacity: 0.8;
            }}
            50% {{
                width: 70%;
                opacity: 1;
            }}
            100% {{
                width: 100%;
                opacity: 0.8;
            }}
        }}
        
        .status-text {{
            margin-top: 20px;
            font-size: 12px;
            color: #6b7280;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">📄</div>
        <h2>Loading PDF</h2>
        <div class="filename">{filename}</div>
        <div class="loader-container">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        <div class="status-text">Preparing document viewer...</div>
    </div>
</body>
</html>
        """
        web_view.setHtml(html)
    
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
      background: linear-gradient(135deg, #1e1b2e, #2a2550);
      font-family: 'Segoe UI', Arial, sans-serif;
      color: #eee;
      overflow: hidden;
    }}

    .header {{
      background: rgba(45, 40, 80, 0.95);
      padding: 10px 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      border-bottom: 1px solid #5f4b8b;
      box-shadow: 0 0 10px rgba(0,0,0,0.4);
      backdrop-filter: blur(10px);
    }}

    .filename {{
      font-size: 14px;
      font-weight: 500;
      color: #cfc8ff;
      flex: 1;
    }}

    .controls {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .btn {{
      background: #6c5ce7;
      color: #fff;
      border: none;
      padding: 6px 12px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 13px;
      transition: all 0.2s ease;
    }}

    .btn:hover {{
      background: #8e7cff;
      box-shadow: 0 0 8px #8e7cff;
    }}

    .search-box {{
      padding: 6px 8px;
      border: 1px solid #5f4b8b;
      border-radius: 5px;
      background: #2f284f;
      color: #fff;
      width: 160px;
    }}

    .zoom-controls {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .zoom-slider {{
      width: 120px;
      accent-color: #8e7cff;
    }}

    .zoom-display {{
      min-width: 50px;
      text-align: center;
      font-size: 12px;
      color: #c3b4ff;
    }}

    .viewer-container {{
      width: 100%;
      height: calc(100vh - 60px);
      background: #1f1a33;
      position: relative;
      overflow: auto;
      scroll-behavior: smooth;
    }}

    .pdf-canvas {{
      display: block;
      margin: 15px auto;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
      border-radius: 6px;
      background: #fff;
      cursor: text;
    }}

    .page-info {{
      position: fixed;
      top: 70px;
      right: 20px;
      background: rgba(100, 85, 150, 0.8);
      color: white;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 13px;
      z-index: 200;
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
      background: rgba(120, 90, 255, 0.3);
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

    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

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
        const pageDiv = document.createElement('div');
        pageDiv.style.position = 'relative';
        pageDiv.style.margin = '15px auto';
        pageDiv.style.width = viewport.width + 'px';
        pageDiv.style.height = viewport.height + 'px';
        
        const canvas = document.createElement('canvas');
        canvas.className = 'pdf-canvas';
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        
        const context = canvas.getContext('2d');
        const renderContext = {{canvasContext: context, viewport: viewport}};

        page.render(renderContext).promise.then(function() {{
          return page.getTextContent();
        }}).then(function(textContent) {{
          const textLayerDiv = document.createElement('div');
          textLayerDiv.className = 'text-layer';
          textLayerDiv.style.width = viewport.width + 'px';
          textLayerDiv.style.height = viewport.height + 'px';
          
          pdfjsLib.renderTextLayer({{
            textContent: textContent,
            container: textLayerDiv,
            viewport: viewport,
            textDivs: []
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
            span.style.backgroundColor = '#9b59b6';
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

    document.getElementById('searchBox').addEventListener('keypress', function(e) {{
      if (e.key === 'Enter') {{
        searchPDF();
      }}
    }});
  </script>
</body>
</html>"""
        
        web_view.setHtml(html)
        print("PDF.js loaded ")
    
    def show_error(self, web_view: QWebEngineView):
        """Show error message"""
        
        error_html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>PDF Load Error</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: linear-gradient(135deg, #1e1b2e, #2a2550);
      color: #e0dcff;
      font-family: 'Segoe UI', Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }}

    .error-box {{
      background: rgba(45, 40, 80, 0.9);
      border: 1px solid #5f4b8b;
      box-shadow: 0 0 25px rgba(127, 90, 240, 0.2);
      border-radius: 12px;
      padding: 40px 50px;
      max-width: 400px;
      text-align: center;
      backdrop-filter: blur(10px);
      animation: fadeIn 0.6s ease;
    }}

    h2 {{
      color: #ff5c8a;
      font-size: 24px;
      margin-bottom: 15px;
    }}

    p {{
      margin: 10px 0;
      color: #cfc8ff;
      font-size: 14px;
    }}

    .filename {{
      font-weight: 600;
      color: #a995ff;
    }}

    .retry-btn {{
      margin-top: 25px;
      background: linear-gradient(135deg, #7f5af0, #5f4b8b);
      color: #fff;
      border: none;
      border-radius: 50px;
      padding: 10px 25px;
      font-size: 14px;
      cursor: pointer;
      box-shadow: 0 0 10px rgba(127, 90, 240, 0.4);
      transition: all 0.3s ease;
    }}

    .retry-btn:hover {{
      background: linear-gradient(135deg, #9d8aff, #7f5af0);
      box-shadow: 0 0 20px rgba(157, 138, 255, 0.7);
      transform: translateY(-2px);
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body>
  <div class="error-box">
    <h2>Error Loading PDF</h2>
    <p><strong>Error:</strong>File not available to download</p>
    <button class="retry-btn" onclick="window.location.reload()">↻ Retry</button>
  </div>
</body>
</html>"""
        web_view.setHtml(error_html)