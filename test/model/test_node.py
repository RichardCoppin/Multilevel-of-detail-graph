import unittest

from model import node
from model import scene

class Set_0_Basics(unittest.TestCase):

    def setUp(self):
        self.scene = scene.Scene()


    def test_add_node(self):
        test_node = node.Node(self.scene)

if __name__ == '__main__':
    unittest.main(exit=False)
