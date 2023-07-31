from __future__ import annotations

import math
from PySide6.QtCore import (
    Qt,
    QRect,
    QRectF,
    QLine
)
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsSceneMouseEvent    
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QMouseEvent,
    QKeyEvent
)

from src.ui.graphics_node import Graphics_Node
from src.ui.constants import (
    GRID_SIZE,
    KEY_MAPPING, 
    LARGE_GRID
)


class Graphics_Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


        self.grid_size = GRID_SIZE 
        self.large_grid = LARGE_GRID 
        self.super_large_grid = LARGE_GRID * LARGE_GRID

        self.define_colors()

        self.define_pens()

        self.scene_width, self.scene_height = 64_000, 64_000
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)
        self.setBackgroundBrush(self._color_background)

        self.functions = {
            'delete_selected': self.delete_selected,'default': super().keyPressEvent
        }


    def rescale_grid(self, scale):
        self.grid_size = GRID_SIZE * scale
        self._dark_thick_line_width = 2 * scale
        self._dark_line_width = 1 * scale
        self._light_line_width = 1 * scale         
        self._pen_light.setWidthF(self._light_line_width)
        self._pen_dark.setWidthF(self._dark_line_width)
        self._pen_thick_dark.setWidthF(self._dark_thick_line_width)


    def define_pens(self):
        self._dark_thick_line_width = 3
        self._dark_line_width = 2
        self._light_line_width = 1
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidthF(self._light_line_width)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidthF(self._dark_line_width)
        self._pen_thick_dark= QPen(self._color_dark)
        self._pen_thick_dark.setWidthF(self._dark_thick_line_width)


    def define_colors(self):
        self._color_background = QColor('#393939')
        self._color_light = QColor('#292929')
        self._color_dark = QColor('#202020')


    def drawBackground(self, painter: QPainter, rect: QRectF | QRect) -> None:
        super().drawBackground(painter, rect)
        
        light_lines, dark_lines, very_dark_lines = self.define_grid_lines(rect)

        painter.setPen(self._pen_light)
        painter.drawLines(light_lines)

        painter.setPen(self._pen_dark)
        painter.drawLines(dark_lines)

        painter.setPen(self._pen_thick_dark)
        painter.drawLines(very_dark_lines)        

        self.addEllipse(QRect(-10, -10, 20, 20), QColor("Yellow"))


    def define_grid_lines(self, rect: QRectF | QRect):
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.ceil(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        grid_size = int(self.grid_size)
        
        first_left = left - (left % grid_size)
        first_top = top - (top % grid_size)

        h_light_lines, h_dark_lines, h_very_dark_lines = (
            self._generate_vertical_lines(left, right, bottom, grid_size, first_top)
        )
        v_light_lines, v_dark_lines, v_very_dark_lines = (
            self._generate_horizontal_lines(right, top, bottom, grid_size, first_left)
        )
        
        light_lines = h_light_lines + v_light_lines
        dark_lines = h_dark_lines + v_dark_lines
        very_dark_lines = h_very_dark_lines + v_very_dark_lines
        
        return light_lines, dark_lines, very_dark_lines


    def _generate_vertical_lines(self, left, right, bottom, grid_size, first_top):
        h_light_lines = list()
        h_dark_lines = list()
        h_very_dark_lines = list()

        for y in range(first_top, bottom, grid_size):
            if y % (grid_size * self.large_grid) == 0:
                if y % (grid_size * self.super_large_grid) == 0:
                    h_very_dark_lines.append(QLine(left, y, right, y))
                else:                
                    h_dark_lines.append(QLine(left, y, right, y))
            else:
                h_light_lines.append(QLine(left, y, right, y))
        return h_light_lines,h_dark_lines,h_very_dark_lines


    def _generate_horizontal_lines(self, right, top, bottom, grid_size, first_left):
        v_light_lines = list()
        v_dark_lines = list()
        v_very_dark_lines = list()
        for x in range(first_left, right, grid_size):
            if x % (grid_size * self.large_grid) == 0:
                if x % (grid_size * self.super_large_grid) == 0:
                    v_very_dark_lines.append(QLine(x, top, x, bottom))
                else:
                    v_dark_lines.append(QLine(x, top, x, bottom))
            else:
                v_light_lines.append(QLine(x, top, x, bottom))
        return v_light_lines,v_dark_lines,v_very_dark_lines


    def add_node(self, node: Graphics_Node):
        self.addItem(node)
    

    def delete_selected(self, event: QKeyEvent):
        for item in self.selectedItems():
            item.remove()
        super().keyPressEvent(event)
    


    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.parent()._parent.set_status_bar_text(
            f"({int(event.scenePos().x())}, "
            f"{int(event.scenePos().y())}) "
        )        
        return super().mouseMoveEvent(event)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        match event.button():
            case Qt.MouseButton.MiddleButton:
                self.middle_MouseButtonPress(event)
            case Qt.MouseButton.LeftButton:
                self.left_MouseButtonPress(event)
            case Qt.MouseButton.RightButton:
                self.right_MouseButtonPress(event)
            case _:
                super().mousePressEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        match event.button():
            case Qt.MouseButton.MiddleButton:
                self.middle_MouseButtonRelease(event)
            case Qt.MouseButton.LeftButton:
                self.left_MouseButtonRelease(event)
            case Qt.MouseButton.RightButton:
                self.right_MouseButtonRelease(event)
            case _:
                super().mouseReleaseEvent(event)

    
    def middle_MouseButtonPress(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)            


    def middle_MouseButtonRelease(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)        


    def left_MouseButtonPress(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)


    def left_MouseButtonRelease(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)


    def right_MouseButtonPress(self, event: QMouseEvent) -> None:
        new_node = Graphics_Node(
            title="New Node Title", 
            parent=None, 
            position=event.scenePos()
        )
        self.add_node(new_node)

        super().mousePressEvent(event)


    def right_MouseButtonRelease(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)

    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        _function_name = KEY_MAPPING.get(event.key(), 'default')
        _function = self.functions.get(_function_name, super().keyPressEvent)
        _function(event)

