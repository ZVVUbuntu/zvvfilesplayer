"""Equalizer module"""
import os
import sys
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QLabel, QPushButton, QSlider, 
							 QComboBox, QLineEdit, QCheckBox,
							 QScrollArea, QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings, QSize
from . import vlc, styles


class Equalizer(QWidget):
	"""Equalizer class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		#EQUALIZER
		self.eq = vlc.AudioEqualizer()
		
#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 1, 1, 1)
		self.vbox_main.setSpacing(3)
		self.setLayout(self.vbox_main)

	#add hbox turn and presets
		self.hbox_presets = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_presets)
		#turn
		self.turn_eq = QCheckBox(self.tr("Eq on/off"))
		self.turn_eq.stateChanged.connect(self.on_off_eq)
		self.hbox_presets.addWidget(self.turn_eq)
		#combo presets
		self.combo_presets = QComboBox()
		self.combo_presets.setFixedHeight(32)
		self.hbox_presets.addWidget(self.combo_presets)
		default_path_presets = os.path.join(os.getcwd(), "presets")
		list_presets = os.listdir(default_path_presets)
		list_presets.sort()
		self.combo_presets.addItem(self.tr("Choose:"))
		for item in list_presets:
			self.combo_presets.addItem(item)
		self.combo_presets.activated.connect(self.choose_preset)

	#add scroll slider
		self.scroll_sliders = QScrollArea()
		self.scroll_sliders.setWidgetResizable(True)
		self.vbox_main.addWidget(self.scroll_sliders)
		#add sliders vbox
		self.widget_sliders = QWidget()
		self.scroll_sliders.setWidget(self.widget_sliders)
		self.vbox_sliders = QVBoxLayout()
		self.widget_sliders.setLayout(self.vbox_sliders)
		
		#list_sliders
		self.list_sliders = []
		
		#list_sliders_names
		self.list_slider_names = [
								"Preamp:", "31 Hz:", "62 Hz:",
								"125 Hz:", "250 Hz:", "500 Hz:",
								"1 KHz:", "2 KHz", "4 KHz:",
								"8 KHz:", "16 KHz:",
							]
		for item in self.list_slider_names:
			index = self.list_slider_names.index(item)
			self.hbox = QHBoxLayout()
			self.vbox_sliders.addLayout(self.hbox)
			self.label_name = QLabel(item + '\t')
			self.hbox.addWidget(self.label_name)
			self.slider = Slider_band()
			self.list_sliders.append(self.slider)
			self.slider.BAND_NUM = index
			self.slider.valueChanged.connect(self.change_slider_num)
			self.hbox.addWidget(self.slider)
			self.label_value = QLabel()
			self.hbox.addWidget(self.label_value)
			
	#hbox_tools
		self.hbox_tools = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_tools)
		#button_accept
		self.button_accept = Button_tool()
		self.button_accept.set_info(text="Accept", icon=':/accept_icon.png')
		self.button_accept.clicked.connect(self.press_accept)
		self.hbox_tools.addWidget(self.button_accept)
		#button_reset
		self.button_reset = Button_tool()
		self.button_reset.set_info(text="Reset", icon=':/reset_icon.png')
		self.button_reset.clicked.connect(self.press_reset)
		self.hbox_tools.addWidget(self.button_reset)
		
		#AUTORUN
		self.check_sliders()
##############################################################################

	def choose_preset(self):
		"""Choose preset"""
		if self.combo_presets.currentIndex() > 0:
			presets_path = os.path.join(os.getcwd(), "presets")
			current_text = self.combo_presets.currentText()
			get_preset_path = os.path.join(presets_path, current_text)
			if os.path.exists(get_preset_path):
				with open(get_preset_path, 'r', encoding='utf-8') as file_load:
					list_nums = json.load(file_load)
					for slider in self.list_sliders:
						index = self.list_sliders.index(slider)
						value = list_nums[index]
						slider.setValue(value)
						if index == 0:
							self.eq.set_preamp(value)
							self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))
						else:
							if index > 0:
								self.eq.set_amp_at_index(value, index-1)
								self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))
			self.press_accept()
		else:
			self.press_reset()

	def on_off_eq(self):
		"""On/Off equalizer"""
		self.check_sliders()
		self.check_equalizer()
		
	def check_sliders(self):
		"""Check sliders"""
		if self.turn_eq.isChecked():
			self.combo_presets.setEnabled(True)
			for slider in self.list_sliders:
				slider.setEnabled(True)
		else:
			self.combo_presets.setEnabled(False)
			for slider in self.list_sliders:
				slider.setEnabled(False)

	def check_equalizer(self):
		"""Check equalizer"""
		if self.turn_eq.isChecked():
			self.press_accept()
		else:
			self.parentWidget.PLAYER.set_equalizer(None)

	def press_reset(self):
		band_count = vlc.libvlc_audio_equalizer_get_band_count()
		for i in range(band_count):
			self.eq.set_amp_at_index(0.0, i)
		for item in self.list_sliders:
			item.setValue(0)
		self.combo_presets.setCurrentIndex(0)
		
	def change_slider_num(self):
		"""Change slider num"""
		if self.turn_eq.isChecked():
			slider = self.sender()
			value = slider.value()
			index = slider.BAND_NUM
			if index == 0:
				self.eq.set_preamp(value)
			else:
				self.eq.set_amp_at_index(value, index-1)
			self.press_accept()
			self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))

	def press_accept(self):
		"""Press accept"""
		if self.turn_eq.isChecked():
			self.parentWidget.PLAYER.set_equalizer(self.eq)

############################################################################################

class Slider_band(QSlider):
	"""Slider band"""
	def __init__(self):
		super().__init__()
		self.setOrientation(Qt.Horizontal)
		self.setStyleSheet(styles.get_slider_style())
		self.setRange(-20, 20)
		self.BAND_NUM = 0
		
############################################################################################

class Button_tool(QPushButton):
	"""Button tool class"""
	def __init__(self):
		super().__init__()
		self.setFixedHeight(30)
		self.setIconSize(QSize(25, 25))
		self.setStyleSheet(styles.get_button_style())
		self.setCursor(Qt.PointingHandCursor)
		self.setFocusPolicy(Qt.NoFocus)
		
	def set_info(self, text='', icon=''):
		"""Set info"""
		self.setText(text)
		self.setIcon(QIcon(icon))
		
