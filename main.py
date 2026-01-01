import sys  
import os

from ui.main_window import CypherLensApp

if __name__ == "__main__":
    app = CypherLensApp()
    app.mainloop()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)