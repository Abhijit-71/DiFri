import os, sys

def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS  #type:ignore
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
