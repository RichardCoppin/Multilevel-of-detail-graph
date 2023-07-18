from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsTextItem
)
from PySide6.QtCore import Qt



class Graphics_Node(QGraphicsItem):
    def __init__(self, title, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self._title = title

        self.define_colors()
        self.define_title()


    def define_colors(self):
        self._title_color = Qt.GlobalColor.white


    def define_title(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setPlainText(self._title)
