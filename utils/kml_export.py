"""
KML Export for QSOMapGE
-----------------------
Exports QSOs as KML for Google Earth, with:
- One placemark per QSO (with color by mode)
- Lines from your location to each QSO (with color by band)
- Grouping by band (folders)
- All colors and names are taken from the config/colors dicts
"""

from utils.grid_locator import locator_to_latlon

def export_qsos_to_kml(qsos, filename, my_locator=None, band_colors=None, mode_colors=None):
    """
    Export QSOs to a KML file for Google Earth.

    Args:
        qsos (list): List of QSO dicts.
        filename (str): Output KML file path.
        my_locator (str): Your own grid locator (for lines).
        band_colors (dict): Mapping band -> color (hex, e.g. #FF0000).
        mode_colors (dict): Mapping mode -> color (hex, e.g. #00FF00).
    """
    def kml_color(hex_color, alpha="ff"):
        """
        Convert #RRGGBB to KML color aabbggrr (alpha first, then blue, green, red).
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return f"{alpha}ffffff"  # default: white
        r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
        return f"{alpha}{b}{g}{r}"

    # Your own position (for lines)
    my_pos = locator_to_latlon(my_locator) if my_locator else None

    # Group QSOs by band
    band_groups = {}
    for qso in qsos:
        band = qso.get("band", "Unknown")
        band_groups.setdefault(band, []).append(qso)

    # KML header
    kml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '<Document>',
        '<name>QSOMapGE Export</name>',
    ]

    # Define styles for each band and mode
    style_defs = []
    if band_colors:
        for band, color in band_colors.items():
            style_defs.append(
                f"""
                <Style id="line_{band}">
                    <LineStyle>
                        <color>{kml_color(color, "ff")}</color>
                        <width>2</width>
                    </LineStyle>
                </Style>
                """
            )
    if mode_colors:
        for mode, color in mode_colors.items():
            style_defs.append(
                f"""
                <Style id="marker_{mode}">
                    <IconStyle>
                        <color>{kml_color(color, "ff")}</color>
                        <scale>1.2</scale>
                        <Icon>
                            <href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href>
                        </Icon>
                    </IconStyle>
                </Style>
                """
            )
    kml.extend(style_defs)

    # For each band, create a Folder
    for band, qsos_in_band in band_groups.items():
        kml.append(f'<Folder><name>{band}</name>')
        for qso in qsos_in_band:
            call = qso.get('call', 'Unknown')
            grid = qso.get('gridsquare')
            mode = qso.get('mode', 'Unknown').upper()
            name = qso.get('name', '')
            pos = locator_to_latlon(grid) if grid else None
            if not pos:
                continue
            lat, lon = pos
            marker_style = f'marker_{mode}' if mode_colors and mode in mode_colors else ""
            # Placemark for QSO
            kml.append(f"""
                <Placemark>
                    <name>{mode}</name>
                    <description><![CDATA[
                        <b>Call:</b> {call}<br/>
                        <b>Band:</b> {band}<br/>
                        <b>Mode:</b> {mode}<br/>
                        <b>Name:</b> {name}<br/>
                        <b>Locator:</b> {grid}
                    ]]></description>
                    <styleUrl>#{marker_style}</styleUrl>
                    <Point>
                        <coordinates>{lon},{lat},0</coordinates>
                    </Point>
                </Placemark>
            """)
            # Line from your position to QSO
            if my_pos:
                line_style = f'line_{band}' if band_colors and band in band_colors else ""
                my_lat, my_lon = my_pos
                kml.append(f"""
                    <Placemark>
                        <name>{call} ({band})</name>
                        <styleUrl>#{line_style}</styleUrl>
                        <LineString>
                            <coordinates>
                                {my_lon},{my_lat},0
                                {lon},{lat},0
                            </coordinates>
                        </LineString>
                    </Placemark>
                """)
        kml.append('</Folder>')

    # KML footer
    kml.append('</Document></kml>')

    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(kml))