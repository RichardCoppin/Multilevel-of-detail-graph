import math
from PySide6.QtCore import (
    QRect,
    QRectF,
    QLine,
    QPoint
)
from PySide6.QtWidgets import (
    QGraphicsScene
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen
)

from ui.graphics_node import Graphics_Node

GRID_SIZE = 20
LARGE_GRID = 5


class Graphics_Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.grid_size = GRID_SIZE 
        self.large_grid = LARGE_GRID 

        self.define_colors()

        self.define_pens()

        self.scene_width, self.scene_height = 64_000, 64_000
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)
        self.setBackgroundBrush(self._color_background)


    def define_pens(self):
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)


    def define_colors(self):
        self._color_background = QColor('#393939')
        self._color_light = QColor('#292929')
        self._color_dark = QColor('#202020')


    def drawBackground(self, painter: QPainter, rect: QRectF | QRect) -> None:
        super().drawBackground(painter, rect)
        
        light_lines, dark_lines = self.define_grid_lines(rect)

        painter.setPen(self._pen_light)
        painter.drawLines(light_lines)

        painter.setPen(self._pen_dark)
        painter.drawLines(dark_lines)


    def define_grid_lines(self, rect: QRectF | QRect):
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.ceil(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        h_light_lines = list()
        h_dark_lines = list()

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.large_grid) == 0:
                h_dark_lines.append(QLine(left, y, right, y))
            else:
                h_light_lines.append(QLine(left, y, right, y))

        v_light_lines = list()
        v_dark_lines = list()
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.large_grid) == 0:
                v_dark_lines.append(QLine(x, top, x, bottom))
            else:
                v_light_lines.append(QLine(x, top, x, bottom))
        
        light_lines = h_light_lines + v_light_lines
        dark_lines = h_dark_lines + v_dark_lines
        
        return light_lines, dark_lines


    def add_node(self, node: Graphics_Node):
        self.addItem(node)
    