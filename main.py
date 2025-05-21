import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui.main_window import MainWindow
from utils.logger import setup_logger
from core.i18n import I18n
from core.config_manager import ConfigManager

def main():
    # Load config and language
    config = ConfigManager.load()
    lang = config.get("language", "en")
    i18n = I18n(lang)

    # Set up logging with config log level
    setup_logger(log_level=config.get("log_level", "INFO"))

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("resources/icons/Flow block.png"))
    window = MainWindow(i18n)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()