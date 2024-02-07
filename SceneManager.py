from __future__ import annotations

from typing import TYPE_CHECKING, List, Set

from PyQt6.QtCore import QSize

if TYPE_CHECKING:
	from FilledRect import FilledRect
	from PreviewRect import PreviewRect
	from Connection import Connection


class SceneManager:
	scene_size: QSize = QSize(0, 0)
	previewRect: PreviewRect = None
	rects: List[FilledRect] = []
	canCreateNewRect = False
	connections: Set[Connection] = set()
