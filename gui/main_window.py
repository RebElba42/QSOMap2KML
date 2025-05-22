import os
import logging
from PySide6.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox, QToolBar
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from gui.status_bar import StatusBar
from gui.config_dialog import ConfigDialog
from gui.map_preview import MapPreview
from gui.auto_msgboxes import AutoCloseInfoBox
from core.config_manager import ConfigManager
from core.i18n import I18n
from utils.adif_parser import parse_adif
from utils.kml_export import export_qsos_to_kml
from utils.app_utils import get_app_stylesheet

class MainWindow(QMainWindow):
    """
    Main application window for QSOMap2KML.
    All UI texts are internationalized using the I18n module.
    """
    def __init__(self, i18n: I18n):
        super().__init__()
        self.i18n = i18n
        self.setWindowTitle("QSOMap2KML © 2025 by DB4REB")
        self.setMinimumSize(900, 600)
        self.status_bar = StatusBar(self, self.i18n)
        self.setStatusBar(self.status_bar)
        self.map_preview = MapPreview(self, self.i18n)
        self.setCentralWidget(self.map_preview)
        self.qsos = []
        self._create_actions()
        self._create_menu()
        self._create_toolbar()

    def _icon(self, filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return QIcon(os.path.join(base_dir, "../resources/icons", filename))

    def _create_actions(self):
        # File actions (Menu)
        self.open_action_menu = QAction(self._icon("Upload image.png"), self.i18n.t("menu_open_adif"), self)
        self.open_action_menu.setToolTip(self.i18n.t("tooltip_open_adif"))
        self.open_action_menu.triggered.connect(self.open_adif)

        self.export_kml_action_menu = QAction(self._icon("Export.png"), self.i18n.t("menu_export_kml"), self)
        self.export_kml_action_menu.setToolTip(self.i18n.t("tooltip_export_kml"))
        self.export_kml_action_menu.triggered.connect(self.export_kml)
        self.export_kml_action_menu.setEnabled(bool(self.qsos))

        self.exit_action_menu = QAction(self._icon("Close.png"), self.i18n.t("menu_exit"), self)
        self.exit_action_menu.setToolTip(self.i18n.t("tooltip_exit"))
        self.exit_action_menu.triggered.connect(self.close)

        # File actions (Toolbar)
        self.open_action_toolbar = QAction(self._icon("Upload image.png"), self.i18n.t("menu_open_adif"), self)
        self.open_action_toolbar.setToolTip(self.i18n.t("tooltip_open_adif"))
        self.open_action_toolbar.triggered.connect(self.open_adif)

        self.export_kml_action_toolbar = QAction(self._icon("Export.png"), self.i18n.t("menu_export_kml"), self)
        self.export_kml_action_toolbar.setToolTip(self.i18n.t("tooltip_export_kml"))
        self.export_kml_action_toolbar.triggered.connect(self.export_kml)
        self.export_kml_action_toolbar.setEnabled(bool(self.qsos))

        self.exit_action_toolbar = QAction(self._icon("Close.png"), self.i18n.t("menu_exit"), self)
        self.exit_action_toolbar.setToolTip(self.i18n.t("tooltip_exit"))
        self.exit_action_toolbar.triggered.connect(self.close)

        # Settings actions
        self.config_action_menu = QAction(self._icon("Settings.png"), self.i18n.t("menu_configuration"), self)
        self.config_action_menu.setToolTip(self.i18n.t("tooltip_configuration"))
        self.config_action_menu.triggered.connect(self.open_config)

        self.config_action_toolbar = QAction(self._icon("Settings.png"), self.i18n.t("menu_configuration"), self)
        self.config_action_toolbar.setToolTip(self.i18n.t("tooltip_configuration"))
        self.config_action_toolbar.triggered.connect(self.open_config)

        # Help actions
        self.about_action_menu = QAction(self._icon("Info.png"), self.i18n.t("menu_about"), self)
        self.about_action_menu.setToolTip(self.i18n.t("tooltip_about"))
        self.about_action_menu.triggered.connect(self.show_about)

        self.about_action_toolbar = QAction(self._icon("Info.png"), self.i18n.t("menu_about"), self)
        self.about_action_toolbar.setToolTip(self.i18n.t("tooltip_about"))
        self.about_action_toolbar.triggered.connect(self.show_about)

    def _create_menu(self):
        menubar = self.menuBar()
        menubar.clear()
        # File menu
        file_menu = menubar.addMenu(self.i18n.t("menu_file"))
        file_menu.addAction(self.open_action_menu)
        file_menu.addAction(self.export_kml_action_menu)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action_menu)
        # Settings menu
        settings_menu = menubar.addMenu(self.i18n.t("menu_settings"))
        settings_menu.addAction(self.config_action_menu)
        # Help menu
        help_menu = menubar.addMenu(self.i18n.t("menu_help"))
        help_menu.addAction(self.about_action_menu)

    def _create_toolbar(self):
        for tb in self.findChildren(QToolBar):
            self.removeToolBar(tb)
        toolbar = QToolBar(self.i18n.t("toolbar_main"))
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        toolbar.addAction(self.open_action_toolbar)
        toolbar.addAction(self.export_kml_action_toolbar)
        toolbar.addAction(self.config_action_toolbar)
        toolbar.addAction(self.about_action_toolbar)
        toolbar.addSeparator()
        toolbar.addAction(self.exit_action_toolbar)

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
                
                def progress(idx, total):
                    self.status_bar.show_progress(idx, total)

                self.map_preview.show_qsos(qsos, progress_callback=progress)
                self.status_bar.hide_progress()
                self.status_bar.showMessage(self.i18n.t("status_loaded_adif").format(count=len(qsos)))      
                self.status_bar.showMessage(self.i18n.t("ready"))         
  
                self.map_preview.show_qsos(qsos)
                logging.info(f"Loaded ADIF file: {file} ({len(qsos)} QSOs)")
                # Enable export actions
                self.export_kml_action_menu.setEnabled(True)
                self.export_kml_action_toolbar.setEnabled(True)
            except Exception as e:
                self.status_bar.hide_progress()
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

    def reload_language(self, lang_code):
        self.i18n = I18n(lang_code)
        logging.debug(f"Reloaded language: {lang_code}")
        self.status_bar.set_i18n(self.i18n)
        self._create_actions()
        self._create_menu()
        self._create_toolbar()
        self.map_preview.i18n = self.i18n
        self.status_bar.showMessage(self.i18n.t("ready"))

    def export_kml(self):
        file, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.t("dialog_export_kml_title"),
            "QSO-Export",
            "KML (*.kml)"
        )
        if file:
            from core.config_manager import ConfigManager
            config = ConfigManager.load()
            my_locator = config.get("my_grid")
            band_colors = config.get("bands_colors", {})
            mode_colors = config.get("modes_colors", {})
            lang = self.i18n.lang if hasattr(self.i18n, "lang") else "en"
            def progress(idx, total):
                self.status_bar.show_progress(idx, total)        
                    
            export_qsos_to_kml(
                self.qsos, file, my_locator, band_colors, mode_colors,
                i18n=self.i18n, lang=lang, progress_callback=progress
            )
            
            self.status_bar.hide_progress() 
            self.status_bar.showMessage(self.i18n.t("ready"))
            AutoCloseInfoBox(
                self,
                self.i18n.t("export_kml_title"),
                self.i18n.t("status_kml_exported"),
                os.path.join(os.path.dirname(__file__), "../resources/icons/Ok.png")
            ).exec()
