import unittest

from nodes.leaf_node import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        cases = [
            [("p", "This is a paragraph of text"), True, '<p>This is a paragraph of text</p>',
             ("a", "Click me!", {"href": "https://www.boot.dev", "target": "_blank"}), True, '<a href="https://www.google.com">Click me!</a>'],
        ]
        for case in cases:
            node = LeafNode(case[0][0], case[0][1])
            equal = case[1]
            should_be = case[2]
            if equal:
                self.assertEqual(
                    node.to_html(), should_be)


if __name__ == "__main__":
    unittest.main()
