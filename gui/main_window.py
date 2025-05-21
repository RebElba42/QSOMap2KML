import os
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox, QToolBar
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from gui.status_bar import StatusBar
from gui.config_dialog import ConfigDialog
from gui.map_preview import MapPreview
from core.i18n import I18n
from utils.adif_parser import parse_adif

class MainWindow(QMainWindow):
    """
    Main application window for QSOMapGE.
    All UI texts are internationalized using the I18n module.
    """
    def __init__(self, i18n: I18n):
        super().__init__()
        self.i18n = i18n
        self.setWindowTitle("QSOMapGE")
        self.setMinimumSize(900, 600)
        self.status_bar = StatusBar(self, self.i18n)
        self.setStatusBar(self.status_bar)
        self.map_preview = MapPreview(self)
        self.setCentralWidget(self.map_preview)
        self.qsos = []
        self._create_actions()
        self._create_menu()
        self._create_toolbar()

    def _icon(self, filename):
        # Helper to get the absolute path for icons
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return QIcon(os.path.join(base_dir, "../resources/icons", filename))

    def _create_actions(self):
        # File actions
        self.open_action = QAction(self._icon("Upload image.png"), self.i18n.t("menu_open_adif"), self)
        self.open_action.setToolTip(self.i18n.t("tooltip_open_adif"))
        self.open_action.triggered.connect(self.open_adif)

        self.exit_action = QAction(self._icon("Close.png"), self.i18n.t("menu_exit"), self)
        self.exit_action.setToolTip(self.i18n.t("tooltip_exit"))
        self.exit_action.triggered.connect(self.close)

        # Settings actions
        self.config_action = QAction(self._icon("Settings.png"), self.i18n.t("menu_configuration"), self)
        self.config_action.setToolTip(self.i18n.t("tooltip_configuration"))
        self.config_action.triggered.connect(self.open_config)

        # Help actions
        self.about_action = QAction(self._icon("Info.png"), self.i18n.t("menu_about"), self)
        self.about_action.setToolTip(self.i18n.t("tooltip_about"))
        self.about_action.triggered.connect(self.show_about)

    def _create_menu(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu(self.i18n.t("menu_file"))
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Settings menu
        settings_menu = menubar.addMenu(self.i18n.t("menu_settings"))
        settings_menu.addAction(self.config_action)

        # Help menu
        help_menu = menubar.addMenu(self.i18n.t("menu_help"))
        help_menu.addAction(self.about_action)

    def _create_toolbar(self):
        toolbar = QToolBar(self.i18n.t("toolbar_main"))
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.config_action)
        toolbar.addAction(self.about_action)
        toolbar.addSeparator()
        toolbar.addAction(self.exit_action)

    def open_adif(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            self.i18n.t("dialog_open_adif_title"),
            "",
            self.i18n.t("dialog_open_adif_filter")
        )
        if file:
            self.status_bar.showMessage(self.i18n.t("status_loading_adif"))
            try:
                qsos = parse_adif(file)
                self.qsos = qsos
                self.status_bar.showMessage(self.i18n.t("status_loaded_adif").format(count=len(qsos)))
                self.map_preview.show_qsos(qsos)
                logging.info(f"Loaded ADIF file: {file} ({len(qsos)} QSOs)")
            except Exception as e:
                self.status_bar.showMessage(self.i18n.t("status_error_adif"))
                logging.error(f"Error loading ADIF file: {file} - {e}")
                QMessageBox.critical(self, "Error", str(e))

    def open_config(self):
        dialog = ConfigDialog(self, self.i18n)
        dialog.exec()

    def show_about(self):
        QMessageBox.about(
            self,
            self.i18n.t("about_title"),
            self.i18n.t("about_text")
        )