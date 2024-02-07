import os
from sys import argv, exit

from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
	QWidget,
	QApplication,
	QGridLayout
)

from DrawField import DrawField
from Scene import Scene


class Window(QWidget):
	def __init__(self, canvas_width: int, canvas_height: int):
		super().__init__()
		padding = 0

		self.setFixedSize(canvas_width, canvas_height)
		self.setWindowTitle('Rectangles')

		grid_layout = QGridLayout()
		grid_layout.setContentsMargins(padding, padding, padding, padding)

		self.__drawField = DrawField(Scene(canvas_width, canvas_height))

		grid_layout.addWidget(self.__drawField)

		self.setLayout(grid_layout)

		self.show()

	def keyPressEvent(self, event: QKeyEvent):
		self.__drawField.keyPressEvent(event)

	def keyReleaseEvent(self, event: QKeyEvent):
		self.__drawField.keyReleaseEvent(event)


if __name__ == "__main__":
	os.system('cls')

	App = QApplication(argv)
	window = Window(1000, 1000)
	exit(App.exec())
