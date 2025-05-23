#!/bin/bash
# Build macOS Executable mit Nuitka

nuitka \
  --standalone \
  --onefile \
  --enable-plugin=pyside6 \
  --include-data-file=resources/xyzservices/data/providers.json=resources/xyzservices/data/providers.json \
  --include-data-dir=resources/icons=resources/icons \
  --include-data-file=resources/translations/de.json=resources/translations/de.json \
  --include-data-file=resources/translations/en.json=resources/translations/en.json \
  --macos-app-icon=resources/icons/flow_block.ico \
  --output-filename=QSOMap2KML \
  --output-dir=dist \
  main.py