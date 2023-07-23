from __future__ import annotations

from src.model.node import Node

def add_node_to_scene(scene: Scene, node_name: str, node_id: str = None):
    new_node = Node(scene, node_name, node_id)
    scene.add_node(new_node=new_node)


class Scene():
    def __init__(self) -> None:
        
        self.nodes = dict()
        self.edges = list()
        self.groups = list()


    def add_node(self, new_node: Node):
        self.nodes[new_node.id] = new_node

    
    def __contains__(self, key):
        return key in self.nodes

