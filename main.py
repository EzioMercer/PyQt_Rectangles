import os
from sys import argv, exit

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPixmap, QColor, QKeyEvent
from PyQt6.QtWidgets import (
	QWidget,
	QApplication,
	QLabel,
	QGridLayout
)

from DrawField import DrawField


class Window(QWidget):
	def __init__(self, canvas_width: int, canvas_height: int):
		super().__init__()
		padding = 12
		font_size = 12
		grid_gap = 8

		self.setStyleSheet(f'font-size: {font_size}px')
		self.setFixedWidth(canvas_width + padding * 2)
		self.setFixedHeight(canvas_height + padding * 2 + font_size * 2 + grid_gap * 2)
		self.setWindowTitle('Rectangles')

		self.__coord_x_label = QLabel('Coordinate x:')
		self.__coord_y_label = QLabel('Coordinate y:')

		grid_layout = QGridLayout()
		grid_layout.setContentsMargins(padding, padding, padding, padding)
		grid_layout.addWidget(self.__coord_x_label, 0, 0)
		grid_layout.addWidget(self.__coord_y_label, 1, 0)

		canvas = QPixmap(canvas_width, canvas_height)
		canvas.fill(QColor('black'))

		self.__drawField = DrawField(self, canvas)

		grid_layout.addWidget(self.__drawField, 2, 0)

		self.setLayout(grid_layout)

		self.show()

	def update_coords_labels(self, pos: QPoint):
		self.__coord_x_label.setText('Coordinate x: ' + str(pos.x()))
		self.__coord_y_label.setText('Coordinate y: ' + str(pos.y()))

	def keyPressEvent(self, event: QKeyEvent):
		self.__drawField.keyPressEvent(event)

	def keyReleaseEvent(self, event: QKeyEvent):
		self.__drawField.keyReleaseEvent(event)


if __name__ == "__main__":
	os.system('cls')

	App = QApplication(argv)
	window = Window(1000, 1000)
	exit(App.exec())
