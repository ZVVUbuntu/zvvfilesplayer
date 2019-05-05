"""Zbutton module"""
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class Zbutton(QPushButton):
	"""MyButton class"""
	def __init__(self):
		super().__init__()
		self.setFixedSize(35, 35)
		self.setIconSize(QSize(30, 30))
		self.setCursor(Qt.PointingHandCursor)
		self.setFocusPolicy(Qt.NoFocus)
		self.setStyleSheet(self.get_button_style())
		
	def set_info(self, text='', icon=None):
		"""Set info"""
		if text:
			self.setText(text)
		if icon:
			self.setIcon(QIcon(icon))
			
	def get_button_style(self):
		"""Get button style"""
		STYLE = ("""QPushButton{
						border:1px solid silver;
						font-size:14px;
					} 
					QPushButton::hover{
						border:1px solid orange; 
						background-color:#fff9c6;
					}
					QPushButton::menu-indicator{image: url(' '); width:0px;}
					QPushButton::checked{
						border: 1px solid orange; 
						background-color:orange;
					}""")
		return STYLE
