"""Time slider class"""
from PyQt5.QtWidgets import QSlider, QStyle
from PyQt5.QtCore import Qt
from . import styles


class TimeSlider(QSlider):
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.setMouseTracking(True)
		self.MOUSE_PRESS_STATE = False
		self.create_slider()
		
	def create_slider(self):
		"""Create slider"""
		self.setOrientation(Qt.Horizontal)
		self.setStyleSheet(styles.get_progress_slider_style())
		
	def mouseMoveEvent(self, ev):
		""" Jump to pointer position while moving """
		value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), ev.x(), self.width())
		if value:
			self.parentWidget.parent().show_move(value)
			if self.MOUSE_PRESS_STATE:
				self.setValue(value)
		
	def mousePressEvent(self, ev):
		"""Release mouse button"""
		self.MOUSE_PRESS_STATE = False
		value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), ev.x(), self.width())
		if value:
			self.parentWidget.parent().set_pos(value)
			self.setValue(value)
		
	def enterEvent(self, ev):
		"""mouse cursor enter event"""
		self.parentWidget.label_move_time.show()
		
	def leaveEvent(self, ev):
		"""Mouse cursor leave event"""
		self.parentWidget.label_move_time.clear()
		self.parentWidget.label_move_time.hide()
		self.MOUSE_PRESS_STATE = False
