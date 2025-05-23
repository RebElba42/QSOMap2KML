import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev, PyInstaller and Nuitka."""
    # Nuitka-Onefile erkennt man an sys.nuitka_onefile
    if getattr(sys, 'frozen', False) or getattr(sys, 'nuitka_onefile', False):
        # Im gefrorenen Modus: immer vom Ordner der EXE (Temp-Ordner) aus!
        base_path = os.path.dirname(sys.executable)
        #print("Nuitka/PyInstaller-Modus, base_path:", base_path)
    else:
        # Im Entwicklermodus: vom Projekt-Hauptverzeichnis (eine Ebene über utils)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        #print("Entwicklermodus, base_path:", base_path)
    abs_path = os.path.join(base_path, relative_path)
    #print("resource_path resolved:", abs_path)
    return abs_path

def get_app_stylesheet():
    """ Get Stylesheet for applications Darkmode """
    return """
        QWidget {
            background-color: #232629;
            color: #f0f0f0;
        }
        QMenuBar, QMenuBar::item {
            background: #232629;
            color: #f0f0f0;
        }
        QMenuBar::item:selected {
            background: #444;
        }
        QMenu {
            background-color: #232629;
            color: #f0f0f0;
        }
        QMenu::item:selected {
            background-color: #444;
        }
        QToolBar {
            background: #232629;
            border: none;
        }
        QStatusBar {
            background: #232629;
            color: #f0f0f0;
        }
        QMainWindow {
            background: #232629;
        }
        QLineEdit, QComboBox, QSpinBox, QTextEdit {
            background-color: #333;
            color: #f0f0f0;
        }
        QPushButton {
            background-color: #444;
            color: #f0f0f0;
        }
        QToolTip {
            background-color: #232629;
            color: #f0f0f0;
            border: 1px solid #f0f0f0;
        }
    """
    
def call_progress(progress_callback, done, total):
    ''' Call the progress callback if provided '''
    if not callable(progress_callback):
        return
    #if progress_callback and (done % 10 == 0 or done == total):
    if progress_callback:
        progress_callback(done, total)