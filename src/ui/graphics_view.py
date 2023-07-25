import math

from PySide6.QtWidgets import (
    QWidget, 
    QGraphicsScene, 
    QGraphicsView
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QMouseEvent,
    QWheelEvent
)
from PySide6.QtCore import (
    Qt,
    QEvent
)

from src.ui.constants import LARGE_GRID

class Graphics_View(QGraphicsView):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent=parent)

        self.zoom_factor = 1.25
        self.zoom_level = 0
        self.zoom_step = 1
        self.scale_factor = 1
        self._scale = (1, 1)

        self._define_Behaviour_flags()


    def _define_Behaviour_flags(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)   #AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
    

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
        print("")

    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragMode() == QGraphicsView.DragMode.ScrollHandDrag:
            dx = float(event.position().x()) - float(self.mouse_begin.x())
            dy = float(event.position().y()) - float(self.mouse_begin.y())
            # print(self.mouse_begin, (dx, dy), event.position(), self.transform())
            self.translate(dx / (self._scale[0]), dy / (self._scale[1]))
            self.mouse_begin = event.position()
        return super().mouseMoveEvent(event)


    def middle_MouseButtonPress(self, event: QMouseEvent) -> None:
        # #FIXME: SPoofing mouse buttons, doesn't sound like a good idea:
        print('View:', event)
        # release_event = QMouseEvent(
        #     QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.MouseButton.MiddleButton,
        #     event.buttons() & ~Qt.MouseButton.MiddleButton, event.modifiers()
        # )
        # super().mouseReleaseEvent(release_event)

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.mouse_begin = event.position()

        # fake_event = QMouseEvent(
        #     event.type(), event.localPos(), event.screenPos(), Qt.MouseButton.LeftButton,
        #     (event.buttons()) & ~Qt.MouseButton.MiddleButton, event.modifiers()
        # )
        # super().mousePressEvent(fake_event)            


    def middle_MouseButtonRelease(self, event: QMouseEvent) -> None:
        # print('View:', event)     
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        release_event = QMouseEvent(
            QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.MouseButton.LeftButton,
            event.buttons() & ~Qt.MouseButton.LeftButton, event.modifiers()
        )
        super().mouseReleaseEvent(release_event)        


    def left_MouseButtonPress(self, event: QMouseEvent) -> None:
        # print('View:', event) 
        super().mousePressEvent(event)


    def left_MouseButtonRelease(self, event: QMouseEvent) -> None:
        # print('View:', event)  
        super().mouseReleaseEvent(event)


    def right_MouseButtonPress(self, event: QMouseEvent) -> None:
        # print('View:', event)     
        super().mousePressEvent(event)


    def right_MouseButtonRelease(self, event: QMouseEvent) -> None:
        # print('View:', event)
        super().mouseReleaseEvent(event)



    def wheelEvent(self, event: QWheelEvent) -> None:
        zoom_step = math.copysign(1, event.angleDelta().y())
        scale_factor = self.zoom_factor ** zoom_step
        self.scale(scale_factor, scale_factor)
        
        self._scale = (self.transform().m11(), self.transform().m22())

        self.zoom_level += zoom_step
        if self.zoom_level % LARGE_GRID == 0:
            self.scene().rescale_grid(2**(-(self.zoom_level/LARGE_GRID)))
                