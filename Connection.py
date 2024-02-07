from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QLabel

from RectShape import RectShape
from Scene import Scene


class Connection:
	def __init__(self, draw_field: QLabel, scene: Scene, rect1: RectShape, rect2: RectShape):
		self.__draw_field = draw_field
		self.__rect1 = rect1
		self.__rect2 = rect2

		scene.connections.add(self)

	def draw(self):
		canvas = self.__draw_field.pixmap()
		painter = QPainter(canvas)

		pen = QPen()

		pen.setWidth(2)
		pen.setColor(QColor('white'))
		painter.setPen(pen)

		painter.drawLine(
			self.__rect1.center_coords,
			self.__rect2.center_coords
		)

		painter.end()

		self.__draw_field.setPixmap(canvas)
