from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QLabel

from RectShape import RectShape
from Scene import Scene
from Utils.Geometry import is_rect_in_screen, is_rect_colliding_with_rects


class PreviewRect(RectShape):
	def __init__(self, draw_field: QLabel, scene: Scene, pos: QPoint):
		super().__init__(draw_field, pos)

		self.__scene = scene

		self.__scene.preview_rect = self

		self.draw()

	def move(self, new_pos: QPoint):
		# The center of Preview Rectangle must be under the pointer always
		self.pos = QPoint(
			new_pos.x() - RectShape.size().width() // 2,
			new_pos.y() - RectShape.size().height() // 2
		)

	def __has_collision(self) -> bool:
		return (
			not is_rect_in_screen(self, self.__scene.size, 0) or
			is_rect_colliding_with_rects(self, self.__scene.rects)
		)

	def prepare_fill(self, painter: QPainter):
		pen = QPen()

		has_collision = self.__has_collision()

		self.__scene.can_create_new_rect = not has_collision

		color_name = 'red' if has_collision else 'green'

		pen.setColor(QColor(color_name))
		painter.setPen(pen)
