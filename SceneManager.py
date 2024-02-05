from __future__ import annotations

from typing import TYPE_CHECKING, List, Set

if TYPE_CHECKING:
	from FilledRect import FilledRect
	from PreviewRect import PreviewRect
	from Connection import Connection


class SceneManager:
	previewRect: PreviewRect = None
	rects: List[FilledRect] = []
	canCreateNewRect = False
	selectedRect: FilledRect = None
	connections: Set[Connection] = set()
