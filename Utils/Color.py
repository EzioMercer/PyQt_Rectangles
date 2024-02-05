from random import choice

from PyQt6.QtGui import QColor


def get_random_color() -> QColor:
	color_name = choice(QColor.colorNames())

	return QColor(color_name)


def get_text_color(background_color: QColor) -> QColor:
	a = 1 - (0.299 * background_color.redF() + 0.587 * background_color.greenF() + 0.114 * background_color.blueF())

	is_dark_color = (background_color.alphaF() > 0) and (a >= 0.3)

	return QColor('white') if is_dark_color else QColor('black')
