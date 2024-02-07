from __future__ import annotations

from typing import TYPE_CHECKING, List, Set

from PyQt6.QtCore import QSize

if TYPE_CHECKING:
	from FilledRect import FilledRect
	from PreviewRect import PreviewRect
	from Connection import Connection


class Scene:
	def __init__(self, canvas_width: int, canvas_height: int):
		self.__size: QSize = QSize(canvas_width, canvas_height)
		self.__selected_rect: FilledRect | None = None
		self.__preview_rect: PreviewRect | None = None
		self.__rects: List[FilledRect] = []
		self.__can_create_new_rect = False

		# Used Set instead of List to effectively remove an item
		self.__connections: Set[Connection] = set()

	@property
	def size(self):
		return self.__size

	@property
	def selected_rect(self):
		return self.__selected_rect

	@selected_rect.setter
	def selected_rect(self, new_val: FilledRect):
		self.__selected_rect = new_val

	@property
	def preview_rect(self):
		return self.__preview_rect

	@preview_rect.setter
	def preview_rect(self, new_val: PreviewRect):
		self.__preview_rect = new_val

	@property
	def rects(self):
		return self.__rects

	@property
	def can_create_new_rect(self):
		return self.__can_create_new_rect

	@can_create_new_rect.setter
	def can_create_new_rect(self, new_val: bool):
		self.__can_create_new_rect = new_val

	@property
	def connections(self):
		return self.__connections
