from typing import List

from PyQt6.QtCore import QPoint, QSize

from RectShape import RectShape


def is_point_in_rect(rect: RectShape, point: QPoint) -> bool:
	return (
		(rect.pos.x() + RectShape.size().width()) > point.x() > rect.pos.x() and
		(rect.pos.y() + RectShape.size().height()) > point.y() > rect.pos.y()
	)


def is_rect_in_screen(rect: RectShape, scene_size: QSize, offset: int = 0) -> bool:
	# check if any corner dots of rect inside the screen

	return (
		(rect.pos.x() - offset) > 0 and
		(rect.pos.x() + RectShape.size().width() + offset) < scene_size.width() and
		(rect.pos.y() - offset) > 0 and
		(rect.pos.y() + RectShape.size().height() + offset) < scene_size.height()
	)


def are_two_rects_colliding(rect1: RectShape, rect2: RectShape, offset: int = 0) -> bool:
	# check if any corner dots of rect1 (which is not rect2) inside rect 2

	if rect1 is rect2:
		return False

	return (
		rect1.pos.x() < (rect2.pos.x() + RectShape.size().width() + offset) and
		(rect1.pos.x() + RectShape.size().width() + offset) > rect2.pos.x() and
		rect1.pos.y() < (rect2.pos.y() + RectShape.size().height() + offset) and
		(rect1.pos.y() + RectShape.size().height() + offset) > rect2.pos.y()
	)


def is_rect_colliding_with_rects(rect: RectShape, rects_list: List[RectShape], offset: int = 0) -> bool:
	for rects_list_item in rects_list:
		if are_two_rects_colliding(rect, rects_list_item, offset):
			return True

	return False
