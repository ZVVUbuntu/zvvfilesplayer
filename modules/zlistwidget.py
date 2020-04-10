"""My ListWidget module"""
import os
from PyQt5.QtWidgets import QListWidget, QListView, QAbstractItemView, QListWidgetItem, QMenu
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QFileInfo, QSize
from . import paths


class Zlistwidget(QListWidget):
	"""Empty tab class"""
	def __init__(self):
		super().__init__()
		self.setObjectName('Zlistwidget')
		self.CURRENT_ITEM = None
		self.setViewMode(QListView.ListMode)
		self.setMovement(QListView.Static)
		self.setFlow(QListView.TopToBottom)
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.setTextElideMode(Qt.ElideRight)
		self.setFocusPolicy(Qt.NoFocus)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setSortingEnabled(True)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.press_context_menu)
		
	def add_row(self, path):
		"""Add row"""
		if os.path.isdir(path):
			sql = "INSERT INTO userfolders (path) VALUES(?)"
			insert_params = [path, ]
			paths.BASE_CURSOR.execute(sql, insert_params)
			paths.BASE_CONNECTION.commit()
			_id = paths.BASE_CURSOR.lastrowid
			self.item = MyItem()
			self.item.set_info(path, _id)
			self.addItem(self.item)
			
	def press_context_menu(self, qp):
		"""Press context mneu"""
		item_at_pos = self.itemAt(qp)
		if item_at_pos:
			self.CURRENT_ITEM = item_at_pos
			cursor_position = QCursor().pos()
			self.menu = QMenu()
			self.menu.addAction(QIcon(':/trash.png'), 'Remove', self.remove_fav_item)
			self.menu.move(cursor_position)
			self.menu.show()
			
	def remove_fav_item(self):
		"""Remove fav item"""
		if self.CURRENT_ITEM:
			_id = self.CURRENT_ITEM._ID
			sql = "DELETE FROM userfolders WHERE _id=(?)"
			remove_params = [_id, ]
			paths.BASE_CURSOR.execute(sql, remove_params)
			paths.BASE_CONNECTION.commit()
			item = self.takeItem(self.row(self.CURRENT_ITEM))
			del item
			self.CURRENT_ITEM = None
			
	def set_items(self):
		"""Set fav items"""
		self.clear()
		sql = "SELECT * FROM userfolders"
		paths.BASE_CURSOR.execute(sql)
		found_items = paths.BASE_CURSOR.fetchall()
		for item in found_items:
			_id, path = item
			self.item = MyItem()
			self.item.set_info(path, _id)
			self.addItem(self.item)
	
##########################################################################

class MyItem(QListWidgetItem):
	"""Path item class"""
	def __init__(self):
		super().__init__()
		self.setFlags(Qt.ItemIsEnabled)
		self.setSizeHint(QSize(190, 30))
		self.PATH = None
		self._ID = None
		
	def set_info(self, path, _id=0):
		"""Set info"""
		name = os.path.split(path)[1]
		#icon = QFileIconProvider().icon(QFileInfo(path))
		self.setText(name)
		self.setToolTip(name)
		self.setIcon(QIcon(':/folder.png'))
		self.PATH = path
		self._ID = _id
