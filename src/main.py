import sys
from collections import namedtuple
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QBrush,
    QPainter,
    QPen,
    QWheelEvent
)
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

point = namedtuple('point', ['x', 'y'])


class GraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        self.origin = point(0, 0)
        self.translation = False
        super().__init__(*args, **kwargs)

    def wheelEvent(self, event):
        # Zoom Factor
        zoomInFactor = 1.1

        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        zoomFactor = zoomInFactor ** (event.angleDelta().y() / 120)
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self.origin = point(event.x(), event.y())
            self.translation = True
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.translation = False
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.translation:
            delta = point(event.x() - self.origin.x, event.y() - self.origin.y)
            self.translate(delta.x, delta.y)
            self.origin = point(event.x(), event.y())
        return super().mouseMoveEvent(event)


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Defining a scene rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene = QGraphicsScene(0, 0, 400, 200)

        # Draw a rectangle item, setting the dimensions.
        rect = QGraphicsRectItem(0, 0, 200, 50)
        rect.setPos(50, 20)
        rect.setTransformOriginPoint(100, 25)
        brush = QBrush(Qt.red)
        rect.setBrush(brush)

        # Define the pen (line)
        pen = QPen(Qt.cyan)
        pen.setWidth(10)
        rect.setPen(pen)

        ellipse = QGraphicsEllipseItem(0, 0, 100, 100)
        ellipse.setTransformOriginPoint(50, 50)
        ellipse.setPos(75, 30)

        brush = QBrush(Qt.blue)
        ellipse.setBrush(brush)

        pen = QPen(Qt.green)
        pen.setWidth(5)
        ellipse.setPen(pen)

        # Add the items to the scene. Items are stacked in the order they are added.
        self.scene.addItem(ellipse)
        self.scene.addItem(rect)


        # Set all items as moveable and selectable.
        for item in self.scene.items():
            item.setFlag(QGraphicsItem.ItemIsMovable)
            item.setFlag(QGraphicsItem.ItemIsSelectable)

        # Define our layout.
        vbox = QVBoxLayout()

        up = QPushButton("Up")
        up.clicked.connect(self.up)
        vbox.addWidget(up)

        down = QPushButton("Down")
        down.clicked.connect(self.down)
        vbox.addWidget(down)

        self.rotation_slider = QSlider()
        self.rotation_slider.setRange(-180, 180)
        self.rotation_slider.valueChanged.connect(self.rotate)
        vbox.addWidget(self.rotation_slider)

        self.view = GraphicsView(self.scene)
        self.view.setBackgroundBrush(QBrush(Qt.white))

        self.view.setRenderHint(QPainter.Antialiasing)

        hbox = QHBoxLayout(self)
        hbox.addLayout(vbox)
        hbox.addWidget(self.view)

        self.setLayout(hbox)

    def up(self):
        """ Iterate all selected items in the view, moving them forward. """
        items = self.scene.selectedItems()
        for item in items:
            z = item.zValue()
            item.setZValue(z + 1)

    def down(self):
        """ Iterate all selected items in the view, moving them backward. """
        items = self.scene.selectedItems()
        for item in items:
            z = item.zValue()
            item.setZValue(z - 1)

    def rotate(self, value):
        """ Rotate the object by the received number of degrees """
        items = self.scene.selectedItems()
        for item in items:
            item.setRotation(value)

    def rotate_delta(self, delta):
        items = self.scene.selectedItems()
        for item in items:
            value = item.rotation()
            item.setRotation(value + delta)

    # def wheelEvent(self, a0: QWheelEvent) -> None:
    #     # self.rotate_delta(a0.angleDelta().y()/120)
    #     self.scene.
    #     return super().wheelEvent(a0)



app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()
