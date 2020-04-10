"""Player module"""
import os
import re
import random
import time
import datetime
from PyQt5.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout, QComboBox, QMenu,
							 QPushButton, QLabel, QSlider, QButtonGroup, QSizePolicy,
							 QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem,
							 QFileDialog, QShortcut)
from PyQt5.QtGui import QIcon, QFont, QColor, QFontMetrics, QPixmap, QImage, QKeySequence, QBrush
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSettings, QSize, QUrl, QFileInfo, QDir, QCoreApplication, QTimer, QThread
from tinytag import TinyTag
from . import controls, vlc, zbutton, equalizer, paths


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
		self.EQ = vlc.AudioEqualizer()
		self.EQ_BAND_COUNT = vlc.libvlc_audio_equalizer_get_band_count()
		self.player_events = self.PLAYER.event_manager()
		self.player_events.event_attach(vlc.EventType.MediaPlayerLengthChanged, self.check_duration)
		#self.player_events.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.check_position_state)
		self.player_events.event_attach(vlc.EventType.MediaPlayerPaused, self.change_pause_state)
		self.player_events.event_attach(vlc.EventType.MediaPlayerPlaying, self.check_duration_onplay)
		
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(1)
		self.setLayout(self.vbox_main)
		
		#label_title
		self.label_title = Title_label(self)
		self.vbox_main.addWidget(self.label_title)
		
	#table_widget
		self.table_widget = MyTableWidget(self)
		self.table_widget.itemDoubleClicked.connect(self.press_item)
		self.vbox_main.addWidget(self.table_widget)
		self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
		
	#controls_widget
		self.controls_widget = controls.Controls(self)
		self.vbox_main.addWidget(self.controls_widget)
		self.controls_widget.button_play_pause.clicked.connect(self.press_play)
		self.controls_widget.button_next.clicked.connect(self.press_next_file)
		self.controls_widget.button_prev.clicked.connect(self.press_prev_file)
		self.controls_widget.button_minus_time.clicked.connect(self.press_minus_time)
		self.controls_widget.button_plus_time.clicked.connect(self.press_plus_time)
		
	#timer_check_end
		self.timer_check_end = QTimer()
		self.timer_check_end.setInterval(1000)
		self.timer_check_end.timeout.connect(self.check_position_state)
		self.timer_check_end.start()
		
	#remove_shortcut
		self.remove_shortcut = QShortcut(self)
		self.remove_shortcut.setKey(QKeySequence("Delete"))
		self.remove_shortcut.setContext(Qt.ApplicationShortcut)
		self.remove_shortcut.activated.connect(self.press_remove_item)
		#play_pause_shortcut
		self.play_pause_shortcut = QShortcut(self)
		self.play_pause_shortcut.setKey(QKeySequence("Space"))
		self.play_pause_shortcut.setContext(Qt.ApplicationShortcut)
		self.play_pause_shortcut.activated.connect(self.press_pause)
		
	#AUTORUN
		self.set_default_volume()
		self.label_title.set_default_info()
		
##################################################################################
		
	def press_remove_item(self):
		"""Press remove items"""
		current_item = self.table_widget.currentItem()
		if current_item:
			if current_item == self.CURRENT_ITEM_NOW:
				self.CURRENT_ITEM_NOW = None
			self.table_widget.removeRow(current_item.row())
				
	def press_create_playlist(self):
		"""Press create playlist"""
		if self.table_widget.rowCount() > 0:
			file_name = os.path.join(QDir.homePath(), 'playlist.m3u')
			filePath = QFileDialog.getSaveFileName(self, "Save playlist", file_name, ("Playlists (*.pls *.m3u *.m3u8)"), options = QFileDialog.DontUseNativeDialog)
			if filePath:
				path = filePath[0]
				if path:
					with open(path, 'w', encoding='utf-8') as file_save:
						file_save.write('#EXTM3U\n')
						for row in range(self.table_widget.rowCount()):
							item = self.table_widget.item(row, 0)
							time_item = self.table_widget.item(row, 1)
							title = item.TITLE
							url = item.URL
							human_duration = time_item.text()
							file_save.write('#EXTINF:-1,{0}_&_{1}\n'.format(title, human_duration))
							file_save.write('{0}\n'.format(url))
					
	def press_add_files(self):
		"""Press add files"""
		get_files = QFileDialog.getOpenFileUrls(self, 'Add file(s)', QUrl(QDir.homePath()),
										 ("Audio (*.mp3 *.wav *.ogg *.ac3 *.flac)"), options = QFileDialog.DontUseNativeDialog)
		if get_files[0]:
			get_files = set(get_files[0])
			self.table_widget.add_files(get_files)
		
	def press_add_folder(self):
		"""Press add folder"""
		get_folder = QFileDialog.getExistingDirectory(self, 'Choose folder', QDir.homePath(),
								QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks | 
								QFileDialog.DontUseNativeDialog)
		if get_folder:
			self.table_widget.add_folder(get_folder)
		
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
		self.label_title.set_file_info(title, url)
		
	def clear_all(self):
		"""Clear all"""
		self.table_widget.setRowCount(0)
		self.CURRENT_ITEM_NOW = None
		
	def clear_info(self):
		"""Clar info"""
		self.controls_widget.clear_info()
		self.label_title.set_default_info()
		if self.CURRENT_ITEM_NOW:
			self.CURRENT_ITEM_NOW.setIcon(QIcon(':/note.png'))
			self.CURRENT_ITEM_NOW = None
		
######################################PLAYER#############################################################

	def set_default_volume(self):
		"""Set default volume"""
		volume = paths.VOLUME
		vlc.libvlc_audio_set_volume(self.PLAYER, volume)
		self.volume_change(volume)

	def volume_change(self, value):
		"""Volume change"""
		#volume = "Volume: {0}".format(str(value))
		self.PLAYER.audio_set_volume(value)
		self.controls_widget.volume_button.set_info(value)
		self.controls_widget.volume_button.volume_popup.volume_slider.setValue(value)
		paths.VOLUME = value

	def press_play(self):
		"""Press play"""
		if self.PLAYER.get_state() == vlc.State.Playing:
			self.press_pause()
		if self.PLAYER.get_state() == vlc.State.Paused:
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
		self.CURRENT_URL = url
		self.media = self.instance.media_new(url)
		self.PLAYER.set_media(self.media)
		self.PLAYER.play()
		
	def change_pause_state(self, event):
		"""Change pause state"""
		self.controls_widget.button_play_pause.set_info(icon=':/play.png')
######################################TIME CONTROL#########################################################

	def check_duration_onplay(self, event):
		"""Check duration on play"""
		self.controls_widget.button_play_pause.set_info(icon=':/pause.png')
		time_max = self.controls_widget.time_slider.maximum()
		if not time_max:
			self.check_duration(None)

	def check_duration(self, event):
		"""Check duration"""
		try:
			last_time = self.PLAYER.get_media().get_duration()
			if last_time:
				self.controls_widget.time_slider.setRange(0, last_time)
				last_time = time.strftime('%H:%M:%S', time.gmtime(last_time/1000.0))
				self.controls_widget.label_pos_last.setText(str(last_time))
		except:
			pass
		
	def check_position_state(self, event=None):
		"""Check position state"""
		if self.PLAYER.get_state() == vlc.State.Playing:
			value = self.PLAYER.get_position()
			value = value * self.controls_widget.time_slider.maximum()
			#current_time = int(value)
			self.move_time(value)
		if self.PLAYER.get_state() == vlc.State.Ended:
			self.choose_play_mode()
		
	def show_move(self, value):
		"""Show move position"""
		move_time = time.strftime('%H:%M:%S', time.gmtime(value/1000.0))
		self.controls_widget.label_move_time.setText(move_time)
		
	def move_time(self, position):
		"""Position"""
		if not self.controls_widget.time_slider.MOUSE_PRESS_STATE:
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
			current_mode = self.controls_widget.combo_playmodes.currentIndex()
			if current_mode == 1:
				self.player_play(self.label_title.TITLE, self.CURRENT_URL)
			if current_mode in [2, 3]:
				self.press_next_file()

	def press_prev_file(self):
		"""Press prev file"""
		max_files = self.table_widget.rowCount()
		if max_files:
			current_item = self.CURRENT_ITEM_NOW
			if current_item:
				current_row = current_item.row()
				if self.controls_widget.combo_playmodes.currentIndex() == 3:
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
				if self.controls_widget.combo_playmodes.currentIndex() == 3:
					current_row = random.randrange(0, (max_files-1))
				else:
					current_row += 1
				self.next_file(current_row)
			else:
				current_row = 0
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
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.setRowCount(0)
		self.setColumnCount(2)
		self.verticalHeader().setSectionsClickable(False)
		self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.setHorizontalHeaderLabels(("Name", "Time",))
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.horizontalHeader().hide()
		self.setShowGrid(False)
		self.setWordWrap(False)
		self.setAcceptDrops(True)
		self.setObjectName('Music_table')
		self.music_extensions = ['mp3', 'wav', 'ogg', 'ac3', 'flac',]
		self.pls_extension = ['pls', 'm3u', 'm3u8',]
		
	def dragEnterEvent(self, event):
		event.accept()
		
	def dragMoveEvent(self, event):
		event.accept()
		
	def dropEvent(self, e):
		list_files = e.mimeData().urls()
		first_path = QUrl(list_files[0].url()).toLocalFile()
		if os.path.isdir(first_path):
			self.add_folder(first_path)
		elif QFileInfo(first_path).suffix() in self.pls_extension:
			self.read_playlist(first_path)
		else:
			self.add_files(list_files)
				
	def add_folder(self, folder_path):
		"""Add folder"""
		if paths.PLAYLIST_CLEAR_STATE:
			self.parentWidget.clear_all()
		musics_reg_exp = ["*.mp3", "*.wav", "*.ogg", "*.ac3", "*.flac",]
		files = QDir(folder_path).entryInfoList(musics_reg_exp, QDir.Files)
		self.set_duration(files)
				
	def add_files(self, get_files):
		"""Add files"""
		self.set_duration(get_files)
		
	def read_playlist(self, pls_file):
		"""Read playlist"""
		self.parentWidget.clear_all()
		with open(pls_file, 'r', encoding='utf-8') as file_load:
			title = path = None
			for line in file_load.readlines():
				if '#EXTINF' in line:
					line = line.split('\n')[0]
					title_time = line.split(',', 1)[1]
					try:
						title, human_duration = title_time.split('_&_')
					except:
						title, human_duration = title_time, ''
				if os.path.exists(line.split('\n')[0]):
					path = line.split('\n')[0]
				if title and path:
					self.add_row(title, path, human_duration)
					title = path = None
				
	def add_row(self, name, path, human_duration=''):
		"""Add row"""
		#name
		fileNameItem = MyItem()
		fileNameItem.setText(name)
		fileNameItem.setIcon(QIcon(':/note.png'))
		fileNameItem.TITLE = name
		fileNameItem.URL = path
		#time
		timeItem = MyItem()
		timeItem.setTextAlignment(Qt.AlignCenter)
		timeItem.setFlags(Qt.NoItemFlags)
		if human_duration: timeItem.setText(human_duration)
		#set
		row = self.rowCount()
		self.insertRow(row)
		self.setItem(row, 0, fileNameItem)
		self.setItem(row, 1, timeItem)
		
	def set_duration(self, get_files=[]):
		"""Set duration"""
		self.my_thread = My_thread(get_files)
		self.my_thread.finished.connect(self.thread_finished)
		self.my_thread.notifyProgress.connect(self.update_progress)
		self.my_thread.start()
		
	def thread_finished(self):
		normal_list = self.my_thread.new_list
		for item in normal_list:
			path, duration = item
			title = os.path.split(path)[1]
			self.add_row(title, path, duration)
			
	def update_progress(self, normal_list):
		"""Update download progress"""
		QCoreApplication.processEvents()
		for item in normal_list:
			path, duration = item
			title = os.path.split(path)[1]
			self.add_row(title, path, duration)
		#QCoreApplication.processEvents()

##################################################################################

class MyItem(QTableWidgetItem):
	"""MyItem class"""
	def __init__(self):
		super().__init__()
		self.TITLE = None
		self.URL = None
		self.setFlags(self.flags() ^ Qt.ItemIsEditable)
		
##################################################################################

class Title_label(QFrame):
	"""Title label class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.eq_win = equalizer.Equalizer(self.parentWidget)
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.TAG = TinyTag
		self.TITLE = None
	#hbox_main
		self.hbox_main = QHBoxLayout()
		#self.hbox_main.setSpacing(20)
		self.setLayout(self.hbox_main)
	#label_cover
		self.label_cover = QLabel()
		self.label_cover.setFixedSize(120, 120)
		self.label_cover.setScaledContents(True)
		self.label_cover.setObjectName('Label_cover')
		self.hbox_main.addWidget(self.label_cover)
	#vbox_file_info
		self.vbox_file_info = QVBoxLayout()
		self.hbox_main.addLayout(self.vbox_file_info)
		#label_main_title
		self.label_main_title = QLabel()
		self.label_main_title.setObjectName('Label_title')
		self.label_main_title.setWordWrap(True)
		self.vbox_file_info.addWidget(self.label_main_title)
		#label_info
		self.label_info = QLabel()
		self.label_info.setObjectName('Label_info')
		self.vbox_file_info.addWidget(self.label_info)
		#hbox_tools
		self.hbox_tools = QHBoxLayout()
		self.hbox_tools.setContentsMargins(20, 0, 0, 0)
		self.vbox_file_info.addLayout(self.hbox_tools)
		#button_open_folder
		self.button_open_folder = zbutton.Zbutton()
		self.button_open_folder.setObjectName('Tool_music_button')
		self.button_open_folder.set_info(icon=":/add_folder.png", tool_tip='Open folder')
		self.button_open_folder.set_size(32, 32)
		self.button_open_folder.clicked.connect(self.parentWidget.press_add_folder)
		self.hbox_tools.addWidget(self.button_open_folder)
		#button_add_file
		self.button_add_file = zbutton.Zbutton()
		self.button_add_file.setObjectName('Tool_music_button')
		self.button_add_file.set_info(icon=":/open_files.png", tool_tip='Add file(s)')
		self.button_add_file.set_size(32, 32)
		self.button_add_file.clicked.connect(self.parentWidget.press_add_files)
		self.hbox_tools.addWidget(self.button_add_file)
		#button_create_playlist
		self.button_create_playlist = zbutton.Zbutton()
		self.button_create_playlist.setObjectName('Tool_music_button')
		self.button_create_playlist.set_info(icon=":/pls.png", tool_tip='Create playlist')
		self.button_create_playlist.set_size(32, 32)
		self.button_create_playlist.clicked.connect(self.parentWidget.press_create_playlist)
		self.hbox_tools.addWidget(self.button_create_playlist)
		#button_eq
		self.button_eq = zbutton.Zbutton()
		self.button_eq.setObjectName('Tool_music_button')
		self.button_eq.set_info(icon=":/eq.png", tool_tip='Equalizer')
		self.button_eq.set_size(32, 32)
		self.button_eq.clicked.connect(self.press_eq_button)
		self.hbox_tools.addWidget(self.button_eq)
		#
		self.hbox_tools.addStretch()
		#button_menu
		self.button_menu = zbutton.Zbutton()
		self.button_menu.setObjectName('Tool_music_button')
		self.button_menu.set_info(text='. . .')
		self.button_menu.set_size(32, 32)
		self.hbox_tools.addWidget(self.button_menu)
		#add menu
		self.menu_tools = QMenu()
		self.menu_tools.addAction(QIcon(":/remove_file.png"), 'Remove item', self.parentWidget.press_remove_item)
		self.menu_tools.addAction(QIcon(":/clear_icon.png"),'Clear all', self.parentWidget.clear_all)
		self.button_menu.setMenu(self.menu_tools)
		###
		self.setFixedHeight(130)
		
	def set_default_info(self):
		"""Set default info"""
		self.label_cover.setPixmap(QPixmap(':/app_icon.png'))
		self.set_title('ZVVFilesPlayer <b style="color:#2ea2ff;">(v.3.2.3)</b>')
		self.label_info.setText("Author: <b style='color:lightgreen'>Vyacheslav Zubik</b>. Ukraine, Kherson. Email:  <b style='color:#2ea2ff'>ZVVUbuntu@gmail.com</b>")
		
	def set_file_info(self, title, path):
		"""Set file info"""
		try:
			get_tag = self.TAG.get(path, image=True)
			bitrate, samplerate, image = get_tag.bitrate, get_tag.samplerate, get_tag.get_image()
			if bitrate: bitrate = str(int(bitrate))
			if samplerate: samplerate = str(int(samplerate))
		except:
			bitrate = samplerate = image = ''
		try:
			title = get_tag.artist + ' - ' + get_tag.title
		except:
			pass
		self.set_info(title, bitrate, samplerate, image)
		
	def clear_info(self):
		"""Clear info"""
		self.label_cover.clear()
		self.label_main_title.clear()
		self.label_info.clear()
		
	def set_info(self, title, bitrate, samplerate, image):
		"""Set info"""
		self.clear_info()
		self.set_title(title)
		info = 'Bitrate: <b style="color:lightgreen">{0}</b> kb/s, Samplerate: <b style="color:#2ea2ff">{1}</b> kHz'.format(bitrate, samplerate)
		if bitrate: self.label_info.setText(info)
		pixmap = QPixmap(':/music_cover.jpg')
		if image: 
			qimage = QImage()
			qimage = qimage.fromData(image)
			if qimage.format(): pixmap = pixmap.fromImage(qimage)
			else: pass
		else: pixmap.load(':/music_cover.jpg')
		self.label_cover.setPixmap(pixmap)
		
	def set_title(self, text):
		"""Set title"""
		if text:
			self.label_main_title.setText(text)
			self.TITLE = text
			
	def press_eq_button(self):
		"""Press eq button"""
		position = self.button_eq.rect().bottomLeft()
		self.eq_win.move(self.button_eq.mapToGlobal(position))
		self.eq_win.show()
		self.button_eq.setFocus()
		
###################################################################################

class My_thread(QThread):
	notifyProgress = QtCore.pyqtSignal(list)
	def __init__(self, get_files):
		super().__init__()
		self.get_files = get_files
		self.new_list = []
		
	def run(self):
		self.TAG = TinyTag
		for item in self.get_files:
			if type(item) == QFileInfo: path = item.filePath()
			else: path = QUrl(item).toLocalFile()
			try:
				get_tag = self.TAG.get(path)
				duration = get_tag.duration
				if int(duration) > 3600: duration_template = '%H:%M:%S'
				else: duration_template = '%M:%S'
				human_duration = time.strftime(duration_template, time.gmtime(duration))
			except:
				human_duration = ' - '
			self.new_list.append((path, human_duration))
			if self.get_files.index(item) == 0 or len(self.new_list) % 20 == 0:
				self.notifyProgress.emit(self.new_list)
				self.new_list = []
