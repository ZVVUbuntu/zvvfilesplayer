"""Widgets module"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QLabel, QPushButton, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from . import panel, player_widget, options


class Widgets(QWidget):
	"""Widgets class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
	#hbox_main
		self.hbox_main = QHBoxLayout()
		self.hbox_main.setContentsMargins(1, 1, 1, 1)
		self.setLayout(self.hbox_main)
	#left_player_widget
		self.left_player_widget = player_widget.Player()
		self.left_player_widget.setMinimumWidth(400)
		self.hbox_main.addWidget(self.left_player_widget)
	#right_files_widget
		self.files = panel.Panel(self)
		self.hbox_main.addWidget(self.files)
		self.files.button_config.clicked.connect(self.press_config_button)
	#options
		self.options_window = options.Options(self)
		
#######################################################################################

	def resizeEvent(self, event):
		"""Resize event"""
		if event.size().width() < QDesktopWidget().screenGeometry().width() / 2:
			if self.files.isVisible():
				self.files.hide()
		else:
			if not self.files.isVisible():
				self.files.show()

	def press_config_button(self):
		"""Press config button"""
		#self.options_window = options.Options(self)
		self.options_window.move_window()
		self.files.button_config.setFocus()
		
