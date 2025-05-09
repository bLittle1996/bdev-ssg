from unittest import TestCase

from blocknode import BlockNode, text_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode


def debug_children(node: HTMLNode, depth=1):
    indent = " " * (depth * 2)
    for c in node.children:
        print(f"{indent}{c}")
        debug_children(c, depth + 1)


class TextBlockNode(TestCase):
    def test_text_to_html_nodes(self):
        cases: list[tuple[str, ParentNode]] = [
            ("# heading", ParentNode("h1", [LeafNode(None, "heading")])),
            (
                "# **head**_ing_",
                ParentNode("h1", [LeafNode("strong", "head"), LeafNode("em", "ing")]),
            ),
            ("## heading", ParentNode("h2", [LeafNode(None, "heading")])),
            ("### heading", ParentNode("h3", [LeafNode(None, "heading")])),
            ("#### heading", ParentNode("h4", [LeafNode(None, "heading")])),
            ("##### heading", ParentNode("h5", [LeafNode(None, "heading")])),
            ("###### heading", ParentNode("h6", [LeafNode(None, "heading")])),
            ("########### heading", ParentNode("h6", [LeafNode(None, "heading")])),
            (
                "> single line",
                ParentNode("blockquote", [LeafNode(None, "single line")]),
            ),
            (
                "> two lines\n> how craaazy",
                ParentNode("blockquote", [LeafNode(None, "two lines\nhow craaazy")]),
            ),
            (
                "> two lines\n>\n> how craaazy",
                ParentNode("blockquote", [LeafNode(None, "two lines\n\nhow craaazy")]),
            ),
            ("- hi", ParentNode("ul", [ParentNode("li", [LeafNode(None, "hi")])])),
            (
                "- hi\n- ho",
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "hi")]),
                        ParentNode("li", [LeafNode(None, "ho")]),
                    ],
                ),
            ),
            ("1. hi", ParentNode("ol", [ParentNode("li", [LeafNode(None, "hi")])])),
            (
                "1. hi\n55. ho",
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode(None, "hi")]),
                        ParentNode("li", [LeafNode(None, "ho")]),
                    ],
                ),
            ),
            (
                "```trash _code_ (it's mine :) )```",
                ParentNode(
                    "pre",
                    [
                        ParentNode(
                            "code", [LeafNode(None, "trash _code_ (it's mine :) )")]
                        )
                    ],
                ),
            ),
        ]

        for input, expected in cases:
            self.assertEqual(BlockNode(input).to_html_node(), expected, f"")

    def test_text_to_blocks(self):
        # i'm getting lazy so I'm just gonna use the example of boot.dev
        input = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        expected = [
            BlockNode("# This is a heading"),
            BlockNode(
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
            ),
            BlockNode(
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ),
        ]
        self.assertListEqual(text_to_blocks(input), expected)
