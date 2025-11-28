import unittest
import io
from contextlib import redirect_stdout
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        cases = [
            [("div", "div tag", "", {"style": "color:red"}),
             ("div", "div tag", "", {"style": "color:red"}), True],
            [("a", "a tag", "", {"target": "_blank", "href": "https://www.google.com"}),
             ("div", "div tag", "", {"style": "color:red"}), False],
        ]
        for case in cases:
            node = HTMLNode(case[0][0], case[0][1], case[0][2], case[0][3])
            node2 = HTMLNode(case[1][0], case[1][1], case[1][2], case[1][3])
            equal = case[2]
            if equal:
                self.assertEqual(node.props_to_html(), node2.props_to_html())
            else:
                self.assertNotEqual(node.props_to_html(),
                                    node2.props_to_html())

    def test_print(self):
        cases = [
            [("div", "div tag", "", {"style": "color:red"}),
                ("div", "div tag", "", {"style": "color:red"}), True],
            [("a", "a tag", "", {"target": "_blank", "href": "https://www.google.com"}),
                ("div", "div tag", "", {"style": "color:red"}), True],
        ]
        for case in cases:
            with io.StringIO() as buffer, redirect_stdout(buffer):
                node = HTMLNode(case[0][0], case[0][1], case[0][2], case[0][3])
                node2 = HTMLNode(case[1][0], case[1][1],
                                 case[1][2], case[1][3])
                equal = case[2]
                print(node)
                output = buffer.getvalue()
                if equal:
                    self.assertTrue(output == f"{case[0][0]} | {case[0][1]}\n")
                else:
                    print(node2)
                    lines = output.split("\n")
                    self.assertFalse(lines[0] == lines[1])


if __name__ == "__main__":
    unittest.main()
