#!/bin/bash
# filepath: /Users/reb/Source/GitHub/QSOMapGE/build_mac.sh

pyinstaller \
  --noconfirm \
  --windowed \
  --clean \
  --icon=resources/icons/Flow\ block.png \
  --name QSOMap2KML \
  --add-data "resources:resources" \
  --add-data "config:config" \
  main.py

echo "Fertig! Das Binary liegt in dist/QSOMap2KML"