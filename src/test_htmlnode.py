import unittest

from htmlnode import HTMLNode, LeafNode


class HTMLNodeTest(unittest.TestCase):
    def test_props_to_html(self):
        cases = [
            (HTMLNode(), ""),
            (HTMLNode(props={"hello": "world"}), 'hello="world"'),
            (
                HTMLNode(props={"data-whatever": '"yeah man"'}),
                'data-whatever="&quot;yeah man&quot;"',
            ),
            (HTMLNode(props={"one": "two", "three": "four"}), 'one="two" three="four"'),
        ]

        for node, expected in cases:
            self.assertEqual(node.props_to_html(), expected, node)


class LeafNodeTest(unittest.TestCase):
    def test_to_html(self):
        cases = [
            (LeafNode(None, ""), ""),
            (LeafNode(None, "Hello, world!"), "Hello, world!"),
            (LeafNode("p", ""), "<p></p>"),
            (LeafNode("p", "<div>lmao</div>"), "<p>&lt;div&gt;lmao&lt;/div&gt;</p>"),
            (LeafNode("p", "just some normal text"), "<p>just some normal text</p>"),
            (
                LeafNode("p", "just some text", {"data-kind": "normal"}),
                '<p data-kind="normal">just some text</p>',
            ),
        ]

        for node, expected in cases:
            self.assertEqual(node.to_html(), expected, node)
