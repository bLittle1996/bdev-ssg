import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            TextNode("funny pic", TextType.LINK)
        with self.assertRaises(ValueError):
            TextNode("funny pic", TextType.IMAGE)
        good_node = TextNode("hi")
        self.assertEqual(good_node.text, "hi")
        self.assertEqual(good_node.type, TextType.TEXT)
        self.assertEqual(good_node.url, None)

    def test_to_html_node(self):
        cases = [
            (TextNode("hello world"), LeafNode(None, "hello world")),
            (TextNode("hello world", TextType.TEXT), LeafNode(None, "hello world")),
            (TextNode("hello world", TextType.BOLD), LeafNode("strong", "hello world")),
            (TextNode("hello world", TextType.ITALIC), LeafNode("em", "hello world")),
            (TextNode("hello world", TextType.CODE), LeafNode("code", "hello world")),
            (
                TextNode("look at this", TextType.LINK, "deez"),
                LeafNode("a", "look at this", {"href": "deez"}),
            ),
            (
                TextNode("look at this", TextType.IMAGE, "deez"),
                LeafNode("img", "", {"href": "deez", "alt": "look at this"}),
            ),
        ]

        for text_node, html_node in cases:
            self.assertEqual(text_node.to_html_node(), html_node)

    def test_eq(self):
        cases = [
            (TextNode("hello world"), TextNode("hello world"), True),
            (TextNode("hello world"), TextNode("HELLO WORLD"), False),
            (TextNode("hello world", TextType.BOLD), TextNode("hello world"), False),
            (
                TextNode("hello world", TextType.LINK, "stub"),
                TextNode("hello world", TextType.LINK, "stub"),
                True,
            ),
            (
                TextNode("hello world", TextType.LINK, "stub"),
                TextNode("hello world", TextType.LINK, "awef"),
                False,
            ),
            (
                TextNode("hello world", TextType.IMAGE, "stub"),
                TextNode("hello world", TextType.LINK, "stub"),
                False,
            ),
        ]

        for a, b, expected in cases:
            if expected == True:
                self.assertEqual(a, b)
            else:
                self.assertNotEqual(a, b)


if __name__ == "__main__":
    unittest.main()
