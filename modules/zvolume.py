"""ZVolume button"""
from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QPoint
from . import zslider, styles


class Zvolume(QPushButton):
	"""ZVolume class"""
	def __init__(self, parentWidget=None):
		super().__init__()
		self.parentWidget = parentWidget
		self.setObjectName('Volume_button')
		self.setFixedSize(80, 40)
		self.setCursor(Qt.PointingHandCursor)
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
		self.VOLUME_ICONS = [
				':/volume_none.png',
				':/volume_min.png',
				':/volume_middle.png',
				':/volume_full.png',
			]
	#hbox_main
		self.hbox_main = QHBoxLayout()
		self.hbox_main.setContentsMargins(5, 1, 5, 1)
		self.setLayout(self.hbox_main)
		#label_icon
		self.label_icon = QLabel()
		self.label_icon.setScaledContents(True)
		self.label_icon.setFixedSize(30, 30)
		self.hbox_main.addWidget(self.label_icon)
		self.hbox_main.setAlignment(Qt.AlignVCenter)
		#label_text
		self.label_text = QLabel()
		self.label_text.setObjectName('Volume_label')
		self.label_text.setAlignment(Qt.AlignCenter)
		self.hbox_main.addWidget(self.label_text)
		#volume_popup
		self.volume_popup = Volume_popup()
		self.volume_popup.volume_slider.valueChanged.connect(self.parentWidget.volume_change)
		###
		self.clicked.connect(self.press_volume_button)
		
	def set_info(self, value):
		"""Set volume info"""
		icon = self.VOLUME_ICONS[1]
		self.label_text.setText(str(value))
		if value <= 0: icon = self.VOLUME_ICONS[0]
		elif value > 0 and value < 33: icon = self.VOLUME_ICONS[1]
		elif value > 33 and value < 85: icon = self.VOLUME_ICONS[2]
		elif value >= 85: icon = self.VOLUME_ICONS[3]
		self.label_icon.setPixmap(QPixmap(icon))
		
	def wheelEvent(self, event):
		"""Wheel event"""
		pd = event.pixelDelta()
		ad = event.angleDelta()
		value = self.parentWidget.PLAYER.audio_get_volume()
		if pd.y() > 0 or ad.y() > 0:value += 2
		if pd.y() < 0 or ad.y() < 0:value -= 2
		if value > 100: value = 100
		if value < 0: value = 0
		self.parentWidget.volume_change(value)
		self.set_info(value)
		
	def press_volume_button(self):
		"""Press volume button"""
		position = self.rect().topLeft()
		pos_y = position.y() - self.size().height()
		self.volume_popup.move(self.mapToGlobal(QPoint(position.x(), pos_y)))
		self.volume_popup.show()
		
##################################################################

class Volume_popup(QFrame):
	"""Volime popup class"""
	def __init__(self):
		super().__init__()
		self.setObjectName('Volume_popup')
		self.create_widgets()
		
	def create_widgets(self):
		"""Create widgets"""
	#hbox_main
		self.hbox_main = QHBoxLayout()
		self.setLayout(self.hbox_main)
	#volume_slider
		self.volume_slider = zslider.ZSlider()
		self.volume_slider.setStyleSheet(styles.get_slider_style())
		self.volume_slider.setRange(0, 100)
		self.hbox_main.addWidget(self.volume_slider)
	###
		self.setFixedWidth(160)
		self.setWindowFlags(Qt.Popup)
		
