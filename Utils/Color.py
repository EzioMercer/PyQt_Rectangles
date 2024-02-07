from random import choice

from PyQt6.QtGui import QColor


def get_random_color() -> QColor:
	color_name = choice(QColor.colorNames())

	return QColor(color_name)


def get_text_color(background_color: QColor) -> QColor:
	# Please see links below to understand the formula
	# https://stackoverflow.com/a/1855903/13349770
	# https://www.w3.org/TR/AERT/#color-contrast

	luminance = (
					0.299 * background_color.red() +
					0.587 * background_color.green() +
					0.114 * background_color.blue()
				) / 255

	need_dark_color = luminance > 0.5

	return QColor('black') if need_dark_color else QColor('white')
