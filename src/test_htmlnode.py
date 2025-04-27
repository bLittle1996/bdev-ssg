import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_eq(self):
        cases = [
            (HTMLNode(), HTMLNode(), True),
            (HTMLNode("div"), HTMLNode(), False),
            (HTMLNode("div"), HTMLNode("div"), True),
            (HTMLNode("div", "hi"), HTMLNode("div", "hi"), True),
            (HTMLNode("div", "hi"), HTMLNode("div", "bye"), False),
            (HTMLNode("div", "hi", [HTMLNode()]), HTMLNode("div", "bye"), False),
            (
                HTMLNode("div", "hi", [HTMLNode()]),
                HTMLNode("div", "bye", [HTMLNode()]),
                False,
            ),
            (
                HTMLNode("div", "hi", [HTMLNode()], {"yeah": "no"}),
                HTMLNode("div", "hi", [HTMLNode()], {"yeah": "no"}),
                True,
            ),
            (
                HTMLNode("div", "hi", [HTMLNode()], {"yeah": "no"}),
                HTMLNode("div", "bye", [HTMLNode()], {"no": "yeah"}),
                False,
            ),
            (
                HTMLNode("div", "hi", [HTMLNode()], {"yeah": "no"}),
                HTMLNode("div", "hi", [HTMLNode("cry")], {"yeah": "yeah"}),
                False,
            ),
            (
                HTMLNode("div", "hi", [HTMLNode("wow")], {"yeah": "no"}),
                HTMLNode("div", "hi", [HTMLNode("wow")], {"yeah": "yeah"}),
                False,
            ),
        ]

        for a, b, expected in cases:
            self.assertEqual(
                a == b,
                expected,
                f"{a} == {b}",
            )


class LeafNodeTest(unittest.TestCase):
    def test_to_html(self):
        cases = [
            (LeafNode(None, ""), ""),
            (LeafNode(None, "Hello, world!"), "Hello, world!"),
            (LeafNode("p", ""), "<p></p>"),
            (
                LeafNode("p", "<script>alert('lmao')</script>"),
                "<p>&lt;script&gt;alert('lmao')&lt;/script&gt;</p>",
            ),
            (LeafNode("p", "just some normal text"), "<p>just some normal text</p>"),
            (
                LeafNode("p", "just some text", {"data-kind": "normal"}),
                '<p data-kind="normal">just some text</p>',
            ),
            # self-closing tags
            (
                LeafNode(
                    "img", "I'll best you<img></img>", {"href": "1", "alt": "one"}
                ),
                '<img href="1" alt="one">',
            ),
        ]

        for node, expected in cases:
            self.assertEqual(node.to_html(), expected, node)


class ParentNodeTest(unittest.TestCase):
    def test_to_html(self):
        self.maxDiff = None
        cases = [
            (ParentNode("div"), "<div></div>"),
            (ParentNode("p", [LeafNode(None, "some text")]), "<p>some text</p>"),
            (ParentNode("div", props={"id": "main"}), '<div id="main"></div>'),
            (
                ParentNode(
                    "div",
                    [
                        LeafNode("h1", "WHY CATS ARE GREAT"),
                        LeafNode("p", "Here are a list of reasons why:"),
                        ParentNode(
                            "ul",
                            [
                                LeafNode("li", "they are cute"),
                                LeafNode("li", "they are soft"),
                                LeafNode("li", "they are wonderful"),
                                ParentNode(
                                    "li",
                                    [
                                        LeafNode("strong", "because i said so"),
                                    ],
                                ),
                            ],
                            {"id": "irrefutable-proof"},
                        ),
                    ],
                    props={"id": "main", "class": "kitty-cats-are-so-cuuuute"},
                ),
                '<div id="main" class="kitty-cats-are-so-cuuuute"><h1>WHY CATS ARE GREAT</h1><p>Here are a list of reasons why:</p><ul id="irrefutable-proof"><li>they are cute</li><li>they are soft</li><li>they are wonderful</li><li><strong>because i said so</strong></li></ul></div>',
            ),
        ]

        for node, expected in cases:
            self.assertEqual(node.to_html(), expected, node)
