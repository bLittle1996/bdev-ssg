import unittest

from htmlnode import HTMLNode


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
