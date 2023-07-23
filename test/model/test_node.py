import unittest

from src.model import node
from src.model import scene

class Set_0_Node_Basics(unittest.TestCase):
    def test_create_node(test):
        test.scene = scene.Scene
        test.node = node.Node(scene, id='New Node')
        test.assertIsNotNone(node)


if __name__ == '__main__':
    unittest.main(exit=False)