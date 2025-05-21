from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium
import logging
from folium.plugins import BeautifyIcon
from folium import Element
from utils.grid_locator import locator_to_latlon
from utils.kml_export import format_adif_date, format_adif_time
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
                mode = qso.get('mode', '').upper()
                name = qso.get('name', '')
                date_raw = qso.get('date', '') or qso.get('qso_date', '')
                time_raw = qso.get('time', '') or qso.get('time_on', '')
                lang = self.i18n.lang if hasattr(self.i18n, "lang") else "en"
                date = format_adif_date(date_raw, lang)
                time = format_adif_time(time_raw)
                pos = locator_to_latlon(grid) if grid else None

                tooltip = self.i18n.t("qso_tooltip").format(
                    call=call,
                    band=band,
                    mode=mode,
                    name=name,
                    date=date,
                    time=time
                ) if self.i18n else f"Call: {call}\nBand: {band}\nMode: {mode}\nName: {name}\nDate: {date}\nTime: {time}"

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

            band_legend = "<b>Bands:</b><br>"
            for band, color in band_colors.items():
                band_legend += f'<i style="background:{color};width:12px;height:12px;display:inline-block;margin-right:4px"></i> {band}<br>'

            # Legend for Modes
            mode_legend = "<b>Modes:</b><br>"
            for mode, color in mode_colors.items():
                mode_legend += f'<i style="background:{color};width:12px;height:12px;display:inline-block;margin-right:4px"></i> {mode}<br>'

            legend_html = f"""
            <div style="
                position: fixed; 
                top: 10px; left: 10px; width: 180px; z-index:9999; 
                background: white; border:2px solid grey; border-radius:6px; 
                padding: 8px; font-size:12px; opacity: 0.9;">
                {band_legend}<hr style="margin:4px 0;">{mode_legend}
            </div>
            """         
            m.get_root().html.add_child(Element(legend_html))  
            html = m.get_root().render()
            self.setHtml(html)
        except Exception as e:
            logging.error(f"Error displaying QSOs on map: {e}")