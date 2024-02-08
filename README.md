# PyQt_Rectangles

### Mode: Creating/moving rectangle

+ To create rectangle, you need to double-click on the screen.
  Because rectangles cannot be created everywhere, then in this mode you will have a visual hint that will show whether
  it is possible to create a rectangle in the specified place or not:

	+ If the hint is red, then you will not be able to create the rectangle

	+ If the hint is green, then you will be able to create the rectangle

+ To move rectangle, you need to left-click and hold on rectangle and start moving mouse

### Mode: Creating connection between two rectangles

+ **In this mode, you can't neither create nor move rectangle.**
  To enter this mode, you should press and hold <kbd>Ctrl</kbd> key.

	1. You should left-click on rectangle to select it.
	   If you left-click on the selected rectangle, you will unselect it
	2. Click any other rectangle to create a connection between it and selected rectangle.
	   If you left-click on rectangle which already has a connection with the selected rectangle, then a connection will
	   be removed
