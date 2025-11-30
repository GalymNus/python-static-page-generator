import unittest
from nodes.parent_node import ParentNode
from nodes.leaf_node import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        cases = [
            ("p", [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ], True, "")
        ]
        for case in cases:
            node = ParentNode(case[0], case[1])
            equal = case[2]
            if equal:
                self.assertEqual(node.to_html(
                ), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

        def test_to_html_with_children(self):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(parent_node.to_html(),
                             "<div><span>child</span></div>")

        def test_to_html_with_grandchildren(self):
            grandchild_node = LeafNode("b", "grandchild")
            child_node = ParentNode("span", [grandchild_node])
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(
                parent_node.to_html(),
                "<div><span><b>grandchild</b></span></div>",
            )


if __name__ == "__main__":
    unittest.main()
