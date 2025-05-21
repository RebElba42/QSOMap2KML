from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium
import tempfile
import os

class MapPreview(QWebEngineView):
    """
    Widget to preview QSOs on a map using folium and QWebEngineView.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.temp_html = None

    def show_qsos(self, qsos):
        # Default map center (Germany)
        m = folium.Map(location=[51, 10], zoom_start=4)
        for qso in qsos:
            # Hier solltest du später echte Koordinaten berechnen!
            # Zum Testen: zufällige Marker
            folium.Marker(
                location=[51, 10],  # Dummy-Koordinaten
                popup=qso.get('call', 'Unknown')
            ).add_to(m)
        fd, path = tempfile.mkstemp(suffix=".html")
        m.save(path)
        self.load(f"file://{path}")
        self.temp_html = path

    def closeEvent(self, event):
        if self.temp_html and os.path.exists(self.temp_html):
            os.remove(self.temp_html)
        super().closeEvent(event)