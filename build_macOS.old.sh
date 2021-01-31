#!/bin/bash
cd "$( dirname "$0" )"
python3.8 -m PyInstaller "SomePythonThings Music.spec" --add-data "resources-sptmusic:resources-sptmusic" --icon "resources-sptmusic/icon.icns" --noconsole --hidden-import="pkg_resources.py2_warn" --exclude-module eel --exclude-module tkinter