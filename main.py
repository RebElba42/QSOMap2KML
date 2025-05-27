import sys, os
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import qInstallMessageHandler
from gui.main_window import MainWindow
from utils.logger import setup_logger
from core.i18n import I18n
from utils.app_utils import resource_path, get_app_stylesheet
from core.config_manager import ConfigManager

def qt_message_handler(mode, context, message):
    import logging
    logging.getLogger("qt").info(message)

def main():
    qInstallMessageHandler(qt_message_handler)
    # Load config and language
    config = ConfigManager.load()
    lang = config.get("language", "en")
    # Set up logging with config log level
    setup_logger(log_level=config.get("log_level", "INFO"))

    i18n = I18n(lang)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("resources/icons/flow_block.ico")))
    app.setApplicationName("QSOMap2KML © 2025 by DB4REB")
    # Darkmode setzen, wenn aktiviert

    if config.get("dark_mode", True):
        app.setStyle("Fusion")
        app.setStyleSheet(get_app_stylesheet())    
    window = MainWindow(i18n)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()