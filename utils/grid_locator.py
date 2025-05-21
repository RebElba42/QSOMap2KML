import math

def locator_to_latlon(locator):
    """
    Converts a Maidenhead locator (e.g. JN47FD) to (lat, lon).
    Returns (lat, lon) as floats. Returns None if invalid.
    """
    if not locator or len(locator) < 4:
        return None
    locator = locator.strip().upper()
    A = ord('A')
    lon = (ord(locator[0]) - A) * 20 - 180
    lat = (ord(locator[1]) - A) * 10 - 90
    lon += int(locator[2]) * 2
    lat += int(locator[3]) * 1
    if len(locator) >= 6:
        lon += (ord(locator[4]) - A) * 5 / 60
        lat += (ord(locator[5]) - A) * 2.5 / 60
    # Mittelpunkt des Feldes
    lon += 1
    lat += 0.5
    return (lat, lon)