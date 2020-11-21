#Modules
import os
import sys
import time
import wget
import json
import pydub
import random
import platform
import datetime
import subprocess
import webbrowser
import darkdetect
import pydub.playback
import simpleaudio as sa
from sys import platform as _platform
from ast import literal_eval
from PyQt5 import QtWidgets, QtGui, QtCore
from notifypy import Notify
from functools import partial
from threading import Thread
from urllib.request import urlopen
from qt_thread_updater import get_updater

#Globals
debugging = False
volume = 100
actualVersion = 1.0
shuffle = False
replay = False
playing = False
muted = False
skipped = False
goBack = False
font = ""
realpath = "."
music_files = ('Common Media Files (*.wav; *.mp3; *.pcm; *.aiff; *.aac; *.ogg; *.wma; *.flac);;Other media files (*.*)')
files = []
buttons = {}
texts = {}
progressbars = {}
lists = {}
labels = {}
sliders = {}
playerIsRunning = False
t = None # t will be defined after KillableThread class definition
elementNumber = 0
trackNumber = 0
playingObj = None
justContinue = False
lastConvertedTrack = ''
totalTime = 0
passedTime = 0
seeking = True
seekerValueManuallyChanged = False
starttime = 0 
playedTime = 0
song_length = 0
background_picture_path = ''
settingsWindow = None
forceClose = False
goRun=False
canRun=True
settings = { #Default settings loaded, those which change will be overwritten
    "settings_version": actualVersion,
    "minimize_to_tray": False,
    "bakcgroundPicture":"None",
    "mode":'auto',
    }
defaultSettings = {
    "settings_version": actualVersion,
    "minimize_to_tray": False,
    "bakcgroundPicture":"None",
    "mode":'auto',
}

#StyleSheets:
lightModeStyleSheet = """
    * {{
        color: #000000;
        font-size:14px;
        font-family:{0};
        background-color: #FFFFFF;
    }}

    #centralwidget {{
        border-image: url(\"{1}\") 0 0 0 0 stretch stretch;
    }}

    QPushButton {{
        border-image: none;
        background-color:  rgba(15, 140, 140, 1.0);
        width: 100px;
        height: 30px;
        color: #FFFFFF;
        border-radius: 3px;
    }}

    QScrollBar
    {{
        background-color: rgb(30, 200, 200);
    }}

    QScrollBar:vertical
    {{
        background-color: rgb(30, 200, 200);
    }}

    QScrollBar::handle:vertical 
    {{
        margin-top: 17px;
        margin-bottom: 17px;
        border: none;
        min-height: 30px;
        background-color: rgba(255, 255, 255, 1);
    }}

    QScrollBar::add-line:vertical 
    {{
        border: none;
        background-color: rgba(255, 255, 255, 1);
    }}

    QScrollBar::sub-line:vertical 
    {{
        border: none;
        background-color: rgba(255, 255, 255, 1);
    }}

    QScrollBar:horizontal
    {{
        background: rgb(30, 200, 200);
    }}

    QScrollBar::handle:horizontal 
    {{
        margin-left: 17px;
        margin-right: 17px;
        border: none;
        min-width: 30px;
        background-color: rgba(255, 255, 255, 1);
    }}

    QScrollBar::add-line:horizontal 
    {{
        border: none;
        background-color: rgba(255, 255, 255, 1);
    }}

    QScrollBar::sub-line:horizontal 
    {{
        border: none;
        background-color: rgba(255, 255, 255, 1);
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
    QAbstractItemView {{
        background-color: rgb(255, 255, 255);
        margin: 0px;
        border-radius: 3px;
    }}

    QMenuBar {{
        background-color: #FFFFFF;
        color: #000000;
    }}

    QMenu {{
        background-color: #FFFFFF;
        border-radius: 10px;
    }}

    QMenu::item {{
        border: 3px solid #FFFFFF;
        padding-right: 10px;
        padding-left: 5px;
        padding: 3px;
        color: #000000;
        padding-left: 8px;
    }}

    QMenu::item:selected {{
        border: 3px solid rgba(20, 170, 170, 1.0);
        background-color: rgba(20, 170, 170, 1.0);
    }}
    QMenuBar::item {{
        background-color: #FFFFFF;
        border: 3px solid  #FFFFFF;
        padding-right: 5px;
        padding-left: 5px;
    }}

    QMenuBar::item:selected {{
        background-color: rgba(20, 170, 170, 1.0);
        border: 3px solid rgba(20, 170, 170, 1.0);
    }}

    QSlider {{
        background-color: none;
    }}

    QSlider::handle:horizontal {{
        border-radius: 7px;
        background-color: rgba(20, 170, 170, 1.0);/*20, 170, 170, 1.0*/
        border: 0px solid rgba(00, 100, 100, 1.0);
    }}

    QSlider::add-page:horizontal {{
        background-color: #EEEEEE;
        border: 1px solid #BBBBBB;
        border-radius: 2px;
    }}

    QSlider::sub-page:horizontal {{
        background-color: rgba(20, 170, 170, 1.0);
        border: 1px solid rgba(20, 140, 140, 1.0);
        border-radius: 2px;
    }}

    QLabel {{
         color: #000000;
    }}

    QListWidget {{
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
    }}

    QListWidget::item
    {{
        background-color: rgba(255, 255, 255, 0.0);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(255, 255, 255);
    }}

    QListWidget::item:hover
    {{
        background-color: rgba(255, 255, 255, 0.3);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(255, 255, 255);
    }}

    QListWidget::item:selected
    {{
        background-color: rgba(20, 170, 170, 0.5);
        padding: 5px;
        padding-left: 10px;
        outline: 50px;
        border-bottom: 1px solid rgb(255, 255, 255);
    }}

    QGroupBox {{
        background-color: rgba(255, 255, 255, 0.5);
        border-top: 1px solid rgb(255, 255, 255);
    }}

    #squarePurpleButton {{
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
        color: black;
    }}
    
    #squarePurpleButton:hover {{
        background-color: rgba(20, 170, 170, 0.5);
        color: black;
    }}

    #squareRedButton {{
        border-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5);
        color: black;
    }}

    #squareRedButton:hover {{
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

    #settingsBackground {{
        background-color: rgba(255, 255, 255, 0.5);
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
        border: 1px solid rgb(255, 255, 255);
        border-right: none;
    }}

    QProgressBar {{
        border: none;
        border-radius: 0px;
        border-top: 1px solid rgb(255, 255, 255);
        background-color: rgba(255, 255, 255, 0.5)
    }}

    QProgressBar::chunk
    {{
        background-color: rgba(20, 180, 180, 0.5);
    }}
"""

darkModeStyleSheet = """
    * {{
        color: #EEEEEE;
        font-size:14px;
        font-family:{0};
        background-color: #333333;
    }}

    #centralwidget {{
        border-image: url(\"{1}\") 0 0 0 0 stretch stretch;
    }}

    QPushButton {{
        border-image: none;
        background-color:  rgba(15, 140, 140, 1.0);
        width: 100px;
        height: 30px;
         color: #EEEEEE;
        border-radius: 3px;
    }}

    QScrollBar
    {{
        background-color: rgba(0, 100, 100, 1.0);
    }}

    QScrollBar:vertical
    {{
        background-color: rgb(10, 150, 150);
    }}

    QScrollBar::handle:vertical 
    {{
        margin-top: 17px;
        margin-bottom: 17px;
        border: none;
        min-height: 30px;
        background-color: rgba(51, 51, 51, 1);
    }}

    QScrollBar::add-line:vertical 
    {{
        border: none;
        background-color: rgba(51, 51, 51, 1);
    }}

    QScrollBar::sub-line:vertical 
    {{
        border: none;
        background-color: rgba(51, 51, 51, 1);
    }}

    QScrollBar:horizontal
    {{
        background: rgb(10, 150, 150);
    }}

    QScrollBar::handle:horizontal 
    {{
        margin-left: 17px;
        margin-right: 17px;
        border: none;
        min-width: 30px;
        background-color: rgba(51, 51, 51, 1);
    }}

    QScrollBar::add-line:horizontal 
    {{
        border: none;
        background-color: rgba(51, 51, 51, 1);
    }}

    QScrollBar::sub-line:horizontal 
    {{
        border: none;
        background-color: rgba(51, 51, 51, 1);
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
    QAbstractItemView {{
        background-color: rgb(41, 41, 41);
        margin: 0px;
        border-radius: 3px;
    }}

    QMenuBar {{
        background-color: #333333;
        color: #EEEEEE;;
    }}

    QMenu {{
        background-color: #333333;
        border-radius: 10px;
    }}

    QMenu::item {{
        border: 3px solid #333333;
        padding-right: 10px;
        padding-left: 5px;
        padding: 3px;
        color: #EEEEEE;;
        padding-left: 8px;
    }}

    QMenu::item:selected {{
        border: 3px solid rgba(15, 140, 140, 1.0);
        background-color: rgba(15, 140, 140, 1.0);
    }}
    QMenuBar::item {{
        background-color: #333333;
        border: 3px solid  #333333;
        padding-right: 5px;
        padding-left: 5px;
    }}

    QMenuBar::item:selected {{
        background-color: rgba(15, 140, 140, 1.0);
        border: 3px solid  rgba(15, 140, 140, 1.0);
    }}

    QSlider {{
        background-color: none;
    }}

    QSlider::handle:horizontal {{
        border-radius: 7px;
        background-color: rgba(20, 170, 170, 1.0);/*20, 170, 170, 1.0*/
        border: 0px solid rgba(00, 100, 100, 1.0);
    }}

    QSlider::add-page:horizontal {{
        background-color: #333333;
        border: 1px solid #222222;
        border-radius: 2px;
    }}

    QSlider::sub-page:horizontal {{
        background-color: rgba(20, 170, 170, 1.0);
        border: 1px solid rgba(0, 100, 100, 1.0);
        border-radius: 2px;
    }}

    QLabel {{
         color: #EEEEEE;
    }}

    QListWidget {{
        background-color: rgba(51, 51, 51, 0.5);
        border-radius: 3px;
        border: 1px solid rgb(51, 51, 51);
    }}

    QListWidget::item
    {{
        background-color: rgba(51, 51, 51, 0.0);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(51, 51, 51);
    }}

    QListWidget::item:hover
    {{
        background-color: rgba(51, 51, 51, 0.3);
        padding: 5px;
        padding-left: 10px;
        border: none;
        border-bottom: 1px solid rgb(51, 51, 51);
    }}

    QListWidget::item:selected
    {{
        background-color: rgba(20, 170, 170, 0.5);
        padding: 5px;
        padding-left: 10px;
        outline: 50px;
        border-bottom: 1px solid rgb(51, 51, 51);
    }}

    QGroupBox {{
        background-color: rgba(51, 51, 51, 0.5);
        border-top: 1px solid rgb(51, 51, 51);
    }}

    #squarePurpleButton {{
        border-radius: 3px;
        border: 1px solid rgb(51, 51, 51);
        background-color: rgba(51, 51, 51, 0.5);
        color: white;
    }}
    
    #squarePurpleButton:hover {{
        background-color: rgba(20, 170, 150, 0.5);
        color: white;
    }}

    #squareRedButton {{
        border-radius: 3px;
        border: 1px solid rgb(51, 51, 51);
        background-color: rgba(51, 51, 51, 0.5);
        color: white;
    }}

    #squareRedButton:hover {{
        background-color: rgba(255, 0, 0, 0.5);
        color: white;
    }}

    QComboBox
    {{   
        border-image: none;
        selection-background-color: rgba(20, 170, 150, 1.0);
        margin:0px;
        border: 1px solid rgb(51, 51, 51);
        background-color: rgba(51, 51, 51, 0.5);
        border-radius: 0px;
        padding-left: 7px;
        border-bottom-right-radius: 3px;
        border-top-right-radius: 3px;
    }}

    #settingsBackground {{
        background-color: rgba(51, 51, 51, 0.5);
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
        border: 1px solid rgb(51, 51, 51);
        border-right: none;
    }}

    QProgressBar {{
        border: none;
        border-radius: 0px;
        border-top: 1px solid rgb(51, 51, 51);
        background-color: rgba(51, 51, 51, 0.5)
    }}

    QProgressBar::chunk
    {{
        background-color: rgba(10, 150, 150, 0.5);
    }}
"""

#Functions
def log(s, force=True):
    global debugging
    if(debugging or "WARN" in str(s) or "FAILED" in str(s) or not(force)):
        print((time.strftime('[%H:%M:%S] ', time.gmtime(time.time())))+str(s))

def notify(title, body, icon='icon-sptmusic.png'):
    global realpath
    notify=False
    if _platform == 'win32':
        if int(platform.release()) >= 10:
            notify=True
    elif _platform == 'darwin':
        notify=False
    elif _platform == 'linux' or _platform=='linux2':
        notify=True
    if(notify):
        try:
            notification = Notify()
            notification.title = str(title)
            notification.message = str(body)
            try:
                notification.icon = realpath+'/'+icon
            except:
                pass
            notification.send(block=True)
        except Exception as e:
            log("[  FAILED ] Unable to show notification: "+str(e))

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
        os.system('start /B {0}'.format(filename))
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
    #get_updater().call_in_main(texts["create"].setPlainText, "The program is being installed. Please wait until the installation process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
    #get_updater().call_in_main(texts["extract"].setPlainText, "The program is being installed. Please wait until the installation process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
    p1 = os.system('cd; echo "{0}" | sudo -S apt install ./"somepythonthings-music_update.deb" -y'.format(passwd))
    if(p1 == 0):  # If the installation is done
        p2 = os.system('cd; rm "./somepythonthings-music_update.deb"')
        if(p2 != 0):  # If the downloaded file cannot be removed
            log("[  WARN  ] Could not delete update file.")
        installationProgressBar('Installing')
        get_updater().call_in_main(throw_info,"SomePythonThings Music Updater","The update has been applied succesfully. Please reopen the application")
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
        #get_updater().call_in_main(texts["create"].setPlainText, "The installer is being downloaded. Please wait until the download process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
        #get_updater().call_in_main(texts["extract"].setPlainText, "The installer is being downloaded. Please wait until the download process finishes. This shouldn't take more than a couple of minutes.\n\nPlease DO NOT close the application")
        p1 = os.system('cd; rm somepythonthings-music_update.dmg')
        if(p1!=0):
            log("[  WARN  ] unable to delete somepythonthings-music_update.dmg")
            #raise SystemError("Unable to delete somepythonthings-music_update.dmg, process exit code "+str(p1))
        print(links['macos'])
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
    #get_updater().call_in_main(texts["create"].setPlainText, "Please follow on-screen instructions to continue")
    #get_updater().call_in_main(texts["extract"].setPlainText, "Please follow on-screen instructions to continue")
    throw_info("SomePythonThings Music Updater", "The update file has been downloaded successfully. When you click OK, SomePythonThings Music is going to be closed and a DMG file will automatically be opened. Then, you'll need to drag the application on the DMG to the applications folder (also on the DMG). Click OK to continue")
    p2 = os.system('cd; open ./"somepythonthings-music_update.dmg"')
    log("[  INFO  ] macOS installation unix output code is \"{0}\"".format(p2))
    sys.exit()

def install_ffmpeg_linux_part1(again=False):
    global music
    if(QtWidgets.QMessageBox.Ok == QtWidgets.QMessageBox.question(music, 'SomePythonThings Music Assistant', "SomePythoThings Music needs to install the following packages in order to run: \"ffmpeg\", \"libavcodec-extra\"\nIf you click OK, SomePythonThings Music will download and install the required packages.", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Ok)):
        installationProgressBar('Installing')
        time.sleep(0.2)
        if not again:
            passwd = str(QtWidgets.QInputDialog.getText(music, "Autentication needed - SomePythonThings Music Assistant", "Please write your password to perform the ffmpeg installation. \nThis password is NOT going to be stored anywhere in any way and it is going to be used ONLY for the update.\nIf you want, you can check that on the source code on github: \n(https://github.com/martinet101/SomePythonThings-Music/)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0])
        else:
            passwd = str(QtWidgets.QInputDialog.getText(music, "Autentication needed - SomePythonThings Music Assistant", "An error occurred while autenticating. Insert your password again (This attempt will be the last one)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0])
        t = Thread(target=install_ffmpeg_linux_part2, args=(passwd, again))
        t.start()

def install_ffmpeg_linux_part2(passwd, again=False):
    installationProgressBar('Installing')
    p1 = os.system('cd; echo "{0}" | sudo -S apt install ffmpeg libavcodec-extra -y'.format(passwd))
    if(p1 == 0):  # If the installation is done
        installationProgressBar('Installing')
        get_updater().call_in_main(throw_info,"SomePythonThings Music Assistant","Ffmpeg was installed successfully. Please restart the application")
        get_updater().call_in_main(sys.exit)
        sys.exit()
    else:  # If the installation is falied on the 1st time
        if not again:
            get_updater().call_in_main(install_ffmpeg_linux_part1, True)
        else:
            installationProgressBar('Stop')
            get_updater().call_in_main(throw_error, "SomePythonThings Music Assistant", "Unable to apply the update. Please try again later.")

def download_ffpmeg_win():
    try:
        response = urlopen("http://www.somepythonthings.tk/resources/ffmpeg-win.res")
        url = response.read().decode("utf8")
        global texts
        os.system('cd %windir%\\..\\ & mkdir SomePythonThings')
        time.sleep(0.01)
        get_updater().call_in_main(throw_info, 'SomePythonThings Music', 'SomePythonThings Music needs ffmpeg to be installed on your computer in order to run. \nFfmpeg is going to be downloaded and prepared for the installation. Please wait until the download is finished.\nPress OK to continue')
        os.chdir("{0}/../SomePythonThings".format(os.environ['windir']))
        installationProgressBar('Downloading')
        filedata = urlopen(url)
        datatowrite = filedata.read()
        filename = ""
        with open("{0}/../SomePythonThings/SomePythonThings-Music-Ffmpeg-Installer.exe".format(os.environ['windir']), 'wb') as f:
            f.write(datatowrite)
            filename = f.name
        installationProgressBar('Launching')
        log("[   OK   ] file downloaded to C:\\SomePythonThings\\{0}".format(filename))
        get_updater().call_in_main(launch_ffmpeg_win, filename)
    except Exception as e:
        if debugging:
            raise e
        get_updater().call_in_main(throw_error, "SomePythonThings Music", "An error occurred while downloading the SomePythonTings Music installer. Please check your internet connection and try again later\n\nError Details:\n{0}".format(str(e)))

def launch_ffmpeg_win(filename):
    try:
        installationProgressBar('Launching')
        throw_info("SomePythonThings Music Updater", "The file has been downloaded successfully and the setup will start now. When clicking OK, the application will close and a User Account Control window will appear. Click Yes on the User Account Control Pop-up asking for permissions to launch SomePythonThings-Music-Ffmpeg-Installer.exe. Then follow the on-screen instructions.")
        os.system('start /B {0}'.format(filename))
        get_updater().call_in_main(sys.exit)
        sys.exit()
    except Exception as e:
        if debugging:
            raise e
        throw_error("SomePythonThings Music Updater", "An error occurred while launching the Ffmpeg installer.\n\nError Details:\n{0}".format(str(e)))

def download_ffmpeg_macOS():
    get_updater().call_in_main(throw_info, 'SomePythonThings Music Assistant', "SomePythonThings Music needs ffmpeg in order to play music. Ffmpeg installer is going to be downloaded and installed. Click OK to continue.")
    url = "https://www.somepythonthings.tk/resources/ffmpeg-mac.res"
    os.chdir(os.path.expanduser('~'))
    installationProgressBar()
    filename = wget.download(url, out="resources.res")
    file = open(filename, 'r')
    url = file.read()
    file.close()
    os.system('cd; rm resources.res')
    os.system('cd; rm {0}/ffmpeg-plugin-for-somepythonthings-music.pkg'.format(os.path.expanduser('~')))
    filename = wget.download(url, out='{0}/ffmpeg-plugin-for-somepythonthings-music.pkg'.format(os.path.expanduser('~')))
    print(filename)
    print(os.path.expanduser('~'))
    get_updater().call_in_main(ask_ffmpeg_macOS)

def ask_ffmpeg_macOS():
    if(QtWidgets.QMessageBox.Ok == QtWidgets.QMessageBox.question(music, 'SomePythonThings Music Assistant', "SomePythoThings Music needs to install ffmpeg in order to run\nIf you click OK, SomePythonThings Music will download and install the required packages.", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Ok)):
        install_ffmpeg_macOS_part1()
    else:
        throw_warning('SomePythonThings Music', "If you don't install ffmpeg, SomePythonThings Music will not work!")
        installationProgressBar('Stop')


def install_ffmpeg_macOS_part1(again=False):
    global music
    installationProgressBar('Installing')
    time.sleep(0.2)
    if not again:
        passwd = str(QtWidgets.QInputDialog.getText(music, "Autentication needed - SomePythonThings Music Assistant", "Please write your password to perform the ffmpeg installation. \nThis password is NOT going to be stored anywhere in any way and it is going to be used ONLY for the update.\nIf you want, you can check that on the source code on github: \n(https://github.com/martinet101/SomePythonThings-Music/)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0])
    else:
        passwd = str(QtWidgets.QInputDialog.getText(music, "Autentication needed - SomePythonThings Music Assistant", "An error occurred while autenticating. Insert your password again (This attempt will be the last one)\n\nPassword:", QtWidgets.QLineEdit.Password, '')[0])
    t = Thread(target=install_ffmpeg_macOS_part2, args=(passwd, again))
    t.start()

def install_ffmpeg_macOS_part2(passwd, again=False):
    installationProgressBar('Installing')
    try:
        subprocess.run('cd; echo "{0}" | sudo -S installer -pkg "{1}" -target / -allowUntrusted && echo "Done!"'.format(passwd, '{0}/ffmpeg-plugin-for-somepythonthings-music.pkg'.format(os.path.expanduser('~'))), shell=True, check=True)
        installationProgressBar(action='Stop')
        installationProgressBar('Installing')
        get_updater().call_in_main(throw_info,"SomePythonThings Music Assistant","Ffmpeg was installed successfully. Please restart the application")
        get_updater().call_in_main(sys.exit)
        sys.exit()
    except:  # If the installation is falied on the 1st time
        if not again:
            get_updater().call_in_main(install_ffmpeg_macOS_part1, True)
        else:
            installationProgressBar('Stop')
            get_updater().call_in_main(throw_error, "SomePythonThings Music Assistant", "Unable to apply the update. Please try again later.")




def getWindowStyleScheme():
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
    if(mode=='auto' and _platform != 'darwin'):
        log('[        ] Auto mode selected and os is not macOS. Swithing to light...')
        mode='light'
    if(mode=='auto'):
        if(darkdetect.isDark()):
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

def toStyleMainList():
    global playing, lists, trackNumber, music, font, t
    try:
        for item in range(0, lists['main'].count()):
            lists['main'].item(item).setFont(QtGui.QFont(font, weight=QtGui.QFont.Normal))
        if(playing):
            lists['main'].item(trackNumber).setFont(QtGui.QFont(font, weight=QtGui.QFont.Bold))
    except AttributeError:
        log('[  WARN  ] An error occurred on playback thread, trackNumber is {0}...'.format(str(trackNumber)))
        try:
            t.shouldBeRuning = False
        except AttributeError:
            pass
        t = KillableThread(target=startPlayback)
        t.daemon = True
        t.start()

def removeFromPlaylist():
    global lists, files, trackNumber, justContinue, passedTime
    trackToRemove = lists['main'].currentRow()
    if(trackToRemove>=0):
        log('[        ] Index of files list is {0}, deleting song in position {0}'.format(int(trackToRemove)))
        files.remove(files[trackToRemove])
        lists['main'].takeItem(trackToRemove)
        passedTime = 0.0
        if(trackNumber>len(files)):
            toStrictlyPause()
        if(trackNumber == trackToRemove):
            justContinue = True
        log('[   OK   ] Actual playlist:'+str(files))
    else:
        log('[  WARN  ] No song selected to detete!')
    
def toShuffle():
    global shuffle, buttons
    if(shuffle):
        log("[   OK   ] Shuffle disabled")
        shuffle=False
        shuffleAction.setChecked(False)
        buttons['shuffle'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/shuffle-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Shuffle enabled")
        shuffle=True
        shuffleAction.setChecked(True)
        buttons['shuffle'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/shuffle-icon.svg\") 0 0 0 0 stretch stretch")
        
def toReplay():
    global replay, buttons
    if(replay):
        log("[   OK   ] Replay disabled")
        replay=False
        replayAction.setChecked(False)
        buttons['replay'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/replay-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Replay enabled")
        replay=True
        replayAction.setChecked(True)
        buttons['replay'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/replay-icon.svg\") 0 0 0 0 stretch stretch")

def toPlay(finalized=False, track=0):
    global playing, buttons, files, t, seekerValueManuallyChanged
    if(not playing):
        log("[   OK   ] Playing")
        if(files==[]):
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
    else:
        log("[   OK   ] Sending pause signal...")
        playing=False
        toStyleMainList()
        if(finalized):
            get_updater().call_in_main(labels['songname'].setText, "No music playing")
            get_updater().call_in_main(labels['actualtime'].setText, '-:--:--')
            seekerValueManuallyChanged = False
            refreshProgressbar(0)
        buttons['play'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/play-icon.svg\") 0 0 0 0 stretch stretch")

def toSkip():
    log('[   OK   ] Setting skip signal...')
    global skipped
    skipped=True

def toGoBack():
    log('[   OK   ] Setting goBack signal...')
    global goBack
    goBack=True

def toMute():
    global volume, muted, buttons, sliders
    if(muted):
        log("[   OK   ] Unmuting...")
        muted=False
        sliders['volume'].setStyleSheet('QSlider {height: 2px;background-color: none;}QSlider::handle{background-color: rgba(10, 150, 150, 1.0);border: 0px solid rgba(00, 120, 120, 1.0);border-radius: 7px;}QSlider::add-page:horizontal{background-color: white;border: 1px solid #DDDDDD;border-radius: 2px;}QSlider::sub-page:horizontal{background-color: rgba(20, 170, 170, 1.0);border: 1px solid rgba(10, 150, 150, 1.0);border-radius: 2px;}')
        buttons['audio'].setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/audio-icon.svg\") 0 0 0 0 stretch stretch")
    else:
        log("[   OK   ] Muting...")
        muted=True
        sliders['volume'].setStyleSheet('QSlider {height: 2px;background-color: none;}QSlider::handle{background-color: rgba(170, 170, 170, 1.0);border: 0px solid rgba(170, 170, 170, 1.0);border-radius: 7px;}QSlider::add-page:horizontal{background-color: white;border: 1px solid #DDDDDD;border-radius: 2px;}QSlider::sub-page:horizontal{background-color: rgba(200, 200, 200, 1.0);border: 1px solid rgba(150, 150, 150, 1.0);border-radius: 2px;}')
        buttons['audio'].setStyleSheet("background-color: rgba(20, 170, 170, 1.0); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/audio-off-icon.svg\") 0 0 0 0 stretch stretch")
    changeVolume()

def changeVolume():
    global volume, muted, buttons, sliders, playing, justContinue, passedTime
    volume = sliders['volume'].value()
    log('[   OK   ] Volume changed to '+str(volume))
    if(volume>100):
        volume=100
    if(playing):
        justContinue = True
        passedTime = playedTime

def getVolume():
    global volume, muted
    log('[   OK   ] Volume is set to {0}% returning value -{1}dB'.format(volume, (100-volume)/2))
    if(volume==0 or muted):
        return 500
    return (100-volume)/2

def toPauseAndStopSeeking():
    toStrictlyPause()
    stopSeeking()

def openFile():
    icon="icon-sptmusic-128.png"
    global files, music, elementNumber
    try:
        log('[        ] Dialog in process')
        
        music.show()
        filepaths = QtWidgets.QFileDialog.getOpenFileNames(music, "Select a music file", '', music_files)
        log('[   OK   ] Dialog Completed')
        if(filepaths[0] == []):
            log("[  WARN  ] User aborted dialog")
            return 0
        for filepath in filepaths[0]:
            file = open(filepath, 'r')
            filename = file.name
            file.close()
            try:
                files.append(filename)
                log('[   OK   ] File "'+str(filename)+'" processed')
            except Exception as e:
                if debugging:
                    raise e
                throw_error("Error processing file!","Unable to read file \""+filename+"\"")
                try:
                    file.close()
                except:
                    pass
            newItem =  QtWidgets.QListWidgetItem(QtGui.QIcon(str(realpath)+"/"+str(icon)), getSongTitle(filename))
            lists['main'].addItem(newItem)
            elementNumber += 1
    except Exception as e:
        if debugging:
            raise e
        throw_error("SomePythonThings Music", "An error occurred while selecting one or more files. \n\nError detsils: "+str(e))

def addFile(filepath):
    icon="icon-sptmusic-128.png"
    global files, music, elementNumber
    try:
        file = open(filepath, 'r')
        filename = file.name
        file.close()
        try:
            files.append(filename)
            log('[   OK   ] File "'+str(filename)+'" processed')
        except Exception as e:
            if debugging:
                raise e
            throw_error("Error processing file!","Unable to read file \""+filename+"\"")
            try:
                file.close()
            except:
                pass
        newItem =  QtWidgets.QListWidgetItem(QtGui.QIcon(str(realpath)+"/"+str(icon)), getSongTitle(filename))
        lists['main'].addItem(newItem)
        elementNumber += 1
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
    global playing
    if(playing):
        toPlay()

def saveSettings(silent=True, minimize_to_tray=False, bakcgroundPicture='None', mode='auto'):
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
                "minimize_to_tray":minimize_to_tray,
                "bakcgroundPicture":bakcgroundPicture,
                "mode":mode,
                }))
            settingsFile.close()
            if(not(silent)):
                throw_info("SomePythonThings Music", "Settings saved successfuly")
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
    settingsWindow.setMinimumSize(400, 200)
    settingsWindow.setMaximumSize(400, 200)
    settingsWindow.setWindowTitle("SomePythonThings Music Settings")
    settingsWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
    settingsWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
    settingsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    modeSelector = QtWidgets.QComboBox(settingsWindow)
    modeSelector.insertItem(0, 'Light')
    modeSelector.insertItem(1, 'Dark')
    if(_platform=='darwin'):
        modeSelector.insertItem(2, 'Auto')
    modeSelector.resize(230, 30)
    modeSelector.move(150, 20)
    modeSelectorLabel = QtWidgets.QLabel(settingsWindow)
    modeSelectorLabel.setText("Application mode: ")
    modeSelectorLabel.move(20, 20)
    modeSelectorLabel.setObjectName('settingsBackground')
    modeSelectorLabel.resize(130, 30)
    traySelector = QtWidgets.QComboBox(settingsWindow)
    traySelector.insertItem(0, 'Quit SomePythonThings Music')
    traySelector.insertItem(1, 'Minimize to System Tray')
    traySelector.resize(230, 30)
    traySelector.move(150, 60)
    traySelectorLabel = QtWidgets.QLabel(settingsWindow)
    traySelectorLabel.setText("✖ button action: ")
    traySelectorLabel.move(20, 60)
    traySelectorLabel.setObjectName('settingsBackground')
    traySelectorLabel.resize(130, 30)
    saveButton = QtWidgets.QPushButton(settingsWindow)
    saveButton.setText("Save settings and close")
    saveButton.resize(360, 40)
    saveButton.move(20, 140)
    saveButton.setObjectName('squarePurpleButton')
    saveButton.clicked.connect(partial(saveAndCloseSettings, modeSelector, traySelector, settingsWindow))

    try:
        if(settings['mode'].lower() == 'light'):
            modeSelector.setCurrentIndex(0)
        elif(settings['mode'].lower() == 'auto'):
            if(_platform=='darwin'):
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

    settingsWindow.show()

def saveAndCloseSettings(modeSelector, traySelector, settingsWindow):
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
    forceClose = True
    settingsWindow.close()
    music.setStyleSheet(getWindowStyleScheme())
    saveSettings(silent=False, minimize_to_tray=settings['minimize_to_tray'], bakcgroundPicture=settings['bakcgroundPicture'], mode=settings['mode'])

def getLenght(file):
    return pydub.AudioSegment.from_file(file).duration_seconds

def getFileType(file): #from file.mp3, returns MP3, from file.FiLeExT, returns FILEEXT 
    return file.split('.')[-1].upper()
    
def getSongTitle(file):
    return str(file.replace('\\', '/').split('/')[-1])

def play_with_simpleaudio(seg):
    return sa.play_buffer(
        seg.raw_data,
        num_channels=seg.channels,
        bytes_per_sample=seg.sample_width,
        sample_rate=seg.frame_rate
    )

def startPlayback(track=0):
    global files, labels, skipped, playerIsRunning, goBack, playing, trackNumber, replay, lastConvertedTrack, playingObj, justContinue, totalTime, passedTime, seeking, seekerValueManuallyChanged, starttime, playedTime, song_length
    playerIsRunning = True
    stopped=False
    passedTime = 0.0
    if(isinstance(track, int)):
        trackNumber=track
    else:
        trackNumber=0
    lastConvertedTrack = ''
    songToPlay = ''
    try:
        if(len(files) == 0):
            #get_updater().call_in_main(toPlay, True)
            playerIsRunning = False
            replay = False
            toStrictlyPause()
            sys.exit()
        while trackNumber<len(files):
            log('[        ] Starting new play round, index is {0}'.format(str(trackNumber)))
            if not stopped:
                track = files[trackNumber]
                log('[        ] Track number {0}'.format(trackNumber))
                log('[        ] Actual track file is '+str(track))
                log('[        ] Actual track filename is  '+getSongTitle(track))
                song_length = getLenght(track)
                get_updater().call_in_main(labels['totaltime'].setText, str(datetime.timedelta(seconds=int(song_length))))
                filename=getSongTitle(track)
                get_updater().call_latest(labels['songname'].setText, filename)
                if(not(lastConvertedTrack == getSongTitle(track))):
                    log('[   OK   ] Converting playback to Numpy...')
                    songToPlay = pydub.AudioSegment.from_file(track)
                    lastConvertedTrack = getSongTitle(track)
                else:
                    log('[  WARN  ] Song already converted to NumPy Array!')
                log('[        ] Start time is {0} ms'.format(passedTime*1000))
                playingObj = play_with_simpleaudio(songToPlay[int(passedTime*1000):].fade_in(100).fade_out(100)-getVolume())
                log('[   OK   ] Playing (play line is passed)')
                buttons['play'].setStyleSheet("background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/pause-icon.svg\") 0 0 0 0 stretch stretch")
                toStyleMainList()
                import time
                starttime = time.time()
                totalTime = getLenght(track)-passedTime
                pausedAt = 0
                playedTime = 0
                while(playingObj.is_playing()):
                    firsttime = time.time()
                    playedTime = time.time()-starttime+passedTime
                    get_updater().call_in_main(labels['actualtime'].setText, str(datetime.timedelta(seconds=int(playedTime))))
                    if(seeking):
                        seekerValueManuallyChanged = False
                        refreshProgressbar(playedTime*1000/(totalTime+passedTime))
                        #get_updater().call_in_main(sliders['seeker'].setValue, playedTime*1000/(totalTime+passedTime))
                    time.sleep(0.05 - 0*(time.time()-firsttime))
                    if(not(playing)):
                        playingObj.stop()
                        pausedAt = time.time()-starttime+passedTime
                        log('[   OK   ] Paused at moment {}'.format((time.time()-starttime)))
                        stopped=True
                        while not(playing):
                            continue
                        log('[        ] Continuing playback...')
                    if(skipped):
                        log('[        ] Skipping...')
                        playingObj.stop()
                    if(goBack):
                        log('[        ] Going back...')
                        playingObj.stop()
                    if(justContinue):
                        playingObj.stop()
                        log('[        ] Passing away...')
                if(skipped):
                    log('[   OK   ] Skipped')
                    if not(shuffle):
                        trackNumber += 1
                    else:
                        trackNumber = random.randint(0, len(files))
                    passedTime = 0.0
                    skipped=False
                    continue
                if(goBack):
                    log('[   OK   ] Went back.')
                    if(playedTime-passedTime>3):
                        trackNumber += 0#Stay on the same track
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
                    #get_updater().call_in_main(sliders['seeker'].setValue, 1000)
                    refreshProgressbar(1000)
                    if not(shuffle):
                        trackNumber += 1
                    else:
                        trackNumber = random.randint(0, len(files))
                    passedTime = 0.0
                else:
                    log('[   OK   ] Catched previous stop, setting start time...')
                    stopped=False
                    passedTime = pausedAt
            else:
                log('[        ] Playback is stopped, blocking...')
                stopped = False
                while not(playing):
                    continue              
        if not stopped:
            if replay:
                startPlayback()
            else:
                get_updater().call_in_main(toPlay, True)
        playerIsRunning = False
    except Exception as e:
        playerIsRunning = False
        playing = True
        get_updater().call_in_main(toPlay, True)
        get_updater().call_in_main(throw_error, "SomePythonThings Music", "An error occurred during the playback.\n\nPlease consider re-installing ffmpeg by clicking on \"Settings\" menu > \"Re-install ffmpeg\"\n\nError details:\""+str(e))
        if(debugging):
            raise e

def goToSong():
    global lists, trackNumber, playing, t, playerIsRunning, justContinue
    try:
        t.shouldBeRuning = False
        log('[  KILL  ] Killing playback thread to start a new one...')
    except AttributeError:
        log('[  WARN  ] Unable to kill thread, thread was not running...')
    trackNumber = lists['main'].currentRow()
    if(trackNumber<0):
        trackNumber = 0
    log('[   OK   ] Selected track number {}'.format(trackNumber))
    playerIsRunning = False
    playing = False
    toStrictlyPlay(track=trackNumber)

def goToMaybeSpecificTime():
    global sliders, totalTime, passedTime, justContinue, seeking, seekerValueManuallyChanged, starttime, playedTime, song_length
    if(seekerValueManuallyChanged):
        timeToGo = sliders['seeker'].value()*(song_length)/1000
        log('[        ] Starting goToSpecificTime with time value : '+str(timeToGo))
        justContinue = True
        passedTime=timeToGo
        seekerValueManuallyChanged = False
    else:
        seekerValueManuallyChanged = True

def stopSeeking():
    log('[        ] Stopping seeking...')
    global seeking
    seeking=False

def startSeeking():
    global seeking
    log('[        ] Starting seeking...')
    time.sleep(0.1)
    seeking=True

def savePlaylist():
    global files, music
    toStrictlyPause()
    try:
        log('[        ] Asking where to save the playlist...')
        music.show()
        filename = QtWidgets.QFileDialog.getSaveFileName(music, "Save the playlist as...", 'Unnamed Playlist.sptplaylist', ('SomePythonThings Playlist File (*.sptplaylist)'))[0]
        log('[   OK   ] Got string "{0}" from getSaveFileName()'.format(str(filename)))
        if(filename==''):
            log('[  WARN  ] User aborted dialog!')
        else:
            file = open(filename, 'w')
            try:
                toWrite="""Well, you discovered how to open a SomePythonThings Music Playlist. 
 this file, after the 3 "#", has, by order, all the files contained on the playlist.
 Please be careful when editing this file from a text editor, you could just destroy the .sptplaylist file...



 ###
 """
                for element in files:
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

def openPlaylist(playlist=''):
    global files, music, elementNumber
    log('[        ] Playlist attribute value is {0}'.format(playlist))
    playAfter = False
    try:
        if(playlist == '' or playlist == False):
            log('[        ] Dialog in process')
            
            music.show()
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
                raise FileTypeNotSupported('This platlist file is not a valid .sptplaylist file!')
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
    get_updater().call_in_main(bottomBar.setValue, value/10)
    get_updater().call_in_main(sliders['seeker'].setValue, value)

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

def throw_info(title, body, icon="icon-sptmusic-128.png", exit=False):
    global music
    music.show()
    log("[  INFO  ] "+body)
    msg = QtWidgets.QMessageBox(music)
    if(os.path.exists(str(realpath)+"/"+str(icon))):
        msg.setIconPixmap(QtGui.QPixmap(str(realpath)+"/"+str(icon)))
    else:
        msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()
    if(exit):
        sys.exit()

def throw_warning(title, body, warning=None):
    global music
    music.show()
    log("[  WARN  ] "+body)
    if(warning != None ):
        log("\t Warning reason: "+warning)
    msg = QtWidgets.QMessageBox(music)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(body)
    msg.setWindowTitle(title)
    msg.exec_()

def throw_error(title, body, error="Not Specified"):
    global music
    music.show()
    log("[  ERROR ] "+body+"\n\tError reason: "+error)
    msg = QtWidgets.QMessageBox(music)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
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
    throw_info("About SomePythonThings Music", "SomePythonThings Music\nVersion "+str(actualVersion)+"\n\nThe SomePythonThings Project\n\n © 2020 SomePythonThings\nhttps://www.somepythonthings.tk\n\n\nThe iconset has a CC Atribution 4.0 License", exit=False)

def checkForDependencies(bypassCheck=False):
    if(_platform == 'win32'):
        if(os.system('ffmpeg -version')!=0 or os.system('ffplay -version')!=0 or os.system('ffprobe -version')!=0 or bypassCheck):
            log('[  WARN  ] FFMPEG not found!')
            t = Thread(target=download_ffpmeg_win)
            t.daemon = True
            t.start()
        else:
            log('[   OK   ] FFMPEG library found')
    elif(_platform=="linux" or _platform=='linux2'):
        if(os.system('ffmpeg -version')!=0 or os.system('ffplay -version')!=0 or os.system('ffprobe -version')!=0 or bypassCheck):
            get_updater().call_in_main(install_ffmpeg_linux_part1)
            log('[  WARN  ] FFMPEG not found!')
        else:
            log('[   OK   ] FFMPEG library found')
    elif (_platform=='darwin'):
        if(bypassCheck):
            t = Thread(target=download_ffmpeg_macOS)
            t.daemon = True
            t.start()

def setProgramAsRunning():
    global defaultSettings, goRun, canRun
    if(os.path.exists(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/running.lock')):
        os.remove(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/running.lock')
        time.sleep(0.5)
        if(os.path.exists(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/running.lock')):
            with open(os.path.expanduser('~').replace('\\', '/')+'/.SomePythonThings/Music/show.lock', mode='a'): pass
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
                        music.show()
                        music.raise_()
                        music.activateWindow()
                        os.remove('show.lock')
                    except:
                        os.remove('show.lock')
            except Exception as e:
                if(debugging):
                    raise e
        except Exception as e:
            if(debugging):
                raise e
        time.sleep(0.3)

def on_key(key):
    global volume, sliders
    if key == QtCore.Qt.Key_Space:
        toPlay(finalized=False)
    elif key == QtCore.Qt.Key_Down:
        sliders['volume'].setValue(sliders['volume'].value()-10)
    elif key == QtCore.Qt.Key_Up:
        sliders['volume'].setValue(sliders['volume'].value()+10)
    elif key == QtCore.Qt.Key_Minus:
        sliders['volume'].setValue(sliders['volume'].value()-10)
    elif key == QtCore.Qt.Key_Plus:
        sliders['volume'].setValue(sliders['volume'].value()+10)
    elif key == QtCore.Qt.Key_Left:
        sliders['seeker'].setValue(sliders['seeker'].value()-10)
    elif key == QtCore.Qt.Key_Right:
        sliders['seeker'].setValue(sliders['seeker'].value()+10)
    #else:
    #   log('key pressed: %i' % key)

def resizeWidgets():
    global music, buttons, texts, progressbars, font
    height = music.height()
    width = music.width()
        
    buttons['play'].resize(50, 50)
    buttons['play'].setStyleSheet("QPushButton{background-color: rgba(255, 255, 255, 0.8); border-radius: 25px; border-image: url(\""+realpath+"/icons-sptmusic/play-icon.svg\") 0 0 0 0 stretch stretch} QPushButton:checked{background-color: rgba(00, 130, 130, 1.0);}")
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

    sliders['volume'].move(width-145, height-105)
    sliders['volume'].resize(120, 40)
    sliders['seeker'].move(int((width/2)-200), height-55)
    sliders['seeker'].resize(400, 40)
    labels['actualtime'].resize(100, 40)
    labels['actualtime'].move(int((width/2)-300), height-49)
    labels['totaltime'].resize(100, 40)
    labels['totaltime'].move(int((width/2)+200), height-49)
    labels['songname'].resize(width-130-int((width/2)-20)-50, 30)
    labels['songname'].move(int(20), height-100)

    lists['main'].move(170, 40)
    lists['main'].resize(width-190, height-180)

    log("[   OK   ] Resizing content to fit "+str(width)+'x'+str(height))
    bottomBar.resize(width, 120)
    bottomBar.move(0, height-120)

# main code
if __name__ == '__main__':
    
    Thread(target=setProgramAsRunning, daemon=True).start()

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

    elif _platform == "darwin":
        log("[   OK   ] OS detected is macOS")
        font = "Lucida Grande"
        realpath = "/Applications/SomePythonThings Music.app/Contents/Resources/resources-sptmusic"
    
    elif _platform == "win32":
        if int(platform.release()) >= 10: #Font check: os is windows 10
            font = "Segoe UI"#"Cascadia Mono"
            log("[   OK   ] OS detected is win32 release 10 ")
        else:# os is windows 7/8
            font="Segoe UI"#"Consolas"
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
        resized = QtCore.pyqtSignal()
        keyRelease = QtCore.pyqtSignal(int)

        def __init__(self, parent=None):
            super(Window, self).__init__(parent=parent)
            ui = Ui_MainWindow()
            ui.setupUi(self)
            self.resized.connect(resizeWidgets)

        def resizeEvent(self, event):
            self.resized.emit()
            return super(Window, self).resizeEvent(event)
        
        def keyReleaseEvent(self, event):
            super(Window, self).keyReleaseEvent(event)
            self.keyRelease.emit(event.key())
        
        def closeEvent(self, event):
            global forceClose
            if(settings['minimize_to_tray'] and not(forceClose)):
                music.hide()
                log("[        ] Minimizing to system tray...")
                event.ignore()
            else:
                event.accept()
                forceClose = False

    

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

    class FileTypeNotSupported(Exception):
        pass

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
            settings = defaultSettings
            if(debugging):
                raise e


        music.setMinimumSize(700, 330)
        music.setStyleSheet(getWindowStyleScheme())

        bottomBar = QtWidgets.QProgressBar(music)
        bottomBar.setTextVisible(False)
        bottomBar.setMinimum(0)
        bottomBar.setMaximum(100)
        bottomBar.setValue(0)

        i = 10
        for button in ['audio', 'replay', 'first-track', 'play', 'last-track', 'shuffle']:
            buttons[button] = QtWidgets.QPushButton(music)
            buttons[button].move(i, 40)
            i += 50
            buttons[button].resize(50, 50)
            buttons[button].setStyleSheet("QPushButton{background-color: rgba(255, 255, 255, 0.8); border-radius: 20px; border-image: url(\""+realpath+"/icons-sptmusic/"+button+"-icon.svg\") 0 0 0 0 stretch stretch } QPushButton:clicked{background-color: rgba(00, 130, 130, 1.0);}")

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
        
        buttons['delete'].setObjectName("squareRedButton")#.setStyleSheet("""QPushButton{border-radius: 0px;border: none;background-color: rgba(255, 255, 255, 0.5);color: black;}QPushButton:hover{background-color: rgba(255, 0, 0, 0.5);color: white;}""")
        
        buttons['add'].setObjectName("squarePurpleButton")#.setStyleSheet("""QPushButton{border-radius: 0px;border: none;background-color: rgba(255, 255, 255, 0.5);color: black;}QPushButton:hover{background-color: rgba(20, 170, 150, 0.7);color: white;}""")
        
        buttons['save'].setObjectName("squarePurpleButton")#.setStyleSheet("""QPushButton{border-radius: 0px;border: none;background-color: rgba(255, 255, 255, 0.5);color: black;}QPushButton:hover{background-color: rgba(20, 170, 150, 0.7);color: white;}""")

        buttons['open'].setObjectName("squarePurpleButton")#.setStyleSheet("""QPushButton{border-radius: 0px;border: none;background-color: rgba(255, 255, 255, 0.5);color: black;}QPushButton:hover{background-color: rgba(20, 170, 150, 0.7);color: white;}""")

        sliders['volume'] = QtWidgets.QSlider(QtCore.Qt.Horizontal, music)
        sliders['volume'].setMinimum(0)
        sliders['volume'].setMaximum(100)
        sliders['volume'].setValue(volume)
        sliders['volume'].valueChanged.connect(changeVolume)

        sliders['seeker'] = QtWidgets.QSlider(QtCore.Qt.Horizontal, music)
        sliders['seeker'].setMinimum(0)
        sliders['seeker'].setMaximum(1000)
        sliders['seeker'].sliderPressed.connect(toPauseAndStopSeeking)
        sliders['seeker'].sliderReleased.connect(toStrictlyPlay)
        sliders['seeker'].valueChanged.connect(goToMaybeSpecificTime)

        labels['actualtime'] = QtWidgets.QLabel(music)
        labels['actualtime'].setText('-:--:--')
        labels['actualtime'].setAlignment(QtCore.Qt.AlignRight)
        labels['totaltime'] = QtWidgets.QLabel(music)
        labels['totaltime'].setText('-:--:--')
        labels['totaltime'].setAlignment(QtCore.Qt.AlignLeft)
        labels['songname'] = QtWidgets.QLabel(music)
        labels['songname'].setText('No music playing')
        labels['songname'].setAlignment(QtCore.Qt.AlignLeft)


        lists['main'] = QtWidgets.QListWidget(music)
        lists['main'].itemDoubleClicked.connect(goToSong)


        menuBar = music.menuBar()

        
        icon = QtGui.QIcon("{0}/icon-sptmusic.png".format(realpath))
        tray = QtWidgets.QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        trayMenu = QtWidgets.QMenu()
        tray.setContextMenu(trayMenu)

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


        
        playlistMenu = menuBar.addMenu("Playlist")
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



        settingsMenu = menuBar.addMenu("Settings")
        installDependenciesAction = QtWidgets.QAction(" Re-install ffmpeg   ", music)
        installDependenciesAction.triggered.connect(partial(checkForDependencies, True))
        settingsMenu.addAction(installDependenciesAction)
        openSettingsAction = QtWidgets.QAction(" Settings...    ", music)
        openSettingsAction.triggered.connect(openSettingsWindow)
        settingsMenu.addAction(openSettingsAction)
        if(_platform=='darwin'):
            openSettingsAction = QtWidgets.QAction("Settings...    ", music)
            openSettingsAction.triggered.connect(openSettingsWindow)
            settingsMenu.addAction(openSettingsAction)



        helpMenu = menuBar.addMenu("Help")
        openHelpAction = QtWidgets.QAction("Online manual", music)
        openHelpAction.triggered.connect(openHelp)
        helpMenu.addAction(openHelpAction)
        aboutAction = QtWidgets.QAction("About SomePythonThings Music    ", music)
        aboutAction.triggered.connect(about)
        helpMenu.addAction(aboutAction)
        updatesAction = QtWidgets.QAction("Check for updates", music)
        updatesAction.triggered.connect(checkDirectUpdates)
        helpMenu.addAction(updatesAction)

        helpMenu = trayMenu.addMenu("Help")
        openHelpAction = QtWidgets.QAction("Online manual", music)
        openHelpAction.triggered.connect(openHelp)
        helpMenu.addAction(openHelpAction)
        aboutAction = QtWidgets.QAction("About SomePythonThings Music    ", music)
        aboutAction.triggered.connect(about)
        helpMenu.addAction(aboutAction)
        updatesAction = QtWidgets.QAction("Check for updates", music)
        updatesAction.triggered.connect(checkDirectUpdates)
        helpMenu.addAction(updatesAction)


        
        showMusicAction = QtWidgets.QAction("Show SomePythonThigs Music ", music)
        showMusicAction.triggered.connect(music.show)
        trayMenu.addAction(showMusicAction)

        quitMusicAction = QtWidgets.QAction("Quit SomePythonThigs Music ", music)
        quitMusicAction.triggered.connect(sys.exit)
        trayMenu.addAction(quitMusicAction)
        if(len(sys.argv)>1):
            if('runanyway' in sys.argv[1].lower()):
                goRun=True
                canRun=True
        while(not(goRun)): pass
        if(canRun):
            music.show()
            if(_platform == "win32"):
                from PyQt5 import QtWinExtras
                loadbutton = QtWinExtras.QWinTaskbarButton(music)
                loadbutton.setWindow(music.windowHandle())
                taskbprogress = loadbutton.progress()
                taskbprogress.setRange(0, 100)
                taskbprogress.setValue(0)
                taskbprogress.show()
            resizeWidgets()
            upadtesThread = Thread(target=updates_thread)
            upadtesThread.daemon = True
            upadtesThread.start()
            log("[        ] Program loaded, starting UI...")
            i = 1
            isThereAFile = False
            if(len(sys.argv)>1):
                if('SPTPLAYLIST' == getFileType(sys.argv[1])):
                    openPlaylist(sys.argv[1])
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
                toPlay()
            dependenciesThread = Thread(target=checkForDependencies)
            dependenciesThread.daemon = True
            dependenciesThread.start()
            app.exec_()
        else:
            tray.setVisible(False)
            log('[  EXIT  ] Exiting...')
            sys.exit()
    except Exception as e:
        if not debugging:
            throw_error("Fatal Error!", "SomePythonThings Music crashed by a fatal error. If it's the first time you see that, just reopen the program. If it's not the first time, please mail me at somepythonthingschannel@gmail.com and send me the details of the error (This would be very helpful ;D )\n\nException details: \nException Type: {0}\n\nException Arguments:\n{1!r}".format(type(e).__name__, e.args)+"\n\nException Comments:\n"+str(e))
        else:
            raise e
    log('[  EXIT  ] Reached end of the script')