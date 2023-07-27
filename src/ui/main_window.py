from PySide6.QtWidgets import (
    QWidget, 
    QMainWindow, 
    QVBoxLayout, 
    QStatusBar, 
    QLabel,
    QHBoxLayout,
    QGraphicsView
)

from PySide6.QtCore import (
    Qt, 
    QRect,
    QPoint
)
from PySide6.QtGui import QColor


from ui.graphics_scene import Graphics_Scene
from ui.graphics_node import Graphics_Node
from ui.graphics_view import Graphics_View

WINDOW_HEIGHT = 768
WINDOW_WIDTH = 1024


class Main_Window(QMainWindow):
    def __init__(self, application: QWidget, parent: QWidget | None = None, flags: Qt.WindowFlags | Qt.WindowType = Qt.WindowFlags()) -> None:
        super().__init__(parent, flags)

        self.screen_dimensions = application.screens()[0].availableGeometry()
                
        self._init_ui()

        self.show()


    def _init_ui(self):
        self.setObjectName("Window")
        self.setWindowTitle("Multi-Level-Of-Detail")
        
        self.define_window_geometry()
        
        self.centralWidget: QWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.define_layouts()
        self.define_status_bar()
        self.define_graphics_scene()

        self._add_debug_items()
    

    def define_window_geometry(self):
        self.window_height = WINDOW_HEIGHT
        self.window_width = WINDOW_WIDTH
        screen_width = self.screen_dimensions.width()
        screen_height = self.screen_dimensions.height()
        self.setGeometry(
            (screen_width - self.window_width) // 2, 
            (screen_height - self.window_height) // 2, 
            self.window_width, 
            self.window_height
        )


    def define_layouts(self):
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)
        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        self.bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)


    def define_status_bar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.status_text = QLabel()
        self.status_text.setGeometry(100, 80, 500, 20)
        self.status_text.setText("This is the status bar")

        self.statusbar.insertPermanentWidget(1, self.status_text)


    def set_status_bar_text(self, text:str):
        self.status_text.setText(text)


    def define_graphics_scene(self):
        self.view = Graphics_View(self)
        self.top_layout.addWidget(self.view)

        self.graphics_scene = Graphics_Scene(self.view)
        self.view.setScene(self.graphics_scene)

        
    def _add_debug_items(self):
        graphics_scene = self.graphics_scene

        graphics_scene.addRect(QRect(-100, -100, 200, 200), QColor("Green"))
        new_node = Graphics_Node(
            title="New Node Title", 
            parent=None, 
            position=QPoint(0, 0)
        )
        graphics_scene.add_node(new_node)


    def paint(self):
        return super().paint()