"""Controls module"""
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from . import time_slider, zbutton, zvolume, paths


class Controls(QFrame):
	"""Controls class"""
	def __init__(self, parentWidget):
		super().__init__()
		self.parentWidget = parentWidget
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
		self.setObjectName('Controls_widget')
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(0, 0, 0, 0)
		self.vbox_main.setSpacing(1)
		self.setLayout(self.vbox_main)
		
	#hbox_time_control
		self.hbox_time_control = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_time_control)
		#button_minus_time
		self.button_minus_time = zbutton.Zbutton()
		self.button_minus_time.set_info(text="-10")
		#self.button_minus_time.setObjectName('Round_button')
		self.hbox_time_control.addWidget(self.button_minus_time)
		#vbox_position
		self.vbox_position = QVBoxLayout()
		self.vbox_position.setContentsMargins(8, 0, 8, 0)
		self.vbox_position.setSpacing(0)
		self.hbox_time_control.addLayout(self.vbox_position)
		#hbox_pos_labels
		self.hbox_pos_labels = QHBoxLayout()
		self.vbox_position.addLayout(self.hbox_pos_labels)
		#.l current
		self.label_pos_current = QLabel()
		self.label_pos_current.setObjectName('Label_current_time_position')
		self.hbox_pos_labels.addWidget(self.label_pos_current)
		#stretch
		self.hbox_pos_labels.addStretch()
		#move time
		self.label_move_time = QLabel()
		self.label_move_time.setObjectName('Label_move_time_position')
		self.label_move_time.hide()
		self.hbox_pos_labels.addWidget(self.label_move_time)
		#stretch
		self.hbox_pos_labels.addStretch()
		#.l last
		self.label_pos_last = QLabel()
		self.label_pos_last.setObjectName('Label_max_time_position')
		self.hbox_pos_labels.addWidget(self.label_pos_last)
		#time_slider
		self.time_slider = time_slider.TimeSlider(self)
		self.vbox_position.addWidget(self.time_slider)
		#button_plus_time
		self.button_plus_time = zbutton.Zbutton()
		self.button_plus_time.set_info(text="+15")
		#self.button_plus_time.setObjectName('Round_button')
		self.hbox_time_control.addWidget(self.button_plus_time)
	
	#hbox_play_controls
		self.hbox_play_controls = QHBoxLayout()
		self.hbox_play_controls.setContentsMargins(0, 0, 0, 0)
		self.hbox_play_controls.setSpacing(3)
		self.vbox_main.addLayout(self.hbox_play_controls)
		#modes combo
		self.combo_playmodes = QComboBox()
		self.combo_playmodes.setFixedSize(60, 40)
		self.combo_playmodes.setFocusPolicy(Qt.NoFocus)
		self.combo_playmodes.setIconSize(QSize(24, 24))
		self.combo_playmodes.addItem(QIcon(':/stop.png'), "")
		self.combo_playmodes.addItem(QIcon(':/replay.png'), "")
		self.combo_playmodes.addItem(QIcon(':/next_icon.png'), "")
		self.combo_playmodes.addItem(QIcon(':/shuffle.png'), "")
		list_modes = ['stop', 'replay', 'next', 'shuffle', ]
		for item in list_modes:
			index = list_modes.index(item)
			self.combo_playmodes.setItemData(index, item, Qt.ToolTipRole)
		self.combo_playmodes.activated.connect(self.change_play_mode)
		self.hbox_play_controls.addWidget(self.combo_playmodes)
		self.hbox_play_controls.setAlignment(self.combo_playmodes, Qt.AlignBottom)
		#
		self.hbox_play_controls.addStretch()
		#button_prev
		self.button_prev = zbutton.Zbutton()
		self.button_prev.set_info(icon=":/prev.png")
		self.hbox_play_controls.addWidget(self.button_prev)
		#play
		self.button_play_pause = zbutton.Zbutton()
		self.button_play_pause.set_info(icon=":/play.png")
		self.button_play_pause.set_size(60, 60)
		#self.button_play_pause.setObjectName('Round_button')
		self.hbox_play_controls.addWidget(self.button_play_pause)
		#button_next
		self.button_next = zbutton.Zbutton()
		self.button_next.set_info(icon=":/next.png")
		self.hbox_play_controls.addWidget(self.button_next)
		#
		self.hbox_play_controls.addStretch()
	#volume
		self.volume_button = zvolume.Zvolume(self.parentWidget)
		self.hbox_play_controls.addWidget(self.volume_button)
		self.hbox_play_controls.setAlignment(self.volume_button, Qt.AlignBottom)
		
		#AUTOSTART
		self.set_default_playmode()
#######################################################################################
		
	def clear_info(self):
		"""Clear info"""
		self.time_slider.setValue(0)
		self.time_slider.setRange(0, 1)
		self.label_pos_current.clear()
		self.label_pos_last.clear()
		
	def change_play_mode(self, index=0):
		"""Change play mode"""
		paths.PLAY_MODE = index
		
	def set_default_playmode(self):
		"""Set default play mode"""
		play_mode = paths.PLAY_MODE
		self.combo_playmodes.setCurrentIndex(play_mode)
