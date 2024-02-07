from abc import ABC, abstractmethod

from PyQt6.QtCore import QPoint, QSize
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QLabel


class RectShape(ABC):
	__height: int = 100
	__width: int = __height * 2

	def __init__(self, draw_field: QLabel, center_pos: QPoint):
		self.__draw_field = draw_field

		# The center of Rectangle must be under the pointer when created
		self.pos = QPoint(
			center_pos.x() - RectShape.size().width() // 2,
			center_pos.y() - RectShape.size().height() // 2
		)

	@staticmethod
	def size() -> QSize:
		return QSize(RectShape.__width, RectShape.__height)

	@property
	def draw_field(self) -> QLabel:
		return self.__draw_field

	@property
	def center_coords(self) -> QPoint:
		return QPoint(
			self.pos.x() + RectShape.size().width() // 2,
			self.pos.y() + RectShape.size().height() // 2
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
			RectShape.size().width(),
			RectShape.size().height()
		)

		self.draw_text(painter)

		painter.end()

		self.draw_field.setPixmap(canvas)
