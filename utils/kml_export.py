"""
KML Export for QSOMap2KML
-----------------------
Exports QSOs as KML for Google Earth, with:
- One placemark per QSO (with color by mode)
- Lines from your location to each QSO (with color by band, in a hidden folder)
- Grouping by band (folders)
- All colors and names are taken from the config/colors dicts
- QTH Pinpoint for your location
- Date and time formatted and localized in tooltips
"""

from utils.grid_locator import locator_to_latlon
from datetime import datetime

def format_adif_date(date_str, lang="en"):
    """Format ADIF date YYYYMMDD to localized string."""
    if not date_str or len(date_str) != 8:
        return date_str
    year, month, day = date_str[:4], date_str[4:6], date_str[6:8]
    if lang == "de":
        return f"{day}.{month}.{year}"
    return f"{year}-{month}-{day}"

def format_adif_time(time_str):
    """Format ADIF time HHMMSS or HHMM to HH:MM or HH:MM:SS."""
    if not time_str or len(time_str) < 4:
        return time_str
    hour, minute = time_str[:2], time_str[2:4]
    if len(time_str) >= 6:
        second = time_str[4:6]
        return f"{hour}:{minute}:{second}"
    return f"{hour}:{minute}"

def export_qsos_to_kml(qsos, filename, my_locator=None, band_colors=None, mode_colors=None, i18n=None, lang="en"):
    """
    Export QSOs to a KML file for Google Earth.

    Args:
        qsos (list): List of QSO dicts.
        filename (str): Output KML file path.
        my_locator (str): Your own grid locator (for lines).
        band_colors (dict): Mapping band -> color (hex, e.g. #FF0000).
        mode_colors (dict): Mapping mode -> color (hex, e.g. #00FF00).
        i18n: I18n instance for translations.
        lang (str): Language code ("en" or "de").
    """
    def kml_color(hex_color, alpha="ff"):
        """Convert #RRGGBB to KML color aabbggrr (alpha first, then blue, green, red)."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return f"{alpha}ffffff"  # default: white
        r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
        return f"{alpha}{b}{g}{r}"

    my_pos = locator_to_latlon(my_locator) if my_locator else None

    # Group QSOs by band
    band_groups = {}
    for qso in qsos:
        band = qso.get("band", "Unknown")
        band_groups.setdefault(band, []).append(qso)

    # KML header
    now = datetime.now()
    if lang == "de":
        export_time = now.strftime("%d.%m.%Y - %H:%M")
    else:
        export_time = now.strftime("%Y-%m-%d - %H:%M")
    kml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '<Document>',
        f'<name>QSOMap Export - {export_time}</name>',
    ]
    # QTH as Starting Pos
    if my_pos:
        my_lat, my_lon = my_pos
        kml.append(f"""
            <LookAt>
                <longitude>{my_lon}</longitude>
                <latitude>{my_lat}</latitude>
                <altitude>0</altitude>
                <range>2000000</range>
                <tilt>0</tilt>
                <heading>0</heading>
                <altitudeMode>relativeToGround</altitudeMode>
            </LookAt>
        """)
        
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

    # Legende als Placemark
    legend_html = "<b>Bands:</b><br>"
    for band, color in (band_colors or {}).items():
        legend_html += f'<span style="color:{color}">&#9632;</span> {band}<br>'
    legend_html += "<br><b>Modes:</b><br>"
    for mode, color in (mode_colors or {}).items():
        legend_html += f'<span style="color:{color}">&#9632;</span> {mode}<br>'

    kml.append(f"""
        <Placemark>
            <name>Legend</name>
            <description><![CDATA[{legend_html}]]></description>
            <Point>
                <coordinates>0,0,0</coordinates>
            </Point>
        </Placemark>
    """)

    # QTH Pinpoint
    if my_pos:
        my_lat, my_lon = my_pos
        kml.append(f"""
            <Placemark>
                <name>QTH</name>
                <description>{i18n.t('qth_tooltip') if i18n else 'Your location'}</description>
                <Point>
                    <coordinates>{my_lon},{my_lat},0</coordinates>
                </Point>
            </Placemark>
        """)

    # Band folders with QSO markers
    for band, qsos_in_band in band_groups.items():
        kml.append(f'<Folder><name>{band}</name>')
        for qso in qsos_in_band:
            call = qso.get('call', 'Unknown').upper()
            grid = qso.get('gridsquare')
            mode = qso.get('mode', 'Unknown').upper()
            name = qso.get('name', '')
            date_raw = qso.get('date', '') or qso.get('qso_date', '')
            time_raw = qso.get('time', '') or qso.get('time_on', '')
            date = format_adif_date(date_raw, lang)
            time = format_adif_time(time_raw)
            pos = locator_to_latlon(grid) if grid else None
            if not pos:
                continue
            lat, lon = pos
            marker_style = f'marker_{mode}' if mode_colors and mode in mode_colors else ""
            if i18n and hasattr(i18n, "t"):
                desc_template = i18n.t("kml_popup")
                # Falls keine Übersetzung vorhanden ist, gibt t() meist den Key zurück
                if desc_template == "kml_popup":
                    desc_template = "Mode: {mode}<br>Band: {band}<br>Name: {name}<br>Date: {date}<br>Time: {time}"
            else:
                desc_template = "Mode: {mode}<br>Band: {band}<br>Name: {name}<br>Date: {date}<br>Time: {time}"
            description = desc_template.format(mode=mode, band=band, name=name, date=date, time=time)
            kml.append(f"""
                <Placemark>
                    <name>{call} ({mode})</name>
                    <description><![CDATA[{description}]]></description>
                    <styleUrl>#{marker_style}</styleUrl>
                    <Point>
                        <coordinates>{lon},{lat},0</coordinates>
                    </Point>
                </Placemark>
            """)
        kml.append('</Folder>')

    # Hidden folder for all lines
    if my_pos:
        kml.append('<Folder><name>Lines</name><visibility>1</visibility>')
        for band, qsos_in_band in band_groups.items():
            for qso in qsos_in_band:
                grid = qso.get('gridsquare')
                pos = locator_to_latlon(grid) if grid else None
                if not pos:
                    continue
                lat, lon = pos
                line_style = f'line_{band}' if band_colors and band in band_colors else None
                kml.append(f"""
                    <Placemark>
                        {f'<styleUrl>#{line_style}</styleUrl>' if line_style else ''}
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