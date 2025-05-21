from PyQt6.QtWidgets import QStatusBar

class StatusBar(QStatusBar):
    """
    Status bar for QSOMapGE.
    All UI texts are internationalized using the I18n module.
    """
    def __init__(self, parent=None, i18n=None):
        super().__init__(parent)
        self.i18n = i18n
        self.showMessage(self.i18n.t("ready") if self.i18n else "Ready")