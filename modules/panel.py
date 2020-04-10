"""Panel module"""
import os
import sys
import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							QLabel, QPushButton, QComboBox, QMenu,
							QFileSystemModel, QAbstractItemView, QHeaderView, 
							QTreeView, QLineEdit, QFrame)
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import (Qt, QDir, QSize, QStorageInfo, QStandardPaths, QUrl, QFileInfo)
from . import flowbox, paths, zbutton, fav_button


class Panel(QFrame):
	"""Panel class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		self.MUSIC_FILES_EXTENTSIONS = ["*.mp3", "*.wav", "*.ogg", "*.ac3", "*.flac",]
		self.ALL_EXTENSIONS = self.MUSIC_FILES_EXTENTSIONS + ["*.pls", "*.m3u", "*.m3u8",]
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(3)
		self.setLayout(self.vbox_main)
	#hbox_drives
		self.hbox_drives = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_drives)
		self.create_drives_flowbox()
	#hbox_path
		self.hbox_path = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_path)
		#button_back
		self.button_back = zbutton.Zbutton()
		self.button_back.set_info(icon=':/back_icon.png')
		self.button_back.clicked.connect(self.press_back_button)
		self.hbox_path.addWidget(self.button_back)
		#combobox_path_history
		self.combobox_path_history = QComboBox()
		self.combobox_path_history.setFixedHeight(40)
		self.combobox_path_history.setFocusPolicy(Qt.NoFocus)
		self.combobox_path_history.activated.connect(self.press_combobox_path)
		self.hbox_path.addWidget(self.combobox_path_history)
		###
		self.search_filter_line = QLineEdit()
		self.search_filter_line.addAction(QIcon(':/filter_icon.png'), QLineEdit.LeadingPosition)
		self.search_filter_line.setPlaceholderText("quick search")
		self.search_filter_line.setClearButtonEnabled(True)
		self.search_filter_line.setFixedSize(200, 40)
		self.search_filter_line.textChanged.connect(self.change_text_filter)
		self.hbox_path.addWidget(self.search_filter_line)
		#button_config
		self.button_config = zbutton.Zbutton()
		self.button_config.set_info(icon=':/config_icon.png', tool_tip='Options')
		self.hbox_path.addWidget(self.button_config)
		
	#files_model
		self.files_model = QFileSystemModel()
		self.files_model.setNameFilterDisables(False)
		self.files_model.setNameFilters(self.ALL_EXTENSIONS)
		self.files_model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot | QDir.DirsFirst)
	#tree_view
		self.tree_view = QTreeView()
		self.tree_view.setObjectName('Files_table')
		self.tree_view.setModel(self.files_model)
		self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.tree_view.setIconSize(QSize(32, 32))
		self.tree_view.setRootIsDecorated(False)
		self.tree_view.header().setStretchLastSection(False)
		self.tree_view.header().setSectionResizeMode(0, QHeaderView.Stretch)
		self.tree_view.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
		self.tree_view.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
		self.tree_view.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)
		self.tree_view.setDragEnabled(True)
		self.tree_view.clicked.connect(self.press_item)
		self.tree_view.doubleClicked.connect(self.press_double_table_item)
		self.vbox_main.addWidget(self.tree_view)
		
		#add drives
		self.add_default_places()
		self.add_mount_drives()
		self.fav_button_drive = fav_button.Fav_drive_button(self)
		self.fav_button_drive.setObjectName('Fav_drives')
		self.fav_button_drive.set_info(text='Favs', icon=':/fav_icon.png')
		self.fav_button_drive.set_size(100, 30)
		self.flowbox_drives.flowLayout.addWidget(self.fav_button_drive)
		
		###AUTORUN
		self.MAIN_PATH = paths.LAST_FOLDER
		self.go_path(self.MAIN_PATH)
		
################################################################################################

	def create_drives_flowbox(self):
		"""Create drives flowbox"""
		self.flowbox_drives = flowbox.Window()
		self.flowbox_drives.setObjectName('Flowbox')
		self.hbox_drives.addWidget(self.flowbox_drives)
		
	def press_item(self, modelIndex):
		"""Press item"""
		if paths.MOUSECLICK_AUTOLOAD:
			path = self.files_model.filePath(modelIndex)
			if os.path.isdir(path):
				self.parentWidget.left_player_widget.table_widget.add_folder(path)

	def press_double_table_item(self, modelIndex):
		"""Press double on table item"""
		path = self.files_model.filePath(modelIndex)
		if os.path.isdir(path):
			if not self.tree_view.rootIsDecorated():
				self.go_path(path)
		if os.path.isfile(path):
			QDesktopServices.openUrl(QUrl.fromLocalFile(path))

	def press_combobox_path(self):
		"""Press combobox path"""
		current_path = self.combobox_path_history.currentText()
		self.go_path(current_path)
		
	def go_path(self, path):
		"""Go path"""
		if os.path.exists(path):
			self.files_model.setRootPath(path)
			self.tree_view.setRootIndex(self.files_model.index(path))
			self.set_combo_path(path)
			self.combo_remove_tails()
			self.check_back_button_state()
			paths.LAST_FOLDER = path

	def press_back_button(self):
		"""Press back button"""
		current_path = self.combobox_path_history.currentText()
		if self.combobox_path_history.currentIndex() > 0:
			prev_path = self.combobox_path_history.itemText(self.combobox_path_history.currentIndex() - 1)
			if os.path.exists(prev_path):
				self.go_path(prev_path)
			
	def check_back_button_state(self):
		"""Check back button state"""
		if self.combobox_path_history.count() > 1:
			if not self.button_back.isEnabled():
				self.button_back.setEnabled(True)
		else:
			if self.button_back.isEnabled():
				self.button_back.setEnabled(False)

	def set_combo_path(self, path):
		"""Set text path"""
		find_index = self.combobox_path_history.findText(path)
		if find_index >= 0:
			self.combobox_path_history.setCurrentIndex(find_index)
		else:
			self.combobox_path_history.addItem(QIcon(':/folder.png'), path)
			self.combobox_path_history.setCurrentIndex(self.combobox_path_history.count() - 1)

	def combo_remove_tails(self):
		"""Combo remove tails"""
		index = self.combobox_path_history.currentIndex()
		max_items = self.combobox_path_history.count()
		for i in range(max_items-1, index, -1):
			self.combobox_path_history.removeItem(i)
			
	def add_default_places(self):
		"""Add default places"""
		list_pathes = [
					QDir.toNativeSeparators(QDir().homePath()),
					QDir.toNativeSeparators(QStandardPaths.writableLocation(QStandardPaths.MusicLocation)),
					]
		for item in list_pathes:
			self.add_drive_button(root_path=item, icon=':/folder.png')
			
	def add_mount_drives(self):
		"""Add mount drives"""
		show_fs = ['fuseblk', 'ext4', 'FAT32', 'NTFS', 'vfat',]
		for drive in QStorageInfo.mountedVolumes():
			if drive.isValid() and drive.isReady():
				if drive.fileSystemType() in show_fs:
					path = drive.rootPath()
					if QFileInfo(path).isReadable():
						size = '{0:.1f} GB'.format(drive.bytesTotal()/1000/1000/1000)
						name = list(filter(None, os.path.split(path)))[-1]
						title = '{name} ({size})'.format(size=size, name=name)
						self.add_drive_button(root_path=path, icon=':/hdd.png', title=title)
							
	def add_drive_button(self, root_path='', icon='', title=''):
		"""Add drive button"""
		if not title:
			title = os.path.split(root_path)[-1][:10]
		self.button_drive = Button_drive()
		self.button_drive.setText(title)
		self.button_drive.setIcon(QIcon(icon))
		self.button_drive.DRIVE_PATH = root_path
		self.button_drive.setToolTip(root_path)
		self.button_drive.clicked.connect(self.press_drive_button)
		self.flowbox_drives.flowLayout.addWidget(self.button_drive)
				
	def press_drive_button(self):
		"""Press drive button"""
		self.combobox_path_history.clear()
		path = self.sender().DRIVE_PATH
		self.go_path(path)
			
	def change_text_filter(self, text):
		"""Change text filter"""
		self.files_model.setNameFilterDisables(False)
		if text:
			extensions = paths.MUSIC_EXTENSIONS + paths.PLS_EXTENSIONS
			filter_name = ['*{name}*.{ext}'.format(name=text, ext=x) for x in extensions]
			self.files_model.setNameFilters(filter_name)
			self.files_model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot | QDir.DirsFirst)
		else:
			self.files_model.setNameFilterDisables(False)
			self.files_model.setNameFilters(self.ALL_EXTENSIONS)
			self.files_model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot | QDir.DirsFirst)
			
	def change_treeview_mode(self, state):
		"""Change treeview mode"""
		if state:
			self.tree_view.setRootIsDecorated(True)
		else:
			self.tree_view.setRootIsDecorated(False)
			self.tree_view.collapseAll()
		
######################################################################################

class Button_drive(QPushButton):
	"""Button drive class"""
	def __init__(self):
		super().__init__()
		self.DRIVE_PATH = None
		self.create_button()
		
	def create_button(self):
		"""Create button"""
		self.setFixedHeight(30)
		self.setCursor(Qt.PointingHandCursor)
		self.setFocusPolicy(Qt.NoFocus)
		
######################################################################################
