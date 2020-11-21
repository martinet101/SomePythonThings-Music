rmdir /Q /S build
rmdir /Q /S dist
python -m PyInstaller "SomePythonThings Music.py" --add-data "resources-sptmusic;./resources-sptmusic" --icon "resources-sptmusic/icon.ico" --noconsole --hidden-import="pkg_resources.py2_warn" --exclude-module eel --exclude-module tkinter
pause