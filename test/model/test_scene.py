import unittest

from src.model import scene

class Set_0_Scene_Basics(unittest.TestCase):

    def setUp(test) -> None:
        test.scene = scene.Scene()


    def test_create_scene(test):
        test_scene = scene.Scene()
        test.assertIsNotNone(test_scene)


    def test_add_node(test):
        test.assertNotIn("Node Name", test.scene)
        scene.add_node_to_scene(test.scene, "Node Name")
        test.assertIn("Node Name", test.scene)


if __name__ == '__main__':
    unittest.main(exit=False)
