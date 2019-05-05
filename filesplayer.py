"""Main file - ZVVFilesPlayer"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from modules import widgets, resources


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
		self.showMaximized()
		self.setMinimumWidth(500)
		self.setWindowTitle('ZVVFilesPlayer')
		self.setWindowIcon(QIcon(':/app_icon.png'))
		self.show()

#################################################################

APP = QApplication(sys.argv)
WIN = Zvvfiles_player()
sys.exit(APP.exec_())
