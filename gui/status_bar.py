from PySide6.QtWidgets import QStatusBar, QProgressBar

class StatusBar(QStatusBar):
    def __init__(self, parent, i18n):
        super().__init__(parent)
        self.i18n = i18n
        self.progress = QProgressBar(self)
        self.progress.setVisible(False)
        self.addPermanentWidget(self.progress)
        self.showMessage(self.i18n.t("ready"))

    def set_i18n(self, i18n):
        """Set new Language after Config update."""
        self.i18n = i18n
        self.showMessage(self.i18n.t("ready"))

    def show_progress(self, value, maximum):
        self.progress.setMaximum(maximum)
        self.progress.setValue(value)
        self.progress.setVisible(True)
        self.showMessage(f"{value}/{maximum}")

    def hide_progress(self):
        self.progress.setVisible(False)
        self.clearMessage()