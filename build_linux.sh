#!/bin/bash
cd "$( dirname "$0" )"
python3 -m PyInstaller "SomePythonThings Music.py" --add-data "resources-sptmusic:resources-sptmusic" --icon "resources-sptmusic/icon.icns" --noconsole --hidden-import="pkg_resources.py2_warn" --exclude-module eel --exclude-module tkinter --onefile
