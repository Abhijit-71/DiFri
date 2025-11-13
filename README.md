## Do check the Desktop branch for latest commits on desktop build , android development is paused by the owner if intrested you can visit Android branch.

# DiFri Browser
![Project logo](Desktop/svg/dbrowser_logo.svg)



A lightweight **Python browser** built with **PyQt6** and **QWebEngineView**, initialized using **`uv init`** for package management.
With a builtin in content filter , blocking certain domains and keywords a clean GUI.

---

## 🖥 Features

* Embedded **Chromium-based browser** using **QWebEngineView**
* Opens **DiFri HomePage** by default
* Navigation controls:

  * Back
  * Forward
  * Reload
* Address bar for custom URLs
* Download Manager
* Content filter , sfae for kids and schools
* Lightweight and cross-platform (Windows, macOS, Linux) if compiled properly.
* Easy to extend with additional PyQt6 widgets or custom styling

---

## Demo of Browser

![Alt text](Demo/img-1.png)
![Alt text](Demo/img-2.png)
![Alt text](Demo/img-3.png)
===============================
* Demo of testing phase
![Alt text](Demo/demo-gif.gif)



## 🚀 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/Abhijit-71/DiFri.git
cd DiFri
```

2. Initialize the environment and manage packages with **UV**:

```bash
uv install
```

3. Run the browser:

for windows --

```bash
cd Desktop
..\.venv\Scripts\activate.ps1
uv run main.py
```
---
## For Exclusive Platform Development
* Checkout Desktop and Andriod branches
* They just provide all req. and code for specific platform 
---

## 📝 Usage

### Basic Navigation:
* Enter a URL in the **address bar** and press **Enter** to navigate
* Use **Back**, **Forward**, and **Reload** buttons to control navigation
* The browser starts on **DiFri HomePage** by default

### Tab Management:
* Click the **Home** button to open a new tab
* Close tabs with the **X** button on each tab
* Drag tabs to reorder them
* Tab titles and icons update automatically

### Downloads:
* Click the **Download** button to open download manager
* Downloads show progress, can be paused/resumed/cancelled
* Recent downloads history is maintained

### Content Filtering:
* Built-in filter blocks inappropriate content automatically
* Safe for educational and family environments

### PDF Viewing:
* **NEW!** Advanced PDF.js viewer with full text functionality
* Text selection, copying, and search within PDFs
* Zoom slider (25% - 300%) with smooth scaling
* Page navigation and real-time page counter
* Works with any PDF file - guaranteed compatibility
* Loading animation with spinning balls during conversion

---

## ⚡ Current Features (Actually Working)

### ✅ **Fully Implemented & Working:**
* **Multiple Tabs** - Full tab management with close, move, and new tab functionality
* **Download Manager** - Complete download system with progress tracking, pause/resume, and history
* **Content Filter** - Built-in filtering system blocking inappropriate content for kids/schools
* **Navigation Controls** - Back, Forward, Reload, Home buttons
* **Address Bar** - URL input with navigation
* **Custom Menus** - Right-click context menus and toolbar dropdowns
* **Tab Icons & Titles** - Dynamic tab titles and favicons
* **Modern UI** - Dark theme with custom styling

### ✅ **PDF Viewer - FULLY WORKING!**
* **PDF.js Integration** - ✅ **COMPLETE!** Advanced PDF rendering system
* Full text selection, copying, and search functionality
* Zoom slider with smooth scaling (25% - 300%)
* Page navigation with arrow buttons
* Clean filename display and page count
* **Always works - no browser compatibility issues!**

### 🚧 **Partially Working:**
* **Cookie Management** - Basic support through WebEngine

### 📝 **Technical Requirements:**
* **Python version:** 3.8–3.12 (PyQt6 compatibility)
* **Dependencies:** PyQt6, PyQt6-WebEngine, requests, urllib3, UV package manager
* **Platforms:** Windows (tested), macOS/Linux (should work if compiled properly)

### 🎯 **What Actually Works vs Claims:**
| Feature | Status | Details |
|---------|--------|----------|
| Multiple Tabs | ✅ **Working** | Full TabManager with close/move/new functionality |
| Download Manager | ✅ **Working** | Progress tracking, pause/resume, history |
| Content Filter | ✅ **Working** | Blocks inappropriate domains and keywords |
| PDF Support | ✅ **Working** | PDF.js viewer with text selection, search, and zoom |
| Navigation | ✅ **Working** | Back/Forward/Reload/Home buttons |
| Custom Menus | ✅ **Working** | Dropdown menus and context menus |
| Modern UI | ✅ **Working** | Dark theme with custom styling |

### 🔧 **Architecture Components:**
* `TabManager` - Multi-tab functionality
* `DownloadManager` - Complete download system  
* `FilterPage` - Content filtering and security
* `BrowserWindow` - Individual browser instances
* `Navigation` - Browser controls and toolbar

---

## 🔗 References

* [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
* [QWebEngineView Documentation](https://doc.qt.io/qt-6/qwebengineview.html)
* [UV Package Manager](https://uv.software/) (for managing dependencies and project environment)

---

## 👥 Contributors

* **Abhijit-71** - Original project creator and maintainer
* **PDF Viewer Feature** - Advanced PDF.js integration with text functionality

### 📄 PDF Viewer Contribution Details

**Problem Solved:**
- Browser couldn't display PDF files - they were only downloaded automatically
- Users wanted to view PDFs directly with text selection and search capabilities

**Solution Implemented:**

1. **PDF Detection System** - Automatically detects PDF links
2. **PDF.js Integration** - Uses Mozilla's PDF.js for native PDF rendering
3. **Text Layer Support** - Full text selection, copying, and search functionality
4. **Advanced Zoom Interface** - Slider control 25%-300% with smooth scaling
5. **Search Functionality** - In-PDF search with highlighted results
6. **Page Navigation** - Arrow buttons for easy page browsing
7. **Loading Animation** - 3 spinning balls during PDF loading
8. **Clean Display** - Filename without URL parameters + page count

**Technologies Used:**
- **PDF.js** - Mozilla's PDF rendering engine
- **requests** - Network file downloads
- **base64** - PDF data encoding
- **PyQt6 QThread** - Background processing without UI freezing
- **HTML5 Canvas** - High-quality PDF rendering
- **JavaScript** - Interactive PDF controls

**Files Created/Modified:**
- `browser/pdfjs_viewer.py` - Main PDF.js viewer system
- `ui/browser.py` - Browser integration
- `requirements.txt` - Updated dependencies

**Features:**
- ✅ **Text Selection** - Select and copy text from PDFs
- ✅ **Search** - Find text within PDFs with highlighting
- ✅ **Zoom** - Smooth zoom from 25% to 300%
- ✅ **Navigation** - Page-by-page browsing
- ✅ **Responsive** - Works with any PDF size

**Result:**
Every PDF now opens directly in the browser with full text functionality - always works! 🎯📄✅

---

## 🛠 License


