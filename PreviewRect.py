from PyQt6.QtCore import QPoint, QSize
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QLabel

from RectShape import RectShape
from SceneManager import SceneManager
from Utils.Geometry import is_rect_in_screen, is_rect_colliding_with_rects


class PreviewRect(RectShape):
	def __init__(self, draw_field: QLabel, pos: QPoint, screen_size: QSize):
		super().__init__(draw_field, pos)

		self.screen_size = screen_size

		SceneManager.previewRect = self

		self.draw()

	def has_collision(self) -> bool:
		return (
			is_rect_in_screen(self, self.screen_size, 0) or
			is_rect_colliding_with_rects(self, SceneManager.rects)
		)

	def render_method(self, painter: QPainter):
		pen = QPen()

		has_collision = self.has_collision()

		SceneManager.canCreateNewRect = not has_collision

		color_name = 'red' if has_collision else 'green'

		pen.setColor(QColor(color_name))
		painter.setPen(pen)
