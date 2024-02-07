from __future__ import annotations

from enum import Enum

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QMouseEvent, QPixmap, QKeyEvent, QColor
from PyQt6.QtWidgets import QLabel

from FilledRect import FilledRect
from PreviewRect import PreviewRect
from RectShape import RectShape
from Scene import Scene
from Utils.Geometry import is_point_in_rect


class AppMode(Enum):
	TOGGLE_CONNECTION = 0
	CREATE_RECT = 1
	MOVE_RECT = 2


class DrawField(QLabel):
	def __init__(self, scene: Scene):
		super().__init__()

		self.__scene = scene
		self.setFixedSize(self.__scene.size)
		self.setMouseTracking(True)

		self.__canvas = QPixmap(self.__scene.size)
		self.__canvas.fill(QColor('black'))

		self.setPixmap(self.__canvas)

		self.__diff = QPoint(0, 0)
		self.__mode: AppMode = AppMode.CREATE_RECT

		PreviewRect(self, scene, QPoint(-RectShape.size().width(), -RectShape.size().height()))

		self.__draw_all()

	def __empty_screen(self):
		self.setPixmap(self.__canvas)

	def __draw_all(self):
		for rect in self.__scene.rects:
			rect.draw()

		for connection in self.__scene.connections:
			connection.draw()

		if self.__mode == AppMode.CREATE_RECT:
			self.__scene.preview_rect.draw()

	def __rerender(self):
		self.__empty_screen()
		self.__draw_all()

	def __select_rect(self, rect: FilledRect):
		self.__scene.selected_rect = rect
		rect.is_selected = True

	def __remove_selection(self):
		if self.__scene.selected_rect is None:
			return

		self.__scene.selected_rect.is_selected = False
		self.__scene.selected_rect = None

	def mousePressEvent(self, event: QMouseEvent):
		for rect in self.__scene.rects:
			if not is_point_in_rect(rect, event.pos()):
				continue

			if self.__mode == AppMode.TOGGLE_CONNECTION:
				if rect is self.__scene.selected_rect:
					self.__remove_selection()
				elif self.__scene.selected_rect is None:
					self.__select_rect(rect)
				else:
					self.__scene.selected_rect.toggle_connection(rect)
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

		self.__scene.preview_rect.move(event.pos())

		self.__rerender()

	def mouseMoveEvent(self, event: QMouseEvent):
		self.__scene.preview_rect.move(event.pos())

		if self.__scene.selected_rect is None:
			self.__rerender()
			return

		if self.__mode == AppMode.TOGGLE_CONNECTION:
			self.__rerender()
			return

		self.__scene.selected_rect.move(event.pos() - self.__diff)

		self.__rerender()

	def mouseDoubleClickEvent(self, event: QMouseEvent):
		if (
			not self.__scene.can_create_new_rect or
			self.__mode != AppMode.CREATE_RECT
		):
			return

		FilledRect(
			self,
			self.__scene,
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
