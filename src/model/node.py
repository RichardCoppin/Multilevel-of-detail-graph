from src.model.abstract_types import Scene_Type
from src.ui.graphics_node import Graphics_Node


class Node():
    def __init__(self, scene: Scene_Type, id: str, title: str = "") -> None:
        self.scene = scene
        self.id = id 
        self.title = title
        
        self.inputs = list()
        self.outputs = list()
