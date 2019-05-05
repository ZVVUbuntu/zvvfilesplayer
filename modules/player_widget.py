"""Player module"""
import os
import re
import random
import time
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QMenu,
							 QPushButton, QLabel, QSlider, QButtonGroup, QSizePolicy,
							 QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem,
							 QFileDialog, QProgressBar, QStyle)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QSettings, QSize, QUrl, QFileInfo, QDir, QCoreApplication, QTimer
from tinytag import TinyTag
from . import controls, styles, vlc, zbutton, equalizer


class Player(QWidget):
	"""Player class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.CURRENT_ITEM_NOW = None
		self.CURRENT_URL = None
		self.instance = vlc.Instance()
		self.PLAYER = self.instance.media_player_new()
		self.player_events = self.PLAYER.event_manager()
		self.player_events.event_attach(vlc.EventType.MediaPlayerLengthChanged, self.check_duration)
		self.player_events.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.check_position_state)
		self.player_events.event_attach(vlc.EventType.MediaPlayerPlaying, self.check_duration_onplay)
		
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(1)
		self.setLayout(self.vbox_main)
		
		#label_title
		self.label_title = QLabel()
		self.label_title.setAlignment(Qt.AlignCenter)
		self.label_title.setWordWrap(True)
		self.label_title.setFixedHeight(35)
		self.label_title.setStyleSheet('QLabel{font-weight:bold; font-size:18px; border:1px solid silver; background:rgba(224, 224, 224, 0.5);}')
		self.vbox_main.addWidget(self.label_title)
		
	#table_widget
		self.table_widget = MyTableWidget()
		self.table_widget.itemDoubleClicked.connect(self.press_item)
		self.vbox_main.addWidget(self.table_widget)
		self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
		
	#controls_widget
		self.controls_widget = controls.Controls()
		self.vbox_main.addWidget(self.controls_widget)
		self.controls_widget.volume_slider.valueChanged.connect(self.volume_change)
		self.controls_widget.button_play.clicked.connect(self.press_play)
		self.controls_widget.button_pause.clicked.connect(self.press_pause)
		self.controls_widget.button_stop.clicked.connect(self.press_stop)
		self.controls_widget.button_next.clicked.connect(self.press_next_file)
		self.controls_widget.button_prev.clicked.connect(self.press_prev_file)
		self.controls_widget.button_minus_time.clicked.connect(self.press_minus_time)
		self.controls_widget.button_plus_time.clicked.connect(self.press_plus_time)
		self.add_new_buttons()
		
	#timer_check_end
		self.timer_check_end = QTimer()
		self.timer_check_end.setInterval(1000)
		self.timer_check_end.timeout.connect(self.play_end)
		self.timer_check_end.start()
		
	#AUTORUN
		self.eq_win = equalizer.Equalizer(self)
		self.volume_change(30)
##################################################################################

	def add_new_buttons(self):
		"""Create hbox_controls"""
		#button_eq
		self.button_eq = zbutton.Zbutton()
		self.button_eq.set_info(icon=":/eq_icon.png")
		self.button_eq.clicked.connect(self.press_eq_button)
		self.controls_widget.hbox_play_controls.addWidget(self.button_eq)
		#button_menu
		self.button_menu = zbutton.Zbutton()
		self.button_menu.set_info(icon=":/menu_icon.png")
		self.controls_widget.hbox_play_controls.addWidget(self.button_menu)
		#add menu
		self.menu_tools = QMenu()
		self.menu_tools.addAction(QIcon(":/open_icon.png"), 'Add folder', self.press_add_folder)
		self.menu_tools.addAction(QIcon(":/add_files_icon.png"), 'Add file(s)', self.press_add_files)
		self.menu_tools.addSeparator()
		self.menu_tools.addAction(QIcon(":/playlist.png"), 'Create playlist', self.press_create_playlist)
		self.menu_tools.addSeparator()
		self.menu_tools.addAction(QIcon(":/remove_file.png"), 'Remove item', self.press_remove_item)
		self.menu_tools.addAction(QIcon(":/clear_icon.png"),'Clear all', self.clear_all)
		self.menu_tools.addAction(QIcon(":/about_icon.png"),'About', self.press_about)
		self.button_menu.setMenu(self.menu_tools)
		
	def press_about(self):
		"""Press about"""
		from . import about
		self.about_win = about.About()
		self.about_win.show()
		
	def press_remove_item(self):
		"""Press remove items"""
		current_item = self.table_widget.currentItem()
		if current_item:
			self.table_widget.removeRow(current_item.row())
				
	def press_create_playlist(self):
		"""Press create playlist"""
		if self.table_widget.rowCount() > 0:
			file_name = os.path.join(QDir.homePath(), 'playlist.m3u')
			filePath = QFileDialog.getSaveFileName(self, "Save playlist", file_name, ("Playlists (*.pls *.m3u *.m3u8)"))
			if filePath:
				path = filePath[0]
				if path:
					with open(path, 'a', encoding='utf-8') as file_save:
						file_save.write('#EXTM3U\n')
						for row in range(self.table_widget.rowCount()):
							item = self.table_widget.item(row, 0)
							title = item.TITLE
							url = item.URL
							file_save.write('#EXTINF:-1,{0}\n'.format(title))
							file_save.write('{0}\n'.format(url))
						
	def read_playlist(self, pls_file):
		"""Read playlist"""
		self.table_widget.setRowCount(0)
		with open(pls_file, 'r', encoding='utf-8') as file_load:
			title = None
			path = None
			for line in file_load.readlines():
				if '#EXTINF' in line:
					line = line.split('\n')[0]
					title = line.split(',', 1)[1]
				if os.path.exists(line.split('\n')[0]):
					path = line.split('\n')[0]
				if title and path:
					self.add_one_row(title, path)
					title = None
					path = None
					
	def press_add_files(self):
		"""Press add files"""
		get_files = QFileDialog.getOpenFileNames(self, 'Add file(s)', QDir.homePath(),
										 ("Audio (*.mp3 *.wav *.ogg *.ac3 *.flac)"), options = QFileDialog.DontUseNativeDialog)
		if get_files[0]:
			get_files = set(get_files[0])
			for item in get_files:
				title = os.path.split(item)[1]
				self.add_one_row(title, item)
		
	def press_add_folder(self):
		"""Press add folder"""
		get_folder = QFileDialog.getExistingDirectory(self, 'Choose folder', QDir.homePath(),
								QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks | 
								QFileDialog.DontUseNativeDialog)
		if get_folder:
			self.add_folder(get_folder)
		
	def add_folder(self, folder_path):
		"""Add folder"""
		musics_reg_exp = ["*.mp3", "*.wav", "*.ogg", "*.ac3", "*.flac",]
		files = QDir(folder_path).entryInfoList(musics_reg_exp, QDir.Files)
		if files:
			for music_file in files:
				if files.index(music_file) > 100:
					QCoreApplication.processEvents()
				path = music_file.filePath()
				title = music_file.fileName()
				self.add_one_row(title, path)
				
	def press_eq_button(self):
		"""Press eq button"""
		self.eq_win.resize(400, 600)
		self.eq_win.show()
			
##################################################################################

	def add_one_row(self, name, path):
		"""Add one row"""
		self.table_widget.add_row(name, path)

	def press_item(self, item):
		"""Press table item"""
		item.setIcon(QIcon(':/play_state.png'))
		if self.CURRENT_ITEM_NOW:
			if not self.CURRENT_ITEM_NOW == item:
				if self.CURRENT_ITEM_NOW is not None:
					self.CURRENT_ITEM_NOW.setIcon(QIcon(':/note.png'))
		self.CURRENT_ITEM_NOW = item
		title = item.TITLE
		url = item.URL
		self.player_play(title, url)
		
	def clear_all(self):
		"""Clear all"""
		self.table_widget.setRowCount(0)
		self.CURRENT_ITEM_NOW = None
		
	def clear_info(self):
		"""Clar info"""
		self.controls_widget.clear_info()
		self.label_title.clear()
		self.CURRENT_ITEM_NOW.setIcon(QIcon(':/note.png'))
		self.CURRENT_ITEM_NOW = None
		
######################################PLAYER#############################################################

	def volume_change(self, value):
		"""Volume change"""
		volume = "Volume: {0}".format(str(value))
		self.PLAYER.audio_set_volume(value)
		self.controls_widget.label_volume.setText(volume)
		self.controls_widget.volume_slider.setValue(value)

	def press_play(self):
		"""Press play"""
		self.PLAYER.play()

	def press_pause(self):
		"""Press pause"""
		self.PLAYER.pause()
		
	def press_stop(self):
		"""Press stop"""
		self.PLAYER.stop()
		self.clear_info()
		
	def player_play(self, title, url):
		"""Player play"""
		self.label_title.setText(title)
		self.CURRENT_URL = url
		self.media = self.instance.media_new(url)
		self.PLAYER.set_media(self.media)
		self.PLAYER.play()

######################################TIME CONTROL#########################################################

	def check_duration_onplay(self, event):
		"""Check duration on play"""
		time_max = self.controls_widget.time_slider.maximum()
		if not time_max:
			self.check_duration(None)

	def check_duration(self, event):
		"""Check duration"""
		last_time = self.PLAYER.get_media().get_duration()
		if last_time:
			self.controls_widget.time_slider.setRange(0, last_time)
			last_time = time.strftime('%H:%M:%S', time.gmtime(last_time/1000.0))
			self.controls_widget.label_pos_last.setText(str(last_time))
		
	def check_position_state(self, event):
		"""Check position state"""
		value = self.PLAYER.get_position()
		value = value * self.controls_widget.time_slider.maximum()
		current_time = int(value)
		self.move_time(current_time)
		
	def show_move(self, value):
		"""Show move position"""
		move_time = time.strftime('%H:%M:%S', time.gmtime(value/1000.0))
		self.controls_widget.label_move_time.setText(move_time)
		
	def move_time(self, position):
		"""Position"""
		self.controls_widget.time_slider.setValue(position)
		current_label_time = time.strftime('%H:%M:%S', time.gmtime(position/1000.0))
		self.controls_widget.label_pos_current.setText(str(current_label_time))
			
	def set_pos(self, position):
		"""Set position"""
		max_value = self.controls_widget.time_slider.maximum()
		set_time = ((position * 100) / max_value) / 100
		self.PLAYER.set_position(set_time)
		
	def play_end(self):
		"""Play end"""
		if self.PLAYER.get_state() == vlc.State.Ended:
			self.choose_play_mode()
			
	def press_minus_time(self):
		"""Press minus time"""
		current_pos = self.controls_widget.time_slider.value()
		if current_pos:
			current_pos -= 10000
			self.set_pos(current_pos)
		
	def press_plus_time(self):
		"""Press plus time"""
		current_pos = self.controls_widget.time_slider.value()
		if current_pos:
			current_pos += 15000
			self.set_pos(current_pos)
		
#####################################PLAY ORDER##################################################

	def choose_play_mode(self):
		"""Choose mode"""
		if self.table_widget.rowCount() > 0:
			current_mode = self.controls_widget.combo_playmodes.currentText().lower()
			if current_mode == "replay":
				self.player_play(self.label_title.text(), self.CURRENT_URL)
			if current_mode in ["next", "shuffle"]:
				self.press_next_file()

	def press_prev_file(self):
		"""Press prev file"""
		max_files = self.table_widget.rowCount()
		if max_files:
			current_item = self.CURRENT_ITEM_NOW
			if current_item:
				current_row = current_item.row()
				if self.controls_widget.combo_playmodes.currentText().lower() == "shuffle":
					current_row = random.randrange(0, (max_files-1))
				else:
					current_row -= 1
				if current_row < 0:
					current_row = 0
				self.next_file(current_row)

	def press_next_file(self):
		"""Press next file"""
		max_files = self.table_widget.rowCount()
		if max_files > 0:
			current_item = self.CURRENT_ITEM_NOW
			if current_item:
				current_row = current_item.row()
				if self.controls_widget.combo_playmodes.currentText().lower() == "shuffle":
					current_row = random.randrange(0, (max_files-1))
				else:
					current_row += 1
				self.next_file(current_row)
			
	def next_file(self, index):
		"""Play Next file"""
		if index >= 0 and index < self.table_widget.rowCount():
			next_item = self.table_widget.item(index, 0)
			self.table_widget.setCurrentItem(next_item)
			self.press_item(next_item)

##################################################################

class MyTableWidget(QTableWidget):
	"""MyTableWidget class"""
	def __init__(self):
		super().__init__()
		self.setRowCount(0)
		self.setColumnCount(2)
		self.setHorizontalHeaderLabels(("Name", "Time",))
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.horizontalHeader().hide()
		self.verticalScrollBar().setStyleSheet(styles.get_scrollbar_style())
		self.setShowGrid(False)
		self.setWordWrap(False)
		self.setAcceptDrops(True)
		#init tag
		self.TAG = TinyTag
		
	def dragEnterEvent(self, event):
		event.accept()
		
	def dragMoveEvent(self, event):
		event.accept()
		
	def dropEvent(self, e):
		list_files = e.mimeData().urls()
		for item in list_files:
			music_extensions = ['mp3', 'wav', 'ogg', 'ac3', 'flac',]
			pls_extension = ['pls', 'm3u', 'm3u8',]
			if os.path.isfile(QUrl(item.url()).toLocalFile()):
				path = QUrl(item.url()).toLocalFile()
				if QFileInfo(path).suffix() in music_extensions:
					title = os.path.split(path)[1]
					self.add_row(title, path)
				if QFileInfo(path).suffix() in pls_extension:
					self.parent().read_playlist(path)
			if os.path.isdir(QUrl(item.url()).toLocalFile()):
				folder_path = QUrl(item.url()).toLocalFile()
				self.parent().add_folder(folder_path)
				
	def add_row(self, name, path):
		"""Add row"""
		get_tag = self.TAG.get(path)
		duration = get_tag.duration
		#tag = TinyTag.get(path)
		#duration = tag.duration
		if int(duration) > 3600:
			human_duration = time.strftime('%H:%M:%S', time.gmtime(duration))
		else:
			human_duration = time.strftime('%M:%S', time.gmtime(duration))
		#name
		fileNameItem = MyItem()
		fileNameItem.setText(name)
		fileNameItem.setIcon(QIcon(':/note.png'))
		fileNameItem.TITLE = name
		fileNameItem.URL = path
		#time
		timeItem = MyItem()
		timeItem.setTextAlignment(Qt.AlignCenter)
		timeItem.setText(human_duration)
		timeItem.setFlags(Qt.NoItemFlags)
		#set
		row = self.rowCount()
		self.insertRow(row)
		self.setItem(row, 0, fileNameItem)
		self.setItem(row, 1, timeItem)

##################################################################

class MyItem(QTableWidgetItem):
	"""MyItem class"""
	def __init__(self):
		super().__init__()
		self.TITLE = None
		self.URL = None
		self.setFlags(self.flags() ^ Qt.ItemIsEditable)
		
##################################################################


