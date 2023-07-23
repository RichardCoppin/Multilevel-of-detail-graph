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

        self._define_Behaviour_flags()


    def _define_Behaviour_flags(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
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

    
    def middle_MouseButtonPress(self, event: QMouseEvent) -> None:
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


    def middle_MouseButtonRelease(self, event: QMouseEvent) -> None:
        self.setDragMode(QGraphicsView.DragMode.NoDrag)


    def left_MouseButtonPress(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)


    def left_MouseButtonRelease(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)


    def right_MouseButtonPress(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)


    def right_MouseButtonRelease(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)


    def wheelEvent(self, event: QWheelEvent) -> None:
        scale_factor = self.zoom_factor ** math.copysign(1, event.angleDelta().y())
        self.scale(scale_factor, scale_factor)