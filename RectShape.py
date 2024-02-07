from abc import ABC, abstractmethod

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QLabel


class RectShape(ABC):
	height: int = 100
	width: int = height * 2

	def __init__(self, draw_field: QLabel, center_pos: QPoint):
		self.__draw_field = draw_field
		self.pos = QPoint(
			center_pos.x() - RectShape.width // 2,
			center_pos.y() - RectShape.height // 2
		)

	@property
	def draw_field(self) -> QLabel:
		return self.__draw_field

	@property
	def center_coords(self) -> QPoint:
		return QPoint(
			self.pos.x() + RectShape.width // 2,
			self.pos.y() + RectShape.height // 2
		)

	@abstractmethod
	def move(self, new_pos: QPoint):
		self.pos = new_pos

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
