import logging

def parse_adif(filepath):
    """
    Very simple ADIF parser: returns a list of dicts for each QSO.
    Only supports basic ADIF fields.
    """
    qsos = []
    try:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().lower()
                logging.debug(f"ADIF Content utf-8")
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="cp1252") as f:
                content = f.read().lower()
                logging.debug(f"ADIF Content cp1252")
        # Prüfung und Parsen jetzt außerhalb!
        if not content.strip():
            raise ValueError("ADIF file is empty or could not be read.")    
        records = content.split('<eor>')
        for record in records:
            qso = {}
            fields = record.split('<')
            for field in fields:
                if '>' in field:
                    keyval = field.split('>', 1)
                    if len(keyval) == 2:
                        key, val = keyval
                        key = key.split(':')[0].strip()
                        val = val.strip()
                        if key:
                            qso[key] = val
            if qso:
                qsos.append(qso)
        logging.info(f"Parsed {len(qsos)} QSOs from {filepath}")
    except Exception as e:
        logging.error(f"Error parsing ADIF file {filepath}: {e}")
        raise
    return qsos