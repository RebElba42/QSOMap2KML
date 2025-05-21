from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ConfigDialog(QDialog):
    """
    Configuration dialog for QSOMapGE.
    All UI texts are internationalized using the I18n module.
    """
    def __init__(self, parent=None, i18n=None):
        super().__init__(parent)
        self.i18n = i18n
        self.setWindowTitle(self.i18n.t("config_title") if self.i18n else "Configuration")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.i18n.t("config_placeholder") if self.i18n else "Settings will be here (language, colors, grid, name, etc.)"))
        close_btn = QPushButton(self.i18n.t("close") if self.i18n else "Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)