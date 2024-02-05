from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from main import Window

from Utils.Geometry import is_point_in_rect, is_rect_colliding_with_rects, get_coords_for_rect_center, is_rect_in_screen

from PyQt6.QtGui import QMouseEvent, QPixmap, QKeyEvent
from PyQt6.QtWidgets import QLabel

from PyQt6.QtCore import QPoint, Qt

from RectShape import RectShape
from PreviewRect import PreviewRect
from FilledRect import FilledRect
from SceneManager import SceneManager


class DrawField(QLabel):
	def __init__(self, parent_window: Window, canvas: QPixmap):
		super().__init__()

		self.parent_window = parent_window
		self.setFixedWidth(canvas.width())
		self.setFixedHeight(canvas.height())

		self.canvas = canvas
		self.setPixmap(canvas)
		self.setMouseTracking(True)

		self.diff = QPoint(0, 0)

		self.is_connection_toggle_mode = False
		self.is_rect_create_mode = True
		self.is_rect_move_mode = False

		PreviewRect(self, QPoint(-RectShape.width, -RectShape.height), self.size())

		self.draw_all()

	def empty_screen(self):
		self.setPixmap(self.canvas)

	def draw_all(self):
		for rect in SceneManager.rects:
			rect.draw()

		for connection in SceneManager.connections:
			connection.draw()

		if self.is_rect_create_mode:
			SceneManager.previewRect.draw()

	def rerender(self):
		self.empty_screen()
		self.draw_all()

	def select_rect(self, rect: FilledRect):
		SceneManager.selectedRect = rect
		rect.is_selected = True

	def deselect_selected_rect(self):
		if SceneManager.selectedRect is None:
			return

		SceneManager.selectedRect.is_selected = False
		SceneManager.selectedRect = None

	def mousePressEvent(self, event: QMouseEvent):

		for rect in SceneManager.rects:
			if not is_point_in_rect(rect, event.pos()):
				self.is_rect_create_mode = not self.is_connection_toggle_mode
				self.is_rect_move_mode = False

				continue

			self.is_rect_create_mode = False
			self.is_rect_move_mode = not self.is_connection_toggle_mode

			if self.is_connection_toggle_mode:
				if rect is SceneManager.selectedRect:
					self.deselect_selected_rect()
				elif SceneManager.selectedRect is None:
					self.select_rect(rect)
				else:
					SceneManager.selectedRect.toggle_connection(rect)
			else:
				self.deselect_selected_rect()
				self.select_rect(rect)

				self.diff.setX(event.pos().x() - rect.pos.x())
				self.diff.setY(event.pos().y() - rect.pos.y())

			break

		self.rerender()

	def mouseReleaseEvent(self, event: QMouseEvent):

		self.is_rect_move_mode = False

		if self.is_connection_toggle_mode is True:
			self.rerender()
			return

		self.is_rect_create_mode = True

		self.deselect_selected_rect()

		self.diff.setX(0)
		self.diff.setY(0)

		SceneManager.previewRect.move(get_coords_for_rect_center(event.pos()))

		self.rerender()

	def mouseMoveEvent(self, event: QMouseEvent):

		self.parent_window.update_coords_labels(event.pos())

		SceneManager.previewRect.move(get_coords_for_rect_center(event.pos()))

		if SceneManager.selectedRect is None:
			self.rerender()
			return

		if self.is_connection_toggle_mode is True:
			self.rerender()
			return

		old_pos = QPoint(
			SceneManager.selectedRect.pos.x(),
			SceneManager.selectedRect.pos.y()
		)

		SceneManager.selectedRect.move(
			QPoint(
				event.pos().x() - self.diff.x(),
				event.pos().y() - self.diff.y()
			)
		)

		if (
			is_rect_colliding_with_rects(SceneManager.selectedRect, SceneManager.rects, 1) or
			is_rect_in_screen(SceneManager.selectedRect, self.size(), 0)
		):
			SceneManager.selectedRect.move(old_pos)

		self.rerender()

	def mouseDoubleClickEvent(self, event: QMouseEvent):

		if (
			SceneManager.canCreateNewRect is False or
			self.is_rect_create_mode is False
		):
			return

		FilledRect(
			self,
			get_coords_for_rect_center(event.pos())
		)

		self.rerender()

	def keyPressEvent(self, event: QKeyEvent):

		if event.key() != Qt.Key.Key_Control:
			return

		if self.is_rect_move_mode is False:
			self.is_connection_toggle_mode = True

		self.is_rect_create_mode = False

		self.rerender()

	def keyReleaseEvent(self, event: QKeyEvent):

		if event.key() != Qt.Key.Key_Control:
			return

		self.is_connection_toggle_mode = False

		if self.is_rect_move_mode is False:
			self.is_rect_create_mode = True
			self.deselect_selected_rect()

		self.rerender()
