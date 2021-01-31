# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------- Required Modules ------------------------------------------------------------------------------ #
import os
import sys
import time
import glob
import wget
import json
import random
import mutagen
import platform
import tempfile
import datetime
import traceback
import subprocess
import webbrowser
import darkdetect
from sys import platform as _platform
from ast import literal_eval
from pytube import YouTube
from PySide2 import QtWidgets, QtGui, QtCore, QtMultimedia
from functools import partial
from threading import Thread
from urllib.request import urlopen
from moviepy.editor import VideoFileClip
from qt_thread_updater import get_updater
from youtubesearchpython import VideosSearch


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ Globals ---------------------------------------------------------------------------------- #
debugging = False
actualVersion = 2.0

music_files = ('Common Media Files (*.wav; *.mp3; *.pcm; *.aiff; *.aac; *.ogg; *.wma; *.flac);;Other media files (*.*)')
music_extensions = ['*.wav', '*.mp3', '*.pcm', '*.aiff', '*.aac', '*.ogg', '*.wma', '*.flac']
buttons = {}
texts = {}
progressbars = {}
lists = {}
labels = {}
sliders = {}

canRun=True
seeking = True

justContinue = False
playerIsRunning = False
logBlocked = False
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

background_picture_path = ''
logHistory = ""
font = ""
realpath = "."

defaultSettings = {
    "settings_version": actualVersion,
    "minimize_to_tray": False,
    "volume": 100,
    "showTrackNotification": True,
    "showEndNotification": True,
    "bakcgroundPicture":"None",
    "mode":'auto',
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
        border: 1px solid black;
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
        background-color: rgba(255, 255, 255, 0.5)
    }}
    QProgressBar::chunk
    {{
        background-color: rgba(20, 180, 180, 0.5);
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
"""

darkModeStyleSheet = """
    * 
    {{
        color: #EEEEEE;
        font-size:12px;
        font-family:{0};
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
        background-color: rgba(0, 0, 0, 0.5);
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
        background-color: rgba(0, 0, 0, 0.5);
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
        background-color: rgba(0, 0, 0, 0.0);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(0, 0, 0);
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
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 0px;
        padding-left: 7px;
        border-bottom-right-radius: 3px;
        border-top-right-radius: 3px;
    }}
    #settingsBackground
    {{
        background-color: rgba(0, 0, 0, 0.5);
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
        border: 1px solid rgb(0, 0, 0);
        border-right: none;
    }}
    #settingsCheckbox
    {{
        background-color: rgba(0, 0, 0, 0.5);
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
"""

def getTheme():
    if(platform.system()=="Windows"):
        import winreg
        if(int(platform.release())>=10):
            access_registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            access_key = winreg.OpenKey(access_registry, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
            readKeys = {}
            for n in range(20):
                try:
                    x = winreg.EnumValue(access_key, n)
                    readKeys[x[0]]=x[1]
                except:
                    pass
            try:
                return readKeys["AppsUseLightTheme"]
            except:
                return 1
        else:
            return 1
    elif(platform.system()=="Darwin"):
        return int(darkdetect.isLight())
    else:
        return 1

def getWindowStyleSheet():
    global settings, realpath, background_picture_path
    mode = 'auto'
    try:
        if(os.path.exists(settings['background'])):
            background_picture_path =  settings['background']
        else:
            log("[  WARN  ] Custom background picture does not exist")
    except KeyError:
        log("[  WARN  ] Can't get custom background picture")
    log("[   OK   ] Background picture path set to "+str(background_picture_path))
    try:
        if(str(settings["mode"]).lower() in 'darklightauto'):
            mode = str(settings['mode'])
        else:
            log("[  WARN  ] Mode is invalid")
    except KeyError:
        log("[  WARN  ] Mode key does not exist on settings")
    if(mode=='auto' and _platform == 'linux'):
        log('[        ] Auto mode selected and os is not macOS. Swithing to light...')
        mode='light'
    if(mode=='auto'):
        if(getTheme()==0):
            log('[        ] Auto mode selected. Swithing to dark...')
            mode='dark'
        else:
            log('[        ] Auto mode selected. Swithing to light...')
            mode='light'
    log('[   OK   ] mode set to '+str(mode))
    if(mode=='light'):
        return lightModeStyleSheet.format(font, background_picture_path)
    else:
        return darkModeStyleSheet.format(font, background_picture_path)

def checkModeThread():
    lastMode = getTheme()
    while True:
        if(lastMode!=getTheme()):
            get_updater().call_in_main(music.setStyleSheet, getWindowStyleSheet())
            lastMode = getTheme()
        time.sleep(0.1)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- Essential Functions ----------------------------------------------------------------------------- #
def run(s):
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

def log(s, force=False):
    global debugging, logHistory
    if(debugging or "WARN" in str(s) or "FAILED" in str(s) or force):
        print((time.strftime('[%H:%M:%S] ', time.gmtime(time.time())))+str(s))
    try:
        logHistory += str(s)
        logHistory += "\n"
    except Exception as e:
        if(debugging):
            raise e

def notify(title, body, icon=QtGui.QIcon(realpath+"/icon.ico")):
    log(f"[   OK   ] Showing notification with title {title} and body {body}")
    tray.showMessage(title, body, icon)
    

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------ Update Functions ------------------------------------------------------------------------------- #
if(True):
    def checkUpdates_py():
        global music, actualVersion
        try:
            response = urlopen("http://www.somepythonthings.tk/versions/music.ver")
            response = response.read().decode("utf8")
            if float(response.split("///")[0]) > actualVersion:
                get_updater().call_in_main(askUpdates, response)
            else:
                log("[   OK   ] No updates found")
                return 'No'
        except Exception as e:
            if debugging:
                raise e
            log("[  WARN  ] Unacble to reach http://www.somepythonthings.tk/versions/music.ver. Are you connected to the internet?")
            return 'Unable'

    def askUpdates(response):
        notify("SomePythonThings Music Updater", "SomePythonThings Music has a new update!\nActual version: {0}\nNew version: {1}".format(actualVersion, response.split("///")[0]))
        if QtWidgets.QMessageBox.Yes == QtWidgets.QMessageBox.question(music, 'SomePythonThings Music', "There are some updates available for SomePythonThings Music:\nYour version: "+str(actualVersion)+"\nNew version: "+str(response.split("///")[0])+"\nNew features: \n"+response.split("///")[1]+"\nDo you want to download and install them?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes):

            #                'debian': debian link in posotion 2                  'win32' Windows 32bits link in position 3           'win64' Windows 64bits in position 4                   'macos' macOS 64bits INTEL in position 5
            downloadUpdates({'debian': response.split("///")[2].replace('\n', ''), 'win32': response.split("///")[3].replace('\n', ''), 'win64': response.split("///")[4].replace('\n', ''), 'macos':response.split("///")[5].replace('\n', '')})
        else:
            log("[  WARN  ] User aborted update!")

    def downloadUpdates(links):
        log('[   OK   ] Reached downloadUpdates. Download links are "{0}"'.format(links))
        if _platform == 'linux' or _platform == 'linux2':  # If the OS is linux
            log("[   OK   ] platform is linux, starting auto-update...")
            throw_info("SomePythonThings Updater", "The new version is going to be downloaded and installed automatically. \nThe installation time may vary depending on your internet connection and your computer's performance, but it shouldn't exceed a few minutes.\nPlease DO NOT kill the program until the update is done, because it may corrupt the executable files.\nClick OK to start downloading.")
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
            get_updater().call_in_main(throw_info, "SomePythonThings Update", "The new version is going to be downloaded and prepared for the installation. \nThe download time may vary depending on your internet connection and your computer's performance, but it shouldn't exceed a few minutes.\nClick OK to continue.")
            t = Thread(target=download_win, args=(url,))
            t.daemon=True
            t.start()
        elif _platform == 'darwin':
            log("[   OK   ] platform is macOS, starting auto-update...")
            throw_info("SomePythonThings Updater", "The new version is going to be downloaded and installed automatically. \nThe installation time may vary depending on your internet connection and your computer's performance, but it shouldn't exceed a few minutes.\nPlease DO NOT kill the program until the update is done, because it may corrupt the executable files.\nClick OK to start downloading.")
            t = Thread(target=download_macOS, args=(links,))
            t.daemon=True
            t.start()
        else:  # If os is unknown
            webbrowser.open_new('https://www.somepythonthings.tk/programs/somepythonthings-music/')

    def download_win(url):
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

    def launch_win(filename):
        try:
            installationProgressBar('Launching')
            throw_info("SomePythonThings Music Updater", "The file has been downloaded successfully and the setup will start now. When clicking OK, the application will close and a User Account Control window will appear. Click Yes on the User Account Control Pop-up asking for permissions to launch SomePythonThings-Music-Updater.exe. Then follow the on-screen instructions.")
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

    def download_linux(links):
        get_updater().call_in_main(installationProgressBar, 'Downloading')
        p1 = os.system('cd; rm somepythonthings-music_update.deb; wget -O "somepythonthings-music_update.deb" {0}'.format(links['debian']))
        if(p1 == 0):  # If the download is done
            get_updater().call_in_main(install_linux_part1)
        else:  # If the download is falied
            get_updater().call_in_main(throw_error, "SomePythonThings", "An error occurred while downloading the update. Check your internet connection. If the problem persists, try to download and install the program manually.")
            webbrowser.open_new('https://www.somepythonthings.tk/programs/somepythonthings-music/')

    def install_linux_part1(again=False):
        global music
        installationProgressBar('Installing')
        time.sleep(0.2)
        if not again:
            passwd = str(QtWidgets.QInputDialog.getText(music, "Autentication needed - SomePythonThings Music", "Please write your password to perform the update. \nThis password is NOT going to be stored anywhere in any way and it is going to be used ONLY for the update.\nIf you want, you can check that on the source code on github: \n(https://github.com/martinet101/SomePythonThings-Music/)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0])
        else:
            passwd = str(QtWidgets.QInputDialog.getText(music, "Autentication needed - SomePythonThings Music", "An error occurred while autenticating. Insert your password again (This attempt will be the last one)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0])
        t = Thread(target=install_linux_part2, args=(passwd, again))
        t.start()

    def install_linux_part2(passwd, again=False):
        installationProgressBar('Installing')
        p1 = os.system('cd; echo "{0}" | sudo -S apt install ./"somepythonthings-music_update.deb" -y'.format(passwd))
        if(p1 == 0):  # If the installation is done
            p2 = os.system('cd; rm "./somepythonthings-music_update.deb"')
            if(p2 != 0):  # If the downloaded file cannot be removed
                log("[  WARN  ] Could not delete update file.")
            installationProgressBar('Installing')
            get_updater().call_in_main(throw_info,"SomePythonThings Music Updater","The update has been applied succesfully. Please reopen the application")
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

    def download_macOS(links):
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

    def install_macOS():
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
def youtubeWindow():

    dialog = None
    downloadSize = 0

    def openYoutubeLink(link):
        webbrowser.open(link)

    def resizeWidgets():
        h = youtube.height()
        w = youtube.width()
        query.move(10, 10)
        query.resize(w-120, 30)
        button.move(w-100, 10)
        button.resize(90, 30)
        results.move(10, 50)
        results.resize(w-20, h-100)
        closeButton.move(10, h-40)

    def getResults():
        try:
            videosSearch = VideosSearch(query.text(), limit = 50)
            resultsFound = (videosSearch.result()['result'])
            results.clear()
            i = 20
            for video in resultsFound:
                newItem = QtWidgets.QTreeWidgetItem()
                newItem.setText(0, "{0:0>4}".format(str(i)))
                newItem.setText(1, video['title'])
                newItem.setToolTip(1, "Double-click to download")
                newItem.setIcon(1, QtGui.QIcon(realpath.replace("\\", "/")+"/icons-sptmusic/download.ico"))
                newItem.setText(3, video['duration'])
                newItem.setText(4, video['channel']['name'])
                newItem.setText(6, "https://www.youtube.com/watch?v="+video['id'])
                results.addTopLevelItem(newItem)
                
                btn = QtWidgets.QPushButton("Download", youtube)
                btn.resize(100, 20)
                btn.setObjectName("squarePurpleButton")
                btn.setToolTip("Download to your library")
                btn.clicked.connect(startDownload)
                
                results.setItemWidget(newItem, 2, btn)

                url = "https://www.youtube.com/watch?v="+video['id']
                link = QtWidgets.QPushButton(url, youtube)
                link.clicked.connect(partial(openYoutubeLink, url))
                link.setToolTip("Open link on browser")
                link.setObjectName("squarePurpleButton")
                
                results.setItemWidget(newItem, 5, link)

                i -= 1

            if(len(resultsFound) == 0):
                get_updater().call_in_main(throw_error, "SomePythonThings Music", "No results found!")
        except Exception as e:
            get_updater().call_in_main(throw_error, "SomePythonThings Music", "Unable to retrieve youtube results!\n\nPlease try it again later")
            if(debugging):
                raise e

    def startDownload():
        t = KillableThread(target=downloadAndAdd, daemon=True)
        name = results.currentItem().text(1)

        def killDownload():
            t.kill()
        
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
        dialog.canceled.connect(killDownload)
        t.start()
        dialog.exec_()

    def showDownloadProgress(stream, chunk, bytes_remaining):
        global downloadSize
        get_updater().call_in_main(dialog.setValue, (downloadSize-bytes_remaining)/downloadSize*100)

    def downloadAndAdd():
        global downloadSize
        try:
            warn = False
            link = results.currentItem().text(6)
            name = results.currentItem().text(1)
            os.chdir(os.path.expanduser("~"))
            get_updater().call_in_main(dialog.setLabelText, f"Preparing things...")
            try:
                os.chdir("SomePythonThings Music")
                log("[   OK   ] Acessed \"~/SomePythonThings Music\"")
            except FileNotFoundError:
                os.mkdir("SomePythonThings Music")
                log("[  WARN  ] \"~/SomePythonThings Music\" not found, creating it...")
                os.chdir("SomePythonThings Music")

            output_path = os.getcwd().replace("\\", "/")
            log("[   OK   ] Output path is "+output_path)

            get_updater().call_in_main(dialog.setLabelText, f"Fetching \"{name}\" links...")
            yt = YouTube(link)
            yt.register_on_progress_callback(showDownloadProgress)
            file = yt.streams.get_highest_resolution()
            downloadSize = file.filesize
            get_updater().call_in_main(dialog.setRange, 0, 101)
            get_updater().call_in_main(dialog.setLabelText, f"Downloading \"{name}\"...")
            file.download(output_path, name)
            filename = file.get_file_path(name, output_path)
            log(f"[   OK   ] File {filename} downloaded successfully")
            get_updater().call_in_main(dialog.setRange, 0, 0)

            get_updater().call_in_main(dialog.setLabelText, f"Converting \"{name}\" to mp3...")
            VideoFileClip(filename).audio.write_audiofile(filename.replace('mp4', 'mp3'))
            log(f"[   OK   ] File {filename} converted to mp3 successfully")

            try:
                os.remove(filename)
            except:
                log("[ FAILED ] Unable to remove MP4 file, going for 2nd attempt...")
                if(_platform=="win32"):
                    subprocess.call(args="taskkill /im ffmpeg-win64-v4.2.2.exe /f", shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                warn = True
            log(f"[   OK   ] File {filename} removed (because we have already the mp3)")
            oldName = filename
            filename = filename.replace('mp4', 'mp3')

            get_updater().call_in_main(dialog.close)
            get_updater().call_in_main(dialog.setAutoFillBackground,False)
            get_updater().call_in_main(dialog.setWindowFlag,QtCore.Qt.WindowContextHelpButtonHint, True)
            get_updater().call_in_main(dialog.setWindowFlag,QtCore.Qt.WindowCloseButtonHint, True)
            get_updater().call_in_main(dialog.setModal,False)
            get_updater().call_in_main(dialog.setSizeGripEnabled,True)
            get_updater().call_in_main(addFile, filename)
            if(not(warn)):
                if(_platform=="win32"):
                    get_updater().call_in_main(throw_info, "SomePythonThings Music", f"The song {name} has been saved successfully to your library")
            else:
                get_updater().call_in_main(throw_warning, "SomePythonThings Music", f"The song {name} has been saved successfully to your library, but we weren't able to delete some temporary files. We'll try to remove them later")
                try:
                    os.remove(oldName)
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

    global music
    youtube = ClosableWindow(music)
    youtube.setStyleSheet(getWindowStyleSheet())
    youtube.resize(900, 500)
    youtube.setMinimumSize(300, 200)
    youtube.setWindowTitle("Download Youtube Music")
    youtube.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
    youtube.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
    youtube.setWindowModality(QtCore.Qt.ApplicationModal)
    youtube.resized.connect(resizeWidgets)
    youtube.setAutoFillBackground(True)
    youtube.setWindowModality(QtCore.Qt.WindowModal)
    youtube.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    youtube.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
    youtube.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    query = QtWidgets.QLineEdit(youtube)
    query.setPlaceholderText("Imagine Dragons - Believer")
    query.move(10, 10)
    query.returnPressed.connect(getResults)
    query.resize(580, 30)

    button = QtWidgets.QPushButton(youtube)
    button.setText("Search")
    button.setObjectName("squarePurpleButton")
    button.move(600, 10)
    button.resize(90, 30)
    button.clicked.connect(getResults)

    results = QtWidgets.QTreeWidget(youtube)
    results.setColumnCount(7)
    results.setHeaderLabels(["#", " Name", " Download", " Duration", " Publisher", " Youtube link (Click to open)", ""])
    results.setColumnWidth(0, 20)
    results.setColumnWidth(1, 500)
    results.setColumnWidth(2, 100)
    results.setColumnWidth(3, 80)
    results.setColumnWidth(4, 120)
    results.setColumnWidth(5, 400)
    results.setColumnWidth(6, 0)
    results.setFocusPolicy(QtCore.Qt.NoFocus)
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

    query.setFocus()
    youtube.show()

def toStyleMainList():
    global playing, lists, trackNumber, music, font, t
    try:
        for item in range(0, mainList.topLevelItemCount()):
            mainList.topLevelItem(item).setFont(0, QtGui.QFont(font, weight=QtGui.QFont.Normal))
            mainList.topLevelItem(item).setIcon(0, QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(mainList.topLevelItem(item).text(2))))
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

def killPlayProcess():
    global playProcess
    playProcess.stop()

def removeFromPlaylist():
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

def playFile(file, passedTime=0):
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

    playProcess.setMedia(QtCore.QUrl(filePreset+file))
    playProcess.setPosition(int(passedTime*1000))
    playProcess.setVolume(_volume)
    playProcess.play()
    blockPlay = False

def toShuffle():
    global shuffle, buttons
    if(shuffle):
        log("[   OK   ] Shuffle disabled")
        shuffle=False
        shuffleAction.setChecked(False)
        shuffleActionTray.setChecked(False)
        buttons['shuffle'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/shuffle-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Shuffle enabled")
        shuffle=True
        shuffleAction.setChecked(True)
        shuffleActionTray.setChecked(True)
        buttons['shuffle'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/shuffle-icon.svg\") 0 0 0 0 stretch stretch")
        
def toReplay():
    global replay, buttons
    if(replay):
        log("[   OK   ] Replay disabled")
        replay=False
        replayAction.setChecked(False)
        replayActionTray.setChecked(False)
        buttons['replay'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/replay-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Replay enabled")
        replay=True
        replayAction.setChecked(True)
        replayActionTray.setChecked(True)
        buttons['replay'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/replay-icon.svg\") 0 0 0 0 stretch stretch")

def toPlay(finalized=False, track=0):
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
        log("[   OK   ] Sending pause signal...")
        albumArt.setPixmap(QtGui.QPixmap(realpath+"/icon.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
        playing=False
        toStyleMainList()
        if(finalized):
            get_updater().call_in_main(labels['songname'].setText, "No music playing")
            get_updater().call_in_main(labels['actualtime'].setText, '-:--:--')
            seekerValueManuallyChanged = False
            refreshProgressbar(0)
        buttons['play'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/play-icon.svg\") 0 0 0 0 stretch stretch")
        if(_platform=='win32'):
            WindowPlayButton.setIcon(QtGui.QIcon(realpath+"/icons-sptmusic/play-bar.ico"))

def toSkip():
    log('[   OK   ] Setting skip signal...')
    global skipped
    skipped=True
    toStrictlyPlay()

def toGoBack():
    log('[   OK   ] Setting goBack signal...')
    global goBack
    goBack=True
    toStrictlyPlay()

def toMute():
    global volume, muted, buttons, sliders
    if(muted):
        log("[   OK   ] Unmuting...")
        playProcess.setMuted(False)
        muted=False
        muteActionTray.setChecked(False)
        muteAction.setChecked(False)
        sliders['volume'].setObjectName("normal-slider")
        sliders['volume'].setStyleSheet(getWindowStyleSheet())
        buttons['audio'].setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/audio-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Muting...")
        playProcess.setMuted(True)
        muted=True
        muteActionTray.setChecked(True)
        muteAction.setChecked(True)
        sliders['volume'].setObjectName("disabled-slider")
        sliders['volume'].setStyleSheet(getWindowStyleSheet())
        buttons['audio'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/audio-off-icon.svg\") 0 0 0 0 stretch stretch")
    changeVolume()

def increaseVolume():
    sliders['volume'].setValue(sliders['volume'].value()+5)

def decreaseVolume():
    sliders['volume'].setValue(sliders['volume'].value()-5)


def changeVolume():
    global volume, muted, buttons, sliders, playing, justContinue, passedTime
    volume = sliders['volume'].value()
    log('[   OK   ] Volume changed to '+str(volume))
    if(volume>100):
        volume=100
    if(playing):
        playProcess.setVolume(volume)


def toPauseAndStopSeeking():
    stopSeeking()

def openFile():
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
            return 0
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
            newItem
            newItem.setIcon(0, QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(filename)))
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

def addFile(filepath):
    global music, elementNumber
    try:
        file = open(filepath, 'r')
        filename = file.name
        file.close()
        try:
            log('[   OK   ] File "'+str(filename)+'" processed')
            newItem =  QtWidgets.QTreeWidgetItem()
            newItem.setIcon(0, QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(filename)))
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

def toStrictlyPlay(track=0):
    startSeeking()
    global playing
    if(not(playing)):
        toPlay(track=track)

def toStrictlyPause():
    global playing, playProcess
    if(playing):
        toPlay()
        try:
            killPlayProcess()
        except AttributeError:
            pass

def saveSettings(silent=True, minimize_to_tray=False, bakcgroundPicture='None', mode='auto', volume=100, showTrackNotification=True, showEndNotification=True):
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
                "showTrackNotification": showTrackNotification,
                "showEndNotification": showEndNotification,
                "bakcgroundPicture": bakcgroundPicture,
                "mode":mode,
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

def openSettings():
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

def openSettingsWindow():
    global music, settings, settingsWindow
    settingsWindow = Window(music)
    settingsWindow.setMinimumSize(500, 300)
    settingsWindow.setMaximumSize(500, 300)
    settingsWindow.setWindowTitle("SomePythonThings Music Settings")
    settingsWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
    settingsWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
    settingsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    settingsWindow.setAutoFillBackground(True)
    settingsWindow.setWindowModality(QtCore.Qt.WindowModal)
    settingsWindow.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    settingsWindow.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
    settingsWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    modeSelector = QtWidgets.QComboBox(settingsWindow)
    modeSelector.insertItem(0, 'Light')
    modeSelector.insertItem(1, 'Dark')
    if(_platform!='linux'):
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

    saveButton = QtWidgets.QPushButton(settingsWindow)
    saveButton.setText("Save settings and close")
    saveButton.resize(460, 40)
    saveButton.move(20, 240)
    saveButton.setObjectName('squarePurpleButton')
    saveButton.clicked.connect(partial(saveAndCloseSettings, modeSelector, traySelector, volumeSpinner, settingsWindow, trackNotifier, endNotifier))

    try:
        if(settings['mode'].lower() == 'light'):
            modeSelector.setCurrentIndex(0)
        elif(settings['mode'].lower() == 'auto'):
            if(_platform!='linux'):
                modeSelector.setCurrentIndex(2)
            else:
                modeSelector.setCurrentIndex(0)
        elif(settings['mode'].lower() == 'dark'):
            modeSelector.setCurrentIndex(1)
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


    settingsWindow.show()

def saveAndCloseSettings(modeSelector: QtWidgets.QComboBox, traySelector: QtWidgets.QComboBox, volumeSpinner: QtWidgets.QSpinBox, settingsWindow, trackNotifier: QtWidgets.QCheckBox, endNotifier: QtWidgets.QCheckBox):
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
    forceClose = True
    settingsWindow.close()
    music.setStyleSheet(getWindowStyleSheet())
    saveSettings(silent=False, minimize_to_tray=settings['minimize_to_tray'], bakcgroundPicture=settings['bakcgroundPicture'], mode=settings['mode'], volume=settings['volume'], showTrackNotification=settings['showTrackNotification'], showEndNotification=settings['showEndNotification'])

def getLenght(file):
    global debugging
    try:
        return mutagen.File(filename=file).info.length
    except AttributeError:
        log(f"[ FAILED ] Unable to get file {file} length!")
        return 0


def openOnExplorer(file, force=True):
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

def openLog():
    log("[        ] Opening log...")
    os_info = f"" + \
    f"                        OS: {platform.system()}\n"+\
    f"                   Release: {platform.release()}\n"+\
    f"           OS Architecture: {platform.machine()}\n"+\
    f"          APP Architecture: {platform.architecture()[0]}\n"+\
    f"                   Program: SomePythonThings Music Version {actualVersion}"+\
    "\n\n-----------------------------------------------------------------------------------------"
    webbrowser.open("https://www.somepythonthings.tk/error-report/?appName=SomePythonThings Music&errorBody="+os_info.replace('\n', '{newline}').replace(' ', '{space}')+"{newline}{newline}{newline}{newline}SomePythonThings Music Log:{newline}"+str(logHistory+"\n\n\n\n").replace('\n', '{newline}').replace(' ', '{space}'))
    

def getFileType(file): #from file.mp3, returns MP3, from file.FiLeExT, returns FILEEXT 
    return file.split('.')[-1].upper()
    
def getSongTitle(file):
    return str(file.replace('\\', '/').split('/')[-1]).replace("."+file.split('.')[-1], '')

def startPlayback(track=0):
    global labels, skipped, playerIsRunning, playProcess, goBack, playing, trackNumber, replay, blockPlay, playingObj, justContinue, totalTime, passedTime, seeking, seekerValueManuallyChanged, starttime, song_length
    playerIsRunning = True
    stopped=False
    skipped=False
    lastTrack=""
    goBack = False
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
        while trackNumber<mainList.topLevelItemCount():
            log('[        ] Starting new play round, index is {0}'.format(str(trackNumber)))
            if not stopped:
                import time
                track = mainList.topLevelItem(trackNumber).text(2)
                log('[        ] Track number {0}'.format(trackNumber))
                log('[        ] Actual track file is '+str(track))
                log('[        ] Start time is {0} ms'.format(passedTime*1000))
                song_length = getLenght(track)
                filename = getSongTitle(track)

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
                albumArt.setPixmap(QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(track)).pixmap(256, 256).scaledToHeight(96, QtCore.Qt.SmoothTransformation))

                log("[        ] Calling play thread...")
                blockPlay = True
                get_updater().call_in_main(playFile, track, passedTime=passedTime)
                while blockPlay:
                    pass

                log("[   OK   ] Continuing play process, play line passed")

                alreadyPlayed.append(trackNumber)
                get_updater().call_in_main(buttons['play'].setStyleSheet, "background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/pause-icon.svg\") 0 0 0 0 stretch stretch")
                if(_platform=='win32'):
                    WindowPlayButton.setIcon(QtGui.QIcon(realpath+"/icons-sptmusic/pause-bar.ico"))
                get_updater().call_in_main(toStyleMainList)

                msPlayed = 0
                lenght = getLenght(track)*1000
                percentagePlayed = 0
                oldPos = -500
                repatedPositions = -4

                while(True):
                    msPlayed = playProcess.position()
                    if(lenght!=0):
                        percentagePlayed = msPlayed/lenght*100
                    loopStartTime = time.time()
                    get_updater().call_in_main(labels['actualtime'].setText, str(datetime.timedelta(seconds=int(msPlayed/1000))))

                    if(seeking):
                        seekerValueManuallyChanged = False
                        refreshProgressbar(percentagePlayed*10)


                    if(not(playing)):
                        playProcess.pause()
                        get_updater().call_in_main(toStyleMainList)
                        log('[   OK   ] Paused at moment {}'.format((time.time()-starttime)))
                        while not(playing):
                            pass
                        albumArt.setPixmap(QtWidgets.QFileIconProvider().icon(QtCore.QFileInfo(track)).pixmap(256, 256).scaledToHeight(96, QtCore.Qt.SmoothTransformation))
                        log('[        ] Continuing playback...')
                        playProcess.play()
                        get_updater().call_in_main(toStyleMainList)

                    if(skipped):
                        log('[        ] Skipping...')
                        killPlayProcess()
                        break

                    if(goBack):
                        log('[        ] Going back...')
                        killPlayProcess()
                        break

                    if(justContinue):
                        killPlayProcess()
                        log('[        ] Passing away...')
                        break

                    if(oldPos==msPlayed):
                        repatedPositions += 1
                    else:
                        repatedPositions = 0

                    if(lenght<=msPlayed or (repatedPositions>4 and msPlayed!=0)):
                        log('[  KILL  ] Killing play bucle, arrived to end...')
                        break

                    toWait = 0.05 - (time.time()-loopStartTime)
                    if(toWait>0):
                        time.sleep(toWait)
                    oldPos = msPlayed

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

def goToSong():
    global lists, trackNumber, playing, t, playerIsRunning, justContinue
    try:
        t.shouldBeRuning = False
        log('[  KILL  ] Killing playback thread to start a new one...')
    except AttributeError:
        log('[  WARN  ] Unable to kill thread, thread was not running...')
    trackNumber = mainList.indexOfTopLevelItem(mainList.currentItem())
    if(trackNumber<0):
        trackNumber = 0
    log('[   OK   ] Selected track number {}'.format(trackNumber))
    playerIsRunning = False
    playing = False
    toStrictlyPlay(track=trackNumber)

def goToMaybeSpecificTime():
    global sliders, totalTime, passedTime, justContinue, seeking, seekerValueManuallyChanged, starttime, song_length
    if(seekerValueManuallyChanged):
        timeToGo = seeker.value()*(song_length)/1000
        log('[        ] Starting goToSpecificTime with time value : '+str(timeToGo))
        justContinue = True
        passedTime=timeToGo
        seekerValueManuallyChanged = False
    else:
        seekerValueManuallyChanged = True

def goToSpecificTime():
    global sliders, totalTime, passedTime, justContinue, seeking, seekerValueManuallyChanged, starttime, song_length
    timeToGo = seeker.value()*(song_length)
    log('[        ] Starting goToSpecificTime with time value (in ms): '+str(timeToGo))
    playProcess.setPosition(int(timeToGo))
    startSeeking()
    passedTime = playProcess.position()/1000
    seekerValueManuallyChanged = False

def stopSeeking():
    log('[        ] Stopping seeking...')
    global seeking
    seeking=False

def startSeeking():
    global seeking
    log('[        ] Starting seeking...')
    time.sleep(0.1)
    seeking=True

def getList():
    for i in range(mainList.topLevelItemCount()):
        item = mainList.topLevelItem(i)
        yield item.text(2)

def savePlaylist():
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
                    toWrite += str(element)
                    toWrite += "\n"
                toWrite += "###"
                file.write(toWrite)
                file.close()
                throw_info('SomePythonThings Music', 'Playlist saved successfully!')
            except Exception as e:
                file.close()
                log('[  FAILED ] An error occurred while writing data to the file...')
                raise e
    except Exception as e:
        if(debugging):
            raise e
        throw_error('SomePythonThings Music', 'Unable to save playlist.\n\nError details:\n'+str(e))

def removeAllItems():
    global lists
    while mainList.topLevelItemCount()>0:
        try:
            mainList.clear()
        except Exception as e:
            if(debugging):
                raise e

def showMusic(reason=QtWidgets.QSystemTrayIcon.Unknown):
    if(reason != QtWidgets.QSystemTrayIcon.Context):
        music.show()
        music.raise_()
        music.activateWindow()
        if not(music.isMaximized()):
            music.showNormal()

def openPlaylist(playlist=''):
    global music, elementNumber
    toStrictlyPause()
    removeAllItems()
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
                return 0
        else:
            filepath = playlist
            playAfter = True
        file = open(filepath, 'r')
        content = file.read()
        filename = file.name
        file.close()
        try:
            if(len(content.split("###"))<2):
                raise NotImplementedError('This platlist file is not a valid .sptplaylist file!')
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

def refreshProgressbar(value):
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

def installationProgressBar(action = 'Downloading'):
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

def throw_info(title, body, icon="ok.png", exit=False):
    global music
    showMusic()
    log("[  INFO  ] "+body)
    msg = QtWidgets.QMessageBox(music)
    if(os.path.exists(str(realpath)+"/icons-sptmusic/ok.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/icons-sptmusic/ok.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(body)
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

def throw_warning(title, body, warning=None):
    global music
    showMusic()
    log("[  WARN  ] "+body)
    if(warning != None ):
        log("\t Warning reason: "+warning)
    msg = QtWidgets.QMessageBox(music)
    if(os.path.exists(str(realpath)+"/icons-sptmusic/warn.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/icons-sptmusic/warn.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Warning)
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

def throw_error(title, body, error="Not Specified"):
    global music
    showMusic()
    log("[  ERROR ] "+body+"\n\tError reason: "+error)
    msg = QtWidgets.QMessageBox(music)
    if(os.path.exists(str(realpath)+"/icons-sptmusic/error.png")):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/icons-sptmusic/error.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Critical)
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

def updates_thread():
    log("[        ] Starting check for updates thread...")
    checkUpdates_py()
 
def quitMusic():
    log("[  INFO  ] Quitting application...")
    global music
    music.close()
    try:        
        killPlayProcess()
    except AttributeError:
        pass
    sys.exit()

def checkDirectUpdates():
    global actualVersion
    result = checkUpdates_py()
    if(result=='No'):
        throw_info("SomePythonThings Music Updater", "There aren't updates available at this time. \n(The installed version is {0})".format(actualVersion))
    elif(result=="Unable"):
        throw_warning("SomePythonThings Music Updater", "Can't reach SomePythonThings Servers!\n  - Are you connected to the internet?\n  - Is your antivirus or firewall blocking SomePythonThings Music?\nIf none of these solved the problem, please check back later.")

def openHelp():
    webbrowser.open_new("http://www.somepythonthings.tk/programs/somepythonthings-music/help/")

def about():
    throw_info("About SomePythonThings Music", "SomePythonThings Music\nVersion "+str(actualVersion)+"\n\nThe SomePythonThings Project\n\n © 2021 Martí Climent, SomePythonThings\nhttps://www.somepythonthings.tk\n\n\nThe iconset has a CC Non-Commercial Atribution 4.0 License", exit=False)

def readArgs(args):
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

def setProgramAsRunning():
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
                return 0
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
                    if(not(os.path.exists('running.lock'))):
                        with open('running.lock', mode='a'): pass
                    if(os.path.exists('show.lock')):
                        log('[        ] Showing SomePythonThimgs Music...')
                        try:
                            get_updater().call_in_main(music.show)
                            get_updater().call_in_main(music.raise_)
                            get_updater().call_in_main(music.activateWindow)
                            get_updater().call_in_main(music.showNormal)
                            os.remove('show.lock')
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
                                os.remove('show.lock')
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

def on_key(key):
    global volume, sliders
    if key == QtCore.Qt.Key_Space:
        toPlay(finalized=False)
    elif key == QtCore.Qt.Key_Minus:
        sliders['volume'].setValue(sliders['volume'].value()-10)
    elif key == QtCore.Qt.Key_Plus:
        sliders['volume'].setValue(sliders['volume'].value()+10)
    elif key == QtCore.Qt.Key_Left:
        seeker.setValue(seeker.value()-10)
    elif key == QtCore.Qt.Key_Right:
        seeker.setValue(seeker.value()+10)
    elif key == QtCore.Qt.Key_Backspace:
        removeFromPlaylist()
    elif key == QtCore.Qt.Key_Delete:
        removeFromPlaylist()
    elif key == QtCore.Qt.Key_Enter:
        goToSong()
    elif key == QtCore.Qt.Key_Play:
        toPlay()
    elif key == QtCore.Qt.Key_Pause:
        toPlay()
    elif key == QtCore.Qt.Key_MediaPlay:
        toPlay()
    elif key == QtCore.Qt.Key_MediaPause:
        toPlay()
    elif key == QtCore.Qt.Key_MediaPrevious:
        toGoBack()
    elif key == QtCore.Qt.Key_MediaNext:
        toSkip()
    #else:
    #   log('key pressed: %i' % key)

def resizeWidgets():
    global music, buttons, texts, progressbars, font
    height = music.height()
    width = music.width()
        
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

    mainList.move(170, 40)
    mainList.resize(width-190, height-180)

    log("[   OK   ] Resizing content to fit "+str(width)+'x'+str(height))
    bottomBar.resize(width, 120)
    bottomBar.move(0, height-120)

def openLibrary():
    openOnExplorer(os.path.expanduser("~").replace("\\", '/')+"/SomePythonThings Music/", force=True)

def load_library():
    global music_extensions, log, addFile
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
    

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------------- Main Code ---------------------------------------------------------------------------------- #
if __name__ == '__main__':

    Thread(target=setProgramAsRunning, daemon=True).start()
    
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    

    os.chdir(os.path.expanduser("~"))

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
        if(os.path.exists("\\Program Files\\SomePythonThingsMusic\\resources-sptmusic")):
            realpath = "/Program Files/SomePythonThingsMusic/resources-sptmusic"
            log("[   OK   ] Directory set to /Program Files/SomePythonThingsMusic/resources-sptmusic")
        else:
            realpath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
            log("[  WARN  ] Directory /Program Files/SomePythonThingsMusic/ not found, getting working directory...")
    else:
        log("[  WARN  ] Unable to detect OS")

    log("[   OK   ] Platform is {0}, font is {1} and real path is {2}".format(_platform, font, realpath))
    

    background_picture_path='{0}/background-sptmusic.jpg'.format(realpath.replace('c:', 'C:'))
    black_picture_path='{0}/black-sptmusic.png'.format(realpath.replace('c:', 'C:'))
    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            global background_picture_path
            MainWindow.setObjectName("MainWindow")
            MainWindow.setWindowTitle("MainWindow")
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            #self.centralwidget.setStyleSheet("""border-image: url(\""""+background_picture_path+"""\") 0 0 0 0 stretch stretch;""")
            log("[        ] Background picture real path is "+background_picture_path)
            MainWindow.setCentralWidget(self.centralwidget)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

    class Window(QtWidgets.QMainWindow):
        resized = QtCore.Signal()
        keyRelease = QtCore.Signal(int)

        def __init__(self, parent=None):
            super(Window, self).__init__(parent=parent)
            ui = Ui_MainWindow()
            ui.setupUi(self)
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
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle('fusion')
    music = Window()
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

        bottomBar = QtWidgets.QProgressBar(music)
        bottomBar.setTextVisible(False)
        bottomBar.setMinimum(0)
        bottomBar.setMaximum(1000)
        bottomBar.setValue(0)

        playProcess = QtMultimedia.QMediaPlayer(music)
        playProcess.setAudioRole(QtMultimedia.QAudio.MusicRole)

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

        albumArt = QtWidgets.QLabel(music)
        albumArt.resize(96, 96)
        albumArt.setPixmap(QtGui.QPixmap(realpath+"/icon.png").scaledToHeight(96, QtCore.Qt.SmoothTransformation))


        mainList = TreeWidget(music)
        
        mainList.setColumnCount(5)
        mainList.setHeaderLabels(["  Song Title", "  Duration", "  Location", "  Size", "  File Type"])
        mainList.setColumnWidth(0, 400)
        mainList.setColumnWidth(1, 80)
        mainList.setColumnWidth(2, 300)
        mainList.setColumnWidth(3, 100)
        mainList.setColumnWidth(4, 80)
        mainList.setFocusPolicy(QtCore.Qt.NoFocus)
        mainList.setIconSize(QtCore.QSize(24, 24))
        mainList.setSortingEnabled(True)
        mainList.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        mainList.setVerticalScrollMode(QtWidgets.QTreeWidget.ScrollPerPixel)
        mainList.setHorizontalScrollMode(QtWidgets.QTreeWidget.ScrollPerPixel)
        mainList.itemDoubleClicked.connect(goToSong)

        menuBar = music.menuBar()
        menuBar.setNativeMenuBar(False)

        
        icon = QtGui.QIcon("{0}/icon-sptmusic.png".format(realpath))
        tray = QtWidgets.QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setToolTip("SomePythonThings Music")
        tray.setVisible(True)
        trayMenu = QtWidgets.QMenu()
        tray.setContextMenu(trayMenu)
        tray.messageClicked.connect(showMusic)
        tray.activated.connect(showMusic)


        fileMenu = menuBar.addMenu("File")
        openAction = QtWidgets.QAction("Open     ", music)
        openAction.triggered.connect(openFile)
        fileMenu.addAction(openAction)
        quitAction = QtWidgets.QAction("Quit     ", music)
        quitAction.triggered.connect(quitMusic)
        fileMenu.addAction(quitAction)
        hideMusicAction = QtWidgets.QAction("Hide     ", music)
        hideMusicAction.triggered.connect(music.hide)
        fileMenu.addAction(hideMusicAction)

        fileMenu = trayMenu.addMenu("File")
        openAction = QtWidgets.QAction("Open     ", music)
        openAction.triggered.connect(openFile)
        fileMenu.addAction(openAction)
        quitAction = QtWidgets.QAction("Quit     ", music)
        quitAction.triggered.connect(quitMusic)
        fileMenu.addAction(quitAction)
        hideMusicAction = QtWidgets.QAction("Hide     ", music)
        hideMusicAction.triggered.connect(music.hide)
        fileMenu.addAction(hideMusicAction)


        playbackMenu = menuBar.addMenu("Playback")
        volumeMenu = playbackMenu.addMenu("Volume    ")
        increaseAction = QtWidgets.QAction("Increase    ", music)
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
        increaseAction = QtWidgets.QAction("Increase    ", music)
        increaseAction.triggered.connect(increaseVolume)
        volumeMenu.addAction(increaseAction)
        decreaseAction = QtWidgets.QAction("Decrease    ", music)
        decreaseAction.triggered.connect(decreaseVolume)
        volumeMenu.addAction(decreaseAction)
        muteActionTray = QtWidgets.QAction("Mute    ", music)
        muteActionTray.triggered.connect(toMute)
        muteActionTray.setCheckable(True)
        volumeMenu.addAction(muteActionTray)
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
        shuffleActionTray = QtWidgets.QAction("Shuffle    ", music)
        shuffleActionTray.triggered.connect(toShuffle)
        shuffleActionTray.setCheckable(True)
        playbackMenu.addAction(shuffleActionTray)
        replayActionTray = QtWidgets.QAction("Replay    ", music)
        replayActionTray.triggered.connect(toReplay)
        replayActionTray.setCheckable(True)
        playbackMenu.addAction(replayActionTray)


        
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
        openFilesAction = QtWidgets.QAction("Add file(s) ", music)
        openFilesAction.triggered.connect(openFile)
        playlistMenu.addAction(openFilesAction)
        deleteTrackAction = QtWidgets.QAction("Remove selected track ", music)
        deleteTrackAction.triggered.connect(removeFromPlaylist)
        playlistMenu.addAction(deleteTrackAction)
        savePlaylistAction = QtWidgets.QAction("Save playlist to file ", music)
        savePlaylistAction.triggered.connect(savePlaylist)
        playlistMenu.addAction(savePlaylistAction)
        openPlaylistAction = QtWidgets.QAction("Open playlist from file ", music)
        openPlaylistAction.triggered.connect(openPlaylist)
        playlistMenu.addAction(openPlaylistAction)


        libraryMenu = menuBar.addMenu("Library")
        openOnExplorerAction = QtWidgets.QAction("Show on explorer ", music)
        openOnExplorerAction.triggered.connect(openLibrary)
        libraryMenu.addAction(openOnExplorerAction)
        loadTrackAction = QtWidgets.QAction("Load library... ", music)
        loadTrackAction.setShortcut("Ctrl+l")
        loadTrackAction.triggered.connect(load_library)
        libraryMenu.addAction(loadTrackAction)

        libraryMenu = trayMenu.addMenu("Library")
        openOnExplorerAction = QtWidgets.QAction("Show on explorer ", music)
        openOnExplorerAction.triggered.connect(openLibrary)
        libraryMenu.addAction(openOnExplorerAction)
        loadTrackAction = QtWidgets.QAction("Load library... ", music)
        loadTrackAction.triggered.connect(load_library)
        libraryMenu.addAction(loadTrackAction)


        settingsMenu = menuBar.addMenu("Settings")
        logAction = QtWidgets.QAction(" Open Log", music)
        logAction.triggered.connect(openLog)
        settingsMenu.addAction(logAction)
        openSettingsAction = QtWidgets.QAction(" Settings...    ", music)
        openSettingsAction.triggered.connect(openSettingsWindow)
        settingsMenu.addAction(openSettingsAction)

        helpMenu = menuBar.addMenu("Help")
        openHelpAction = QtWidgets.QAction("Online manual", music)
        openHelpAction.triggered.connect(openHelp)
        helpMenu.addAction(openHelpAction)
        updatesAction = QtWidgets.QAction("Check for updates", music)
        updatesAction.triggered.connect(checkDirectUpdates)
        helpMenu.addAction(updatesAction)
        aboutAction = QtWidgets.QAction("About SomePythonThings Music    ", music)
        aboutAction.triggered.connect(about)
        helpMenu.addAction(aboutAction)

        helpMenu = trayMenu.addMenu("Help")
        openHelpAction = QtWidgets.QAction("Online manual", music)
        openHelpAction.triggered.connect(openHelp)
        helpMenu.addAction(openHelpAction)
        updatesAction = QtWidgets.QAction("Check for updates", music)
        updatesAction.triggered.connect(checkDirectUpdates)
        helpMenu.addAction(updatesAction)
        aboutAction = QtWidgets.QAction("About SomePythonThings Music    ", music)
        aboutAction.triggered.connect(about)
        helpMenu.addAction(aboutAction)
        
        showMusicAction = QtWidgets.QAction("Show SomePythonThigs Music ", music)
        showMusicAction.triggered.connect(showMusic)
        trayMenu.addAction(showMusicAction)

        quitMusicAction = QtWidgets.QAction("Quit SomePythonThigs Music ", music)
        quitMusicAction.triggered.connect(quitMusic)
        trayMenu.addAction(quitMusicAction)
        if(len(sys.argv)>1):
            if('runanyway' in sys.argv[1].lower()):
                goRun=True
                canRun=True
        while(not(goRun)): pass
        if(canRun):
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
            Thread(target=updates_thread, daemon=True).start()
            Thread(target=checkModeThread, daemon=True).start()
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
        webbrowser.open("https://www.somepythonthings.tk/error-report/?appName=SomePythonThings Music&errorBody="+os_info.replace('\n', '{newline}').replace(' ', '{space}')+"{newline}{newline}{newline}{newline}SomePythonThings Music Log:{newline}"+str(logHistory+"\n\n\n\n"+traceback_info).replace('\n', '{newline}').replace(' ', '{space}'))
        if(debugging):
            raise e
    try:        
        killPlayProcess()
    except AttributeError:
        pass
log('[  EXIT  ] Reached end of the script')
