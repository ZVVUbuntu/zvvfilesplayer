"""Controls module"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from modules import time_slider, zslider, styles, zbutton


class Controls(QWidget):
	"""Controls class"""
	def __init__(self):
		super().__init__()
		self.create_widgets()

	def create_widgets(self):
		"""Create widgets"""
	#vbox_main
		self.vbox_main = QVBoxLayout()
		self.vbox_main.setContentsMargins(0, 0, 0, 0)
		self.vbox_main.setSpacing(1)
		self.setLayout(self.vbox_main)
		
	#hbox_time_control
		self.hbox_time_control = QHBoxLayout()
		self.vbox_main.addLayout(self.hbox_time_control)
		#button_prev
		self.button_prev = zbutton.Zbutton()
		self.button_prev.set_info(icon=":/prev.png")
		self.hbox_time_control.addWidget(self.button_prev)
		#button_minus_time
		self.button_minus_time = zbutton.Zbutton()
		self.button_minus_time.set_info(text="-10")
		self.hbox_time_control.addWidget(self.button_minus_time)
		#vbox_position
		self.vbox_position = QVBoxLayout()
		self.vbox_position.setContentsMargins(0,0,0,0)
		self.vbox_position.setSpacing(0)
		self.hbox_time_control.addLayout(self.vbox_position)
		#hbox_pos_labels
		self.hbox_pos_labels = QHBoxLayout()
		self.vbox_position.addLayout(self.hbox_pos_labels)
		#.l current
		self.label_pos_current = QLabel()
		self.label_pos_current.setStyleSheet("color:green;")
		self.hbox_pos_labels.addWidget(self.label_pos_current)
		#stretch
		self.hbox_pos_labels.addStretch()
		#move time
		self.label_move_time = QLabel()
		self.label_move_time.setStyleSheet("color:blue;")
		self.label_move_time.hide()
		self.hbox_pos_labels.addWidget(self.label_move_time)
		#stretch
		self.hbox_pos_labels.addStretch()
		#.l last
		self.label_pos_last = QLabel()
		self.label_pos_last.setStyleSheet("color:red;")
		self.hbox_pos_labels.addWidget(self.label_pos_last)
		#time_slider
		self.time_slider = time_slider.TimeSlider(self)
		self.vbox_position.addWidget(self.time_slider)
		#button_plus_time
		self.button_plus_time = zbutton.Zbutton()
		self.button_plus_time.set_info(text="+15")
		self.hbox_time_control.addWidget(self.button_plus_time)
		#button_next
		self.button_next = zbutton.Zbutton()
		self.button_next.set_info(icon=":/next.png")
		self.hbox_time_control.addWidget(self.button_next)
	
	#hbox_play_controls
		self.hbox_play_controls = QHBoxLayout()
		self.hbox_play_controls.setContentsMargins(0, 0, 0, 0)
		self.vbox_main.addLayout(self.hbox_play_controls)
		#play
		self.button_play = zbutton.Zbutton()
		self.button_play.set_info(icon=":/play.png")
		self.hbox_play_controls.addWidget(self.button_play)
		#pause
		self.button_pause = zbutton.Zbutton()
		self.button_pause.set_info(icon=":/pause.png")
		self.hbox_play_controls.addWidget(self.button_pause)
		#stop
		self.button_stop = zbutton.Zbutton()
		self.button_stop.set_info(icon=":/stop_mode.png")
		self.hbox_play_controls.addWidget(self.button_stop)
		#modes combo
		self.combo_playmodes = QComboBox()
		self.combo_playmodes.setFixedSize(150, 35)
		self.combo_playmodes.setFocusPolicy(Qt.NoFocus)
		self.combo_playmodes.addItem(QIcon(':/stop_mode.png'), "Stop")
		self.combo_playmodes.addItem(QIcon(':/replay_mode.png'), "Replay")
		self.combo_playmodes.addItem(QIcon(':/next_mode.png'), "Next")
		self.combo_playmodes.addItem(QIcon(':/shuffle_mode.png'), "Shuffle")
		self.hbox_play_controls.addWidget(self.combo_playmodes)
		
	#empty_label
		self.empty_label = QLabel()
		self.empty_label.setFixedHeight(35)
		self.hbox_play_controls.addWidget(self.empty_label)
		
	#audio_set_volume
		#add vbox volume and label
		self.vbox_volume = QVBoxLayout()
		self.vbox_volume.setSpacing(0)
		self.vbox_volume.setContentsMargins(0, 0, 0, 0)
		self.hbox_play_controls.addLayout(self.vbox_volume)
		#add label volume
		self.label_volume = QLabel()
		self.label_volume.setAlignment(Qt.AlignCenter)
		self.vbox_volume.addWidget(self.label_volume)
		#add volume
		self.volume_slider = zslider.ZSlider()
		self.volume_slider.setRange(0, 100)
		self.volume_slider.setFixedWidth(150)
		self.vbox_volume.addWidget(self.volume_slider)
		
	def clear_info(self):
		"""Clear info"""
		self.time_slider.setValue(0)
		self.time_slider.setRange(0, 0)
		self.label_pos_current.clear()
		self.label_pos_last.clear()
