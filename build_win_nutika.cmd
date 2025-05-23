REM Build Windows Executable mit Nuitka und UPX
REM set PATH=C:\upx;%PATH%
REM --windows-console-mode=disable ^
REM --include-data-dir=resources=resources ^
REM --include-data-dir=config=config ^
nuitka ^
  --standalone ^
  --onefile ^
  --windows-console-mode=disable ^
  --enable-plugin=pyside6 ^
  --include-data-file=resources\xyzservices\data\providers.json=resources\xyzservices\data\providers.json ^
  --include-data-dir=resources\icons=resources\icons ^
  --include-data-file=resources\translations\de.json=resources\translations\de.json ^
  --include-data-file=resources\translations\en.json=resources\translations\en.json ^
  --windows-icon-from-ico=resources\icons\flow_block.ico ^
  --output-filename=QSOMap2KML.exe ^
  --output-dir=dist ^
  main.py