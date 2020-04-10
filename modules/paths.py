import os
import sys
import shutil
import sqlite3
from PyQt5.QtCore import QSettings, QDir

def check_path(path):
	if not os.path.exists(path):
		os.mkdir(path)

if sys.platform.startswith('linux'):
	APP_PATH = os.path.join(QDir.homePath(), '.config', 'zvvfilesplayer')
	check_path(APP_PATH)
BASE_PATH = os.path.join(APP_PATH, 'zvvfpbase.db')
CONFIG_PATH = os.path.join(APP_PATH, 'config.ini')
if not os.path.exists(BASE_PATH):
	src = os.path.join(os.getcwd(), 'zvvfpbase.db')
	shutil.copy(src, APP_PATH)
if not os.path.exists(CONFIG_PATH):
	src = os.path.join(os.getcwd(), 'config.ini')
	shutil.copy(src, APP_PATH)
#BASE
BASE_CONNECTION = sqlite3.connect(BASE_PATH)
BASE_CURSOR = BASE_CONNECTION.cursor()
#CONFIG
SETTINGS = QSettings(CONFIG_PATH, QSettings.IniFormat)
VOLUME = 50
try:
	VOLUME = int(SETTINGS.value('music/volume'))
	if VOLUME <= 0: VOLUME = 50
except:
	VOLUME = 50
EQUALIZER_STATE = int(SETTINGS.value('music/eq'))
PRESET_NUM = int(SETTINGS.value('music/preset'))
PLAY_MODE = int(SETTINGS.value('music/playmode'))
PLAYLIST_CLEAR_STATE = int(SETTINGS.value('music/playlist_clear'))

TREEVIEW_MODE = int(SETTINGS.value('files/treeview_mode'))
MOUSECLICK_AUTOLOAD = int(SETTINGS.value('files/mouseclick_autoload'))
LAST_FOLDER = QDir.homePath()
try:
	LAST_FOLDER = str(SETTINGS.value('files/last_folder'))
	if LAST_FOLDER:
		if os.path.exists(LAST_FOLDER):
			LAST_FOLDER = QDir.toNativeSeparators(LAST_FOLDER)
		else:
			LAST_FOLDER = QDir.homePath()
	else:
		LAST_FOLDER = QDir.homePath()
except:
	LAST_FOLDER = QDir.homePath()


MUSIC_EXTENSIONS = ['mp3', 'wav', 'ogg', 'ac3', 'flac',]
PLS_EXTENSIONS = ['pls', 'm3u', 'm3u8',]
