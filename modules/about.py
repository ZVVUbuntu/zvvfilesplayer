"""About module"""
import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl


class About(QWidget):
	"""About window class"""
	def __init__(self):
		super().__init__()
		self.create_about_window()

	def create_about_window(self):
		"""Create widgets"""
		self.vbox_about = QVBoxLayout()
		self.vbox_about.setContentsMargins(1, 1, 1, 1)
		self.setLayout(self.vbox_about)
		
		#
		self.vbox_about.addStretch()

		#add image
		self.label_image = QLabel()
		self.label_image.setScaledContents(True)
		self.label_image.setAlignment(Qt.AlignCenter)
		self.label_image.setFixedSize(100, 100)
		self.label_image.setPixmap(QPixmap(":/app_icon.png"))
		self.vbox_about.addWidget(self.label_image)
		self.vbox_about.setAlignment(self.label_image, Qt.AlignCenter)

		#add label name_program
		self.label_program = QLabel("ZVVFilesPlayer v.2.0")
		self.label_program.setAlignment(Qt.AlignCenter)
		self.vbox_about.addWidget(self.label_program)
		#add label author
		self.label_author = QLabel(self.tr("Author: <b>Vyacheslav Zubik</b>. Ukraine, Kherson"))
		self.label_author.setAlignment(Qt.AlignCenter)
		self.vbox_about.addWidget(self.label_author)
		#add blog
		self.label_blog = QLabel(self.tr("Follow to my blog:<a href = 'http://zvvubuntu.blogspot.com'>ZVVUbuntu`s Blog</a>"))
		self.label_blog.setAlignment(Qt.AlignCenter)
		self.label_blog.setOpenExternalLinks(True)
		self.vbox_about.addWidget(self.label_blog)
		#add label email
		self.label_email = QLabel("Email:  ZVVUbuntu@gmail.com")
		self.label_email.setAlignment(Qt.AlignCenter)
		self.label_email.setTextInteractionFlags(Qt.TextSelectableByMouse)
		self.vbox_about.addWidget(self.label_email)
		
		#
		self.vbox_about.addStretch()
		
		###
		self.resize(500, 400)
		self.setWindowTitle('About')
		self.setWindowIcon(QIcon(':/about_icon.png'))
		self.setWindowFlags(Qt.Tool)
