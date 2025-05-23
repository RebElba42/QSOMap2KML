# QSOMap2KML

QSOMap2KML is a cross-platform application to visualize amateur radio QSOs from ADIF files on a map (Google Earth KML and interactive preview).  
It features a modern PySide6 GUI, dark mode, band/mode color configuration, internationalization (i18n), and more.

## Features

- Import ADIF files and visualize QSOs as lines and pins in Google Earth (KML)
- Interactive map preview with colored markers and lines (Folium/Leaflet)
- Band and mode color configuration (fully customizable)
- Mouseover tooltips with QSO details (call, band, mode, name, date, time)
- Supports English and German (i18n)
- Asynchronous processing for large files
- Logging with rotating log files
- Color legend for bands and modes in both KML and map preview
- QTH (own location) marker and centering
- Configuration dialog for all settings

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Start the application:

```bash
python main.py
```

## Binary Build (Nuitka)

You can create a standalone executable (Windows, macOS, Linux) using [Nuitka](https://nuitka.net/):

1. **Install Nuitka and a C compiler:**

    ```bash
    pip install nuitka
    # On Windows: install a C compiler (e.g. MSVC or MinGW)
    # On macOS: Xcode command line tools (xcode-select --install)
    # On Linux: sudo apt install build-essential
    ```

2. **Build the executable:**

    ```bash
    nuitka --standalone --onefile --enable-plugin=pyside6 \
      --include-data-dir=resources=resources \
      --include-data-dir=config=config \
      --output-filename=QSOMap2KML.exe \
      main.py
    ```

    Adjust the paths and options for your system as needed.  
    See `build_win_nutika.cmd` (Windows) or `build_mac_nuitka.sh` (macOS) for more examples.

3. **The binary will be located in the `dist/` folder.**

## Configuration

Settings are stored in `config/settings.json`.  
You can configure language, dark mode, your grid locator, band/mode colors, and more via the configuration dialog in the app.

## File Formats

- **ADIF**: Standard amateur radio log format (`.adi`, `.adif`)
- **KML**: Google Earth format for map visualization

## Development

- Python 3.9+
- PySide6 for GUI
- Folium for map preview
- KML export for Google Earth

## Logging

Log files are stored in the `logs/` directory with rotation.

---

## Screenshots

Below are example screenshots of QSOMap2KML:

### Application main window in dark mode

![main Window](resources/screenshots/screenshot_main.jpg)

### Map preview with colored QSO markers, lines, and legend

![Map Preview](resources/screenshots/screenshot_preview.jpg)

### Configuration dialog for bands, modes, and user settings

![Configuration Dialog](resources/screenshots/screenshot_config.jpg)

### KML export visualized in Google Earth
![KML Export View in Google Earth](resources/screenshots/screenshot_kml.jpg)

---

## Contributions & Credits

- Free icon pack used from [small-icons.com](http://www.small-icons.com/packs/32x32-free-design-icons.htm)

---

## License

See [LICENSE](LICENSE).
