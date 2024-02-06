from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	pass

from enum import Enum

from PyQt6.QtGui import QMouseEvent, QPixmap, QKeyEvent, QColor
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QPoint, Qt

from Utils.Geometry import is_point_in_rect, is_rect_colliding_with_rects, get_coords_for_rect_center, is_rect_in_screen
from RectShape import RectShape
from PreviewRect import PreviewRect
from FilledRect import FilledRect
from SceneManager import SceneManager


class AppMode(Enum):
	TOGGLE_CONNECTION = 0
	CREATE_RECT = 1
	MOVE_RECT = 2


class DrawField(QLabel):
	def __init__(self, canvas_width: int, canvas_height: int):
		super().__init__()

		self.__canvas = QPixmap(canvas_width, canvas_height)
		self.__canvas.fill(QColor('black'))

		self.setFixedWidth(self.__canvas.width())
		self.setFixedHeight(self.__canvas.height())

		self.setPixmap(self.__canvas)
		self.setMouseTracking(True)

		self.__diff = QPoint(0, 0)

		self.__mode: AppMode = AppMode.CREATE_RECT

		PreviewRect(self, QPoint(-RectShape.width, -RectShape.height), self.size())

		self.__draw_all()

	def __empty_screen(self):
		self.setPixmap(self.__canvas)

	def __draw_all(self):
		for rect in SceneManager.rects:
			rect.draw()

		for connection in SceneManager.connections:
			connection.draw()

		if self.__mode == AppMode.CREATE_RECT:
			SceneManager.previewRect.draw()

	def __rerender(self):
		self.__empty_screen()
		self.__draw_all()

	def __select_rect(self, rect: FilledRect):
		SceneManager.selectedRect = rect
		rect.is_selected = True

	def __remove_selection(self):
		if SceneManager.selectedRect is None:
			return

		SceneManager.selectedRect.is_selected = False
		SceneManager.selectedRect = None

	def __move_selected_rect(self, new_pos: QPoint):
		old_pos = QPoint(
			SceneManager.selectedRect.pos.x(),
			SceneManager.selectedRect.pos.y()
		)

		SceneManager.selectedRect.move(new_pos)

		if (
			is_rect_colliding_with_rects(SceneManager.selectedRect, SceneManager.rects, 1) or
			not is_rect_in_screen(SceneManager.selectedRect, self.size(), 0)
		):
			SceneManager.selectedRect.move(old_pos)

	def mousePressEvent(self, event: QMouseEvent):
		for rect in SceneManager.rects:
			if not is_point_in_rect(rect, event.pos()):
				continue

			if self.__mode == AppMode.TOGGLE_CONNECTION:
				if rect is SceneManager.selectedRect:
					self.__remove_selection()
				elif SceneManager.selectedRect is None:
					self.__select_rect(rect)
				else:
					SceneManager.selectedRect.toggle_connection(rect)
			else:
				self.__mode = AppMode.MOVE_RECT
				self.__remove_selection()
				self.__select_rect(rect)

				self.__diff.setX(event.pos().x() - rect.pos.x())
				self.__diff.setY(event.pos().y() - rect.pos.y())

			break

		self.__rerender()

	def mouseReleaseEvent(self, event: QMouseEvent):
		if self.__mode == AppMode.TOGGLE_CONNECTION:
			self.__rerender()
			return

		self.__mode = AppMode.CREATE_RECT

		self.__remove_selection()

		self.__diff.setX(0)
		self.__diff.setY(0)

		SceneManager.previewRect.move(get_coords_for_rect_center(event.pos()))

		self.__rerender()

	def mouseMoveEvent(self, event: QMouseEvent):
		SceneManager.previewRect.move(get_coords_for_rect_center(event.pos()))

		if SceneManager.selectedRect is None:
			self.__rerender()
			return

		if self.__mode == AppMode.TOGGLE_CONNECTION:
			self.__rerender()
			return

		# Move by Ox if possible
		self.__move_selected_rect(
			QPoint(
				event.pos().x() - self.__diff.x(),
				SceneManager.selectedRect.pos.y()
			)
		)

		# Move by Oy if possible
		self.__move_selected_rect(
			QPoint(
				SceneManager.selectedRect.pos.x(),
				event.pos().y() - self.__diff.y()
			)
		)

		self.__rerender()

	def mouseDoubleClickEvent(self, event: QMouseEvent):
		if (
			not SceneManager.canCreateNewRect or
			self.__mode != AppMode.CREATE_RECT
		):
			return

		FilledRect(
			self,
			get_coords_for_rect_center(event.pos())
		)

		self.__rerender()

	def keyPressEvent(self, event: QKeyEvent):
		if event.key() != Qt.Key.Key_Control:
			return

		if self.__mode != AppMode.MOVE_RECT:
			self.__mode = AppMode.TOGGLE_CONNECTION

		self.__rerender()

	def keyReleaseEvent(self, event: QKeyEvent):
		if event.key() != Qt.Key.Key_Control:
			return

		if self.__mode == AppMode.TOGGLE_CONNECTION:
			self.__mode = AppMode.CREATE_RECT
			self.__remove_selection()

		self.__rerender()
