import math

from PySide6.QtWidgets import (
    QWidget, 
    QGraphicsView
)

from PySide6.QtGui import (
    QPainter,
    QMouseEvent,
    QWheelEvent
)
from PySide6.QtCore import (
    Qt,
    QEvent
)

from src.ui.constants import LARGE_GRID
from src.ui.graphics_node import Graphics_Node

class Graphics_View(QGraphicsView):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent=parent)

        self._parent = parent

        self.zoom_factor = 1.25
        self.zoom_level = 0
        self.zoom_step = 1
        self.scale_factor = 1
        self._scale = (1, 1)

        self._define_Behaviour_flags()

        self._parent.set_status_bar_text(f"{self.pos()}")

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

    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragMode() == QGraphicsView.DragMode.ScrollHandDrag:
            dx = float(event.position().x()) - float(self._mouse_anchor.x())
            dy = float(event.position().y()) - float(self._mouse_anchor.y())
            # Scale the translation by the scale to ensure that the view moves appropriately.
            self.translate(dx / (self._scale[0]), dy / (self._scale[1]))
            self._mouse_anchor = event.position()
        return super().mouseMoveEvent(event)


    def middle_MouseButtonPress(self, event: QMouseEvent) -> None:
        # Set ViewportANchor otherwise View has weird translation behaviour.
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)   
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self._mouse_anchor = event.position()


    def middle_MouseButtonRelease(self, event: QMouseEvent) -> None:
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        release_event = QMouseEvent(
            QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.MouseButton.LeftButton,
            event.buttons() & ~Qt.MouseButton.LeftButton, event.modifiers()
        )
        super().mouseReleaseEvent(release_event)
        # Need to set ViewportAnchor to 'AnchorUnderMouse' to ensure zooming works as expected.
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)


    def left_MouseButtonPress(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)


    def left_MouseButtonRelease(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)


    def right_MouseButtonPress(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)


    def right_MouseButtonRelease(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)


    def wheelEvent(self, event: QWheelEvent) -> None:
        zoom_step = math.copysign(1, event.angleDelta().y())
        scale_factor = self.zoom_factor ** zoom_step
        self.scale(scale_factor, scale_factor)
        self._scale = (self.transform().m11(), self.transform().m22())
        self._set_grid_scale(zoom_step)


    def _set_grid_scale(self, zoom_step):
        self.zoom_level += zoom_step
        if self.zoom_level % LARGE_GRID == 0:
            self.scene().rescale_grid(2**(-(self.zoom_level/LARGE_GRID)))
                