from __future__ import annotations

from typing import Dict

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtWidgets import QLabel

from Connection import Connection
from RectShape import RectShape
from SceneManager import SceneManager
from Utils.Color import get_text_color, get_random_color
from Utils.Geometry import get_rect_center_coords


class FilledRect(RectShape):
	height: int = 128
	width: int = height * 2
	id: int = 0

	def __init__(self, draw_field: QLabel, pos: QPoint):
		super().__init__(draw_field, pos)

		SceneManager.rects.append(self)
		self.id = FilledRect.id
		FilledRect.id += 1

		self.is_selected = False
		self.pos = pos
		self.connections: Dict[FilledRect, Connection] = {}

		self.bg_color = get_random_color()
		self.text_color = get_text_color(self.bg_color)

		self.draw()

	def connect(self, rect: FilledRect):
		connection = Connection(self.draw_field, self, rect)

		self.connections[rect] = connection
		rect.connections[self] = connection

	def disconnect(self, rect: FilledRect):
		connection = self.connections[rect]

		SceneManager.connections.remove(connection)

		self.connections.pop(rect)
		rect.connections.pop(self)

	def toggle_connection(self, rect: FilledRect):
		if rect in self.connections:
			self.disconnect(rect)
		else:
			self.connect(rect)

	def prepare_fill(self, painter: QPainter):
		brush = QBrush()

		brush.setColor(self.bg_color)
		brush.setStyle(Qt.BrushStyle.SolidPattern)
		painter.setBrush(brush)

		pen = QPen()

		if self.is_selected:
			pen.setColor(QColor('blue'))
			pen.setWidth(4)
		else:
			pen.setColor(QColor('white'))
			pen.setWidth(1)

		painter.setPen(pen)

	def draw_text(self, painter: QPainter):
		text_pos = QPoint(get_rect_center_coords(self.pos))

		painter.setPen(self.text_color)
		painter.drawText(text_pos, str(self.id))
