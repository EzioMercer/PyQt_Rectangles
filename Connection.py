from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QLabel

from RectShape import RectShape
from SceneManager import SceneManager
from Utils.Geometry import get_rect_center_coords


class Connection:
	def __init__(self, draw_field: QLabel, rect1: RectShape, rect2: RectShape):
		self.draw_field = draw_field
		self.rect1 = rect1
		self.rect2 = rect2

		SceneManager.connections.add(self)

	def draw(self):
		canvas = self.draw_field.pixmap()
		painter = QPainter(canvas)

		pen = QPen()

		pen.setWidth(2)
		pen.setColor(QColor('white'))
		painter.setPen(pen)

		painter.drawLine(
			get_rect_center_coords(self.rect1.pos),
			get_rect_center_coords(self.rect2.pos)
		)

		painter.end()

		self.draw_field.setPixmap(canvas)
