"""Main file - ZVVFilesPlayer"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDir
from modules import widgets, resources, paths


class Zvvfiles_player(QMainWindow):
	"""Zvvpanels class"""
	def __init__(self):
		super().__init__()
		self.create_main_window()

	def create_main_window(self):
		"""Create main window"""
	#create_central_widget
		self.central_widget = widgets.Widgets()
		self.setCentralWidget(self.central_widget)

		###
		self.setObjectName('App')
		self.showMaximized()
		self.setMinimumWidth(450)
		self.setWindowTitle('ZVVFilesPlayer')
		self.setWindowIcon(QIcon(':/app_icon.png'))
		self.show()
		
#################################################################

	def closeEvent(self, event):
		"""Close event"""
		volume = paths.VOLUME
		eq_state = paths.EQUALIZER_STATE
		preset = paths.PRESET_NUM
		play_mode = paths.PLAY_MODE
		playlist_clear = paths.PLAYLIST_CLEAR_STATE
		treeview_mode = paths.TREEVIEW_MODE
		mouseclick_autoload = paths.MOUSECLICK_AUTOLOAD
		last_folder = paths.LAST_FOLDER
		paths.SETTINGS.setValue('music/volume', volume)
		paths.SETTINGS.setValue('music/eq', eq_state)
		paths.SETTINGS.setValue('music/preset', preset)
		paths.SETTINGS.setValue('music/playmode', play_mode)
		paths.SETTINGS.setValue('music/playlist_clear', playlist_clear)
		paths.SETTINGS.setValue('files/treeview_mode', treeview_mode)
		paths.SETTINGS.setValue('files/mouseclick_autoload', mouseclick_autoload)
		if last_folder != QDir.homePath():
			paths.SETTINGS.setValue('files/last_folder', last_folder)
		paths.SETTINGS.sync()
		event.accept()

#################################################################

APP = QApplication(sys.argv)
file_css = os.path.join(os.getcwd(), 'styles', 'dark.css')
if os.path.exists(file_css):
	with open(file_css, 'r') as file_open:
		data = file_open.read()
		APP.setStyleSheet(data)
WIN = Zvvfiles_player()
sys.exit(APP.exec_())
