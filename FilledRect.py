from __future__ import annotations

from typing import Dict, Literal

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtWidgets import QLabel

from Connection import Connection
from RectShape import RectShape
from Scene import Scene
from Utils.Color import get_text_color, get_random_color
from Utils.Geometry import is_rect_colliding_with_rects, is_rect_in_screen
from Utils.Math import sign


class FilledRect(RectShape):
	__next_id: int = 0

	def __init__(self, draw_field: QLabel, scene: Scene, pos: QPoint):
		super().__init__(draw_field, pos)

		self.__scene = scene
		self.__scene.rects.append(self)

		self.__id = FilledRect.__next_id
		FilledRect.__next_id += 1

		self.__is_selected = False
		self.__connections: Dict[FilledRect, Connection] = {}

		self.__bg_color = get_random_color()
		self.__text_color = get_text_color(self.__bg_color)

		self.draw()

	@property
	def id(self):
		return self.__id

	@property
	def is_selected(self):
		return self.__is_selected

	@is_selected.setter
	def is_selected(self, new_value: bool):
		self.__is_selected = new_value

	@property
	def connections(self):
		return self.__connections

	def __move_by(self, target: int, axis: Literal['x', 'y']):
		direction = sign(target - getattr(self.pos, axis)())
		vector = QPoint(1, 0) if axis == 'x' else QPoint(0, 1)
		step = vector * direction

		while (
			is_rect_in_screen(self, self.__scene.size) and
			not is_rect_colliding_with_rects(self, self.__scene.rects, 1) and
			getattr(self.pos, axis)() != target and
			direction != 0
		):

			self.pos += step

		self.pos -= step

	def move(self, new_pos: QPoint):
		"""
		The movement by Ox and Oy should work separately

		If you try to move by Ox an Oy simultaneously you will completely get stuck
		if it get stuck by one of Ox or Oy
		"""
		self.__move_by(new_pos.x(), 'x')
		self.__move_by(new_pos.y(), 'y')

	def __connect(self, rect: FilledRect):
		connection = Connection(
			self.draw_field,
			self.__scene,
			self,
			rect
		)

		self.connections[rect] = connection
		rect.connections[self] = connection

	def __disconnect(self, rect: FilledRect):
		connection = self.connections[rect]

		self.__scene.connections.remove(connection)

		self.connections.pop(rect)
		rect.connections.pop(self)

	def toggle_connection(self, rect: FilledRect):
		if rect in self.connections:
			self.__disconnect(rect)
		else:
			self.__connect(rect)

	def prepare_fill(self, painter: QPainter):
		brush = QBrush()

		brush.setColor(self.__bg_color)
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
		text_pos = QPoint(self.center_coords)

		painter.setPen(self.__text_color)
		painter.drawText(text_pos, str(self.__id))
