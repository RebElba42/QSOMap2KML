import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev, PyInstaller and Nuitka """
    # Nuitka setzt sys.frozen == True, aber kein _MEIPASS!
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    if getattr(sys, 'frozen', False):
        # Nuitka: Ressourcen liegen im aktuellen Arbeitsverzeichnis
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
  