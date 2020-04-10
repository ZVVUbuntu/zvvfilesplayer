"""Equalizer module"""
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
							 QLabel, QPushButton, QSlider, 
							 QComboBox, QLineEdit, QCheckBox,
							 QScrollArea, QMenu, QFrame)
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSettings, QSize
from . import paths, styles, zbutton


class Equalizer(QFrame):
	"""Equalizer class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(1, 3, 1, 1)
		self.vbox_main.setSpacing(2)
		self.setLayout(self.vbox_main)
	#hbox_tools
		self.hbox_tools = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_tools)
		#turn
		self.turn_eq = QCheckBox(self.tr("Eq"))
		self.turn_eq.setTristate(False)
		self.turn_eq.stateChanged.connect(self.on_off_eq)
		self.hbox_tools.addWidget(self.turn_eq)
		#combo_presets
		self.model_presets = QStandardItemModel()
		self.combo_presets = QComboBox()
		self.combo_presets.setModel(self.model_presets)
		self.combo_presets.setFocusPolicy(Qt.NoFocus)
		self.combo_presets.setFixedHeight(32)
		self.combo_presets.addItem(self.tr("Choose:"))
		self.combo_presets.activated.connect(self.choose_preset)
		self.hbox_tools.addWidget(self.combo_presets)
		#button_reset
		self.button_reset = zbutton.Zbutton()
		self.button_reset.set_info(icon=':/replay.png', tool_tip=self.tr('Reset'))
		self.button_reset.set_size(32, 32)
		self.button_reset.clicked.connect(self.press_reset)
		self.hbox_tools.addWidget(self.button_reset)
	#hbox_save_preset
		self.hbox_save_preset = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_save_preset)
		#line_preset_name
		self.line_preset_name = QLineEdit()
		self.line_preset_name.setFixedHeight(32)
		self.line_preset_name.setPlaceholderText(self.tr("Preset name"))
		self.line_preset_name.setClearButtonEnabled(True)
		self.line_preset_name.textChanged.connect(self.change_text_preset)
		self.hbox_save_preset.addWidget(self.line_preset_name)
		#button_preset_save
		self.button_preset_save = zbutton.Zbutton()
		self.button_preset_save.set_info(icon=':/save_icon.png', tool_tip=self.tr('Save preset'))
		self.button_preset_save.set_size(32, 32)
		self.button_preset_save.setEnabled(False)
		self.button_preset_save.clicked.connect(self.press_save_new_preset)
		self.hbox_save_preset.addWidget(self.button_preset_save)
	#add scroll slider
		self.scroll_sliders = QScrollArea()
		self.scroll_sliders.setWidgetResizable(True)
		self.vbox_main.addWidget(self.scroll_sliders)
		#add sliders vbox
		self.widget_sliders = QFrame()
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
			
		#AUTORUN
		self.setObjectName('Equalizer_widget')
		self.setWindowFlags(Qt.Popup)
		self.resize(350, 500)
		self.set_eq_state()
		self.add_presets()
		self.check_sliders()
		#self.press_reset()
		self.autostart_preset()
##############################################################################

	def change_text_preset(self, text):
		"""Change preset text"""
		if text: 
			if not self.button_preset_save.isEnabled():
				self.button_preset_save.setEnabled(True)
		else: 
			if self.button_preset_save.isEnabled():
				self.button_preset_save.setEnabled(False)

	def add_presets(self):
		"""Add presets"""
		sql = 'SELECT * FROM presets'
		paths.BASE_CURSOR.execute(sql)
		found_items = paths.BASE_CURSOR.fetchall()
		for item in found_items:
			name, numbers = item
			#add item
			self.item = Preset_item()
			self.item.set_info(name, numbers)
			self.model_presets.appendRow(self.item)

	def press_save_new_preset(self):
		"""Press save new preset"""
		name = self.line_preset_name.text()
		if name:
			name = name.strip()
			#get values
			list_nums = []
			for slider in self.list_sliders:
				list_nums.append(slider.value())
			numbers_string = ','.join([str(n) for n in list_nums])
			#save
			sql = 'INSERT INTO presets VALUES(?,?)'
			insert_params = [name, numbers_string]
			paths.BASE_CURSOR.execute(sql, insert_params)
			paths.BASE_CONNECTION.commit()
			#add item
			self.item = Preset_item()
			self.item.set_info(name, numbers_string)
			self.model_presets.appendRow(self.item)
			#clear
			self.line_preset_name.clear()
			
	def autostart_preset(self):
		"""Autostart preset"""
		if self.turn_eq.isChecked():
			preset_num = paths.PRESET_NUM
			if preset_num <= self.combo_presets.count() - 1:
				self.choose_preset(preset_num)
				self.combo_presets.setCurrentIndex(preset_num)

	def choose_preset(self, index=0):
		"""Choose preset"""
		#index = self.combo_presets.currentIndex()
		paths.PRESET_NUM = index
		if index > 0:
			current_item = self.model_presets.item(index)
			numbers_string = current_item.NUMBERS.split(',')
			list_nums = [int(n) for n in numbers_string]
			for slider in self.list_sliders:
				index = self.list_sliders.index(slider)
				value = list_nums[index]
				slider.setValue(value)
				if index == 0:
					self.parentWidget.EQ.set_preamp(value)
					self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))
				else:
					if index > 0:
						self.parentWidget.EQ.set_amp_at_index(value, index-1)
						self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))
			self.press_accept()
		else:
			self.press_reset()
			
	def set_eq_state(self):
		"""Set equalizer state"""
		eq_state = paths.EQUALIZER_STATE
		self.on_off_eq(eq_state)

	def on_off_eq(self, state):
		"""On/Off equalizer"""
		self.turn_eq.setCheckState(state)
		self.check_sliders()
		self.check_equalizer()
		paths.EQUALIZER_STATE = state
		
	def check_sliders(self):
		"""Check sliders"""
		if self.turn_eq.isChecked():
			self.combo_presets.setEnabled(True)
			self.line_preset_name.setEnabled(True)
			#self.button_preset_save.setEnabled(True)
			for slider in self.list_sliders:
				slider.setEnabled(True)
		else:
			self.combo_presets.setEnabled(False)
			self.line_preset_name.clear()
			self.line_preset_name.setEnabled(False)
			self.button_preset_save.setEnabled(False)
			for slider in self.list_sliders:
				slider.setEnabled(False)

	def check_equalizer(self):
		"""Check equalizer"""
		if self.turn_eq.isChecked():
			self.press_accept()
		else:
			self.parentWidget.PLAYER.set_equalizer(None)

	def press_reset(self):
		band_count = self.parentWidget.EQ_BAND_COUNT
		for i in range(band_count):
			self.parentWidget.EQ.set_amp_at_index(0.0, i)
		for item in self.list_sliders:
			item.setValue(0)
			index = self.list_sliders.index(item)
			self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(0))
		self.combo_presets.setCurrentIndex(0)
		paths.PRESET_NUM = 0
		
	def change_slider_num(self):
		"""Change slider num"""
		if self.turn_eq.isChecked():
			slider = self.sender()
			value = slider.value()
			index = slider.BAND_NUM
			if index == 0:
				self.parentWidget.EQ.set_preamp(value)
			else:
				self.parentWidget.EQ.set_amp_at_index(value, index-1)
			self.press_accept()
			self.vbox_sliders.itemAt(index).itemAt(2).widget().setText(str(value))

	def press_accept(self):
		"""Press accept"""
		if self.turn_eq.isChecked():
			self.parentWidget.PLAYER.set_equalizer(self.parentWidget.EQ)

############################################################################################

class Slider_band(QSlider):
	"""Slider band"""
	def __init__(self):
		super().__init__()
		self.setOrientation(Qt.Horizontal)
		self.setStyleSheet(styles.get_slider_style())
		self.setRange(-20, 20)
		self.BAND_NUM = 0
		
#############################################################################################

class Preset_item(QStandardItem):
	"""Preset item"""
	def __init__(self):
		super().__init__()
		self.NUMBERS = None
		
	def set_info(self, name, numbers):
		"""Set info"""
		self.setText(name)
		self.NUMBERS = numbers
		
