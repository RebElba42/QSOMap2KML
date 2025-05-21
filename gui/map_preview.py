from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium
import logging
from utils.grid_locator import locator_to_latlon

class MapPreview(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
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
            m = folium.Map(location=[51, 10], zoom_start=4)
            marker_count = 0
            for qso in qsos:
                grid = qso.get('gridsquare')
                call = qso.get('call', 'Unknown')
                pos = locator_to_latlon(grid) if grid else None
                if pos:
                    folium.Marker(
                        location=pos,
                        popup=call
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