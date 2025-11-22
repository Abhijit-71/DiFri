### Do check the Desktop branch for latest commits on desktop build , android development is paused by the owner if intrested you can visit Android branch.

# DiFri Browser
![Project logo](Desktop/svg/dbrowser_logo.svg)



A lightweight **Python browser** built with **PyQt6** and **QWebEngineView**, initialized using **`uv init`** for package management.
With a builtin in content filter , blocking certain domains and keywords a clean GUI.

---

## Features

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
* **NEW!** Advanced native chromium viewer with full text functionality
* Text selection and copying
* Zoom slider (25% - 500%) with smooth scaling
* Page navigation and real-time page counter
* Works with any PDF file - guaranteed compatibility
* Provides download option


---

## Demo of Browser

![Alt text](Demo/img-1.png)
![Alt text](Demo/img-2.png)
![Alt text](Demo/img-3.png)
===============================



## Getting Started

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

### **Technical Requirements:**
* **Python version:** 3.8–3.12 (PyQt6 compatibility)
* **Dependencies:** PyQt6, PyQt6-WebEngine, requests, urllib3, UV package manager
* **Platforms:** Windows (tested), macOS/Linux (should work if compiled properly)
---

## References

* [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
* [QWebEngineView Documentation](https://doc.qt.io/qt-6/qwebengineview.html)
* [UV Package Manager](https://uv.software/) (for managing dependencies and project environment)

---

## Contributors 

Thanks goes to these wonderful people:

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<a href="https://github.com/Abhijit-71"><img src="https://avatars.githubusercontent.com/u/yourid?s=50" /></a>
<a href="https://github.com/Riki-Hershowitz"><img src="https://avatars.githubusercontent.com/u/theirid?s=50" /></a>
<!-- ALL-CONTRIBUTORS-BADGE:END -->





