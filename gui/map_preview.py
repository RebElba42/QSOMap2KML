from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium
import logging
from folium.plugins import BeautifyIcon
from utils.grid_locator import locator_to_latlon
from core.config_manager import ConfigManager

class MapPreview(QWebEngineView):
    """
    Zeigt eine Karte mit QSOs und Linien vom eigenen Standort zu jedem QSO-Partner.
    Die Linienfarbe wird pro Band aus der Konfiguration genommen.
    Die Markerfarbe wird pro Mode aus der Konfiguration genommen (BeautifyIcon, beliebige Farbe).
    Tooltip beim Hover zeigt QSO-Infos (i18n).
    """
    def __init__(self, parent=None, i18n=None):
        super().__init__(parent)
        self.i18n = i18n
        self.show_empty_map()

    def show_empty_map(self):
        try:
            m = folium.Map(location=[51, 10], zoom_start=4)
            html = m.get_root().render()
            self.setHtml(html)
            logging.info("Displayed empty map in MapPreview.")
        except Exception as e:
            logging.error(f"Error displaying empty map: {e}")

    def show_qsos(self, qsos):
        try:
            config = ConfigManager.load()
            my_grid = config.get("my_grid", "")
            my_name = config.get("my_name", "")
            my_pos = locator_to_latlon(my_grid)
            band_colors = config.get("bands_colors", {})
            mode_colors = config.get("modes_colors", {})
            m = folium.Map(location=[51, 10], zoom_start=4)

            # Marker für eigenen Standort (sofern gültig)
            if my_pos:
                folium.Marker(
                    location=my_pos,
                    popup=f"{my_name} ({my_grid})",
                    icon=BeautifyIcon(
                        icon_shape='star',
                        border_color='red',
                        text_color='white',
                        background_color='red'
                    )
                ).add_to(m)

            marker_count = 0

            for qso in qsos:
                grid = qso.get('gridsquare')
                call = qso.get('call', 'Unknown').upper()
                band = qso.get('band', '')
                mode = qso.get('mode', '').upper()  # <-- hier!
                name = qso.get('name', '')
                pos = locator_to_latlon(grid) if grid else None

                tooltip = self.i18n.t("qso_tooltip").format(
                    call=call,
                    band=band,
                    mode=mode,
                    name=name
                ) if self.i18n else f"Call: {call}\nBand: {band}\nMode: {mode}\nName: {name}"

                if pos:
                    line_color = band_colors.get(band, "#3388ff")
                    marker_color = mode_colors.get(mode, "#3388ff")
                    if my_pos:
                        folium.PolyLine(
                            locations=[my_pos, pos],
                            color=line_color,
                            weight=2,
                            opacity=0.7
                        ).add_to(m)
                    logging.debug(f"QSO {call}: mode={mode}, marker_color={marker_color}, band={band}, line_color={line_color}")
                    folium.Marker(
                        location=pos,
                        popup=call,
                        tooltip=tooltip,
                        icon=BeautifyIcon(
                            icon_shape='marker',
                            border_color=marker_color,
                            background_color=marker_color,
                            text_color='white',
                            number=mode if mode else "?"
                        )
                    ).add_to(m)
                    marker_count += 1

            if marker_count == 0:
                folium.Marker(
                    location=[51, 10],
                    popup="No QSOs with valid locator"
                ).add_to(m)
                logging.info("No QSOs with valid locator to display on map.")
            else:
                logging.info(f"Displayed {marker_count} QSOs on map.")
            html = m.get_root().render()
            self.setHtml(html)
        except Exception as e:
            logging.error(f"Error displaying QSOs on map: {e}")