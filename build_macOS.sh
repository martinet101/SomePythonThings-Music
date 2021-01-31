#!/bin/bash
cd "$( dirname "$0" )"
python3.8 -m PyInstaller "SomePythonThings Music.py" --add-data "resources-sptmusic:resources-sptmusic" --icon "resources-sptmusic/icon.icns" --windowed --noconsole --hidden-import="pkg_resources.py2_warn" --exclude-module eel --exclude-module tkinter --exclude-module moviepy.audio.fx.all
cd dist/SomePythonThings\ Music.app/Contents/MacOS
sudo codesign --remove-signature "Python"
cp -R /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/moviepy ./moviepy
echo 