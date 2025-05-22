REM Build Windows Executable mit Nuitka und UPX
REM set PATH=C:\upx;%PATH%
nuitka ^
  --standalone ^
  --onefile ^
  --enable-plugin=PySide6 ^
  --windows-console-mode=disable ^
  --include-data-dir=resources=resources ^
  --include-data-dir=config=config ^
  --include-data-file=resources\xyzservices\data\providers.json=xyzservices\data\providers.json ^
  --include-data-dir=resources\translations=resources\translations ^
  --include-data-dir=resources\icons=resources\icons ^
  --windows-icon-from-ico="resources\icons\Flow block.ico" ^
  --output-filename=QSOMap2KML.exe ^
  --output-dir=dist  ^
  main.py
