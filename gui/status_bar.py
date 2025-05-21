from PyQt6.QtWidgets import QStatusBar

class StatusBar(QStatusBar):
    def __init__(self, parent, i18n):
        super().__init__(parent)
        self.i18n = i18n
        self.showMessage(self.i18n.t("ready"))

    def set_i18n(self, i18n):
        """Set new Language after Config update."""
        self.i18n = i18n
        self.showMessage(self.i18n.t("ready"))
    