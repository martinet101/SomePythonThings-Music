# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------- Required Modules ------------------------------------------------------------------------------ #

import os

os.environ["QT_MAC_WANTS_LAYER"] = "1"

import re
import sys
import time
import glob
import wget
import json
import pytube
import random
import urllib
import locale
import mutagen
import platform
import tempfile
import datetime
import traceback
import subprocess
import webbrowser
import darkdetect
import pynput.keyboard
from sys import platform as _platform
from ast import literal_eval
from urllib import request
from PySide2 import QtWidgets, QtGui, QtCore, QtMultimedia, QtMultimediaWidgets
from threading import Thread
from urllib.request import urlopen
from qt_thread_updater import get_updater
from youtubesearchpython import VideosSearch, Suggestions, ResultMode


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ Globals ---------------------------------------------------------------------------------- #
debugging = False
actualVersion = 2.0

music_files = ('Common Media and Video Files (*.wav; *.mp3; *.pcm; *.aiff; *.aac; *.ogg; *.wma; *.flac; *.mp4; *.wmv);;Other compatible media files (*.*)')
music_extensions = ['*.wav', '*.mp3', '*.pcm', '*.aiff', '*.aac', '*.ogg', '*.wma', '*.flac', "*.mp4"]
dataToLog = []
buttons = {}
texts = {}
progressbars = {}
lists = {}
labels = {}
sliders = {}

canRun=True
seeking = True

justContinue = False
bannerIsBeingShowed = False
playerIsRunning = False
logBlocked = False
screenModeChanged = True
videoModeChanged = True
externalVideoTrack = False
seekerValueManuallyChanged = False
forceClose = False
goRun=False
is_win7=False
blockPlay = False
shuffle = False
replay = False
playing = False
muted = False
skipped = False
goBack = False

playProcess = None
settingsWindow = None
t = None # t will be defined after KillableThread class definition
playingObj = None

volume = 100
totalTime = 0
passedTime = 0
starttime = 0
song_length = 0
elementNumber = 0
trackNumber = 0
currentTimeDelay = 0
trackSeeked = 1

background_picture_path = ''
font = ""
fileBeingPlayed = ""
realpath = "."

tempDir = tempfile.TemporaryDirectory()

defaultSettings = {
    "settings_version": actualVersion,
    "minimize_to_tray": False,        # True/False
    "volume": 100,                    # 0-100
    "showTrackNotification": True,    # True/False
    "showEndNotification": True,      # True/False
    "downloadVideo": True,            # True/False
    "downloadQuality": "high",        # high/normal/low
    "loadLibraryAtStartup": True,     # True/False
    "repeatByDefault": False,         # True/False
    "shuffleByDefault": False,        # True/False
    "alertOfKeyboardControl": True,   # Runtime setting for macOS
    "bakcgroundPicture": "None",      # Future functionality (or not)
    "mode": "auto",                   # dark/light/auto (auto is only on macOS and Windows)
    "videoMode": "big",               # big/normal/small/none
    "fullScreen": False,              # True/False
}

settings = defaultSettings.copy() # Default settings loaded, those which change will be overwritten


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- Stylesheets related ----------------------------------------------------------------------------- #
lightModeStyleSheet = """
    * 
    {{
        color: #000000;
        font-size:12px;
        font-family:{0};
        border: none;
        outline: none;
    }}
    #centralwidget
    {{
        border-image: url(\"{1}\") 0 0 0 0 stretch stretch;
    }}
    QMessageBox
    {{
        background-color:#FFFFFF;
    }}
    QPushButton
    {{
        border-image: none;
        background-color:  rgba(15, 140, 140, 1.0);
        width: 100px;
        height: 30px;
        color: #FFFFFF;
        border-radius: 3px;
    }}
    QScrollBar 
    {{
        background-color: rgba(0, 0, 0, 0.0);
    }}
    QScrollBar::handle:vertical
    {{
        margin-top: 17px;
        margin-bottom: 17px;
        border: none;
        min-height: 30px;
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
    }}
    QScrollBar::handle:horizontal
    {{
        margin-left: 17px;
        margin-right: 17px;
        border: none;
        min-width: 30px;
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
    }}
    QScrollBar::add-line 
    {{
        border: none;
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
    }}
    QScrollBar::sub-line 
    {{
        border: none;
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
    }}
    QScrollBar::corner
    {{
        background-color: none;
    }}
    QLabel
    {{   
        border-image: none;
        padding: 3px;
        background-color: none;
    }}
    QComboBox
    {{   
        border-image: none;
        selection-background-color: rgb(255, 255, 255);
        margin:0px;
        border: 1px solid black;
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 3px;
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        border-top:0px;
        padding-left: 7px;
    }}
    QSpinBox
    {{
        border: 1px solid white;
        selection-background-color: rgba(255, 255, 255, 0.7);
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 3px;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
        padding-left: 7px;
    }}
    QSpinBox::up-button
    {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
    }}
    QSpinBox::down-button
    {{
        subcontrol-origin: padding;
        subcontrol-position: bottom right;
    }}
    QSpinBox::up-arrow
    {{
        width: 16px;
        height: 16px;
    }}
    QAbstractItemView
    {{
        background-color: rgb(255, 255, 255);
        margin: 0px;
        border-radius: 3px;
    }}
    QMenuBar
    {{
        background-color: #FFFFFF;
        color: #000000;
    }}
    QMenu
    {{
        background-color: #FFFFFF;
        border-radius: 10px;
    }}
    QMenu::item
    {{
        border: 3px solid #FFFFFF;
        padding-right: 10px;
        padding-left: 5px;
        padding: 3px;
        color: #000000;
        padding-left: 8px;
    }}
    QMenu::item:selected
    {{
        border: 3px solid rgba(20, 170, 170, 1.0);
        background-color: rgba(20, 170, 170, 1.0);
    }}
    QMenuBar::item
    {{
        background-color: #FFFFFF;
        border: 3px solid  #FFFFFF;
        padding-right: 5px;
        padding-left: 5px;
    }}
    QMenuBar::item:selected
    {{
        background-color: rgba(20, 170, 170, 1.0);
        border: 3px solid rgba(20, 170, 170, 1.0);
    }}
    QSlider
    {{
        background-color: none;
    }}
    QSlider::groove
    {{
        background: rgba(255, 255, 255, 0.0);
        height: 6px;
        border: 1px solid white;
        border-radius: 4px;
        left: 8px;
        right: 8px;
    }}
    QSlider::handle
    {{
        height: 12px;
        margin: -5px 0;
        width: 13px;
        border-radius: 7px;
        background-color: rgba(20, 170, 170, 1.0);/*20, 170, 170, 1.0*/
        border: 1px solid rgba(00, 100, 100, 1.0);
    }}
    QLineEdit
    {{
        selection-background-color: rgba(255, 255, 255, 0.4);
        border-radius: 3px;
        padding-left: 5px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.4);
        color: black;
    }}
    QSlider::add-page
    {{
        background-color: #EEEEEE;
        border: 1px solid #DDDDDD;
        border-radius: 4px;
    }}
    #disabled-slider
    {{
        background-color: none;
    }}
    #disabled-slider::groove
    {{
        background: rgba(0, 0, 0, 0.0);
        height: 6px;
        border: 1px solid black;
        border-radius: 4px;
        left: 8px;
        right: 8px;
    }}
    #disabled-slider::handle
    {{
        height: 12px;
        margin: -5px 0;
        width: 13px;
        border-radius: 7px;
        background-color: #EEEEEE;/*20, 170, 170, 1.0*/
        border: 1px solid #DDDDDD;
    }}
    #disabled-slider::add-page
    {{
        background-color: #EEEEEE;
        border: 1px solid #DDDDDD;
        border-radius: 4px;
    }}
    #disabled-slider::sub-page
    {{
        background-color: #EEEEEE;
        border: 1px solid #DDDDDD;
        border-radius: 4px;
    }}
    QSlider::sub-page
    {{
        background-color: rgba(20, 170, 170, 1.0);
        border: 1px solid rgba(0, 100, 100, 1.0);
        border-radius: 4px;
    }}
    QLabel
    {{
         color: #000000;
    }}
    QTreeWidget
    {{
        padding: 5px;
        show-decoration-selected: 0;
        background-color: rgba(255, 255, 255, 0.4);
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
    }}
    QHeaderView::section
    {{
        background-color: rgba(255, 255, 255, 0.2);
        padding: 2px;
        height: 20px;
        margin-bottom: 5px;
        border: 1px solid white;
        border-top:0px;
        border-left:1px;
        border-bottom:0x;
    }}
    QTreeWidget::item
    {{
        height: 25px;
        background-color: rgba(255, 255, 255, 0.0);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(255, 255, 255);
    }}
    #downloadResult::item {{
        height: 110px;
    }}
    QTreeWidget::item:hover
    {{
        background-color: rgba(255, 255, 255, 0.1);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(255, 255, 255);
    }}
    QTreeWidget::item:selected
    {{
        background-color: rgba(255, 255, 255, 0.3);
        padding: 5px;
        padding-left: 10px;
        color: black;
        outline: 50px;
        border-bottom: 1px solid rgb(255, 255, 255);
    }}
    QGroupBox
    {{
        background-color: rgba(255, 255, 255, 0.5);
        border-top: 1px solid rgb(255, 255, 255);
    }}
    #squarePurpleButton
    {{
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
        color: black;
    }}
    #squarePurpleButton:hover
    {{
        background-color: rgba(20, 170, 170, 0.5);
        color: black;
    }}
    #squareRedButton
    {{
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
        color: black;
    }}
    #squareRedButton:hover
    {{
        background-color: rgba(255, 0, 0, 0.5);
        color: black;
    }}
    QComboBox
    {{   
        border-image: none;
        selection-background-color: rgba(20, 170, 150, 1.0);
        margin:0px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 0px;
        padding-left: 7px;
        border-bottom-right-radius: 3px;
        border-top-right-radius: 3px;
    }}
    #settingsBackground
    {{
        background-color: rgba(255, 255, 255, 0.5);
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        border-right: none;
    }}
    #settingsCheckbox
    {{
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        padding-left: 7px;
    }}
    QProgressBar
    {{
        border: none;
        border-radius: 0px;
        border-top: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.4)
    }}
    QProgressBar::chunk
    {{
        background-color: rgba(20, 180, 180, 0.4);
    }}
    QHeaderView::section
    {{
        show-decoration-selected: 0;
        background-color: transparent;
    }}
    QHeaderView
    {{
        show-decoration-selected: 0;
        background-color: transparent;
    }}
    QProgressDialog
    {{
        background-color: #EEEEEE;
    }}
    #ProgressDialogProgressbar
    {{
        border: 0px;
        background-color: #FFFFFF;
        border-radius: 3px;
    }}
    #ProgressDialogProgressbar::chunk
    {{
        border-radius: 3px;
        background-color: rgba(20, 170, 170);
    }}
    QToolTip
    {{
        background-color: #FFFFFF;
        border: none;
        padding: 3px;
    }}
    #nameQLabel{{
        background-color: rgb(255, 255, 255);
        selection-background-color: rgba(20, 180, 180, 0.5);
    }}
"""
darkModeStyleSheet = """
    * 
    {{
        color: #EEEEEE;
        font-size:12px;
        font-family:{0};
        border: none;
        outline: none;
    }}
    QMessageBox
    {{
        background-color:#333333;
    }}
    #centralwidget 
    {{
        border-image: url(\"{1}\") 0 0 0 0 stretch stretch;
    }}
    QPushButton 
    {{
        border-image: none;
        background-color:  rgba(15, 140, 140, 1.0);
        width: 100px;
        height: 30px;
        color: #EEEEEE;
        border-radius: 3px;
    }}
    QScrollBar 
    {{
        background-color: rgba(0, 0, 0, 0.0);
    }}
    QScrollBar::handle:vertical
    {{
        margin-top: 17px;
        margin-bottom: 17px;
        border: none;
        min-height: 30px;
        border-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.5);
    }}
    QScrollBar::handle:horizontal
    {{
        margin-left: 17px;
        margin-right: 17px;
        border: none;
        min-width: 30px;
        border-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.5);
    }}
    QScrollBar::add-line 
    {{
        border: none;
        border-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.5);
    }}
    QScrollBar::sub-line 
    {{
        border: none;
        border-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.5);
    }}
    QScrollBar::corner
    {{
        background-color: none;
    }}
    QLabel
    {{   
        border-image: none;
        padding: 3px;
        background-color: none;
        
    }}
    QComboBox
    {{   
        border-image: none;
        selection-background-color: rgb(0, 0, 0);
        margin:0px;
        border: 1px solid black;
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 3px;
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        border-top:0px;
        padding-left: 7px;
    }}
    QSpinBox
    {{
        border: 1px solid black;
        selection-background-color: rgba(0, 0, 0, 0.7);
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 3px;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
        padding-left: 7px;
    }}
    QSpinBox::up-button 
    {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
    }}
    QSpinBox::down-button 
    {{
        subcontrol-origin: padding;
        subcontrol-position: bottom right;
    }}
    QSpinBox::up-arrow 
    {{
        width: 16px;
        height: 16px;
    }}
    QAbstractItemView 
    {{
        background-color: rgb(41, 41, 41);
        margin: 0px;
        border-radius: 3px;
    }}
    QMenuBar
    {{
        background-color: #333333;
        color: #EEEEEE;;
    }}
    QMenu 
    {{
        background-color: #333333;
        border-radius: 10px;
    }}
    QMenu::item 
    {{
        border: 3px solid #333333;
        padding-right: 10px;
        padding-left: 5px;
        padding: 3px;
        color: #EEEEEE;;
        padding-left: 8px;
    }}
    QMenu::item:selected 
    {{
        border: 3px solid rgba(15, 140, 140, 1.0);
        background-color: rgba(15, 140, 140, 1.0);
    }}
    QMenuBar::item 
    {{
        background-color: #333333;
        border: 3px solid  #333333;
        padding-right: 5px;
        padding-left: 5px;
    }}
    QMenuBar::item:selected 
    {{
        background-color: rgba(15, 140, 140, 1.0);
        border: 3px solid  rgba(15, 140, 140, 1.0);
    }}
    QSlider 
    {{
        background-color: none;
    }}
    QSlider::groove
    {{
        background: rgba(0, 0, 0, 0.0);
        height: 6px;
        border: 1px solid black;
        border-radius: 4px;
        left: 8px;
        right: 8px;
    }}
    QSlider::handle
    {{
        height: 12px;
        margin: -5px 0;
        width: 13px;
        border-radius: 7px;
        background-color: rgba(20, 170, 170, 1.0);/*20, 170, 170, 1.0*/
        border: 1px solid rgba(00, 100, 100, 1.0);
    }}
    QSlider::add-page 
    {{
        background-color: #333333;
        border: 1px solid #222222;
        border-radius: 4px;
    }}
    QSlider::sub-page 
    {{
        background-color: rgba(20, 170, 170, 1.0);
        border: 1px solid rgba(0, 100, 100, 1.0);
        border-radius: 4px;
    }}
    #disabled-slider 
    {{
        background-color: none;
    }}
    #disabled-slider::groove
    {{
        background: rgba(0, 0, 0, 0.0);
        height: 6px;
        border: 1px solid black;
        border-radius: 4px;
        left: 8px;
        right: 8px;
    }}
    #disabled-slider::handle
    {{
        height: 12px;
        margin: -5px 0;
        width: 13px;
        border-radius: 7px;
        background-color: #333333;/*20, 170, 170, 1.0*/
        border: 1px solid #222222;
    }}
    #disabled-slider::add-page
    {{
        background-color: #333333;
        border: 1px solid #222222;
        border-radius: 4px;
    }}
    #disabled-slider::sub-page 
    {{
        background-color: #333333;
        border: 1px solid #222222;
        border-radius: 4px;
    }}
    QLabel 
    {{
         color: #EEEEEE;
    }}
    QTreeWidget
    {{
        border-image: none;
        padding: 5px;
        show-decoration-selected: 0;
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
    }}
    QHeaderView::section
    {{
        background-color: rgba(0, 0, 0, 0.2);
        padding: 2px;
        height: 20px;
        margin-bottom: 5px;
        border: 1px solid black;
        border-top:0px;
        border-left:1px;
        border-bottom:0x;
    }}
    QTreeWidget::item
    {{
        height: 25px;
        border-image: none;
        background-color: rgba(0, 0, 0, 0.0);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(0, 0, 0);
    }}
    #downloadResult::item {{
        height: 90px;
        padding-left: 0px;
    }}
    QTreeWidget::item:hover
    {{
        background-color: rgba(0, 0, 0, 0.1);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(0, 0, 0);
    }}
    QTreeWidget::item:selected
    {{
        background-color: rgba(0, 0, 0, 0.3);
        padding: 5px;
        padding-left: 10px;
        color: white;
        outline: 50px;
        border-bottom: 1px solid rgb(0, 0, 0);
    }}
    QGroupBox 
    {{
        background-color: rgba(0, 0, 0, 0.4);
        border-top: 1px solid rgb(0, 0, 0);
    }}
    #squarePurpleButton 
    {{
        border-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.4);
        color: white;
    }}
    QLineEdit
    {{
        selection-background-color: rgba(0, 0, 0, 0.4);
        border-radius: 3px;
        padding-left: 5px;
        border: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.4);
        color: white;
    }}
    #squarePurpleButton:hover
    {{
        background-color: rgba(20, 170, 150, 0.5);
        color: white;
    }}
    #squareRedButton 
    {{
        border-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.4);
        color: white;
    }}
    #squareRedButton:hover
    {{
        background-color: rgba(255, 0, 0, 0.5);
        color: white;
    }}
    QComboBox
    {{   
        border-image: none;
        selection-background-color: rgba(20, 170, 150, 1.0);
        margin:0px;
        border: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 0px;
        padding-left: 7px;
        border-bottom-right-radius: 3px;
        border-top-right-radius: 3px;
    }}
    #settingsBackground
    {{
        background-color: rgba(0, 0, 0, 0.4);
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        border-right: none;
    }}
    #settingsCheckbox
    {{
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        padding-left: 7px;
    }}
    QProgressBar
    {{
        border: none;
        border-radius: 0px;
        border-top: 1px solid rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.4)
    }}
    QProgressBar::chunk
    {{
        background-color: rgba(10, 150, 150, 0.5);
    }}
    QHeaderView::section
    {{
        show-decoration-selected: 0;
        background-color: transparent;
    }}
    QHeaderView
    {{
        show-decoration-selected: 0;
        background-color: transparent;
    }}
    QProgressDialog
    {{
        background-color: #333333;
    }}
    #ProgressDialogProgressbar
    {{
        border: 0px;
        background-color: #222222;
        border-radius: 3px;
    }}
    #ProgressDialogProgressbar::chunk
    {{
        border-radius: 3px;
        background-color: rgb(20, 120, 120);
    }}
    QToolTip
    {{
        background-color: #333333;
        border: none;
        padding: 3px;
    }}
    QVideoWidget
    {{
        background-color: rgba(0, 0, 0, 0.5);
        border: 1px solid black;
        border-radius: 3px;
    }}
    QAbstractItemView#completerPopup 
    {{
        background-color: #333333;
        border-radius: 10px;
    }}
    QAbstractItemView#completerPopup::item 
    {{
        border: 3px solid #333333;
        padding-right: 10px;
        padding-left: 5px;
        padding: 3px;
        color: #EEEEEE;
        padding-left: 8px;
    }}
    QAbstractItemView#completerPopup::item:selected 
    {{
        border: 3px solid rgba(15, 140, 140, 1.0);
        background-color: rgba(15, 140, 140, 1.0);
    }}
    #nameQLabel{{
        background-color: rgb(27, 27, 27);
        selection-background-color: rgba(20, 170, 170, 0.5);
    }}
"""
def getTheme() -> bool:
    return int(darkdetect.isLight())

def getWindowStyleSheet(banner: bool = False) -> str:
    global settings, realpath, background_picture_path
    if(banner):
        log("[  WARN  ] Returning banner stylesheet!")
        local_background_picture_path = background_picture_path.replace("background-sptmusic", "half-background-sptmusic")
    else:
        log("[  WARN  ] Returning normal window stylesheet!")
        local_background_picture_path = background_picture_path
    mode = 'auto'
    try:
        if(os.path.exists(settings['background'])):
            background_picture_path =  settings['background']
        else:
            log("[  WARN  ] Custom background picture does not exist")
    except KeyError:
        log("[  WARN  ] Can't get custom background picture")
    log("[   OK   ] Background picture path set to "+str(local_background_picture_path))
    try:
        if(str(settings["mode"]).lower() in 'darklightauto'):
            mode = str(settings['mode'])
        else:
            log("[  WARN  ] Mode is invalid")
    except KeyError:
        log("[  WARN  ] Mode key does not exist on settings")
    if(mode=='auto'):
        if(getTheme()==0):
            log('[        ] Auto mode selected. Swithing to dark...')
            mode='dark'
        else:
            log('[        ] Auto mode selected. Swithing to light...')
            mode='light'
    log('[   OK   ] mode set to '+str(mode))
    if(mode=='light'):
        return lightModeStyleSheet.format(font, local_background_picture_path)
    else:
        return darkModeStyleSheet.format(font, local_background_picture_path)

def checkModeThread() -> None:
    lastMode = getTheme()
    while True:
        if(lastMode!=getTheme()):
            get_updater().call_in_main(music.setStyleSheet, getWindowStyleSheet())
            lastMode = getTheme()
        time.sleep(0.1)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- Essential Functions ----------------------------------------------------------------------------- #
def run(s: str) -> int:
    if(is_win7):
        log('[   OK   ] Running subprocess as win7_8...')
        return os.system(s)
    else:
        log('[   OK   ] Running subprocess as non win7_8...')
        process =  subprocess.Popen(s.split(' '), shell=(_platform=='win32'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        process.communicate()
        process.stdin.close()
        process.wait()
        return process.returncode

def log(s: str, force: bool = False) -> None:
    global debugging
    timePrefix = time.strftime('[%H:%M:%S] ', time.gmtime(time.time()))
    if(debugging or "WARN" in str(s) or "FAILED" in str(s) or force):
        print(timePrefix+str(s))
    try:
        dataToLog.append(timePrefix+s+"\n")
    except Exception as e:
        if(debugging):
            raise e

def logToFileWorker() -> None:
    while True:
        if len(dataToLog)>0:
            with open(tempDir.name.replace('\\', '/')+'/log.txt', "a+", errors="ignore") as log:
                try:
                    log.write(dataToLog[0])
                except Exception as e:
                    log.write(f"!--- An error occurred while saving line, missing log line ---!   ({e})\n")
            del dataToLog[0]
        else:
            time.sleep(0.01)

def notify(title: str, body: str, icon: str =realpath+"/icon.ico") -> None:
    log(f"[   OK   ] Showing notification with title {title} and body {body}")
    tray.showMessage(title, body, QtGui.QIcon(icon))
    
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------ Update Functions ------------------------------------------------------------------------------- #
if True: # This conditional is only to be able to collapse the full updates block in VS Code
    def checkUpdates_py(force: bool = False) -> str:
        global music, actualVersion
        try:

            response = urlopen("http://www.somepythonthings.tk/versions/music.ver")
            response = response.read().decode("utf8")
            if float(response.split("///")[0]) > actualVersion:
                get_updater().call_in_main(askUpdates, response)
                return 'Yes'
            elif(force):
                get_updater().call_in_main(askUpdates, response)
                return 'Yes (Forced)'
            else:
                log("[   OK   ] No updates found")
                return 'No'
        except Exception as e:
            if debugging:
                raise e
            log("[  WARN  ] Unable to reach http://www.somepythonthings.tk/versions/music.ver. Are you connected to the internet?")
            return 'Unable'

    def askUpdates(response: str) -> None:
        notify("SomePythonThings Music Updater", "SomePythonThings Music has a new update!\nActual version: {0}\nNew version: {1}".format(actualVersion, response.split("///")[0]))
        if QtWidgets.QMessageBox.Yes == confirm(music, 'SomePythonThings Music', "There are some updates available for SomePythonThings Music:\nYour version: "+str(actualVersion)+"\nNew version: "+str(response.split("///")[0])+"\nNew features: \n"+response.split("///")[1]+"\nDo you want to download and install them?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes):

            #                'debian': debian link in posotion 2                  'win32' Windows 32bits link in position 3           'win64' Windows 64bits in position 4                   'macos' macOS 64bits INTEL in position 5
            downloadUpdates({'debian': response.split("///")[2].replace('\n', ''), 'win32': response.split("///")[3].replace('\n', ''), 'win64': response.split("///")[4].replace('\n', ''), 'macos':response.split("///")[5].replace('\n', '')})
        else:
            log("[  WARN  ] User aborted update!")

    def downloadUpdates(links: dict) -> None:
        log('[   OK   ] Reached downloadUpdates. Download links are "{0}"'.format(links))
        if _platform == 'linux' or _platform == 'linux2':  # If the OS is linux
            log("[   OK   ] platform is linux, starting auto-update...")
            throw_info("SomePythonThings Updater", "The update is being downloaded. Please wait.")
            t = Thread(target=download_linux, args=(links,))
            t.daemon = True
            t.start()
        elif _platform == 'win32':  # if the OS is windows
            log('win32')
            url = ""
            if(platform.architecture()[0] == '64bit'):  # if OS is 64bits
                url = (links["win64"])
            else:  # is os is not 64bits
                url = (links['win32'])
            log(url)
            
            throw_info("SomePythonThings Updater", "The update is being downloaded. Please wait.")
            t = Thread(target=download_win, args=(url,))
            t.daemon=True
            t.start()
        elif _platform == 'darwin':
            log("[   OK   ] platform is macOS, starting auto-update...")
            
            throw_info("SomePythonThings Updater", "The update is being downloaded. Please wait.")
            t = Thread(target=download_macOS, args=(links,))
            t.daemon=True
            t.start()
        else:  # If os is unknown
            webbrowser.open_new('https://www.somepythonthings.tk/programs/somepythonthings-music/')

    def download_win(url: str) -> None:
        try:
            global texts
            os.system('cd %windir%\\..\\ & mkdir SomePythonThings')
            time.sleep(0.01)
            os.chdir("{0}/../SomePythonThings".format(os.environ['windir']))
            installationProgressBar('Downloading')
            filedata = urlopen(url)
            datatowrite = filedata.read()
            filename = ""
            with open("{0}/../SomePythonThings/SomePythonThings-Music-Updater.exe".format(os.environ['windir']), 'wb') as f:
                f.write(datatowrite)
                filename = f.name
            installationProgressBar('Launching')
            log(
                "[   OK   ] file downloaded to C:\\SomePythonThings\\{0}".format(filename))
            get_updater().call_in_main(launch_win, filename)
        except Exception as e:
            if debugging:
                raise e
            get_updater().call_in_main(throw_error, "SomePythonThings Music", "An error occurred while downloading the SomePythonTings Music installer. Please check your internet connection and try again later\n\nError Details:\n{0}".format(str(e)))

    def launch_win(filename: str) -> None:
        try:
            installationProgressBar('Launching')
            throw_info("SomePythonThings Music Updater", "The update has been downloaded and is going to be installed.\nYou may be prompted for permissions, click YES.\nClick OK to start installation")
            os.system('start /B {0} /silent'.format(filename))
            try:        
                killPlayProcess()
            except AttributeError:
                pass
            get_updater().call_in_main(sys.exit)
            sys.exit()
        except Exception as e:
            if debugging:
                raise e
            throw_error("SomePythonThings Music Updater", "An error occurred while launching the SomePythonTings Music installer.\n\nError Details:\n{0}".format(str(e)))

    def download_linux(links: dict) -> None:
        get_updater().call_in_main(installationProgressBar, 'Downloading')
        p1 = os.system('cd; rm somepythonthings-music_update.deb; wget -O "somepythonthings-music_update.deb" {0}'.format(links['debian']))
        if(p1 == 0):  # If the download is done
            get_updater().call_in_main(install_linux_part1)
        else:  # If the download is falied
            get_updater().call_in_main(throw_error, "SomePythonThings", "An error occurred while downloading the update. Check your internet connection. If the problem persists, try to download and install the program manually.")
            webbrowser.open_new('https://www.somepythonthings.tk/programs/somepythonthings-music/')

    def install_linux_part1(again: bool = False) -> None:
        global music
        installationProgressBar('Installing')
        time.sleep(0.2)
        if not again:
            passwd = str(QtWidgets.QInputDialog.getText(music, "Autentication needed - SomePythonThings Music", "Please write your password to perform the update. (SomePythonThings Music needs SUDO access in order to be able to install the update)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0])
        else:
            passwd = str(QtWidgets.QInputDialog.getText(music, "Autentication needed - SomePythonThings Music", "An error occurred while autenticating. Insert your password again (This attempt will be the last one)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0])
        t = Thread(target=install_linux_part2, args=(passwd, again))
        t.start()

    def install_linux_part2(passwd: str, again: bool = False) -> None:
        installationProgressBar('Installing')
        p1 = os.system('cd; echo "{0}" | sudo -S apt install ./"somepythonthings-music_update.deb" -y'.format(passwd))
        if(p1 == 0):  # If the installation is done
            p2 = os.system('cd; rm "./somepythonthings-music_update.deb"')
            if(p2 != 0):  # If the downloaded file cannot be removed
                log("[  WARN  ] Could not delete update file.")
            installationProgressBar('Installing')
            get_updater().call_in_main(throw_info,"SomePythonThings Music Updater","The update has been applied succesfully. Please restart the application")
            try:        
                killPlayProcess()
            except AttributeError:
                pass
            get_updater().call_in_main(sys.exit)
            sys.exit()
        else:  # If the installation is falied on the 1st time
            if not again:
                get_updater().call_in_main(install_linux_part1, True)
            else:
                installationProgressBar('Stop')
                get_updater().call_in_main(throw_error, "SomePythonThings Music Updater", "Unable to apply the update. Please try again later.")

    def download_macOS(links: dict) -> None:
        try:
            installationProgressBar('Downloading')
            p1 = os.system('cd; rm somepythonthings-music_update.dmg')
            if(p1!=0):
                log("[  WARN  ] unable to delete somepythonthings-music_update.dmg")
            wget.download(links['macos'], out='{0}/somepythonthings-music_update.dmg'.format(os.path.expanduser('~')))
            get_updater().call_in_main(install_macOS)
            log("[   OK   ] Download is done, starting launch process.")
        except Exception as e:
            if debugging:
                raise e
            get_updater().call_in_main(throw_error,"SomePythonThings Music Updater", "An error occurred while downloading the update. Check your internet connection. If the problem persists, try to download and install the program manually.\n\nError Details:\n"+str(e))
            webbrowser.open_new('https://www.somepythonthings.tk/programs/somepythonthings-music/')

    def install_macOS() -> None:
        installationProgressBar('Launching')
        time.sleep(0.2)
        throw_info("SomePythonThings Music Updater", "The update file has been downloaded successfully. When you click OK, SomePythonThings Music is going to be closed and a DMG file will automatically be opened. Then, you'll need to drag the application on the DMG to the applications folder (also on the DMG). Click OK to continue")
        p2 = os.system('cd; open ./"somepythonthings-music_update.dmg"')
        log("[  INFO  ] macOS installation unix output code is \"{0}\"".format(p2))
        try:        
            killPlayProcess()
        except AttributeError:
            pass
        sys.exit()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------- Functions ---------------------------------------------------------------------------------- #
def youtubeWindow() -> None:

    dialog = None
    downloadSize = 0

    def openYoutubeLink(link: str) -> None:
        webbrowser.open(link)

    def downloadPictureAndAdd(video: dict, tempdir: tempfile.TemporaryDirectory, i: int) -> None:
        pic = open(os.path.join(tempdir.name, f"pic{i}.webp"), 'w+b')
        try:
            pic.write(urlopen(video['richThumbnail']['url'].replace("https", "http")).read())
        except NotADirectoryError:
            pass
        except KeyError:
            pic.write(urlopen(video['thumbnails'][0]['url']).read())
        except urllib.error.HTTPError:
            pic.write(urlopen(video['thumbnails'][0]['url']).read())
        except TypeError:
            log("[  WARN  ] No GIF preview!!!")
            pic.write(urlopen(video['thumbnails'][0]['url']).read())
        except Exception as e:
            if(debugging):
                raise e
        picPath = pic.name
        get_updater().call_in_main(addResultItem, video, tempdir, i, picPath)
        pic.close()
    
    def addResultItem(video: dict, tempdir: tempfile.TemporaryDirectory, i: int, picPath: str) -> None:
        newItem = QtWidgets.QTreeWidgetItem()
        newItem.setText(0, "{0:0>4}".format(str(i)))
        try:
            stringToShow =  f"   <span style=\" font-size:16px; font-weight:600;\">{video['title']}</span><br><br>   Published by: {video['channel']['name']}<br>   Duration: {video['duration']}"
        except TypeError:
            stringToShow = ""
        newItem.setToolTip(1, "Double-click to download")
        description = QtWidgets.QLabel(youtube)
        description.setWordWrap(True)
        try:
            description.setText(video['descriptionSnippet'][0]["text"])
        except TypeError:
            pass
        except Exception as e:
            description.setText("")
            if(debugging):
                raise e
        webp = QtGui.QMovie(picPath)
        webp.setScaledSize(QtCore.QSize(160, 90))

        output = QtWidgets.QLabel(youtube)
        output.setMovie(webp)

        #newItem.setIcon(0, QtGui.QIcon(QtGui.QPixmap(picPath).scaledToHeight(90, QtCore.Qt.SmoothTransformation)))
        newItem.setText(6, "https://www.youtube.com/watch?v="+video['id'])
        newItem.setText(7, video['title'])
        results.addTopLevelItem(newItem)
        
        btn = QtWidgets.QPushButton("Download", youtube)
        btn.resize(100, 20)
        btn.setObjectName("squarePurpleButton")
        btn.setToolTip("Download to your library")
        btn.clicked.connect(startDownload)
        
        results.setItemWidget(newItem, 0, output)
        webp.start()
        results.setItemWidget(newItem, 2, btn)
        results.setItemWidget(newItem, 1, QtWidgets.QLabel(stringToShow))
        results.setItemWidget(newItem, 3, description)

        url = "https://www.youtube.com/watch?v="+video['id']
        link = QtWidgets.QPushButton(url, youtube)
        link.clicked.connect(lambda: openYoutubeLink(url))
        link.setToolTip("Open link on browser")
        link.setObjectName("squarePurpleButton")
        
        results.setItemWidget(newItem, 5, link)

    def getResults() -> None:
        results.setFocus()
        try:
            videosSearch = VideosSearch(query.text(), limit = 20)
            resultsFound = (videosSearch.result()['result'])
            tempdir = tempfile.TemporaryDirectory()
            results.clear()
            i = 20
            for video in resultsFound:
                Thread(target=downloadPictureAndAdd, args=(video, tempdir, i,), daemon=True).start()

                i -= 1

            if(len(resultsFound) == 0):
                get_updater().call_in_main(throw_error, "SomePythonThings Music", "No results found!")
        except Exception as e:
            get_updater().call_in_main(throw_error, "SomePythonThings Music", "Unable to retrieve youtube results!\n\nPlease try it again later")
            if(debugging):
                raise e

    def startDownload() -> None:

        global settings
        nonlocal resCombo

        t = KillableThread(target=downloadAndAdd, daemon=True)

        if(resCombo.currentIndex() == 2):
            settings["downloadQuality"] = "low"
            

        elif(resCombo.currentIndex() == 1):
            settings["downloadQuality"] = "normal"
            

        elif(resCombo.currentIndex() == 0):
            settings["downloadQuality"] = "high"

        settings["downloadVideo"] = videoCheckBox.isChecked()


        saveSettings()
        name = results.currentItem().text(1)
        nonlocal dialog
        dialog = QtWidgets.QProgressDialog(youtube)
        dialog.setAutoFillBackground(True)
        dialog.setWindowModality(QtCore.Qt.WindowModal)
        dialog.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        dialog.setModal(True)
        dialog.setSizeGripEnabled(False)
        dialog.setWindowTitle('SomePythonThings Music')
        dialog.setLabelText(f'Preparing {name} download...')
        pgsbar = QtWidgets.QProgressBar(dialog)
        pgsbar.setTextVisible(False)
        pgsbar.setObjectName("ProgressDialogProgressbar")
        dialog.setBar(pgsbar)
        dialog.setRange(0, 0)
        dialog.setMinimumDuration(0)
        dialog.setAutoClose(True)
        dialog.show()
        dialog.canceled.connect(lambda: t.kill())
        t.start()
        dialog.exec_()

    def showDownloadProgress(stream: pytube.Stream, chunk: bytes, bytes_remaining: int) -> None:
        global downloadSize
        get_updater().call_in_main(dialog.setValue, (downloadSize-bytes_remaining)/downloadSize*100)

    def downloadAndAdd() -> None:
        global downloadSize
        nonlocal videoCheckBox
        try:
            warn = False
            link = results.currentItem().text(6)
            name = results.currentItem().text(7).replace(".", "").replace("/", "").replace("\\", "")
            os.chdir(os.path.expanduser("~"))
            get_updater().call_in_main(dialog.setLabelText, f"Preparing things...")
            try:
                os.chdir(os.path.expanduser("~")+"/SomePythonThings Music")
                log("[   OK   ] Acessed \"~/SomePythonThings Music\"")
            except FileNotFoundError:
                os.mkdir(os.path.expanduser("~")+"/SomePythonThings Music")
                log("[  WARN  ] \"~/SomePythonThings Music\" not found, creating it...")
                os.chdir(os.path.expanduser("~")+"/SomePythonThings Music")

            output_path = os.path.join(os.path.expanduser("~"), "SomePythonThings Music")
            log("[   OK   ] Output path is "+output_path)

            get_updater().call_in_main(dialog.setLabelText, f"Fetching \"{name}\" links...")
            yt = pytube.YouTube(link)
            yt.register_on_progress_callback(showDownloadProgress)
            audio = None
            video = None
            downloadvideo = videoCheckBox.isChecked()
            highestResolution = ["1080p", "720p", "480p", "360p", "240p", "144p"]
            normalResolution = ["480p", "360p", "240p", "144p"]
            lowestResolution = ["144p", "240p", "360p", "480p"]
            try:
                if(resCombo.currentIndex() == 2):
                    log("[        ] Downloading the lowest resolution")
                    audio = yt.streams.filter(progressive=False, only_audio=True).get_audio_only()
                    if downloadvideo:
                        i = 0
                        while yt.streams.filter(progressive=False, resolution=lowestResolution[i], only_video=True).first() == None or i>10:
                            i += 1
                        video = yt.streams.filter(progressive=False, resolution=lowestResolution[i], only_video=True).first()


                elif(resCombo.currentIndex() == 1):
                    log("[        ] Downloading the normal resolution")
                    audio = yt.streams.filter(progressive=False, only_audio=True).get_audio_only()
                    if downloadvideo:
                        i = 0
                        while yt.streams.filter(progressive=False, resolution=normalResolution[i], only_video=True).first() == None or i>10:
                            i += 1
                        video = yt.streams.filter(progressive=False, resolution=normalResolution[i], only_video=True).first()


                elif(resCombo.currentIndex() == 0):
                    log("[        ] Downloading the highest resolution")
                    audio = yt.streams.filter(progressive=False, only_audio=True).get_audio_only()
                    if downloadvideo:
                        i = 0
                        while yt.streams.filter(progressive=False, resolution=highestResolution[i], only_video=True).first() == None or i>10:
                            i += 1
                        video = yt.streams.filter(progressive=False, resolution=highestResolution[i], only_video=True).first()


            except Exception as e:
                get_updater().call_in_main(throw_error, "SomePythonThings Downloader", "An error occurred while loading your file. \n\nError details:\n"+str(e))
                if(debugging):
                    raise e


            if(downloadvideo):
                log("[        ] Downloading video...")
                downloadSize = video.filesize
                get_updater().call_in_main(dialog.setRange, 0, 101)
                get_updater().call_in_main(dialog.setLabelText, f"Downloading \"{name}\" video...")
                try:
                    log("[        ] Removing possible old file...")
                    os.remove(os.path.join(output_path, name+".downloadedVideoTrack"))
                except Exception as e:
                    log("[  WARN  ] "+str(e))
                video.download(output_path, name+".downloadedVideoTrack")
                filename = video.get_file_path(name+".downloadedVideoTrack", output_path)
                os.rename(filename, filename.replace("downloadedVideoTrack.mp4", ".downloadedVideoTrack"))
            else:
                log("[  WARN  ] NOT downloading video...")

            downloadSize = audio.filesize
            get_updater().call_in_main(dialog.setRange, 0, 101)
            get_updater().call_in_main(dialog.setLabelText, f"Downloading \"{name}\" audio...")
            try:
                log("[        ] Removing possible old file...")
                os.remove(os.path.join(output_path, name+".mp4"))
            except Exception as e:
                log("[  WARN  ] "+str(e))
            log("[        ] Starting audio download...")
            audio.download(output_path, name)
            filename = audio.get_file_path(name, output_path)




            get_updater().call_in_main(dialog.setRange, 0, 0)
            get_updater().call_in_main(dialog.setLabelText, f"Downloading \"{name}\" art...")

            picture = yt.thumbnail_url.replace('https', 'http')
            try:
                request.urlretrieve(picture, filename.replace('mp4', 'jpg'))
            except Exception as e:
                log("[ FAILED ] Unable to dowload media art!")
                if(debugging):
                    raise e
            log(f"[   OK   ] File {filename} downloaded successfully")

            get_updater().call_in_main(dialog.close)
            get_updater().call_in_main(dialog.setAutoFillBackground,False)
            get_updater().call_in_main(dialog.setWindowFlag,QtCore.Qt.WindowContextHelpButtonHint, True)
            get_updater().call_in_main(dialog.setWindowFlag,QtCore.Qt.WindowCloseButtonHint, True)
            get_updater().call_in_main(dialog.setModal,False)
            get_updater().call_in_main(dialog.setSizeGripEnabled,True)
            get_updater().call_in_main(addFile, filename)
            if(_platform=="win32"):
                get_updater().call_in_main(throw_info, "SomePythonThings Music", f"The song {name} has been saved successfully to your library")
            if(warn):
                try:
                    #os.remove(oldName)
                    log("[   OK   ] MP4 File removed at 2nd attempt")
                except:
                    log("[ FAILED ] Unable to remove MP4 file!!!")

        except Exception as e:
            get_updater().call_in_main(throw_error, "SomePythonThings Music", "An error occurred while downloading the file.")
            try: 
                get_updater().call_in_main(dialog.close)
            except:
                pass
            if(debugging):
                raise e

    def loadSuggestions() -> None:
        lang = locale.getdefaultlocale()[0].split("_")[0]
        region = locale.getdefaultlocale()[0].split("_")[1]
        suggestions = (Suggestions(language = lang, region = region).get(query.text(), mode = ResultMode.dict)["result"])
        get_updater().call_latest(setSuggestions, suggestions)
    
    def setSuggestions(suggestions: list) -> None:
        completer.setModel(QtCore.QStringListModel(suggestions, completer))
        completer.complete()

    def showHideRes() -> None:
        if(videoCheckBox.isChecked()):
            resCombo.show()
            resLabel.show()
        else:
            resCombo.hide()
            resLabel.hide()

    def resizeWidgets() -> None:
        h = youtube.height()
        w = youtube.width()
        query.move(10, 10)
        query.resize(w-120, 30)
        button.move(w-100, 10)
        button.resize(90, 30)
        results.move(10, 90)
        results.resize(w-20, h-140)
        closeButton.move(10, h-40)

        videoCheckBox.move(10, 50)
        videoCheckBox.resize(w//2-10, 30)

        resLabel.move((w)//2+10, 50)
        resLabel.resize((w)//4, 30)

        resCombo.move((w//4)*3+10, 50)
        resCombo.resize(w//4-20, 30)

    global music
    youtube = ClosableWindow(music)
    youtube.setStyleSheet(getWindowStyleSheet())
    youtube.resize(900, 500)
    youtube.setMinimumSize(300, 200)
    youtube.setWindowTitle("Download Youtube Music")
    youtube.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
    youtube.resized.connect(resizeWidgets)
    if(_platform == 'darwin'):
        youtube.setAutoFillBackground(True)
        youtube.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        youtube.setWindowModality(QtCore.Qt.ApplicationModal)
        youtube.setWindowModality(QtCore.Qt.WindowModal)
        youtube.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        youtube.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        youtube.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    query = QtWidgets.QLineEdit(youtube)
    query.setPlaceholderText("Search a song, a podcast or a tv show (or whatever you want)")
    query.move(10, 10)
    query.textChanged.connect(lambda: Thread(target=loadSuggestions, daemon=True).start())
    query.returnPressed.connect(getResults)
    query.resize(580, 30)

    completer = QtWidgets.QCompleter([], youtube)
    d = QtWidgets.QStyledItemDelegate()
    completer.popup().setItemDelegate(d)
    completer.popup().setObjectName("completerPopup")
    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    completer.activated.connect(getResults)
    query.setCompleter(completer)

    button = QtWidgets.QPushButton(youtube)
    button.setText("Search")
    button.setObjectName("squarePurpleButton")
    button.move(600, 10)
    button.resize(90, 30)
    button.clicked.connect(getResults)

    results = QtWidgets.QTreeWidget(youtube)
    results.setVerticalScrollMode(QtWidgets.QTreeWidget.ScrollPerPixel)
    results.setColumnCount(8)
    results.setHeaderLabels(["#", " Name", " Download", " Description", " Publisher", " Youtube link (Click to open)", "", ""])
    results.setColumnWidth(0, 200)
    results.setColumnWidth(1, 400)
    results.setColumnWidth(2, 100)
    results.setColumnWidth(3, 400)
    results.setColumnHidden(4, True)
    results.setColumnWidth(5, 400)
    results.setColumnHidden(6, True)
    results.setColumnHidden(7, True)
    results.setObjectName("downloadResult")
    results.setIconSize(QtCore.QSize(160, 90))
    results.move(10, 50)
    results.setSortingEnabled(True)
    results.itemDoubleClicked.connect(startDownload)
    results.resize(620, 370)

    closeButton = QtWidgets.QPushButton(youtube)
    closeButton.setText("Close")
    closeButton.setObjectName("squareRedButton")
    closeButton.move(10, 460)
    closeButton.resize(200, 30)
    closeButton.clicked.connect(youtube.close)

    videoCheckBox = QtWidgets.QCheckBox("Download video track (To watch the videoclip or the lyrics)", youtube)
    videoCheckBox.setObjectName("settingsCheckbox")
    videoCheckBox.clicked.connect(showHideRes)

    resLabel = QtWidgets.QLabel("Video resolution (If available):", youtube)
    resLabel.setObjectName("settingsBackground")

    resCombo = QtWidgets.QComboBox(youtube)
    resCombo.insertItems(0, ["High definition (1080p)", "Standard definition (480p)", "Low definition (144p)"])

    if(settings["downloadQuality"] == "high"):
        resCombo.setCurrentIndex(0)
    elif(settings["downloadQuality"] == "normal"):
        resCombo.setCurrentIndex(1)
    else:
        resCombo.setCurrentIndex(2)
    
    videoCheckBox.setChecked(settings["downloadVideo"])

    showHideRes()

    query.setFocus()
    youtube.show()

def showMediaWindow(skip=False) -> None:
    banner.show()

def openRenameMenu() -> None:
    log("[   OK   ] Showing rename text editor...")
    nameEditor = QtWidgets.QLineEdit()
    nameEditor.setObjectName("nameQLabel")
    nameEditor.editingFinished.connect(renameFile)
    nameEditor.setText(getSongTitle(mainList.currentItem().text(2)))#.replace("\\", "/").split("/")[-1].replace('.'+getFileType(mainList.currentItem().text(2).replace("\\", "/").split("/")[-1]).lower(), "")
    mainList.setItemWidget(mainList.currentItem(), 0, nameEditor)
    nameEditor.setFocus()

def renameFile() -> None:
    log("[   OK   ] Starting rename action...")
    emptyPlayerMedia()
    mainList.itemWidget(mainList.currentItem(), 0).hide()
    newName = mainList.itemWidget(mainList.currentItem(), 0).text()
    originalPath = mainList.takeTopLevelItem(mainList.indexOfTopLevelItem(mainList.currentItem())).text(2).replace("\\", "/")
    fileExt = getFileType(originalPath)
    newPath = originalPath.replace(originalPath.split("/")[-1], newName)
    if not fileExt.lower() in newPath:
        newPath += '.'+fileExt.lower()
    log(f"[        ] Renaming {originalPath} to {newPath}")
    os.rename(originalPath, newPath)
    try:
        os.rename(originalPath.replace(".mp4", ".downloadedVideoTrack"), newPath.replace(".mp4", ".downloadedVideoTrack"))
    except FileNotFoundError:
        pass
    try:
        os.rename(originalPath.replace(".mp4", ".jpg"), newPath.replace(".mp4", ".jpg"))
    except FileNotFoundError:
        pass
    addFile(newPath)

def emptyPlayerMedia() -> None:
    log("[  WARN  ] Unloading media...")
    playProcess.setMedia(QtMultimedia.QMediaContent(None))
    videoPlayProcess.setMedia(QtMultimedia.QMediaContent(None))

def toStyleMainList() -> None:
    global playing, lists, trackNumber, music, font, t
    try:
        for item in range(0, mainList.topLevelItemCount()):
            mainList.topLevelItem(item).setFont(0, QtGui.QFont(font, weight=QtGui.QFont.Normal))
            mainList.topLevelItem(item).setIcon(0, QtGui.QIcon(QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(mainList.topLevelItem(item).text(2))).pixmap(128, 128).scaledToHeight(24, QtCore.Qt.SmoothTransformation)))
        if(playing):
            mainList.topLevelItem(trackNumber).setFont(0, QtGui.QFont(font, weight=QtGui.QFont.Bold))
            mainList.topLevelItem(trackNumber).setIcon(0, QtGui.QIcon(str(realpath)+"/icons-sptmusic/playing.ico"))
        mainList.repaint()
    except AttributeError:
        log('[  WARN  ] An error occurred on playback thread, trackNumber is {0}...'.format(str(trackNumber)))
        try:
            t.shouldBeRuning = False
        except AttributeError:
            pass
        t = KillableThread(target=startPlayback)
        t.daemon = True
        t.start()
    except Exception as e:
        if(debugging):
            raise e

def killPlayProcess() -> None:
    global playProcess
    try:
        playProcess.stop()
        if(externalVideoTrack):
            videoPlayProcess.stop()
    except Exception as e:
        if(debugging):
            raise e

def removeFromPlaylist() -> None:
    global lists, trackNumber, justContinue, passedTime
    for itemToRemove in mainList.selectedItems():
        if(itemToRemove != None):
            try:
                trackToRemove = mainList.indexOfTopLevelItem(itemToRemove)
                log('[        ] Index of files list is {0}, deleting song in position {0}'.format(trackToRemove))
                item = mainList.takeTopLevelItem(trackToRemove)
                del item
                passedTime = 0.0
                log("[   OK   ] File removed!")
            except Exception as e:
                throw_error("Unable to remove track!", "Unable to remove the track from the playlist.\n\nError Details: \n"+str(e))
                if(debugging):
                    raise e
        else:
            log('[  WARN  ] No song selected to detete!')
    
    resultsFound = mainList.findItems('', QtCore.Qt.MatchContains, 0)
    if(len(resultsFound)==0):
        noResultsfoundLabel.show()
    else:
        noResultsfoundLabel.hide()

def removeFromComputer() -> None:
    global lists, trackNumber, justContinue, passedTime
    log("[  WARN  ] Starting track(s) permanent removal!")
    emptyPlayerMedia()
    for itemToRemove in mainList.selectedItems():
        if(itemToRemove != None):
            if QtWidgets.QMessageBox.Yes == warnAndConfirm(music, 'Delete file - SomePythonThings Music', f"Do you really want to delete \"{itemToRemove.text(2)}\" from YOUR COMPUTER? Please note that this action CANNOT be reverted.", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No):
                try:
                    trackToRemove = mainList.indexOfTopLevelItem(itemToRemove)
                    log(f"[  WARN  ] Removing file {itemToRemove.text(2)} from computer...")
                    os.remove(itemToRemove.text(2))
                    if(os.path.isfile(itemToRemove.text(2).replace("mp3", "mp4").replace('/', "\\").replace(".mp4", ".downloadedVideoTrack"))):
                        log("[   OK   ] There's video track, removing it...")
                        os.remove(itemToRemove.text(2).replace("mp3", "mp4").replace('/', "\\").replace(".mp4", ".downloadedVideoTrack"))
                    if(os.path.isfile(itemToRemove.text(2).replace("mp3", "mp4").replace('/', "\\").replace(".mp4", ".jpg"))):
                        log("[   OK   ] There's art file, removing it...")
                        os.remove(itemToRemove.text(2).replace("mp3", "mp4").replace('/', "\\").replace(".mp4", ".jpg"))
                    log('[        ] Index of files list is {0}, deleting song in position {0}'.format(trackToRemove))
                    item = mainList.takeTopLevelItem(trackToRemove)
                    del item
                    passedTime = 0.0
                    log("[   OK   ] File removed!")
                except Exception as e:
                    throw_error("Unable to remove track!", "Unable to remove the track from the playlist.\n\nError Details: \n"+str(e))
                    if(debugging):
                        raise e
            else:
                log("[  WARN  ] User aborted deletion")
        else:
            log('[  WARN  ] No song selected to detete!')


def playFile(file: str, passedTime: int = 0) -> None:
    global playProcess, volume, blockPlay
    log(f"[        ] Startig playback thread, with file \"{file}\" and time {passedTime} s")
    try:
        killPlayProcess()
    except AttributeError:
        pass

    _volume = int(volume)
    if(muted):
        _volume=0

    if(_platform=="win32"):
        filePreset="file:///"
    else: 
        filePreset="file://"

    playProcess.stop()
    playProcess.setMedia(QtCore.QUrl(filePreset+file))
    playProcess.setPosition(int(passedTime*1000))
    playProcess.setVolume(_volume)
    log("[   OK   ] Starting audio player...")
    playProcess.play()

    if(_platform=='win32'):
        videoPath = file.replace('/', "\\").replace(".mp4", ".downloadedVideoTrack")
    else:
        videoPath = file.replace('\\', "/").replace(".mp4", ".downloadedVideoTrack")
    
    if(fileExists(videoPath)):
        videoPlayProcess.stop()
        videoPlayProcess.setMedia(QtCore.QUrl().fromLocalFile(videoPath))
        videoPlayProcess.setPosition(int(passedTime*1000))
        videoPlayProcess.setVolume(0)
        if not(settings["videoMode"] == "none"):
            log("[   OK   ] Starting video player...")
            videoPlayProcess.play()

    blockPlay = False

def plusTenSeconds() -> None:
    get_updater().call_in_main(playProcess.pause)
    get_updater().call_in_main(videoPlayProcess.pause)
    videoPlayProcess.setPosition(playProcess.position()+10000)
    playProcess.setPosition(playProcess.position()+10000)
    get_updater().call_in_main(playProcess.play)
    get_updater().call_in_main(videoPlayProcess.play)

def minusTenSeconds() -> None:
    get_updater().call_in_main(playProcess.pause)
    get_updater().call_in_main(videoPlayProcess.pause)
    videoPlayProcess.setPosition(playProcess.position()-10000)
    playProcess.setPosition(playProcess.position()-10000)
    get_updater().call_in_main(playProcess.play)
    get_updater().call_in_main(videoPlayProcess.play)


def toShuffle() -> None:
    global shuffle, buttons
    if(shuffle):
        log("[   OK   ] Shuffle disabled")
        shuffle=False
        shuffleAction.setChecked(False)
        #shuffleActionTray.setChecked(False)
        buttons['shuffle'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/shuffle-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Shuffle enabled")
        shuffle=True
        shuffleAction.setChecked(True)
        #shuffleActionTray.setChecked(True)
        buttons['shuffle'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/shuffle-icon.svg\") 0 0 0 0 stretch stretch")
        
def toReplay() -> None:
    global replay, buttons
    if(replay):
        log("[   OK   ] Replay disabled")
        replay=False
        replayAction.setChecked(False)
        #replayActionTray.setChecked(False)
        buttons['replay'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/replay-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Replay enabled")
        replay=True
        replayAction.setChecked(True)
        #replayActionTray.setChecked(True)
        buttons['replay'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/replay-icon.svg\") 0 0 0 0 stretch stretch")

def toPlay(finalized: bool = False, track: int = 0) -> None:
    global playing, buttons, t, seekerValueManuallyChanged
    if(not playing):
        log("[   OK   ] Playing")
        if(mainList.topLevelItemCount()==0):
            log('[   OK   ] Calling openFile()...')
            openFile()
        else:
            toStyleMainList()
        playing=True
        if(not(playerIsRunning)):
            t = KillableThread(target=startPlayback, args=(track,))
            t.daemon = True
            t.start()
        else:
            log("[  WARN  ] Player already running!")
        buttons['play'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/pause-icon.svg\") 0 0 0 0 stretch stretch")
        if(_platform=='win32'):
            WindowPlayButton.setIcon(QtGui.QIcon(realpath+"/icons-sptmusic/pause-bar.ico"))
    else:
        log("[        ] Sending pause signal...")
        albumArt.setPixmap(QtGui.QPixmap(realpath+"/icon.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
        playing=False
        log("[   OK   ] Pause signal sent")
        toStyleMainList()
        if(finalized):
            get_updater().call_in_main(labels['songname'].setText, "No music playing")
            get_updater().call_in_main(labels['actualtime'].setText, '-:--:--')
            seekerValueManuallyChanged = False
            refreshProgressbar(0)
        buttons['play'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/play-icon.svg\") 0 0 0 0 stretch stretch")
        if(_platform=='win32'):
            WindowPlayButton.setIcon(QtGui.QIcon(realpath+"/icons-sptmusic/play-bar.ico"))

def toSkip() -> None:
    log('[   OK   ] Setting skip signal...')
    global skipped
    skipped=True
    toStrictlyPlay()

def toGoBack() -> None:
    log('[   OK   ] Setting goBack signal...')
    global goBack
    goBack=True
    toStrictlyPlay()

def toMute() -> None:
    global volume, muted, buttons, sliders
    if(muted):
        log("[   OK   ] Unmuting...")
        playProcess.setMuted(False)
        muted=False
        #muteActionTray.setChecked(False)
        muteAction.setChecked(False)
        sliders['volume'].setObjectName("normal-slider")
        sliders['volume'].setStyleSheet(getWindowStyleSheet())
        buttons['audio'].setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/audio-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Muting...")
        playProcess.setMuted(True)
        muted=True
        #muteActionTray.setChecked(True)
        muteAction.setChecked(True)
        sliders['volume'].setObjectName("disabled-slider")
        sliders['volume'].setStyleSheet(getWindowStyleSheet())
        buttons['audio'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/audio-off-icon.svg\") 0 0 0 0 stretch stretch")
    changeVolume()

def increaseVolume() -> None:
    sliders['volume'].setValue(sliders['volume'].value()+5)

def decreaseVolume() -> None:
    sliders['volume'].setValue(sliders['volume'].value()-5)


def changeVolume() -> None:
    global volume, muted, buttons, sliders, playing, justContinue, passedTime
    volume = sliders['volume'].value()
    log('[   OK   ] Volume changed to '+str(volume))
    if(volume>100):
        volume=100
    if(playing):
        playProcess.setVolume(volume)


def toPauseAndStopSeeking() -> None:
    stopSeeking()

def openFile() -> None:
    global music, elementNumber
    try:
        log('[        ] Dialog in process')
        
        showMusic()
        try:
            os.chdir(os.path.expanduser("~"))
            os.chdir("SomePythonThings Music")
        except FileNotFoundError:
            os.mkdir("SomePythonThings Music")
            os.chdir("SomePythonThings Music")
        path = os.getcwd()
        dialog = QtWidgets.QFileDialog(music)
        dialog.setAutoFillBackground(True)
        dialog.setWindowModality(QtCore.Qt.WindowModal)
        dialog.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        dialog.setModal(True)
        dialog.setSizeGripEnabled(False)
        filepaths = dialog.getOpenFileNames(music, "SomePythonThings Music - Open media files", path, music_files)
        log('[   OK   ] Dialog Completed')
        if(filepaths[0] == []):
            log("[  WARN  ] User aborted dialog")
            return
        for filepath in filepaths[0]:
            file = open(filepath, 'r')
            filename = file.name
            file.close()
            try:
                log('[   OK   ] File "'+str(filename)+'" processed')
            except Exception as e:
                if debugging:
                    raise e
                throw_error("Error processing file!","Unable to read file \""+filename+"\"")
                try:
                    file.close()
                except:
                    pass
            newItem =  QtWidgets.QTreeWidgetItem()
            newItem.setIcon(0, QtGui.QIcon(QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(filename)).pixmap(128,128).scaledToHeight(24, QtCore.Qt.SmoothTransformation)))
            newItem.setText(0, getSongTitle(filename))
            newItem.setText(1, str(datetime.timedelta(seconds=int(getLenght(filename)))))
            newItem.setText(2, filename.replace("\\", "/"))
            newItem.setText(3, "{0:.3f} MB".format(os.path.getsize(filename)/1000000))
            newItem.setText(4, getFileType(filename).lower())
            mainList.addTopLevelItem(newItem)
            elementNumber += 1
    except Exception as e:
        if debugging:
            raise e
        throw_error("SomePythonThings Music", "An error occurred while selecting one or more files. \n\nError detsils: "+str(e))
    resultsFound = mainList.findItems('', QtCore.Qt.MatchContains, 0)
    if(len(resultsFound)==0):
        noResultsfoundLabel.show()
    else:
        noResultsfoundLabel.hide()

def addFile(filepath: str) -> None:
    global music, elementNumber
    try:
        file = open(filepath, 'r')
        filename = file.name
        file.close()
        if(filename=="SomePythonThings Music"):
            return
        if("_downloadedVideoTrack" in filename):
            return
        try:
            log('[   OK   ] File "'+str(filename)+'" processed')
            newItem =  QtWidgets.QTreeWidgetItem()
            newItem.setIcon(0, QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(filename)).pixmap(128, 128).scaledToHeight(24, QtCore.Qt.SmoothTransformation))
            newItem.setText(0, getSongTitle(filename))
            newItem.setText(1, str(datetime.timedelta(seconds=int(getLenght(filename)))))
            newItem.setText(2, filename.replace("\\", "/"))
            newItem.setText(3, "{0:.3f} MB".format(os.path.getsize(filename)/1000000))
            newItem.setText(4, getFileType(filename).lower())
            if (mainList.findItems(filename.replace("\\", "/"), QtCore.Qt.MatchFlags(QtCore.Qt.MatchCaseSensitive), 2) == []):
                mainList.addTopLevelItem(newItem)
                elementNumber += 1
            else:
                log("[  WARN  ] File already in!")
        except Exception as e:
            if debugging:
                raise e
            throw_error("Error processing file!","Unable to read file \""+filename+"\"")
            try:
                file.close()
            except:
                pass
    except Exception as e:
        if debugging:
            raise e
        throw_error("SomePythonThings Music", "An error occurred while adding one file. \n\nError detsils: "+str(e))
    resultsFound = mainList.findItems('', QtCore.Qt.MatchContains, 0)
    if(len(resultsFound)==0):
        noResultsfoundLabel.show()
    else:
        noResultsfoundLabel.hide()

def toStrictlyPlay(track: int = 0) -> None:
    startSeeking()
    global playing
    if(not(playing)):
        toPlay(track=track)

def toStrictlyPause() -> None:
    global playing, playProcess
    if(playing):
        toPlay()
        try:
            killPlayProcess()
        except AttributeError:
            pass

def saveSettings(silent: bool = True, minimize_to_tray = None, bakcgroundPicture = None, mode = None, volume = None, showTrackNotification = None, showEndNotification = None, loadLibraryAtStartup = None, repeatByDefault = None, shuffleByDefault = None, downloadQuality = None, videoMode = None, downloadVideo = None, fullScreen = None) -> bool:
    if minimize_to_tray == None:
        minimize_to_tray=settings["minimize_to_tray"]
    if bakcgroundPicture == None:
        bakcgroundPicture=settings["bakcgroundPicture"]
    if mode == None:
        mode=settings["mode"]
    if volume == None:
        volume=settings["volume"]
    if showTrackNotification == None:
        showTrackNotification=settings["showTrackNotification"]
    if showEndNotification == None:
        showEndNotification=settings["showEndNotification"]
    if loadLibraryAtStartup == None:
        loadLibraryAtStartup=settings["loadLibraryAtStartup"]
    if repeatByDefault == None:
        repeatByDefault=settings["repeatByDefault"]
    if shuffleByDefault == None:
        shuffleByDefault=settings["shuffleByDefault"]
    if downloadQuality == None:
        downloadQuality=settings["downloadQuality"]
    if videoMode == None:
        videoMode=settings["videoMode"]
    if downloadVideo == None:
        downloadVideo=settings["downloadVideo"]
    if(fullScreen == None):
        fullScreen=settings["fullScreen"]
    
    global defaultSettings
    try:
        os.chdir(os.path.expanduser('~'))
        try:
            os.chdir('.SomePythonThings')
        except FileNotFoundError:
            log("[  WARN  ] Can't acces .SomePythonThings folder, creating .SomePythonThings...")
            os.mkdir(".SomePythonThings")
            os.chdir('.SomePythonThings')
        try:
            os.chdir('Music')
        except FileNotFoundError:
            log("[  WARN  ] Can't acces Music folder, creating Music...")
            os.mkdir("Music")
            os.chdir('Music')
        try:
            settingsFile = open('settings.conf', 'w')
            settingsFile.write(str({
                "settings_version": actualVersion,
                "minimize_to_tray": minimize_to_tray,
                "volume": volume,
                "downloadVideo": downloadVideo,
                "downloadQuality": downloadQuality,
                "showTrackNotification": showTrackNotification,
                "showEndNotification": showEndNotification,
                "loadLibraryAtStartup": loadLibraryAtStartup,
                "alertOfKeyboardControl": settings['alertOfKeyboardControl'],
                "repeatByDefault": repeatByDefault,
                "shuffleByDefault": shuffleByDefault,
                "bakcgroundPicture": bakcgroundPicture,
                "mode": mode,
                "videoMode": videoMode,
                "fullScreen": fullScreen,
                }))
            settingsFile.close()
            log("[   OK   ] Settings saved successfully")
            return True
        except Exception as e:
            throw_error('SomePythonThings Music', "An error occurred while loading the settings file. \n\nError details:\n"+str(e))
            log('[        ] Creating new settings.conf')
            saveSettings()
            if(debugging):
                raise e
            return False
    except Exception as e:
        if(not(silent)):
            throw_info("SomePythonThings Music", "Unable to save settings. \n\nError details:\n"+str(e))
        log("[ FAILED ] Unable to save settings")
        if(debugging):
            raise e
        return False

def openSettings() -> dict:
    global defaultSettings
    os.chdir(os.path.expanduser('~'))
    try:
        os.chdir('.SomePythonThings')
        try:
            os.chdir('Music')
            try:
                settingsFile = open('settings.conf', 'r')
                settings = json.loads("\""+str(settingsFile.read().replace('\n', '').replace('\n\r', ''))+"\"")
                settingsFile.close()
                log('[        ] Loaded settings are: '+str(settings))
                return literal_eval(settings)
            except Exception as e:
                log('[        ] Creating new settings.conf')
                saveSettings()
                if(debugging):
                    raise e
                return defaultSettings
        except FileNotFoundError:
            log("[  WARN  ] Can't acces Music folder, creating settings...")
            saveSettings()
            return defaultSettings
    except FileNotFoundError:
        log("[  WARN  ] Can't acces .SomePythonThings folder, creating settings...")
        saveSettings()
        return defaultSettings

def openSettingsWindow() -> None:
    global music, settings, settingsWindow
    settingsWindow = ClosableWindow(music)
    settingsWindow.setMinimumSize(500, 420)
    settingsWindow.setMaximumSize(500, 420)
    settingsWindow.setWindowTitle("SomePythonThings Music Settings")
    settingsWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, debugging)
    settingsWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
    settingsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    if(_platform == 'darwin'):
        settingsWindow.setAutoFillBackground(True)
        settingsWindow.setWindowModality(QtCore.Qt.WindowModal)
        settingsWindow.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        settingsWindow.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        settingsWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    modeSelector = QtWidgets.QComboBox(settingsWindow)
    modeSelector.insertItem(0, 'Light')
    modeSelector.insertItem(1, 'Dark')
    modeSelector.insertItem(2, 'Auto')
    modeSelector.resize(230, 30)
    modeSelector.move(250, 20)
    modeSelectorLabel = QtWidgets.QLabel(settingsWindow)
    modeSelectorLabel.setText("Application mode: ")
    modeSelectorLabel.move(20, 20)
    modeSelectorLabel.setObjectName('settingsBackground')
    modeSelectorLabel.resize(230, 30)

    traySelector = QtWidgets.QComboBox(settingsWindow)
    traySelector.insertItem(0, 'Quit SomePythonThings Music')
    traySelector.insertItem(1, 'Minimize to System Tray')
    traySelector.resize(230, 30)
    traySelector.move(250, 60)
    traySelectorLabel = QtWidgets.QLabel(settingsWindow)
    traySelectorLabel.setText("✖ button action: ")
    traySelectorLabel.move(20, 60)
    traySelectorLabel.setObjectName('settingsBackground')
    traySelectorLabel.resize(230, 30)


    volumeSpinner = QtWidgets.QSpinBox(settingsWindow)
    volumeSpinner.setRange(0, 100)
    volumeSpinner.resize(230, 30)
    volumeSpinner.setSuffix("%")
    volumeSpinner.setSingleStep(5)
    volumeSpinner.move(250, 100)
    volumeSpinnerLabel = QtWidgets.QLabel(settingsWindow)
    volumeSpinnerLabel.setText("Default volume: ")
    volumeSpinnerLabel.move(20, 100)
    volumeSpinnerLabel.setObjectName('settingsBackground')
    volumeSpinnerLabel.resize(230, 30)

    trackNotifier = QtWidgets.QCheckBox(settingsWindow)
    trackNotifier.resize(460, 30)
    trackNotifier.move(20, 140)
    trackNotifier.setObjectName('settingsCheckbox')
    trackNotifier.setText("Show a notification when a new track starts")

    endNotifier = QtWidgets.QCheckBox(settingsWindow)
    endNotifier.resize(460, 30)
    endNotifier.move(20, 180)
    endNotifier.setObjectName('settingsCheckbox')
    endNotifier.setText("Show a notification when the playlist finishes")

    libraryLoader = QtWidgets.QCheckBox(settingsWindow)
    libraryLoader.resize(460, 30)
    libraryLoader.move(20, 220)
    libraryLoader.setObjectName('settingsCheckbox')
    libraryLoader.setText("Load library when the program starts")

    shuffleByDefault = QtWidgets.QCheckBox(settingsWindow)
    shuffleByDefault.resize(460, 30)
    shuffleByDefault.move(20, 260)
    shuffleByDefault.setObjectName('settingsCheckbox')
    shuffleByDefault.setText("Enable shuffle by default")

    repeatByDefault = QtWidgets.QCheckBox(settingsWindow)
    repeatByDefault.resize(460, 30)
    repeatByDefault.move(20, 300)
    repeatByDefault.setObjectName('settingsCheckbox')
    repeatByDefault.setText("Enable replay by default")

    saveButton = QtWidgets.QPushButton(settingsWindow)
    saveButton.setText("Save settings and close")
    saveButton.resize(460, 40)
    saveButton.move(20, 360)
    saveButton.setObjectName('squarePurpleButton')
    saveButton.clicked.connect(lambda: saveAndCloseSettings(modeSelector, traySelector, volumeSpinner, settingsWindow, trackNotifier, endNotifier, libraryLoader, shuffleByDefault, repeatByDefault))

    try:
        if(settings['mode'].lower() == 'light'):
            modeSelector.setCurrentIndex(0)
        elif(settings['mode'].lower() == 'dark'):
            modeSelector.setCurrentIndex(1)
        elif(settings['mode'].lower() == 'auto'):
            modeSelector.setCurrentIndex(2)
        else:
            log("[  WARN  ] Could not detect mode!")
    except KeyError:
        log("[  WARN  ] Could not detect mode!")

    try:
        if(settings['minimize_to_tray'] == False): #the "== False" is here to avoid eval of invalid values and crash of the program
            traySelector.setCurrentIndex(0)
        elif(settings['minimize_to_tray'] == True):
            traySelector.setCurrentIndex(1)
        else:
            log("[  WARN  ] Could not detect close action!")
    except KeyError:
        log("[  WARN  ] Could not detect close action!")
    
    try:
        volumeSpinner.setValue(settings["volume"])
    except KeyError:
        volumeSpinner.setValue(100)
        log("[  WARN  ] Could not detect default volume value!")

    try:
        trackNotifier.setChecked(settings["showTrackNotification"])
    except KeyError:
        log("[  WARN  ] Could not detect track notification value!")

    try:
        endNotifier.setChecked(settings["showEndNotification"])
    except KeyError:
        log("[  WARN  ] Could not detect end notification value!")

    try:
        libraryLoader.setChecked(settings["loadLibraryAtStartup"])
    except KeyError:
        log("[  WARN  ] Could not detect end notification value!")

    try:
        shuffleByDefault.setChecked(settings["shuffleByDefault"])
    except KeyError:
        log("[  WARN  ] Could not detect shuffle by default!")

    try:
        repeatByDefault.setChecked(settings["repeatByDefault"])
    except KeyError:
        log("[  WARN  ] Could not detect repeat by default!")


    settingsWindow.show()

def saveAndCloseSettings(modeSelector: QtWidgets.QComboBox, traySelector: QtWidgets.QComboBox, volumeSpinner: QtWidgets.QSpinBox, settingsWindow, trackNotifier: QtWidgets.QCheckBox, endNotifier: QtWidgets.QCheckBox,
        libraryLoader: QtWidgets.QCheckBox, shuffleByDefault: QtWidgets.QCheckBox, repeatByDefault: QtWidgets.QCheckBox) -> None:
    global settings, forceClose
    if(traySelector.currentIndex() == 1):
        settings['minimize_to_tray'] = True
    else:
        settings['minimize_to_tray'] = False
    if(modeSelector.currentIndex() == 0):
        settings['mode'] = 'light'
    elif(modeSelector.currentIndex() == 1):
        settings['mode'] = 'dark'
    else:
        settings['mode'] = 'auto'
    settings["volume"] = volumeSpinner.value()
    settings["showTrackNotification"] = trackNotifier.isChecked()
    settings["showEndNotification"] = endNotifier.isChecked()
    settings["loadLibraryAtStartup"] = libraryLoader.isChecked()
    settings["repeatByDefault"] = repeatByDefault.isChecked()
    settings["shuffleByDefault"] = shuffleByDefault.isChecked()
    settingsWindow.close()
    music.setStyleSheet(getWindowStyleSheet())
    saveSettings(silent=True, minimize_to_tray=settings['minimize_to_tray'], bakcgroundPicture=settings['bakcgroundPicture'], mode=settings['mode'], volume=settings['volume'], showTrackNotification=settings['showTrackNotification'], showEndNotification=settings['showEndNotification'],loadLibraryAtStartup=settings["loadLibraryAtStartup"], repeatByDefault=settings["repeatByDefault"], shuffleByDefault=settings["shuffleByDefault"], downloadQuality=settings['downloadQuality'])

def getLenght(file: str) -> int:
    global debugging
    try:
        return mutagen.File(filename=file).info.length
    except AttributeError:
        log(f"[ FAILED ] Unable to get file {file} length!")
        return 0


def openOnExplorer(file: str, force: bool = True) -> None:
    if    (_platform == 'win32'):
        try:
            os.system('start explorer /select,"{0}"'.format(file.replace("/", "\\")))
        except:
            log("[  WARN  ] Unable to show file {0} on file explorer.".format(file))
    elif (_platform == 'darwin'):
        if(force):
            try:
                os.system('open "'+file+'"')
            except:
                log("[  WARN  ] Unable to show file {0} on finder.".format(file))
        else:
            try:
                os.system("open "+("/".join(str(file).split("/")[:-1])))
            except:
                log("[  WARN  ] Unable to show file {0} on finder.".format(file))

    elif (_platform == 'linux' or _platform == 'linux2'):
        try:
            t = Thread(target=os.system, args=("xdg-open "+file,))
            t.daemon=True
            t.start()
        except:
            log("[  WARN  ] Unable to show file {0} on default file explorer.".format(file))

def openLog() -> None:
    log("[        ] Opening log...")
    openOnExplorer(tempDir.name.replace('\\', '/')+'/log.txt', force=True)    

def getFileType(file: str) -> str: #from file.mp3, returns MP3, from file.FiLeExT, returns FILEEXT 
    return file.split('.')[-1].upper()

def fileExists(file: str) -> bool:
    try:
        open(file, "r").close()
        return True
    except:
        return False

def getSongTitle(file: str) -> str: # beautify
    name = str(file.replace('\\', '/').split('/')[-1]).replace("."+file.split('.')[-1], '')
    try:
        for item in ['lyrics', 'lyric', 'official', 'vevo', 'videoclip', 'letra', 'lletra', 'explicit', 'audiolyric', "videolyric", "oficial", 'official', 'music', "video", "audio", 'explicit', "HD", "4k", "/", "\\", "()", "[]", "{}", "( )", "[ ]", "{ }", "(  )", "[  ]", "{  }", "(   )", "[   ]", "{   }", "(    )", "[    ]", "{    }"]:
            toReplace = re.compile(re.escape(item), re.IGNORECASE)
            if item != "4k" or not('24' in name):
                name = toReplace.sub('', name)
        toReplace = re.compile(re.escape("by"), re.IGNORECASE)
        name = toReplace.sub('-', name)
        for _ in range(10):
            name.replace('  ', ' ')
        name = name.split(' ')
        for i in range(len(name)):
            name[i] = name[i].capitalize()
        name = ' '.join(name)
        name.replace('[ ]', '')
        name.replace('( )', '')
        name.replace('{ }', '')
        log("[   OK   ] Song name beautified")
    except Exception as e:
        log("[  WARN  ] An error occurred while beautifying")
        if(debugging):
            raise e
    return name.replace("U0026", "&")

def startPlayback(track: int or str = 0) -> None:
    global labels, skipped, playerIsRunning, externalVideoTrack, song_length, fileBeingPlayed, trackSeeked, playProcess, goBack, playing, trackNumber, replay, blockPlay, playingObj, justContinue, totalTime, passedTime, seeking, seekerValueManuallyChanged, starttime
    playerIsRunning = True
    stopped=False
    skipped=False
    lastTrack=""
    goBack = False
    toContinue = True
    passedTime = 0.0
    alreadyPlayed = []
    if(isinstance(track, int)):
        trackNumber=track
    else:
        trackNumber=0
    del track
    try:
        if(mainList.topLevelItemCount() == 0):
            playerIsRunning = False
            replay = False
            toStrictlyPause()
            try:        
                killPlayProcess()
            except AttributeError:
                pass
            sys.exit()
        while trackNumber<mainList.topLevelItemCount() and toContinue:
            log('[        ] Starting new play round, index is {0}'.format(str(trackNumber)))
            if not stopped:
                import time
                track = mainList.topLevelItem(trackNumber).text(2)
                log('[        ] Track number {0}'.format(trackNumber))
                log('[        ] Actual track file is '+str(track))
                log('[        ] Start time is {0} ms'.format(passedTime*1000))
                song_length = getLenght(track)
                filename = getSongTitle(track)
                fileBeingPlayed = track
                log('[        ] Actual track lenght is '+str(song_length))
                get_updater().call_in_main(labels['totaltime'].setText, str(datetime.timedelta(seconds=int(song_length))))
                get_updater().call_latest(labels['songname'].setText, filename)

                try:
                    showNofitication = settings["showTrackNotification"]
                except KeyError:
                    showNofitication = True
                if(showNofitication):
                    if(lastTrack != track):
                        lastTrack=track
                        log("[   OK   ] Shwowing notification...")
                        get_updater().call_in_main(notify, "SomePythonThings Music", getSongTitle(track))
                        time.sleep(0.5)
                if(os.path.isfile(track.replace('mp4', 'jpg').replace('mp3', 'jpg'))):
                    albumArt.setPixmap(QtGui.QPixmap(track.replace('mp4', 'jpg').replace('mp3', 'jpg')).scaledToWidth(96, QtCore.Qt.SmoothTransformation))
                elif(os.path.isfile(track.replace('mp3', 'jpg'))):
                    albumArt.setPixmap(QtGui.QPixmap(track.replace('mp3', 'jpg')).scaledToWidth(96, QtCore.Qt.SmoothTransformation))
                else:
                    albumArt.setPixmap(QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(track)).pixmap(128, 128).scaledToHeight(96, QtCore.Qt.SmoothTransformation))
                
                log("[        ] Calling play thread...")
                blockPlay = True
                get_updater().call_in_main(playFile, track, passedTime=passedTime)
                externalVideoTrack = False
                while blockPlay:
                    time.sleep(0.01)

                if(_platform=='win32'):
                    videoPath = track.replace("mp3", "mp4").replace('/', "\\").replace(".mp4", ".downloadedVideoTrack")
                else:
                    videoPath = track.replace("mp3", "mp4").replace('\\', "/").replace(".mp4", ".downloadedVideoTrack")
                
                if(playProcess.isVideoAvailable()):
                    log("[   OK   ] Video available, showing video...")
                    get_updater().call_in_main(videoPlayer.show)
                elif(fileExists(videoPath)):
                    externalVideoTrack=True
                    log("[   OK   ] Video available in external track, showing video...")
                    get_updater().call_in_main(externalVideoPlayer.show)
                else:
                    log("[   OK   ] Video not available, not showing video...")
                    get_updater().call_in_main(videoPlayer.hide)
                log("[   OK   ] Continuing play process, play line passed")

                alreadyPlayed.append(trackNumber)
                get_updater().call_in_main(buttons['play'].setStyleSheet, "background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/pause-icon.svg\") 0 0 0 0 stretch stretch")
                if(_platform=='win32'):
                    WindowPlayButton.setIcon(QtGui.QIcon(realpath+"/icons-sptmusic/pause-bar.ico"))
                get_updater().call_in_main(toStyleMainList)

                while song_length == 0:
                    time.sleep(0.01)

                msPlayed = 0
                lenght = song_length
                percentagePlayed = 0
                trackSeeked = 1

                videoChecked = False
                noNeedToContinue = False

                lastSeeked = int(time.time())

                userWarned = False

                needToAlignCounter = 0


                while(True):
                    msPlayed = playProcess.position()//trackSeeked
                    lenght = song_length*1000
                    if(msPlayed!=0):
                        if(not(videoChecked)):
                            if(playProcess.isVideoAvailable()):
                                log("[   OK   ] Video available, showing video...")
                                get_updater().call_in_main(videoPlayer.show)
                            else:
                                log("[   OK   ] Video not available, not showing video...")
                                get_updater().call_in_main(videoPlayer.hide)
                            if(externalVideoTrack):
                                log("[   OK   ] Video available, showing video...")
                                get_updater().call_in_main(externalVideoPlayer.show)
                            else:
                                log("[   OK   ] Video not available, not showing video...")
                                get_updater().call_in_main(externalVideoPlayer.hide)
                            videoChecked = True
                        percentagePlayed = msPlayed/lenght*100
                        #log(f"[   Ok   ] Played {percentagePlayed}%")
                    loopStartTime = time.time()
                    if(lastSeeked < int(time.time())): # check every one second
                        if(externalVideoTrack):
                            if(settings["videoMode"] != "none"):
                                if(needToAlignCounter >= 2):
                                    log("[  WARN  ] Video and audio aligner did not work for two times in a row, pausing and restarting...")
                                    get_updater().call_in_main(playProcess.pause)
                                    get_updater().call_in_main(videoPlayProcess.pause)
                                    videoPlayProcess.setPosition(playProcess.position())
                                    time.sleep(0.3)
                                    get_updater().call_in_main(playProcess.play)
                                    get_updater().call_in_main(videoPlayProcess.play)
                                if(videoPlayProcess.position()//500 < playProcess.position()//500):
                                    needToAlignCounter += 1
                                    log(f"[  WARN  ] Video track position: {videoPlayProcess.position()//500}")
                                    log(f"[  WARN  ] Audio track position: {playProcess.position()//500}. Fixing that...")
                                    get_updater().call_in_main(playProcess.pause)
                                    get_updater().call_in_main(videoPlayProcess.pause)
                                    videoPlayProcess.setPosition(playProcess.position())
                                    time.sleep(0.1)
                                    get_updater().call_in_main(playProcess.play)
                                    get_updater().call_in_main(videoPlayProcess.play)
                                    #get_updater().call_in_main(videoPlayProcess.setPosition, playProcess.position())
                                else:
                                    needToAlignCounter = 0
                        lastSeeked = int(time.time())
                    
                    try:
                        get_updater().call_in_main(labels['actualtime'].setText, str(datetime.timedelta(seconds=int(msPlayed/1000))))
                    except ZeroDivisionError:
                        pass

                    if(seeking):
                        seekerValueManuallyChanged = False
                        refreshProgressbar(percentagePlayed*10)

                    if(playProcess.error() == playProcess.Error.ResourceError or videoPlayProcess.error() == videoPlayProcess.Error.ResourceError):
                        if not(userWarned):
                            log("[ FAILED ] Unable to play file!")
                            get_updater().call_in_main(throw_error, "Playback codecs error", "SomePythonThings Music failed to play the actual file due an issue with the codecs. Restarting the application may fix that\n\nIf the error persists, try reinstalling SomePythonThings Music\n\nIf you are running windows, you can also try reinstalling LavFilters or any other video codec pack.")
                            get_updater().call_in_main(toStrictlyPause)
                        userWarned=True


                    if(not(playing)):
                        log("[   OK   ] Pause signal recieved, pausing...")
                        if(_platform=='darwin'):
                            get_updater().call_in_main(playProcess.pause)
                        else:
                            playProcess.pause()
                        get_updater().call_in_main(videoPlayer.hide)
                        get_updater().call_in_main(externalVideoPlayer.hide)
                        if(externalVideoTrack):
                            get_updater().call_in_main(videoPlayProcess.pause)
                        get_updater().call_in_main(toStyleMainList)
                        log('[   OK   ] Paused at moment {}'.format((time.time()-starttime)))
                        while not(playing):
                            time.sleep(0.01)# if "pass" statement here, cpu would run at full speed until play button was triggered.
                        if(os.path.isfile(track.replace('mp4', 'jpg').replace('mp3', 'jpg'))):
                            albumArt.setPixmap(QtGui.QPixmap(track.replace('mp4', 'jpg').replace('mp3', 'jpg')).scaledToWidth(96, QtCore.Qt.SmoothTransformation))
                        elif(os.path.isfile(track.replace('mp3', 'jpg'))):
                            albumArt.setPixmap(QtGui.QPixmap(track.replace('mp3', 'jpg')).scaledToWidth(96, QtCore.Qt.SmoothTransformation))
                        else:
                            albumArt.setPixmap(QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(track)).pixmap(128, 128).scaledToHeight(96, QtCore.Qt.SmoothTransformation))
                        log('[        ] Continuing playback...')
                        get_updater().call_in_main(playProcess.play)
                        if(externalVideoTrack):
                            get_updater().call_in_main(videoPlayProcess.play)
                        
                        if(playProcess.isVideoAvailable()):
                            get_updater().call_in_main(videoPlayer.show)
                        elif(externalVideoTrack):
                            get_updater().call_in_main(externalVideoPlayer.show)

                        
                        videoPlayProcess.setPosition(playProcess.position())

                    if(skipped):
                        log('[        ] Skipping...')
                        get_updater().call_in_main(videoPlayer.hide)
                        noNeedToContinue = True
                        killPlayProcess()
                        break

                    if(goBack):
                        log('[        ] Going back...')
                        killPlayProcess()
                        noNeedToContinue = True
                        get_updater().call_in_main(videoPlayer.hide)
                        break

                    if(justContinue):
                        killPlayProcess()
                        noNeedToContinue = True
                        get_updater().call_in_main(videoPlayer.hide)
                        log('[        ] Passing away...')
                        break

                    if(playProcess.state() == QtMultimedia.QMediaPlayer.StoppedState and percentagePlayed>5):
                        get_updater().call_in_main(videoPlayer.hide)
                        log('[  KILL  ] Killing play bucle, arrived to end...')
                        if(noNeedToContinue):
                            toContinue = False
                        break

                    toWait = 0.05 - (time.time()-loopStartTime)
                    if(toWait>0):
                        time.sleep(toWait)

                if(skipped):
                    log('[   OK   ] Skipped')
                    if not(shuffle):
                        trackNumber += 1
                    else:
                        oldTrackNumber = trackNumber
                        trackNumber = random.randint(0, mainList.topLevelItemCount())
                        if(len(alreadyPlayed) >= mainList.topLevelItemCount()):
                            toStrictlyPause()
                            alreadyPlayed = []
                        else:
                            while ((oldTrackNumber==trackNumber and mainList.topLevelItemCount()>1) or trackNumber in alreadyPlayed) and not replay:
                                trackNumber = random.randint(0, mainList.topLevelItemCount())
                    passedTime = 0.0
                    skipped=False
                    continue
                if(goBack):
                    log('[   OK   ] Went back, actual position is '+str(msPlayed))
                    if(msPlayed>3000):
                        pass# Stay on the same track
                    else:
                        trackNumber -= 1
                    if(trackNumber<=0):
                        trackNumber=0
                    passedTime = 0.0
                    goBack=False
                    continue
                if(justContinue):
                    log('[   OK   ] Passed away.')
                    justContinue = False
                    continue
                if not(stopped):
                    seekerValueManuallyChanged = False
                    refreshProgressbar(1000)
                    if not(shuffle):
                        trackNumber += 1
                    else:
                        oldTrackNumber = trackNumber
                        trackNumber = random.randint(0, mainList.topLevelItemCount())
                        if(len(alreadyPlayed) >= mainList.topLevelItemCount()):
                            toStrictlyPause()
                            alreadyPlayed = []
                        else:
                            while ((oldTrackNumber==trackNumber and mainList.topLevelItemCount()>1) or trackNumber in alreadyPlayed) and not replay:
                                trackNumber = random.randint(0, mainList.topLevelItemCount())
                    passedTime = 0.0
            else:
                log('[        ] Playback is stopped, blocking...')
                stopped = False
                while not(playing):
                    continue              
        if not stopped:
            if replay:
                startPlayback()
            else:
                try:
                    showNofitication = settings["showEndNotification"]
                except KeyError:
                    showNofitication = True
                if(showNofitication):
                        log("[   OK   ] Shwowing notification...")
                        get_updater().call_in_main(notify, "SomePythonThings Music", "Playlist has finished!")
                get_updater().call_in_main(toPlay, True)
        playerIsRunning = False
    except Exception as e:
        try:        
            killPlayProcess()
        except AttributeError:
            pass
        playerIsRunning = False
        playing = True
        get_updater().call_in_main(toPlay, True)
        get_updater().call_in_main(throw_error, "SomePythonThings Music", "An error occurred during the playback.\n\nIs the file corrupt or incompatible?\n\nError Details: \n"+str(e))
        if(debugging):
            raise e

def goToSong() -> None:
    global lists, trackNumber, playing, t, playerIsRunning, justContinue, searchBar
    try:
        t.shouldBeRuning = False
        log('[  KILL  ] Killing playback thread to start a new one...')
    except AttributeError:
        log('[  WARN  ] Unable to kill thread, thread was not running...')
    searchBar.setText('')
    trackNumber = mainList.indexOfTopLevelItem(mainList.currentItem())
    if(trackNumber<0):
        trackNumber = 0
    log('[   OK   ] Selected track number {}'.format(trackNumber))
    playerIsRunning = False
    playing = False
    toStrictlyPlay(track=trackNumber)

def goToSpecificTime() -> None:
    global trackSeeked
    timeToGo = seeker.value()*(song_length*1000)/1000
    log('[        ] Starting goToSpecificTime with time value (in ms): '+str(timeToGo)+', currentTimeDelay = '+str(currentTimeDelay))
    playProcess.setPosition(int(timeToGo*trackSeeked))
    time.sleep(0.1)
    if(externalVideoTrack):
        videoPlayProcess.setPosition(playProcess.position())
    startSeeking()

def stopSeeking() -> None:
    log('[        ] Stopping seeking...')
    global seeking
    seeking=False

def startSeeking() -> None:
    global seeking
    log('[        ] Starting seeking...')
    time.sleep(0.1)
    seeking=True

def getList() -> any:
    for i in range(mainList.topLevelItemCount()):
        item = mainList.topLevelItem(i)
        yield item.text(2)

def savePlaylist() -> None:
    global music
    toStrictlyPause()
    try:
        log('[        ] Asking where to save the playlist...')
        showMusic()
        filename = QtWidgets.QFileDialog.getSaveFileName(music, "Save the playlist as...", 'Unnamed Playlist.sptplaylist', ('SomePythonThings Playlist File (*.sptplaylist)'))[0]
        log('[   OK   ] Got string "{0}" from getSaveFileName()'.format(str(filename)))
        if(filename==''):
            log('[  WARN  ] User aborted dialog!')
        else:
            file = open(filename, 'w')
            try:
                toWrite="""This is a SomePythonThings Music Playlist. This file, after the 3 "#", has, by order, all the files contained on the playlist.Please be careful when editing this file from a text editor, you could just corrupt the file.###\n"""
                for element in getList():
                    try:
                        toWrite += str(element)
                        toWrite += "\n"
                    except Exception as e:
                        throw_warning('SomePythonThings Music', f'Unable add {element} to playlist.\n\nError details:\n'+str(e))
                toWrite += "###"
                file.write(toWrite)
                file.close()
                throw_info('SomePythonThings Music', 'Playlist saved successfully!')
            except Exception as e:
                file.close()
                log('[ FAILED ] An error occurred while writing data to the file...')
                raise e
    except Exception as e:
        if(debugging):
            raise e
        throw_error('SomePythonThings Music', 'Unable to save playlist.\n\nError details:\n'+str(e))

def removeAllItems() -> None:
    global lists
    while mainList.topLevelItemCount()>0:
        try:
            mainList.clear()
            
            resultsFound = mainList.findItems('', QtCore.Qt.MatchContains, 0)
            if(len(resultsFound)==0):
                noResultsfoundLabel.show()
            else:
                noResultsfoundLabel.hide()
        except Exception as e:
            if(debugging):
                raise e

def showMusic(reason: QtWidgets.QSystemTrayIcon.ActivationReason = QtWidgets.QSystemTrayIcon.Unknown) -> None:
    if(reason != QtWidgets.QSystemTrayIcon.Context):
        music.show()
        music.raise_()
        music.activateWindow()
        if not(music.isMaximized()):
            music.showNormal()

def openPlaylist(playlist: str = '') -> None:
    global music, elementNumber
    log('[        ] Playlist attribute value is {0}'.format(playlist))
    playAfter = False
    try:
        if(playlist == '' or playlist == False):
            log('[        ] Dialog in process')
            
            showMusic()
            filepath = QtWidgets.QFileDialog.getOpenFileName(music, "Select a SomePythonThings Playlist file...", '', ('SomePythonThings Playlist file (*.sptplaylist)'))[0]
            log('[   OK   ] Dialog Completed')
            if(filepath == ''):
                log("[  WARN  ] User aborted dialog")
                return
        else:
            filepath = playlist
            playAfter = True
        file = open(filepath, 'r')
        content = file.read()
        filename = file.name
        file.close()
        try:
            if(len(content.split("###"))<2):
                raise FileExistsError('This platlist file is not a valid .sptplaylist file!')
            else:
                toStrictlyPause()
                removeAllItems()
            for songFile in content.split("###")[1].split('\n'):
                if(songFile!=''):
                    addFile(songFile)
                log('[   OK   ] File "'+str(songFile)+'" processed')
            log('[   OK   ] Playlist imported successfully')
            if not(playAfter):
                throw_info('SomePythonThings Music', 'Playlist imported successfuly')
            else:
                toStrictlyPlay()
        except Exception as e:
            throw_error("Error processing file!","Unable to read file \""+filename+"\"")
            if debugging:
                raise e
            try:
                file.close()
            except:
                pass
    except Exception as e:
        throw_error("SomePythonThings Music", "An error occurred while selecting a playlist file. \n\nError detsils: "+str(e))
        if debugging:
            raise e
            
    resultsFound = mainList.findItems('', QtCore.Qt.MatchContains, 0)
    if(len(resultsFound)==0):
        noResultsfoundLabel.show()
    else:
        noResultsfoundLabel.hide()

def refreshProgressbar(value: int) -> None:
    global progressbars, texts, music
    if(_platform=='win32'):
        global taskbprogress
        get_updater().call_in_main(taskbprogress.setRange, 0, 1000)
        get_updater().call_in_main(taskbprogress.setValue, int(value))
        if(value==0):
            get_updater().call_in_main(taskbprogress.hide)
        else:
            get_updater().call_in_main(taskbprogress.show)
    get_updater().call_in_main(bottomBar.setValue, value)
    get_updater().call_in_main(bottomBar.repaint)
    get_updater().call_in_main(seeker.setValue, value)

def installationProgressBar(action: str = 'Downloading') -> None:
    global progressbars, texts, music
    if(_platform=="win32"):
        global taskbprogress
    if(action=="Stop"):
        if(_platform=='win32'):
            get_updater().call_in_main(taskbprogress.hide)
            get_updater().call_in_main(bottomBar.setValue, 0)
        get_updater().call_in_main(bottomBar.setRange, 0, 1000)
    else:
        if(_platform=='win32'):
            get_updater().call_in_main(taskbprogress.setRange, 0, 0)
            get_updater().call_in_main(taskbprogress.setValue, 0)
            get_updater().call_in_main(taskbprogress.show)
        get_updater().call_in_main(bottomBar.setRange, 0, 0)

def throw_info(title: str, body: str, icon: str = "ok.png", exit: bool = False) -> None:
    global music
    showMusic()
    log("[  INFO  ] "+body)
    msg = QtWidgets.QMessageBox(music)
    if(os.path.exists(str(realpath)+"/icons-sptmusic/ok.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/icons-sptmusic/ok.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(body)
    if(_platform == 'darwin'):
        msg.setAutoFillBackground(True)
        msg.setWindowModality(QtCore.Qt.WindowModal)
        msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        msg.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        msg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        msg.setModal(True)
        msg.setSizeGripEnabled(False)
    msg.setWindowTitle(title)
    msg.exec_()
    if(exit):
        try:        
            killPlayProcess()
        except AttributeError:
            pass
        sys.exit()

def throw_warning(title: str, body: str) -> None:
    global music
    showMusic()
    log("[  WARN  ] "+body)
    msg = QtWidgets.QMessageBox(music)
    if(os.path.exists(str(realpath)+"/icons-sptmusic/warn.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/icons-sptmusic/warn.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Warning)
    
    if(_platform == 'darwin'):
        msg.setAutoFillBackground(True)
        msg.setWindowModality(QtCore.Qt.WindowModal)
        msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        msg.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        msg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        msg.setModal(True)
        msg.setSizeGripEnabled(False)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()

def throw_error(title: str, body: str) -> None:
    global music
    showMusic()
    log("[  ERROR ] "+body+"\n\tError reason: "+body)
    msg = QtWidgets.QMessageBox(music)
    if(os.path.exists(str(realpath)+"/icons-sptmusic/error.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/icons-sptmusic/error.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Critical)
    
    if(_platform == 'darwin'):
        msg.setAutoFillBackground(True)
        msg.setWindowModality(QtCore.Qt.WindowModal)
        msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        msg.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        msg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        msg.setModal(True)
        msg.setSizeGripEnabled(False)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()


def confirm(parent: QtWidgets.QMainWindow, title: str, body: str, firstButton: QtWidgets.QAbstractButton, secondButton: QtWidgets.QAbstractButton, defaultButton: QtWidgets.QAbstractButton) -> QtWidgets.QAbstractButton:
    msg = QtWidgets.QMessageBox(parent)
    log("[  WARN  ] "+body)
    if(os.path.exists(str(realpath)+"/icons-sptmusic/ok.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/icons-sptmusic/ok.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Warning)
    
    if(_platform == 'darwin'):
        msg.setAutoFillBackground(True)
        msg.setWindowModality(QtCore.Qt.WindowModal)
        msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        msg.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        msg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        msg.setModal(True)
        msg.setSizeGripEnabled(False)
    msg.setWindowTitle(title)
    msg.setText(body)
    msg.addButton(firstButton)
    msg.addButton(secondButton)
    msg.setDefaultButton(defaultButton)
    msg.exec_()
    return msg.standardButton(msg.clickedButton())

def warnAndConfirm(parent: QtWidgets.QMainWindow, title: str, body: str, firstButton: QtWidgets.QAbstractButton, secondButton: QtWidgets.QAbstractButton, defaultButton: QtWidgets.QAbstractButton) -> QtWidgets.QAbstractButton:
    msg = QtWidgets.QMessageBox(parent)
    log("[  WARN  ] "+body)
    if(os.path.exists(str(realpath)+"/icons-sptmusic/warn.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/icons-sptmusic/warn.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Warning)
    
    if(_platform == 'darwin'):
        msg.setAutoFillBackground(True)
        msg.setWindowModality(QtCore.Qt.WindowModal)
        msg.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        msg.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        msg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        msg.setModal(True)
        msg.setSizeGripEnabled(False)
    msg.setWindowTitle(title)
    msg.setText(body)
    msg.addButton(firstButton)
    msg.addButton(secondButton)
    msg.setDefaultButton(defaultButton)
    msg.exec_()
    print()
    return msg.standardButton(msg.clickedButton())




def updates_thread() -> None:
    log("[        ] Starting check for updates thread...")
    checkUpdates_py()
 
def quitMusic() -> None:
    log("[  INFO  ] Quitting application...")
    global music, forceClose
    forceClose = True
    music.close()
    try:        
        killPlayProcess()
    except AttributeError:
        pass
    sys.exit(0)

def checkDirectUpdates() -> None:
    global actualVersion
    result = checkUpdates_py()
    if(result=='No'):
        throw_info("SomePythonThings Music Updater", "There aren't updates available at this time. \n(The installed version is {0})".format(actualVersion))
    elif(result=="Unable"):
        throw_warning("SomePythonThings Music Updater", "Can't reach SomePythonThings Servers!\n  - Are you connected to the internet?\n  - Is your antivirus or firewall blocking SomePythonThings Music?\nIf none of these solved the problem, please check back later.")

def openHelp() -> None:
    webbrowser.open_new("http://www.somepythonthings.tk/programs/somepythonthings-music/help/")

def about() -> None:
    throw_info("About SomePythonThings Music", "SomePythonThings Music\nVersion "+str(actualVersion)+"\n\nThe SomePythonThings Project\n\n © 2021 Martí Climent, SomePythonThings\nhttps://www.somepythonthings.tk\n\n\nThe iconset has a CC Non-Commercial Atribution 4.0 License", exit=False)

def readArgs(args: list) -> None:
    global t, playerIsRunning
    log('[  ARGS  ] Re-reading args...')
    isThereAFile = False
    i = 0
    if(len(args)>1):
        removeAllItems()
        toStrictlyPause()
        try:
            t.kill()
        except AttributeError:
            pass
        if('SPTPLAYLIST' == getFileType(args[1])):
            openPlaylist(args[1])
            isThereAFile = True
            log('[   OK   ] 1st argument appears to be a playlist...')
        else:
            while i<len(args):
                log('[        ] Detected arguments, checking if they are valid...')
                arg = args[i]
                if(os.path.isfile(arg) and not (getFileType(arg) in 'PYEXELNK')):
                    addFile(arg)
                    isThereAFile = True
                    log('[   OK   ] Argument {0} added successfully'.format(arg))
                else:
                    log('[  WARN  ] Argument {0} is not a valid file!'.format(arg))
                i += 1
    if(isThereAFile):
        playerIsRunning = False
        toStrictlyPlay()

def setProgramAsRunning() -> None:
    global defaultSettings, goRun, canRun
    try:
        os.remove(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/show.lock')
    except PermissionError:
        pass
    except FileNotFoundError:
        pass
    try:
        if(os.path.exists(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/running.lock')):
            try:
                os.remove(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/running.lock')
            except PermissionError:
                pass
            time.sleep(0.5)
            if(os.path.exists(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/running.lock')):
                with open(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/show.lock', mode='a'): pass
                args=""
                for element in sys.argv:
                    args += element+'///'
                args=args[:-3]
                try:
                    f = open('sys.argv', 'w')
                    f.write(args)
                    f.close()
                except Exception as e:
                    if(debugging):
                        raise e
                log('[  WARN  ] SomePythonThings Music Already running!')
                goRun=True
                canRun=False
                return
            else:
                goRun=True
                canRun=True
                log('[   OK   ] SomePythonThings Music not running.')
        else:
            goRun=True
            canRun=True
            log('[   OK   ] SomePythonThings Music not running.')
    except PermissionError:
        pass
    except:
        setProgramAsRunning()
    if(canRun):
        while True:
            try:
                os.chdir(os.path.expanduser('~'))
                try:
                    os.chdir('.SomePythonThings')
                except FileNotFoundError:
                    log("[  WARN  ] Can't acces .SomePythonThings folder, creating .SomePythonThings...")
                    os.mkdir(".SomePythonThings")
                    os.chdir('.SomePythonThings')
                try:
                    os.chdir('Music')
                except FileNotFoundError:
                    log("[  WARN  ] Can't acces Music folder, creating Music...")
                    os.mkdir("Music")
                    os.chdir('Music')
                try:
                    if(not(os.path.exists(os.path.expanduser('~')+'/.SomePythonThings/Music/running.lock'))):
                        with open(os.path.expanduser('~')+'/.SomePythonThings/Music/running.lock', mode='a'): pass
                    if(os.path.exists(os.path.expanduser('~')+'/.SomePythonThings/Music/show.lock')):
                        log('[        ] Showing SomePythonThimgs Music...')
                        try:
                            get_updater().call_in_main(music.show)
                            get_updater().call_in_main(music.raise_)
                            get_updater().call_in_main(music.activateWindow)
                            get_updater().call_in_main(music.showNormal)
                            os.remove(os.path.expanduser('~')+'/.SomePythonThings/Music/show.lock')
                            time.sleep(0.1)
                            log('[        ] Searching for passed args...')
                            try:
                                f = open('sys.argv', 'r')
                                args = f.read().split('///')
                                f.close()
                                log('[        ] found args are "{}"...'.format(str(args)))
                                get_updater().call_in_main(readArgs, args)
                                os.remove('sys.argv')
                            except Exception as e:
                                if(debugging):
                                    raise e
                            break
                        except:
                            try:
                                os.remove(os.path.expanduser('~')+'/.SomePythonThings/Music/show.lock')
                            except PermissionError:
                                pass
                except Exception as e:
                    if(debugging):
                        raise e
            except Exception as e:
                if(debugging):
                    raise e
            time.sleep(0.3)
        setProgramAsRunning()

def on_key(key: QtCore.Qt.Key) -> None:
    global volume, sliders
    if not(searchBar.hasFocus()):
        log('[   OK   ] key pressed: %s' % QtCore.Qt.Key(key))
        if key == QtCore.Qt.Key_Minus:
            sliders['volume'].setValue(sliders['volume'].value()-10)
        elif key == QtCore.Qt.Key_Plus:
            sliders['volume'].setValue(sliders['volume'].value()+10)
        elif key == QtCore.Qt.Key_Right:
            plusTenSeconds()
        elif key == QtCore.Qt.Key_Left:
            minusTenSeconds()
        elif key == QtCore.Qt.Key_Delete:
            removeFromPlaylist()
        elif key == QtCore.Qt.Key_Enter:
            goToSong()
        elif key == QtCore.Qt.Key_Space:
            toPlay()
        elif(_platform != 'win32'):
            if key == QtCore.Qt.Key_Play:
                toStrictlyPlay()
                showMediaWindow()
            elif key == QtCore.Qt.Key_Pause:
                toStrictlyPause()
                showMediaWindow()
            elif key == QtCore.Qt.Key_MediaPlay:
                toPlay()
                showMediaWindow()
            elif key == QtCore.Qt.Key_MediaPause:
                toPlay()
                showMediaWindow(skip=True)
            elif key == QtCore.Qt.Key_MediaPrevious:
                toGoBack()
                showMediaWindow()
            elif key == QtCore.Qt.Key_MediaNext:
                toSkip()
                showMediaWindow()
    else:
        log("[  WARN  ] Ingoring key event, search box has focus...")

def mediaKeyPress(key: pynput.keyboard.Key) -> None:
    if key == pynput.keyboard.Key.media_play_pause:
        log(f"[   OK   ] Pynput key press detected, key is \"{key}\"")
        get_updater().call_in_main(toPlay)
        get_updater().call_latest(showMediaWindow)
        if(_platform=='darwin'):
            killallmusicinstances()
    elif key == pynput.keyboard.Key.media_previous:
        log(f"[   OK   ] Pynput key press detected, key is \"{key}\"")
        get_updater().call_in_main(toGoBack)
        get_updater().call_latest(showMediaWindow, skip=True)
        if(_platform=='darwin'):
            killallmusicinstances()
    elif key == pynput.keyboard.Key.media_next:
        log(f"[   OK   ] Pynput key press detected, key is \"{key}\"")
        get_updater().call_in_main(toSkip)
        get_updater().call_latest(showMediaWindow, skip=True)
        if(_platform=='darwin'):
            killallmusicinstances()


def killallmusicinstances() -> None:
    log("[        ] Killing Music.app instances...")
    for _ in range(10):
        os.system('killall Music')
        time.sleep(0.1)

def changeVideoMode() -> None:
    mainList.setFocus()
    global settings, screenModeChanged, videoModeChanged
    if(settings["videoMode"] == "small"):
        buttons["videoMode"].setText("No video")
        if(externalVideoTrack):
            log("[   OK   ] Pausing video...")
            videoPlayProcess.pause()
        settings["videoMode"] = "none"
    elif(settings["videoMode"] == "none"):
        if(externalVideoTrack):
            videoPlayProcess.setPosition(playProcess.position())
            videoPlayProcess.play()
        buttons["videoMode"].setText("Video mode: Big")
        settings["videoMode"] = "big"
    elif(settings["videoMode"] == "big"):
        buttons["videoMode"].setText("Video mode: Normal")
        settings["videoMode"] = "normal"
    else:
        buttons["videoMode"].setText("Video mode: Small")
        settings["videoMode"] = "small"
    videoModeChanged = True
    log("[   OK   ] Video mode set to "+settings["videoMode"])
    saveSettings()
    resizeWidgets()

def changeScreenMode() -> None:
    global settings, screenModeChanged
    if(settings["fullScreen"] == True):
        buttons["fullScreen"].setText("Full Screen")
        settings["fullScreen"] = False
    else:
        buttons["fullScreen"].setText("Restore")
        settings["fullScreen"] = True

    log("[   OK   ] Screen mode set to "+str(settings["fullScreen"]))
    saveSettings()
    screenModeChanged = True
    resizeWidgets()

def resizeWidgets() -> None:
    global music, buttons, texts, progressbars, font, screenModeChanged, videoModeChanged
    height = music.height()
    width = music.width()
    
    if(videoModeChanged or screenModeChanged):
        if(settings["fullScreen"] == True and settings["videoMode"] == "big"):
            menuBar.hide()
        else:
            menuBar.show()
        videoModeChanged=False

    if(screenModeChanged):
        if(settings["fullScreen"] == True):
            music.showFullScreen()
            height = music.height()
            width = music.width()
        else:
            music.showNormal()
            height = music.height()
            width = music.width()
        screenModeChanged = False
        

    if(settings["videoMode"] == "big"):
        externalVideoPlayer.resize(width, height-120)
        externalVideoPlayer.move(0, 0)
        videoPlayer.resize(width, height-120)
        videoPlayer.move(0, 0)
    elif(settings["videoMode"] == "normal"):
        width = music.width()
        externalVideoPlayer.move(173, 83)
        externalVideoPlayer.resize(width-196, height-226)
        videoPlayer.move(173, 83)
        videoPlayer.resize(width-196, height-226)



    elif(settings["videoMode"] == "small"):
        externalVideoPlayer.resize(96, 96)
        externalVideoPlayer.move(12, height-108)
        videoPlayer.resize(96, 96)
        videoPlayer.move(12, height-108)
    elif(settings["videoMode"] == "none"):
        externalVideoPlayer.resize(0, 0)
        externalVideoPlayer.move(0, 0)
        videoPlayer.resize(0, 0)
        videoPlayer.move(0, 0)



    log("[   OK   ] Resizing content to fit "+str(width)+'x'+str(height))

    buttons['play'].resize(50, 50)
    buttons['play'].move(int((width/2)-25), height-110)
    buttons['first-track'].resize(40, 40)
    buttons['first-track'].move(int((width/2)-20)-60, height-105)
    buttons['last-track'].resize(40, 40)
    buttons['last-track'].move(int((width/2)-20)+60, height-105)
    buttons['shuffle'].resize(40, 40)
    buttons['shuffle'].move(int((width/2)-20)-115, height-105)
    buttons['replay'].resize(40, 40)
    buttons['replay'].move(int((width/2)-20)+115, height-105)
    buttons['audio'].resize(40, 40)
    buttons['audio'].move(width-200, height-105)
    
    buttons['delete'].move(10, 80)
    buttons['delete'].resize(150, 30)
    buttons['add'].move(10, 40)
    buttons['add'].resize(150, 30)
    buttons['save'].move(10, 120)
    buttons['save'].resize(150, 30)
    buttons['open'].move(10, 160)
    buttons['open'].resize(150, 30)
    buttons['youtube'].move(10, 200)
    buttons['youtube'].resize(150, 30)
    buttons['videoMode'].resize(110, 30)
    buttons['videoMode'].move(width-200, height-50)
    buttons['fullScreen'].resize(60, 30)
    buttons['fullScreen'].move(width-80, height-50)

    sliders['volume'].move(width-145, height-105)
    sliders['volume'].resize(120, 40)
    seeker.move(int((width/2)-200), height-55)
    seeker.resize(400, 40)

    labels['actualtime'].resize(100, 40)
    labels['actualtime'].move(int((width/2)-300), height-49)
    labels['totaltime'].resize(100, 40)
    labels['totaltime'].move(int((width/2)+200), height-49)

    albumArt.resize(96, 96)
    albumArt.move(12, height-108)

    labels['songname'].resize(width-250-int((width/2)-20)-50, 30)
    labels['songname'].move(120, height-100)

    searchBar.move(170, 40)
    searchBar.resize(width-190, 30)

    mainList.move(170, 80)
    mainList.resize(width-190, height-220)

    noResultsfoundLabel.move(170, 80)
    noResultsfoundLabel.resize(width-190, height-220)


    bottomBar.resize(width, 120)
    bottomBar.move(0, height-120)

def openLibrary() -> None:
    openOnExplorer(os.path.expanduser("~").replace("\\", '/')+"/SomePythonThings Music/", force=True)

def load_library() -> None:
    global music_extensions
    try:
        os.chdir(os.path.expanduser("~"))
        os.chdir("SomePythonThings Music")
        path = os.getcwd()
        for fileext in music_extensions:
            for file in glob.glob(path+"/"+fileext):
                log("[   OK   ] Adding file "+os.path.abspath(file))
                addFile(os.path.abspath(file))
    except FileNotFoundError:
        pass

def searchOnLibrary() -> None:
    global searchBar, mainList
    resultsFound = mainList.findItems(searchBar.text(), QtCore.Qt.MatchContains, 0)
    if(len(resultsFound)==0):
        noResultsfoundLabel.show()
    else:
        noResultsfoundLabel.hide()
    log(f"[   OK   ] Searching for string \"{searchBar.text()}\"")
    for item in mainList.findItems('', QtCore.Qt.MatchContains, 0):
        if not(item in resultsFound):
            item.setHidden(True)
        else:
            item.setHidden(False)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------- Main Code ---------------------------------------------------------------------------------- #
if __name__ == '__main__':

    print("*-*-*-*-*- starting program main thread, all functions loaded -*-*-*-*-*")

    
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    

    os.chdir(os.path.expanduser("~"))


    Thread(target=logToFileWorker, daemon=True).start()


    if(len(sys.argv)>1):
        arg = sys.argv[1]
        if('debug' in arg):
            debugging=True
    
    log("[        ] SomePythonThings Music version {0}, debugging is set to {1}".format(str(actualVersion), str(debugging)), force=False)

    log("[        ] Actual directory is {0}".format(os.getcwd()))
    if _platform == "linux" or _platform == "linux2":
        log("[   OK   ] OS detected is linux")
        realpath="/bin/resources-sptmusic"
        font = "Ubuntu"
        music_files = ("All files (*.*)")

    elif _platform == "darwin":
        log("[   OK   ] OS detected is macOS")
        font = "Helvetica Neue"
        realpath = "/Applications/SomePythonThings Music.app/Contents/Resources/resources-sptmusic"
    
    elif _platform == "win32":
        if int(platform.release()) >= 10: #Font check: os is windows 10
            font = "Segoe UI"#"Cascadia Mono"
            log("[   OK   ] OS detected is win32 release 10 ")
        else:# os is windows 7/8
            font="Segoe UI"#"Consolas"
            is_win7=True
            log("[   OK   ] OS detected is win32 release 8 or less ")
        if(fileExists("/Program Files/SomePythonThingsMusic/resources-sptmusic/icon.ico")):
            realpath = "/Program Files/SomePythonThingsMusic/resources-sptmusic"
        else:
            realpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")+"/resources-sptmusic"
        log("[   OK   ] Directory set to "+realpath)


    else:
        log("[  WARN  ] Unable to detect OS")

    log("[   OK   ] Platform is {0}, font is {1} and real path is {2}".format(_platform, font, realpath))
    

    background_picture_path='{0}/background-sptmusic.jpg'.format(realpath.replace('c:', 'C:'))
    black_picture_path='{0}/black-sptmusic.png'.format(realpath.replace('c:', 'C:'))


    class MainApplication(QtWidgets.QApplication):
        def __init__(self, parent):
            super(MainApplication, self).__init__(parent)
            self.installEventFilter(self)
            self._prevAppState = QtCore.Qt.ApplicationActive
        
        def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
            if (watched == self and event.type() == QtCore.QEvent.ApplicationStateChange):
                ev = QtGui.QGuiApplication.applicationState()
                if (self._prevAppState == QtCore.Qt.ApplicationActive and ev == QtCore.Qt.ApplicationActive):
                    if(_platform=="darwin"):
                        log("[   OK   ] Dock icon clicked, showing...")
                        showMusic()
                self._prevAppState = ev
    
            
            return super().eventFilter(watched, event)

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            global background_picture_path
            MainWindow.setObjectName("MainWindow")
            MainWindow.setWindowTitle("MainWindow")
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

    class Window(QtWidgets.QMainWindow):
        resized = QtCore.Signal()
        keyRelease = QtCore.Signal(int)

        def __init__(self, parent=None):
            super(Window, self).__init__(parent=parent)
            ui = Ui_MainWindow()
            ui.setupUi(self)
            self.background = QtWidgets.QWidget(self)
            self.background.setObjectName("centralwidget")
            log("[        ] Background picture real path is "+background_picture_path)
            self.setCentralWidget(self.background)
            self.resized.connect(resizeWidgets)
            self.installEventFilter(self)
            
        def resizeEvent(self, event):
            self.resized.emit()
            return super(Window, self).resizeEvent(event)

        def keyReleaseEvent(self, event):
            log('[ EVENTS ] keyRelease activated.')
            if(not(event.key()==QtCore.Qt.Key_Up) and not(event.key()==QtCore.Qt.Key_Down)):
                mainList.clearFocus()
                buttons['play'].clearFocus()
                buttons['replay'].clearFocus()
                buttons['shuffle'].clearFocus()
                buttons['last-track'].clearFocus()
                buttons['first-track'].clearFocus()
                sliders['volume'].clearFocus()
                seeker.clearFocus()
                super(Window, self).keyReleaseEvent(event)
                self.keyRelease.emit(event.key())
        
        def _focusInEvent(self):
            log('[ EVENTS ] focusInEvent activated.')
        
        def closeEvent(self, event):
            log('[ EVENTS ] closeEvent activated.')
            global forceClose
            if(settings['minimize_to_tray'] and not(forceClose)):
                music.hide()
                log("[        ] Minimizing to system tray...")
                event.ignore()
            else:
                if(not(forceClose)):
                    killPlayProcess()
                    time.sleep(0.1)
                    event.accept()
                    sys.exit(0)
                else:
                    event.accept()
                    forceClose = False
        
        def eventFilter(self, object, event):
            try:
                if event.type() == QtCore.QEvent.WindowActivate or event.type() == QtCore.QEvent.FocusIn:
                    self._focusInEvent()
            except KeyboardInterrupt:
                pass
            return False
        
    class ClosableWindow(QtWidgets.QMainWindow):
        resized = QtCore.Signal()
        keyRelease = QtCore.Signal(int)

        def __init__(self, parent=None):
            super(ClosableWindow, self).__init__(parent=parent)
            ui = Ui_MainWindow()
            ui.setupUi(self)
            self.background = QtWidgets.QWidget(self)
            self.background.setObjectName("centralwidget")
            log("[        ] Background picture real path is "+background_picture_path)
            self.setCentralWidget(self.background)
            self.resized.connect(resizeWidgets)
            self.installEventFilter(self)
            
        def resizeEvent(self, event):
            self.resized.emit()
            return super(ClosableWindow, self).resizeEvent(event)

        def keyReleaseEvent(self, event):
            log('[ EVENTS ] keyRelease activated.')
            if(not(event.key()==QtCore.Qt.Key_Up) and not(event.key()==QtCore.Qt.Key_Down)):
                mainList.clearFocus()
                buttons['play'].clearFocus()
                buttons['replay'].clearFocus()
                buttons['shuffle'].clearFocus()
                buttons['last-track'].clearFocus()
                buttons['first-track'].clearFocus()
                sliders['volume'].clearFocus()
                seeker.clearFocus()
                super(ClosableWindow, self).keyReleaseEvent(event)
                self.keyRelease.emit(event.key())
        
        def _focusInEvent(self):
            log('[ EVENTS ] focusInEvent activated.')
        
        def eventFilter(self, object, event):
            try:
                if event.type() == QtCore.QEvent.WindowActivate or event.type() == QtCore.QEvent.FocusIn:
                    self._focusInEvent()
            except KeyboardInterrupt:
                pass
            return False
    
    class TreeWidget(QtWidgets.QTreeWidget):

        def __init__(self, parent):
            super().__init__(parent)
            self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            self.setDropIndicatorShown(True)
            self.setAcceptDrops(True)
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.showMenu)
            self.setSupportedDropActions = QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

        def dragEnterEvent(self, e):
            e.accept()

        def dragMoveEvent(self, e):
            e.accept()

        def dropEvent(self, e):
            for file in e.mimeData().text().replace("file://", "").split("\n"):
                if(_platform=="win32" and len(file)>1):
                    if(file[0] == "/"):
                        file = file[1:]
                if(file != ""):
                    addFile(str(file))
                
        def showMenu(self, pos: QtCore.QPoint):
            x = 0
            x += music.pos().x()
            x += self.pos().x()
            x += pos.x()
            x += 5 # padding
            y = 0
            y += music.pos().y()
            y += self.pos().y()
            y += pos.y()
            y += self.header().height()
            y += self.header().height()
            y += 10 # padding
            log(f"[        ] Showing menu at {x}x{y}")
            menu = QtWidgets.QMenu(music)
            menu.move(x, y)
            menu.addSeparator()
            playAction = QtWidgets.QAction("Play file")
            playAction.triggered.connect(goToSong)
            menu.addAction(playAction)
            menu.addSeparator()
            action = QtWidgets.QAction("Rename file")
            action.triggered.connect(openRenameMenu)
            menu.addAction(action)
            menu.addSeparator()
            deleteAction = QtWidgets.QAction("Remove from playlist")
            deleteAction.triggered.connect(removeFromPlaylist)
            menu.addAction(deleteAction)
            removeAction = QtWidgets.QAction("Delete file")
            removeAction.triggered.connect(removeFromComputer)
            menu.addAction(removeAction)
            menu.addSeparator()

            fileMenu = menu.addMenu("File")
            fileMenu.addAction(hideMusicAction)
            fileMenu.addAction(quitAction)

            playbackMenu = menu.addMenu("Playback")
            volumeMenu = playbackMenu.addMenu("Volume    ")
            volumeMenu.addAction(increaseAction)
            volumeMenu.addAction(decreaseAction)
            volumeMenu.addAction(muteAction)
            playbackMenu.addAction(playAction)
            playbackMenu.addAction(pauseAction)
            playbackMenu.addAction(nextSongAction)
            playbackMenu.addAction(previousSongAction)
            playbackMenu.addAction(plusTenSecondsAction)
            playbackMenu.addAction(minusTenSecondsAction)
            playbackMenu.addAction(previousSongAction)
            playbackMenu.addAction(shuffleAction)
            playbackMenu.addAction(replayAction)

            playlistMenu = menu.addMenu("Playlist")
            playlistMenu.addAction(openFilesAction)
            playlistMenu.addAction(deleteTrackAction)
            playlistMenu.addAction(savePlaylistAction)
            playlistMenu.addAction(openPlaylistAction)


            libraryMenu = menu.addMenu("Library")
            libraryMenu.addAction(openOnExplorerAction)
            libraryMenu.addAction(loadTrackAction)

            settingsMenu = menu.addMenu("Settings")
            settingsMenu.addAction(logAction)
            settingsMenu.addAction(reinstallAction)
            settingsMenu.addAction(openSettingsAction)

            helpMenu = menu.addMenu("Help")
            helpMenu.addAction(openHelpAction)
            helpMenu.addAction(updatesAction)
            helpMenu.addAction(aboutQtAction)
            helpMenu.addAction(aboutAction)

            menu.exec_()

    class Banner():
        def __init__(self):
            self.banner = ClosableWindow()
            self.banner.setStyleSheet(getWindowStyleSheet(banner=True))
            self.banner.setGeometry(40, 40, 500, 120)
            self.banner.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.ToolTip | QtCore.Qt.WindowStaysOnTopHint))

            self.backgroundBar = QtWidgets.QProgressBar(self.banner)
            self.backgroundBar.setTextVisible(False)
            self.backgroundBar.setMinimum(0)
            self.backgroundBar.setMaximum(1000)
            self.backgroundBar.move(0, 0)
            self.backgroundBar.resize(500, 150)

            self.art = QtWidgets.QLabel(self.banner)
            self.art.resize(96, 96)
            self.art.move(12, 12)
            
            self.slider = NonScrollableSlider(QtCore.Qt.Horizontal, self.banner)
            self.slider.setRange(0, 1000)
            self.slider.setEnabled(False)
            self.slider.resize(360, 20)
            self.slider.move(120, 80)
            
            self.title = QtWidgets.QLabel(self.banner)
            self.title.move(120, 10)
            self.title.resize(360, 20)

            self.showButton = QtWidgets.QPushButton(self.banner)
            self.showButton.setText("Open SomePythonThings Music")
            self.showButton.setObjectName("squarePurpleButton")
            self.showButton.clicked.connect(showMusic)
            self.showButton.resize(360, 30)
            self.showButton.move(120, 40)

            self.bannerIsBeingShowed = False

        def show(self):
            if not(self.bannerIsBeingShowed):
                self.bannerIsBeingShowed = True
                self.art.setPixmap(albumArt.pixmap())
                self.title.setText(labels['songname'].text())
                self.banner.show()
                Thread(target=self.timerToClose, daemon=True).start()

        def timerToClose(self):
            get_updater().call_in_main(self.banner.setWindowOpacity, 1)
            for _ in range(10):
                time.sleep(0.3)
                try:
                    get_updater().call_in_main(self.art.setPixmap, albumArt.pixmap())
                    get_updater().call_in_main(self.title.setText, labels['songname'].text())
                    try:
                        get_updater().call_in_main(self.backgroundBar.setValue, int(playProcess.position()//trackSeeked/song_length))
                        get_updater().call_in_main(self.slider.setValue, int(playProcess.position()//trackSeeked/song_length))
                    except ZeroDivisionError:
                        get_updater().call_in_main(self.backgroundBar.setValue, 0)
                        get_updater().call_in_main(self.slider.setValue, 0)
                    get_updater().call_in_main(self.backgroundBar.repaint)
                    get_updater().call_in_main(self.slider.repaint)
                except: # Raised when 2 insatnces of the banner are running
                    pass
            for i in range(30, 0, -1):
                get_updater().call_in_main(self.banner.setWindowOpacity, i/30)
                get_updater().call_in_main(self.art.setPixmap, albumArt.pixmap())
                get_updater().call_in_main(self.title.setText, labels['songname'].text())
                try:
                    get_updater().call_in_main(self.backgroundBar.setValue, int(playProcess.position()//trackSeeked/song_length))
                    get_updater().call_in_main(self.slider.setValue, int(playProcess.position()//trackSeeked/song_length))
                except ZeroDivisionError:
                    get_updater().call_in_main(self.backgroundBar.setValue, 0)
                    get_updater().call_in_main(self.slider.setValue, 0)
                get_updater().call_in_main(self.backgroundBar.repaint)
                get_updater().call_in_main(self.slider.repaint)
                time.sleep(0.02)
            get_updater().call_in_main(self.banner.hide)
            time.sleep(0.05)
            self.bannerIsBeingShowed = False

    class KillableThread(Thread): 
        def __init__(self, *args, **keywords): 
            Thread.__init__(self, *args, **keywords) 
            self.shouldBeRuning = True
        def start(self): 
            self._run = self.run 
            self.run = self.settrace_and_run
            Thread.start(self) 
        def settrace_and_run(self): 
            sys.settrace(self.globaltrace) 
            self._run()
        def globaltrace(self, frame, event, arg): 
            return self.localtrace if event == 'call' else None
        def kill(self):
            self.shouldBeRuning = False
        def localtrace(self, frame, event, arg): 
            if not(self.shouldBeRuning) and event == 'line':
                global playingObj
                log('[  EXIT  ] Trying to kill player...')
                try:
                    playingObj.stop() 
                except AttributeError:
                    pass
                log('[  EXIT  ] Thread killed by shouldBeRunning Signal.')
                raise SystemExit() 
            return self.localtrace

    class NonScrollableSlider(QtWidgets.QSlider):
        def __init__(self, orientation, parent):
            super(NonScrollableSlider, self).__init__(orientation, parent)

        def wheelEvent(self, event):
            event.ignore()

    QtWidgets.QApplication.setStyle('fusion')
    app = MainApplication(sys.argv)
    QtWidgets.QApplication.setStyle('fusion')

    music = Window()

    Thread(target=setProgramAsRunning, daemon=True).start()

    music.keyRelease.connect(on_key)
    try:
        music.resize(1200, 699)
        music.setWindowTitle('SomePythonThings Music') 
        try:
            music.setWindowIcon(QtGui.QIcon("{0}/icon-sptmusic.png".format(realpath)))
        except:
            pass
        
        try:
            readSettings = openSettings()
            i = 0
            for key in readSettings.keys():
                settings[key] = readSettings[key]
                i +=1
            log("[   OK   ] Settings loaded (settings={0})".format(str(settings)))
        except Exception as e:
            log("[ FAILED ] Unable to read settings! ({0})".format(str(e)))
            if(debugging):
                raise e

        try:
            volume = settings["volume"]
        except KeyError:
            log("[  WARN  ] Volume value not found on settings")

        music.setMinimumSize(700, 370)
        music.setStyleSheet(getWindowStyleSheet())


        banner = Banner()

        bottomBar = QtWidgets.QProgressBar(music)
        bottomBar.setTextVisible(False)
        bottomBar.setMinimum(0)
        bottomBar.setMaximum(1000)
        bottomBar.setValue(0)




        buttons['delete'] = QtWidgets.QPushButton(music)
        buttons['delete'].setText('Remove from playlist')
        buttons['delete'].clicked.connect(removeFromPlaylist)
        buttons['add'] = QtWidgets.QPushButton(music)
        buttons['add'].setText('Add file(s) to playlist')
        buttons['add'].clicked.connect(openFile)
        buttons['save'] = QtWidgets.QPushButton(music)
        buttons['save'].setText('Save playlist as file')
        buttons['save'].clicked.connect(savePlaylist)
        buttons['open'] = QtWidgets.QPushButton(music)
        buttons['open'].setText('Open playlist file')
        buttons['open'].clicked.connect(openPlaylist)
        
        buttons['delete'].setObjectName("squareRedButton")
        buttons['delete'].setToolTip("Remove files from playlist, not from computer")
        
        buttons['add'].setObjectName("squarePurpleButton")
        buttons['add'].setToolTip("Add local audio files")

        buttons['save'].setObjectName("squarePurpleButton")
        buttons['save'].setToolTip("Save the current playlist")

        buttons['open'].setObjectName("squarePurpleButton")
        buttons['open'].setToolTip("Open a playlist file")

        
        buttons['youtube'] = QtWidgets.QPushButton(music)
        buttons['youtube'].setText('Download music')
        buttons['youtube'].clicked.connect(youtubeWindow)
        buttons['youtube'].setObjectName("squarePurpleButton")
        buttons['youtube'].setToolTip("Download music from Youtube servers")



        albumArt = QtWidgets.QLabel(music)
        albumArt.resize(96, 96)
        albumArt.setPixmap(QtGui.QPixmap(realpath+"/icon.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))


        noResultsfoundLabel = QtWidgets.QLabel(music)
        noResultsfoundLabel.setText("No music found\n\nYou can download music using the \"Download music\" button on the top left corner of the window")
        noResultsfoundLabel.setFont(noResultsfoundLabel.font().setPixelSize(24))
        noResultsfoundLabel.hide()
        noResultsfoundLabel.setAlignment(QtCore.Qt.AlignCenter)

        mainList = TreeWidget(music)
        
        mainList.setColumnCount(5)
        mainList.setHeaderLabels(["  Song Title", "  Duration", "  Location", "  Size", "  File Type"])
        mainList.setColumnWidth(0, 400)
        mainList.setColumnWidth(1, 80)
        mainList.setColumnWidth(2, 300)
        mainList.setColumnWidth(3, 100)
        mainList.setColumnWidth(4, 80)
        

        mainList.setIconSize(QtCore.QSize(24, 24))
        mainList.setSortingEnabled(True)
        mainList.setSelectionMode(QtWidgets.QTreeWidget.SingleSelection)
        mainList.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        mainList.setVerticalScrollMode(QtWidgets.QTreeWidget.ScrollPerPixel)
        mainList.setHorizontalScrollMode(QtWidgets.QTreeWidget.ScrollPerPixel)
        mainList.itemDoubleClicked.connect(goToSong)

        searchBar = QtWidgets.QLineEdit(music)
        searchBar.textChanged.connect(searchOnLibrary)
        searchBar.setPlaceholderText("Search on your music...")


        playProcess = QtMultimedia.QMediaPlayer(music)
        playProcess.setAudioRole(QtMultimedia.QAudio.MusicRole)

        videoPlayProcess = QtMultimedia.QMediaPlayer(music)
        videoPlayProcess.setAudioRole(QtMultimedia.QAudio.MusicRole)


        videoPlayer = QtMultimediaWidgets.QVideoWidget(music)
        videoPlayer.hide()

        externalVideoPlayer = QtMultimediaWidgets.QVideoWidget(music)
        externalVideoPlayer.hide()


        playProcess.setVideoOutput(videoPlayer)
        videoPlayProcess.setVideoOutput(externalVideoPlayer)


        sliders['volume'] = QtWidgets.QSlider(QtCore.Qt.Horizontal, music)
        sliders['volume'].setMinimum(0)
        sliders['volume'].setMaximum(100)
        sliders['volume'].setValue(volume)
        sliders['volume'].valueChanged.connect(changeVolume)

        
        
        seeker = NonScrollableSlider(QtCore.Qt.Horizontal, music)
        seeker.setMinimum(0)
        seeker.setMaximum(1000)
        seeker.sliderPressed.connect(stopSeeking)
        seeker.sliderReleased.connect(goToSpecificTime)

        labels['actualtime'] = QtWidgets.QLabel(music)
        labels['actualtime'].setText('-:--:--')
        labels['actualtime'].setAlignment(QtCore.Qt.AlignRight)
        labels['totaltime'] = QtWidgets.QLabel(music)
        labels['totaltime'].setText('-:--:--')
        labels['totaltime'].setAlignment(QtCore.Qt.AlignLeft)
        labels['songname'] = QtWidgets.QLabel(music)
        labels['songname'].setText('No music playing')
        labels['songname'].setAlignment(QtCore.Qt.AlignLeft)

        i = 10
        for button in ['audio', 'replay', 'first-track', 'play', 'last-track', 'shuffle']:
            buttons[button] = QtWidgets.QPushButton(music)
            buttons[button].move(i, 40)
            i += 50
            buttons[button].resize(50, 50)
            buttons[button].setStyleSheet("QPushButton{background-color: rgba(255, 255, 255, 0.8); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/"+button+"-icon.svg\") 0 0 0 0 stretch stretch } QPushButton:clicked{background-color: rgba(00, 130, 130, 1.0);}")

        buttons['play'].setStyleSheet("QPushButton{background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/play-icon.svg\") 0 0 0 0 stretch stretch} QPushButton:checked{background-color: rgba(00, 130, 130, 1.0);}")
    


        buttons['shuffle'].clicked.connect(toShuffle)
        buttons['replay'].clicked.connect(toReplay)
        buttons['play'].clicked.connect(toPlay)
        buttons['audio'].clicked.connect(toMute)
        buttons['last-track'].clicked.connect(toSkip)
        buttons['first-track'].clicked.connect(toGoBack)



        buttons['videoMode'] = QtWidgets.QPushButton(music)
        buttons['videoMode'].setText('Video Mode: ')
        buttons['videoMode'].clicked.connect(changeVideoMode)
        buttons['videoMode'].setObjectName("squarePurpleButton")
        buttons['videoMode'].setToolTip("Change video view mode between Big, Normal, Small and Hidden")
        

        buttons['fullScreen'] = QtWidgets.QPushButton(music)
        buttons['fullScreen'].setText('Full Screen')
        buttons['fullScreen'].clicked.connect(changeScreenMode)
        buttons['fullScreen'].setObjectName("squarePurpleButton")
        buttons['fullScreen'].setToolTip("Change window view mode between full screen and normal")
        
        icon = QtGui.QIcon("{0}/icon-sptmusic.png".format(realpath))
        tray = QtWidgets.QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setToolTip("SomePythonThings Music")
        tray.setVisible(True)
        trayMenu = QtWidgets.QMenu()
        tray.setContextMenu(trayMenu)
        tray.messageClicked.connect(showMusic)
        tray.activated.connect(showMusic)

        menuBar = music.menuBar()
        menuBar.setNativeMenuBar(False)

        fileMenu = menuBar.addMenu("File")
        hideMusicAction = QtWidgets.QAction("Hide     ", music)
        hideMusicAction.setShortcut("Ctrl+H")
        hideMusicAction.triggered.connect(music.hide)
        fileMenu.addAction(hideMusicAction)
        quitAction = QtWidgets.QAction("Quit     ", music)
        quitAction.triggered.connect(quitMusic)
        quitAction.setShortcut("Ctrl+Q")
        fileMenu.addAction(quitAction)

        fileMenu = trayMenu.addMenu("File")
        fileMenu.addAction(hideMusicAction)
        fileMenu.addAction(quitAction)


        playbackMenu = menuBar.addMenu("Playback")
        volumeMenu = playbackMenu.addMenu("Volume    ")
        increaseAction = QtWidgets.QAction("Increase    ", music)
        increaseAction.setShortcut("Ctrl+Plus")
        increaseAction.triggered.connect(increaseVolume)
        volumeMenu.addAction(increaseAction)
        decreaseAction = QtWidgets.QAction("Decrease    ", music)
        decreaseAction.triggered.connect(decreaseVolume)
        volumeMenu.addAction(decreaseAction)
        muteAction = QtWidgets.QAction("Mute    ", music)
        muteAction.triggered.connect(toMute)
        muteAction.setCheckable(True)
        volumeMenu.addAction(muteAction)
        playAction = QtWidgets.QAction("Play    ", music)
        playAction.triggered.connect(toStrictlyPlay)
        playbackMenu.addAction(playAction)
        pauseAction = QtWidgets.QAction("Pause    ", music)
        pauseAction.triggered.connect(toStrictlyPause)
        playbackMenu.addAction(pauseAction)
        nextSongAction = QtWidgets.QAction("Next song    ", music)
        nextSongAction.triggered.connect(toSkip)
        playbackMenu.addAction(nextSongAction)
        previousSongAction = QtWidgets.QAction("Previous song    ", music)
        previousSongAction.triggered.connect(toGoBack)
        playbackMenu.addAction(previousSongAction)
        plusTenSecondsAction = QtWidgets.QAction("Forward 10 seconds", music)
        plusTenSecondsAction.triggered.connect(plusTenSeconds)
        plusTenSecondsAction.setShortcut("MoveToNextChar")
        playbackMenu.addAction(plusTenSecondsAction)
        minusTenSecondsAction = QtWidgets.QAction("Rewind 10 seconds", music)
        minusTenSecondsAction.triggered.connect(plusTenSeconds)
        minusTenSecondsAction.setShortcut("MoveToPreviousChar")
        playbackMenu.addAction(minusTenSecondsAction)
        shuffleAction = QtWidgets.QAction("Shuffle    ", music)
        shuffleAction.triggered.connect(toShuffle)
        shuffleAction.setCheckable(True)
        playbackMenu.addAction(shuffleAction)
        replayAction = QtWidgets.QAction("Replay    ", music)
        replayAction.triggered.connect(toReplay)
        replayAction.setCheckable(True)
        playbackMenu.addAction(replayAction)

        playbackMenu = trayMenu.addMenu("Playback")
        volumeMenu = playbackMenu.addMenu("Volume    ")
        volumeMenu.addAction(increaseAction)
        volumeMenu.addAction(decreaseAction)
        volumeMenu.addAction(muteAction)
        playbackMenu.addAction(playAction)
        playbackMenu.addAction(pauseAction)
        playbackMenu.addAction(nextSongAction)
        playbackMenu.addAction(previousSongAction)
        playbackMenu.addAction(plusTenSecondsAction)
        playbackMenu.addAction(minusTenSecondsAction)
        playbackMenu.addAction(shuffleAction)
        playbackMenu.addAction(replayAction)


        
        playlistMenu = menuBar.addMenu("Playlist")
        openFilesAction = QtWidgets.QAction("Add file(s) ", music)
        openFilesAction.setShortcut("Ctrl+A")
        openFilesAction.triggered.connect(openFile)
        playlistMenu.addAction(openFilesAction)
        deleteTrackAction = QtWidgets.QAction("Remove selected track ", music)
        deleteTrackAction.setShortcut("Ctrl+Del")
        deleteTrackAction.triggered.connect(removeFromPlaylist)
        playlistMenu.addAction(deleteTrackAction)
        savePlaylistAction = QtWidgets.QAction("Save playlist to file ", music)
        savePlaylistAction.setShortcut("Ctrl+S")
        savePlaylistAction.triggered.connect(savePlaylist)
        playlistMenu.addAction(savePlaylistAction)
        openPlaylistAction = QtWidgets.QAction("Open playlist from file ", music)
        openPlaylistAction.setShortcut("Ctrl+O")
        openPlaylistAction.triggered.connect(openPlaylist)
        playlistMenu.addAction(openPlaylistAction)

        playlistMenu = trayMenu.addMenu("Playlist")
        playlistMenu.addAction(openFilesAction)
        playlistMenu.addAction(deleteTrackAction)
        playlistMenu.addAction(savePlaylistAction)
        playlistMenu.addAction(openPlaylistAction)


        libraryMenu = menuBar.addMenu("Library")
        openOnExplorerAction = QtWidgets.QAction("Show on explorer ", music)
        openOnExplorerAction.triggered.connect(openLibrary)
        openOnExplorerAction.setShortcut("Ctrl+Shift+l")
        libraryMenu.addAction(openOnExplorerAction)
        loadTrackAction = QtWidgets.QAction("Load library ", music)
        loadTrackAction.setShortcut("Ctrl+l")
        loadTrackAction.triggered.connect(load_library)
        libraryMenu.addAction(loadTrackAction)

        libraryMenu = trayMenu.addMenu("Library")
        libraryMenu.addAction(openOnExplorerAction)
        libraryMenu.addAction(loadTrackAction)


        settingsMenu = menuBar.addMenu("Settings")
        logAction = QtWidgets.QAction(" Open Log", music)
        logAction.triggered.connect(openLog)
        settingsMenu.addAction(logAction)
        reinstallAction = QtWidgets.QAction(" Reinstall SomePythonThigs Music   ", music)
        reinstallAction.triggered.connect(lambda: checkUpdates_py())
        settingsMenu.addAction(reinstallAction)
        openSettingsAction = QtWidgets.QAction(" Settings    ", music)
        openSettingsAction.triggered.connect(openSettingsWindow)
        settingsMenu.addAction(openSettingsAction)

        helpMenu = menuBar.addMenu("Help")
        openHelpAction = QtWidgets.QAction("Online manual", music)
        openHelpAction.triggered.connect(openHelp)
        helpMenu.addAction(openHelpAction)
        updatesAction = QtWidgets.QAction("Check for updates", music)
        updatesAction.triggered.connect(checkDirectUpdates)
        helpMenu.addAction(updatesAction)
        aboutQtAction = QtWidgets.QAction("About Qt framework   ", music)
        aboutQtAction.triggered.connect(lambda: QtWidgets.QMessageBox.aboutQt(music, "About the Qt framework - SomePythonThings Music"))
        helpMenu.addAction(aboutQtAction)
        aboutAction = QtWidgets.QAction("About SomePythonThings Music    ", music)
        aboutAction.triggered.connect(about)
        helpMenu.addAction(aboutAction)

        helpMenu = trayMenu.addMenu("Help")
        helpMenu.addAction(openHelpAction)
        helpMenu.addAction(updatesAction)
        helpMenu.addAction(aboutAction)
        
        showMusicAction = QtWidgets.QAction("Show SomePythonThigs Music ", music)
        showMusicAction.triggered.connect(showMusic)
        trayMenu.addAction(showMusicAction)

        quitMusicAction = QtWidgets.QAction("Quit SomePythonThigs Music ", music)
        quitMusicAction.triggered.connect(quitMusic)
        trayMenu.addAction(quitMusicAction)

        fullScreen = False

        if(settings["videoMode"] == "small"):
            buttons["videoMode"].setText("Video mode: Small")
        elif(settings["videoMode"] == "none"):
            buttons["videoMode"].setText("No video")
        elif(settings["videoMode"] == "big"):
            buttons["videoMode"].setText("Video mode: Big")
        elif(settings["videoMode"] == "normal"):
            buttons["videoMode"].setText("Video mode: Normal")
        else:
            buttons["videoMode"].setText("Change video mode")
        log("[   OK   ] Video mode set to "+settings["videoMode"])
        videoModeChanged = True



        if(settings["fullScreen"] == True):
            fullScreen=True
        screenModeChanged = True
        resizeWidgets()


        if(_platform=='darwin'):
            newMenuBar = QtWidgets.QMenuBar(music)
            newMenuBar.setNativeMenuBar(True)

            fileMenu = newMenuBar.addMenu("File")
            fileMenu.addAction(hideMusicAction)
            fileMenu.addAction(quitAction)

            playbackMenu = newMenuBar.addMenu("Playback")
            volumeMenu = playbackMenu.addMenu("Volume    ")
            volumeMenu.addAction(increaseAction)
            volumeMenu.addAction(decreaseAction)
            volumeMenu.addAction(muteAction)
            playbackMenu.addAction(playAction)
            playbackMenu.addAction(pauseAction)
            playbackMenu.addAction(nextSongAction)
            playbackMenu.addAction(previousSongAction)
            playbackMenu.addAction(shuffleAction)
            playbackMenu.addAction(replayAction)

            playlistMenu = newMenuBar.addMenu("Playlist")
            playlistMenu.addAction(openFilesAction)
            playlistMenu.addAction(deleteTrackAction)
            playlistMenu.addAction(savePlaylistAction)
            playlistMenu.addAction(openPlaylistAction)


            libraryMenu = newMenuBar.addMenu("Library")
            libraryMenu.addAction(openOnExplorerAction)
            libraryMenu.addAction(loadTrackAction)

            settingsMenu = newMenuBar.addMenu("Settings")
            settingsMenu.addAction(logAction)
            settingsMenu.addAction(reinstallAction)
            settingsMenu.addAction(openSettingsAction)
            defaultOpenSettingsAction = QtWidgets.QAction("Settings", music)
            defaultOpenSettingsAction.triggered.connect(openSettingsWindow)
            settingsMenu.addAction(defaultOpenSettingsAction)

            helpMenu = newMenuBar.addMenu("Help")
            helpMenu.addAction(openHelpAction)
            helpMenu.addAction(updatesAction)
            helpMenu.addAction(aboutQtAction)
            helpMenu.addAction(aboutAction)



        log("[        ] Starting Pynput keyboard thread...")
        if(_platform=='darwin'):
            if(settings["alertOfKeyboardControl"]):
                throw_info("SomePythonThings Music", "In order to be able to monitor the media keys (Play, pause, skip, previous, etc.), due to PySide2 limitations, you will need to allow SomePythonThings Music to recieve other applications key presses on System Preferences.")
                settings["alertOfKeyboardControl"] = False
                saveSettings(silent=False, minimize_to_tray=settings['minimize_to_tray'], bakcgroundPicture=settings['bakcgroundPicture'], mode=settings['mode'], volume=settings['volume'], showTrackNotification=settings['showTrackNotification'], showEndNotification=settings['showEndNotification'],loadLibraryAtStartup=settings["loadLibraryAtStartup"], repeatByDefault=settings["repeatByDefault"], shuffleByDefault=settings["shuffleByDefault"])
        if(_platform=='win32'):
            pynput.keyboard.Listener(on_press=mediaKeyPress).start()

        if(len(sys.argv)>1):
            if('runanyway' in sys.argv[1].lower()):
                goRun=True
                canRun=True
        while(not(goRun)): pass
        if(canRun):
            if(fullScreen):
                music.showFullScreen()
            else:
                showMusic()
            if(_platform == "win32"):
                from PySide2 import QtWinExtras
                loadbutton = QtWinExtras.QWinTaskbarButton(music)
                loadbutton.setWindow(music.windowHandle())
                taskbprogress = loadbutton.progress()
                taskbprogress.setRange(0, 100)
                taskbprogress.setValue(0)
                taskbprogress.show()

                buttonsBar = QtWinExtras.QWinThumbnailToolBar(music)
                buttonsBar.setWindow(music.windowHandle())
                WindowPreviousButton = QtWinExtras.QWinThumbnailToolButton(music)
                WindowPreviousButton.clicked.connect(toGoBack)
                WindowPreviousButton.setIcon(QtGui.QIcon(realpath+"/icons-sptmusic/first-track-bar.ico"))
                buttonsBar.addButton(WindowPreviousButton)
                WindowPlayButton = QtWinExtras.QWinThumbnailToolButton(music)
                WindowPlayButton.clicked.connect(toPlay)
                WindowPlayButton.setIcon(QtGui.QIcon(realpath+"/icons-sptmusic/play-bar.ico"))
                buttonsBar.addButton(WindowPlayButton)
                WindowNextButton = QtWinExtras.QWinThumbnailToolButton(music)
                WindowNextButton.clicked.connect(toSkip)
                WindowNextButton.setIcon(QtGui.QIcon(realpath+"/icons-sptmusic/last-track-bar.ico"))
                buttonsBar.addButton(WindowNextButton)

            resizeWidgets()
            Thread(target=updates_thread, daemon=True, name="Updates Thread").start()
            Thread(target=checkModeThread, daemon=True, name="Light/Dark theme check thread").start()
            log("[        ] Program loaded, starting UI...")
            i = 1
            isThereAFile = False
            if(len(sys.argv)>1):
                if('SPTPLAYLIST' == getFileType(sys.argv[1])):
                    openPlaylist(sys.argv[1])
                    isThereAFile = True
                    log('[   OK   ] 1st argument appears to be a playlist...')
                else:
                    while i<len(sys.argv):
                        log('[        ] Detected arguments, checking if they are valid...')
                        arg = sys.argv[i]
                        if(os.path.isfile(arg)):
                            addFile(arg)
                            isThereAFile = True
                            log('[   OK   ] Argument {0} added successfully'.format(arg))
                        else:
                            log('[  WARN  ] Argument {0} is not a valid file!'.format(arg))
                        i += 1
            if(isThereAFile):
                toStrictlyPlay()
            else:
                if(settings['loadLibraryAtStartup']):
                    log("[   OK   ] No file detected, loading library...")
                    load_library()
            if(settings["shuffleByDefault"]):
                toShuffle()
            if(settings["repeatByDefault"]):
                toReplay()
            
            resultsFound = mainList.findItems('', QtCore.Qt.MatchContains, 0)
            if(len(resultsFound)==0):
                noResultsfoundLabel.show()
            else:
                noResultsfoundLabel.hide()
            app.exec_()
        else:
            tray.setVisible(False)
            log('[  EXIT  ] Exiting...')
            try:        
                killPlayProcess()
            except AttributeError:
                pass
            sys.exit()
    except Exception as e:
        try:        
            killPlayProcess()
        except AttributeError:
            pass
        log("[ FAILED ] A FATAL ERROR OCCURRED. PROGRAM WILL BE TERMINATED AFTER ERROR REPORT")
        try:
            throw_error('SomePythonThings Music', "SomePythonThings Music crashed because of a fatal error.\n\nAn Error Report will be generated and opened automatically\n\nSending the report would be very appreciated. Sorry for any inconveniences")
        except:
            pass
        os_info = f"" + \
        f"                        OS: {platform.system()}\n"+\
        f"                   Release: {platform.release()}\n"+\
        f"           OS Architecture: {platform.machine()}\n"+\
        f"          APP Architecture: {platform.architecture()[0]}\n"+\
        f"                   Program: SomePythonThings Music Version {actualVersion}"+\
        "\n\n-----------------------------------------------------------------------------------------"
        traceback_info = "Traceback (most recent call last):\n"
        try:
            for line in traceback.extract_tb(e.__traceback__).format():
                traceback_info += line
            traceback_info += f"\n{type(e).__name__}: {str(e)}"
        except:
            traceback_info += "\nUnable to get traceback"
            if(debugging):
                raise e
        with open(tempDir.name.replace('\\', '/')+'/log.txt', 'r') as f:
            webbrowser.open("https://www.somepythonthings.tk/error-report/?appName=SomePythonThings Music&errorBody="+os_info.replace('\n', '{l}').replace(' ', '{s}')+"{l}{l}{l}{l}SomePythonThings Music Log:{l}"+str(f.read()+"\n\n\n\n"+traceback_info).replace('\n', '{l}').replace(' ', '{s}'))
        if(debugging):
            raise e
    try:        
        killPlayProcess()
    except AttributeError:
        pass

log('[  EXIT  ] Reached end of the script')

sys.exit(0)
