import unittest
from nodes.text_node import TextNode, TextType
from funcs import text_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        cases = [
            [("This is a text node", TextType.BOLD, "https://www.boot.dev"),
             ("This is a text node", TextType.BOLD, "https://www.boot.dev"), True],
            [("This is a text node", TextType.LINK, "https://www.boot.dev"),
             ("This is a text node", TextType.BOLD, "https://www.boot.dev"), False],
        ]
        for case in cases:
            node = TextNode(case[0][0], case[0][1], case[0][2])
            node2 = TextNode(case[1][0], case[1][1], case[1][2])
            equal = case[2]
            if equal:
                self.assertEqual(node, node2)
            else:
                self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("One", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("Two", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()
