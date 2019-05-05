"""Widgets module"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from . import panel, player_widget


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
		self.files = panel.Panel()
		self.hbox_main.addWidget(self.files)
		
#######################################################################################

	def resizeEvent(self, event):
		"""Resize event"""
		if event.size().width() < 900:
			if self.files.isVisible():
				self.files.hide()
		else:
			if not self.files.isVisible():
				self.files.show()
