# Browser Module Documentation

## PDF.js Viewer (`pdfjs_viewer.py`)

### Overview
Advanced PDF viewer implementation using Mozilla's PDF.js library for rendering PDFs with full text functionality.

### Features
- **Text Selection & Copy**: Full text layer support for selecting and copying PDF content
- **Search Functionality**: In-document search with highlighted results
- **Zoom Controls**: Slider-based zoom from 25% to 300%
- **Page Navigation**: Arrow-based page browsing
- **Responsive Design**: Adapts to different PDF sizes and screen resolutions

### Dependencies
- **External**: PDF.js 3.11.174 (CDN)
- **Python**: PyQt6, requests, urllib3
- **Network**: Requires internet connection for PDF.js library
- **Note**: Local PDF.js files removed to avoid confusion with CDN usage

### Security Considerations
- SSL verification disabled for PDF downloads (`verify=False`)
- Downloads PDFs from external URLs without validation
- Consider implementing URL whitelist for production use

### Usage Example
```python
from browser.pdfjs_viewer import PDFJSViewer

viewer = PDFJSViewer()
viewer.show_pdf(web_view, "https://example.com/document.pdf")
```

### Configuration
- **Timeout**: 15 seconds for PDF downloads
- **File Size**: No explicit limit (memory dependent)
- **Supported Formats**: PDF only

### Error Handling
- Network timeouts
- Invalid PDF files
- HTTP errors (non-200 responses)
- PDF.js rendering failures

### Performance Notes
- PDFs are downloaded completely before rendering
- Large files may cause memory issues
- Background processing prevents UI blocking

### Browser Compatibility
- Uses modern JavaScript features (ES6+)
- Requires WebEngine with JavaScript support
- PDF.js handles cross-browser compatibility