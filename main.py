import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from utils.logger import setup_logger
from core.i18n import I18n
from core.config_manager import ConfigManager

def main():
    # Load config and language
    config = ConfigManager.load()
    lang = config.get("language", "en")
    i18n = I18n(lang)

    # Set up logging (no console output)
    setup_logger(debug=(config.get("log_level", "INFO") == "DEBUG"))

    app = QApplication(sys.argv)
    window = MainWindow(i18n)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()