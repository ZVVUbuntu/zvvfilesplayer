"""Fav button module"""
import os
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QDir, QUrl
from . import zbutton, zlistwidget


class Fav_drive_button(zbutton.Zbutton):
	"""Fav button class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.setAcceptDrops(True)
		self.fav_win = Fav_popup_win(self.parentWidget)
		self.clicked.connect(self.press_fav_button)

	def dragEnterEvent(self, event):
		"""Drag enter event"""
		if event.mimeData().hasUrls():
			files =  event.mimeData().urls()
			if len(files) == 1:
				get_file = files[0]
				path = QDir.toNativeSeparators(get_file.toLocalFile())
				if os.path.isdir(path):
					event.accept()
		
	def dragMoveEvent(self, event):
		"""Drag Move event"""
		if event.mimeData().hasUrls():
			files =  event.mimeData().urls()
			if len(files) == 1:
				get_file = files[0]
				path = QDir.toNativeSeparators(get_file.toLocalFile())
				if os.path.isdir(path):
					event.acceptProposedAction()
		
	def dropEvent(self, event):
		if event.mimeData().hasUrls():
			files =  event.mimeData().urls()
			if len(files) == 1:
				get_file = files[0]
				path = QDir.toNativeSeparators(get_file.toLocalFile())
				if os.path.isdir(path):
					self.fav_win.add_row(path)
			
	def press_fav_button(self):
		"""Press save button"""
		position = self.rect().bottomLeft()
		self.fav_win.move(self.mapToGlobal(position))
		self.fav_win.show()
		self.setFocus()
		self.fav_win.list_widget.set_items()
#########################################################################################

class Fav_popup_win(QFrame):
	"""Fav popup win"""
	def __init__(self, parentWidget=None):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(0, 0, 0, 0)
		self.vbox_main.setSpacing(0)
		self.setLayout(self.vbox_main)
		#list_widget
		self.list_widget = zlistwidget.Zlistwidget()
		self.list_widget.setObjectName('Favs_listwidget')
		self.list_widget.itemClicked.connect(self.press_item)
		self.vbox_main.addWidget(self.list_widget)
		###
		self.setObjectName('Fav_window')
		self.setFixedWidth(200)
		self.setMinimumHeight(200)
		self.setWindowFlags(Qt.Popup)
		
	def add_row(self, path):
		"""Add row"""
		self.list_widget.add_row(path)
		
	def press_item(self, listItem):
		"""Press item"""
		path = listItem.PATH
		self.parentWidget.go_path(path)
		self.hide() 
