from typing import Optional
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsTextItem
)
from PySide6.QtCore import Qt, QRect, QPoint

DEFAULT_BORDER_COLOR = '#FF536267'
SELECTED_BORDER_COLOR = '#FFd6fffa'
DEFAULT_BANNER_COLOR = '#FF536267'
DEFAULT_BACKGROUND_COLOR = '#E685a3b2'

class Graphics_Node(QGraphicsItem):
    def __init__(self, title, parent: QtWidgets.QWidget | None = None, position: QPoint = QPoint(0, 0)) -> None:
        super().__init__(parent)

        self.parent = parent
        self.position: QPoint = position

        self._define_colors()
        self._define_pens_and_brushes()
        self._define_title(title)
        self._define_geometry()
        self._define_behaviour_flags()


    def _define_geometry(self):
        self.width = 180
        self.height = 240
        self.radius = 5
        self.banner_height = 25


    def _define_colors(self):
        self._title_color = Qt.GlobalColor.white
        self._default_border_color = QtGui.QColor(DEFAULT_BORDER_COLOR)
        self._selected_border_color = QtGui.QColor(SELECTED_BORDER_COLOR)
        self._default_banner_color = QtGui.QColor(DEFAULT_BANNER_COLOR)
        self._selected_banner_color = QtGui.QColor(DEFAULT_BANNER_COLOR)
        self._selected_banner_color = QtGui.QColor(DEFAULT_BANNER_COLOR)
        self._default_background_color = QtGui.QColor(DEFAULT_BACKGROUND_COLOR)


    def _define_pens_and_brushes(self):
        self._default_border_pen  = QtGui.QPen(self._default_border_color)
        self._selected_border_pen = QtGui.QPen(self._selected_border_color)

        self._default_banner_brush  = QtGui.QBrush(self._default_border_color)
        self._selected_banner_brush = QtGui.QBrush(self._selected_border_color)

        self._default_background_brush = QtGui.QBrush(self._default_background_color)


    def _define_title(self, title):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setPos(self.position)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title = title


    def _define_behaviour_flags(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)


    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)


    def boundingRect(self) -> QRect:
        return QRect(self.position.x(), self.position.y(), self.width, self.height)


    def paint(
        self, 
        painter: QtGui.QPainter, 
        option: QtWidgets.QStyleOptionGraphicsItem, 
        widget: Optional[QtWidgets.QWidget] = ...
    ) -> None: 
        self._paint_background(painter)
        self._paint_title_banner(painter)
        self._paint_border(painter)


    def _paint_title_banner(self, painter):
        path_title = QtGui.QPainterPath()
        path_title.setFillRule(Qt.FillRule.WindingFill)
        path_title.addRoundedRect(
            self.position.x(), self.position.y(), self.width, self.banner_height, self.radius, self.radius
        )
        y_offset = self.position.y() + self.banner_height - self.radius
        path_title.addRect(self.position.x(), y_offset, self.radius, self.radius)
        path_title.addRect(self.position.x() + self.width - self.radius, y_offset, self.radius, self.radius)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._default_banner_brush)
        painter.drawPath(path_title)


    def _paint_background(self, painter):
        path_title = QtGui.QPainterPath()
        path_title.setFillRule(Qt.FillRule.WindingFill)
        path_title.addRoundedRect(
            self.position.x(), self.position.y() + self.banner_height - self.radius, 
            self.width, self.height - self.banner_height + self.radius,
            self.radius, self.radius
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._default_background_brush)
        painter.drawPath(path_title)


    def _paint_border(self, painter):
        path_outline = QtGui.QPainterPath()
        path_outline.addRoundedRect(
            self.position.x(), self.position.y(), self.width, self.height, self.radius, self.radius
        )
        painter.setPen(self._default_border_pen if not self.isSelected() else self._selected_border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path_outline)


    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)    
        print(event)


    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)    
        print(event)

