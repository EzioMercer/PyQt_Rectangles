from abc import ABC, abstractmethod

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QLabel


class RectShape(ABC):
	height: int = 100
	width: int = height * 2

	def __init__(self, draw_field: QLabel, pos: QPoint):
		self.__draw_field = draw_field
		self.__pos = pos

	@property
	def draw_field(self):
		return self.__draw_field

	@property
	def pos(self):
		return self.__pos

	def move(self, new_pos: QPoint):
		self.__pos = new_pos

	@abstractmethod
	def prepare_fill(self, painter: QPainter):
		return NotImplemented

	def draw_text(self, painter: QPainter):
		return NotImplemented

	def draw(self):
		canvas = self.draw_field.pixmap()
		painter = QPainter(canvas)

		self.prepare_fill(painter)

		painter.drawRect(
			self.pos.x(),
			self.pos.y(),
			RectShape.width,
			RectShape.height
		)

		self.draw_text(painter)

		painter.end()

		self.draw_field.setPixmap(canvas)
