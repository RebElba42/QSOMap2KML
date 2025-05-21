from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QHBoxLayout, QColorDialog, QCheckBox, QFormLayout
)
from PyQt6.QtGui import QColor
from core.config_manager import ConfigManager
from utils.logger import set_log_level

# Beispiel-Bänder und Modes (kannst du anpassen)
BANDS = ["160m", "80m", "40m", "20m", "15m", "10m"]
MODES = ["SSB", "CW", "FT8", "FM", "AM"]

class ConfigDialog(QDialog):
    """
    Configuration dialog for QSOMapGE.
    Supports i18n and editing all config fields, including color pickers.
    """
    def __init__(self, parent=None, i18n=None):
        super().__init__(parent)
        self.i18n = i18n
        self.setWindowTitle(self.i18n.t("config_title") if self.i18n else "Configuration")
        self.setMinimumWidth(400)
        self.config = ConfigManager.load()

        layout = QVBoxLayout()
        form = QFormLayout()

        # Language
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("Deutsch", "de")
        idx = 0 if self.config.get("language", "en") == "en" else 1
        self.lang_combo.setCurrentIndex(idx)
        form.addRow(QLabel(self.i18n.t("config_language")), self.lang_combo)

        # Dark Mode
        self.darkmode_checkbox = QCheckBox(self.i18n.t("config_dark_mode"))
        self.darkmode_checkbox.setChecked(self.config.get("dark_mode", True))
        form.addRow(self.darkmode_checkbox)

        # Own Locator
        self.locator_edit = QLineEdit(self.config.get("my_grid", ""))
        form.addRow(QLabel(self.i18n.t("config_own_locator")), self.locator_edit)

        # Own Name
        self.name_edit = QLineEdit(self.config.get("my_name", ""))
        form.addRow(QLabel(self.i18n.t("config_own_name")), self.name_edit)

        # Log Level
        self.loglevel_combo = QComboBox()
        self.loglevel_combo.addItems(["INFO", "DEBUG"])
        self.loglevel_combo.setCurrentText(self.config.get("log_level", "INFO"))
        form.addRow(QLabel(self.i18n.t("config_log_level")), self.loglevel_combo)

        # Band Colors
        self.band_color_buttons = {}
        band_colors = self.config.get("bands_colors", {})
        for band in BANDS:
            color = band_colors.get(band, "#cccccc")
            btn = QPushButton()
            btn.setStyleSheet(f"background-color: {color}")
            btn.clicked.connect(lambda _, b=band: self.pick_band_color(b))
            self.band_color_buttons[band] = btn
            row = QHBoxLayout()
            row.addWidget(QLabel(band))
            row.addWidget(btn)
            form.addRow(QLabel(self.i18n.t("config_band_color_for").format(band=band)), btn)

        # Mode Colors
        self.mode_color_buttons = {}
        mode_colors = self.config.get("modes_colors", {})
        for mode in MODES:
            color = mode_colors.get(mode, "#cccccc")
            btn = QPushButton()
            btn.setStyleSheet(f"background-color: {color}")
            btn.clicked.connect(lambda _, m=mode: self.pick_mode_color(m))
            self.mode_color_buttons[mode] = btn
            form.addRow(QLabel(self.i18n.t("config_mode_color_for").format(mode=mode)), btn)

        layout.addLayout(form)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton(self.i18n.t("save"))
        save_btn.clicked.connect(self.save_config)
        close_btn = QPushButton(self.i18n.t("close"))
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def pick_band_color(self, band):
        current = self.band_color_buttons[band].palette().button().color().name()
        color = QColorDialog.getColor(QColor(current), self, self.i18n.t("pick_color_for").format(item=band))
        if color.isValid():
            self.band_color_buttons[band].setStyleSheet(f"background-color: {color.name()}")

    def pick_mode_color(self, mode):
        current = self.mode_color_buttons[mode].palette().button().color().name()
        color = QColorDialog.getColor(QColor(current), self, self.i18n.t("pick_color_for").format(item=mode))
        if color.isValid():
            self.mode_color_buttons[mode].setStyleSheet(f"background-color: {color.name()}")



    def save_config(self):
        self.config["language"] = self.lang_combo.currentData()
        self.config["dark_mode"] = self.darkmode_checkbox.isChecked()
        self.config["my_grid"] = self.locator_edit.text().strip().upper()
        self.config["my_name"] = self.name_edit.text().strip()
        self.config["log_level"] = self.loglevel_combo.currentText()
        # Farben speichern
        self.config["bands_colors"] = {band: self.band_color_buttons[band].palette().button().color().name() for band in self.band_color_buttons}
        self.config["modes_colors"] = {mode: self.mode_color_buttons[mode].palette().button().color().name() for mode in self.mode_color_buttons}
        ConfigManager.save(self.config)
        set_log_level(self.config["log_level"])
        if self.parent() and hasattr(self.parent(), "reload_language"):
            self.parent().reload_language(self.config["language"]) 
        if hasattr(self.parent(), "qsos") and hasattr(self.parent(), "map_preview"):
            self.parent().map_preview.show_qsos(self.parent().qsos)
        self.accept()