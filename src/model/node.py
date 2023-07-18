from model.abstract_types import Scene_Type
from ui.graphics_node import Graphics_Node


class Node():
    def __init__(self, scene: Scene_Type, title: str = "") -> None:
        self.scene = scene
        self.title = title
        
        self.inputs = list()
        self.outputs = list()

