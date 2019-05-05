from PyQt5.QtWidgets import QSlider, QStyle
from PyQt5.QtCore import Qt


class ZSlider(QSlider):
	def __init__(self):
		super().__init__()
		self.create_slider()
		
	def create_slider(self):
		
		self.setOrientation(Qt.Horizontal)
		self.set_style()



	def mousePressEvent(self, ev):
		""" Jump to click position """
		self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), ev.x(), self.width()))
		
	def mouseMoveEvent(self, ev):
		""" Jump to pointer position while moving """
		self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), ev.x(), self.width()))


	def set_style(self):
		SLIDER_STYLE = ("""
		QSlider::groove:horizontal {
			border: 1px solid #bbb;
			background: white;
			height: 10px;
			border-radius: 4px;
		}

		QSlider::sub-page:horizontal {
		background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
		    stop: 0 #66e, stop: 1 #bbf);
		background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
		    stop: 0 #bbf, stop: 1 #55f);
		border: 1px solid #777;
		height: 10px;
		border-radius: 4px;
		}

		QSlider::add-page:horizontal {
		background: #fff;
		border: 1px solid #777;
		height: 10px;
		border-radius: 4px;
		}

		QSlider::handle:horizontal {
		background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
		    stop:0 #eee, stop:1 #ccc);
		border: 1px solid #777;
		width: 13px;
		margin-top: -2px;
		margin-bottom: -2px;
		border-radius: 4px;
		}

		QSlider::handle:horizontal:hover {
		background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
		    stop:0 #fff, stop:1 #ddd);
		border: 1px solid #444;
		border-radius: 4px;
		}

		QSlider::sub-page:horizontal:disabled {
		background: #bbb;
		border-color: #999;
		}

		QSlider::add-page:horizontal:disabled {
		background: #eee;
		border-color: #999;
		}

		QSlider::handle:horizontal:disabled {
		background: #eee;
		border: 1px solid #aaa;
		border-radius: 4px;
		}
		""")

		self.setStyleSheet(SLIDER_STYLE)
