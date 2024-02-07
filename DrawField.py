from __future__ import annotations

from enum import Enum

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QMouseEvent, QPixmap, QKeyEvent, QColor
from PyQt6.QtWidgets import QLabel

from FilledRect import FilledRect
from PreviewRect import PreviewRect
from RectShape import RectShape
from SceneManager import SceneManager
from Utils.Geometry import is_point_in_rect


class AppMode(Enum):
	TOGGLE_CONNECTION = 0
	CREATE_RECT = 1
	MOVE_RECT = 2


class DrawField(QLabel):
	def __init__(self):
		super().__init__()

		self.__canvas = QPixmap(SceneManager.scene_size)
		self.__canvas.fill(QColor('black'))

		self.setFixedSize(SceneManager.scene_size)

		self.setPixmap(self.__canvas)
		self.setMouseTracking(True)

		self.__diff = QPoint(0, 0)
		self.__selected_rect: FilledRect | None = None

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
		self.__selected_rect = rect
		rect.is_selected = True

	def __remove_selection(self):
		if self.__selected_rect is None:
			return

		self.__selected_rect.is_selected = False
		self.__selected_rect = None

	def mousePressEvent(self, event: QMouseEvent):
		for rect in SceneManager.rects:
			if not is_point_in_rect(rect, event.pos()):
				continue

			if self.__mode == AppMode.TOGGLE_CONNECTION:
				if rect is self.__selected_rect:
					self.__remove_selection()
				elif self.__selected_rect is None:
					self.__select_rect(rect)
				else:
					self.__selected_rect.toggle_connection(rect)
			else:
				self.__mode = AppMode.MOVE_RECT

				self.__remove_selection()
				self.__select_rect(rect)

				self.__diff = event.pos() - rect.pos

			break

		self.__rerender()

	def mouseReleaseEvent(self, event: QMouseEvent):
		if self.__mode == AppMode.TOGGLE_CONNECTION:
			self.__rerender()
			return

		self.__mode = AppMode.CREATE_RECT

		self.__remove_selection()

		self.__diff = QPoint(0, 0)

		SceneManager.previewRect.move(event.pos())

		self.__rerender()

	def mouseMoveEvent(self, event: QMouseEvent):
		SceneManager.previewRect.move(event.pos())

		if self.__selected_rect is None:
			self.__rerender()
			return

		if self.__mode == AppMode.TOGGLE_CONNECTION:
			self.__rerender()
			return

		self.__selected_rect.move(event.pos() - self.__diff)

		self.__rerender()

	def mouseDoubleClickEvent(self, event: QMouseEvent):
		if (
			not SceneManager.canCreateNewRect or
			self.__mode != AppMode.CREATE_RECT
		):
			return

		FilledRect(
			self,
			event.pos()
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
