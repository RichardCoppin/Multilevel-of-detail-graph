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

class Graphics_View(QGraphicsView):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent=parent)

        self.zoom_factor = 1.25
        self.zoom = 10
        self.zoom_step = 1

        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
    

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        else:
            super().mousePressEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    
    def middleMouseButtonPress(self, event: QMouseEvent) -> None:
        #FIXME: SPoofing mouse buttons, doesn't sound like a good idea:
        release_event = QMouseEvent(
            QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.MouseButton.MiddleButton,
            event.buttons() & ~Qt.MouseButton.MiddleButton, event.modifiers()
        )
        super().mouseReleaseEvent(release_event)

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        fake_event = QMouseEvent(
            event.type(), event.localPos(), event.screenPos(), Qt.MouseButton.LeftButton,
            event.buttons() | Qt.MouseButton.LeftButton, event.modifiers()
        )
        super().mousePressEvent(fake_event)            


    def middleMouseButtonRelease(self, event: QMouseEvent) -> None:
        self.setDragMode(QGraphicsView.DragMode.NoDrag)


    def wheelEvent(self, event: QWheelEvent) -> None:
        scale_factor = self.zoom_factor ** math.copysign(1, event.angleDelta().y())
        self.scale(scale_factor, scale_factor)