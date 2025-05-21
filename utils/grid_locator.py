import math

import math

def locator_to_latlon(locator):
    """
    Converts a Maidenhead locator (e.g. JN47FD) to (lat, lon).
    Returns (lat, lon) as floats (center of the square).
    Returns None if invalid.
    """
    if not locator or len(locator) < 4:
        return None
    locator = locator.strip().upper()
    try:
        lon = (ord(locator[0]) - ord('A')) * 20 - 180
        lat = (ord(locator[1]) - ord('A')) * 10 - 90
        lon += int(locator[2]) * 2
        lat += int(locator[3]) * 1
        if len(locator) >= 6:
            lon += (ord(locator[4]) - ord('A')) * 5 / 60
            lat += (ord(locator[5]) - ord('A')) * 2.5 / 60
            # Mittelpunkt des 6-stelligen Feldes
            lon += 2.5 / 60
            lat += 1.25 / 60
        else:
            # Mittelpunkt des 4-stelligen Feldes
            lon += 1
            lat += 0.5
        return (lat, lon)
    except Exception:
        return None