"""Options win module"""
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QDesktopWidget, QCheckBox, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from . import paths


class Options(QFrame):
	"""Options win class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.checkbox_treeview_mode = My_checkbox()
		self.checkbox_mouseclick_autload = My_checkbox()
		self.checkbox_playlist_clear = My_checkbox()
		self.checkbox_treeview_mode.stateChanged.connect(self.change_state_checkbox)
		self.checkbox_mouseclick_autload.stateChanged.connect(self.change_state_checkbox)
		self.checkbox_playlist_clear.stateChanged.connect(self.change_state_checkbox)
		self.OPTIONS_LIST = [
				('Change treeview mode <b style="color:lightblue;">[Files panel]</b>:', 'treeview_mode', self.checkbox_treeview_mode, ),
				('Load folder by mouse click <b style="color:lightblue;">[Files panel]</b>:', 'mouseclick_autload', self.checkbox_mouseclick_autload, ),
				('Clear playlist before adding folders <b style="color:lightblue;">[Music player]</b>:', 'playlist_clear', self.checkbox_playlist_clear, ),
			]
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.setLayout(self.vbox_main)
		#add options
		for item in self.OPTIONS_LIST:
			self.hbox = QHBoxLayout()
			self.label = QLabel()
			self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
			self.label.setText(item[0])
			item[2]._ID = item[1]
			self.hbox.addWidget(self.label)
			self.hbox.addWidget(item[2])
			self.vbox_main.addLayout(self.hbox)
		#
		self.vbox_main.addStretch()
		###
		self.setObjectName('Options_window')
		self.setWindowFlags(Qt.Popup)
		self.resize(650, 450)
		
		#AUTORUN
		self.set_options()
#######################################################################################
		
	def move_window(self):
		"""Move window to center"""
		# geometry of the main window
		qr = self.frameGeometry()
		# center point of screen
		cp = QDesktopWidget().availableGeometry().center()
		# move rectangle's center point to screen's center point
		qr.moveCenter(cp)
		# top left of rectangle becomes top left of window centering it
		self.move(qr.topLeft())
		self.show() 
		
#######################################################################################

	def set_options(self):
		"""Set options"""
		treeview_mode = paths.TREEVIEW_MODE
		mouseclick_autoload = paths.MOUSECLICK_AUTOLOAD
		playlist_clear = paths.PLAYLIST_CLEAR_STATE
		self.set_treeview_mode(treeview_mode)
		self.set_mouseclick_autoload(mouseclick_autoload)
		self.set_playlist_clear(playlist_clear)

	def change_state_checkbox(self, state=False):
		"""Change state checkbox"""
		current_widget = self.sender()
		if current_widget._ID == 'treeview_mode':
			self.set_treeview_mode(state)
		if current_widget._ID == 'mouseclick_autload':
			self.set_mouseclick_autoload(state)
		if current_widget._ID == 'playlist_clear':
			self.set_playlist_clear(state)
			
	def set_treeview_mode(self, state):
		"""Set treeview mode"""
		self.parentWidget.files.change_treeview_mode(state)
		paths.TREEVIEW_MODE = state
		self.checkbox_treeview_mode.setCheckState(state)
		
	def set_mouseclick_autoload(self, state):
		"""Set mouseclick autoload"""
		paths.MOUSECLICK_AUTOLOAD = state
		self.checkbox_mouseclick_autload.setCheckState(state)
		
	def set_playlist_clear(self, state):
		"""Set playlist clear"""
		paths.PLAYLIST_CLEAR_STATE = state
		self.checkbox_playlist_clear.setCheckState(state)
		
#######################################################################################

class My_checkbox(QCheckBox):
	"""My QCheckBox class"""
	def __init__(self):
		super().__init__()
		self._ID = None
		self.setTristate(False)
