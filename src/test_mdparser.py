import unittest

from textnode import TextNode, TextType
from mdparser import split_nodes_delimiter


class MDParserTest(unittest.TestCase):
    def test_split_nodes_delimiter_no_delimiter(self):
        text_node = TextNode("I am so bold")
        output = split_nodes_delimiter([text_node], "lol", TextType.CODE)
        expected = [TextNode("I am so bold")]
        self.assertListEqual(output, expected)

    def test_split_nodes_delimiter_no_pair(self):
        cases = [
            (TextNode("**I am so bold"), "**"),
            (TextNode("I am **so bold"), "**"),
            (TextNode("I am so bold**"), "**"),
            (TextNode("*I am so bold**"), "**"),
        ]

        for node, delimiter in cases:
            # should result in the same exact list
            self.assertListEqual(
                split_nodes_delimiter([node], delimiter, TextType.BOLD),
                [node],
            )

    def test_split_nodes_delimiter_full_replace(self):
        text_node = TextNode("_Emphasize me_")
        expected = TextNode("Emphasize me", TextType.ITALIC)
        self.assertListEqual(
            split_nodes_delimiter([text_node], "_", TextType.ITALIC), [expected]
        )

    def test_split_nodes_delimiter_delim_at_start(self):
        input = [TextNode("**Yabba** dabba doo", TextType.TEXT)]
        expected = [
            TextNode("Yabba", TextType.BOLD),
            TextNode(" dabba doo", TextType.TEXT),
        ]
        self.assertListEqual(
            split_nodes_delimiter(input, "**", TextType.BOLD), expected, input
        )

    def test_split_nodes_delimiter_delim_at_middle(self):
        input = [TextNode("Yabba **dabba** doo", TextType.TEXT)]
        expected = [
            TextNode("Yabba ", TextType.TEXT),
            TextNode("dabba", TextType.BOLD),
            TextNode(" doo", TextType.TEXT),
        ]
        self.assertListEqual(
            split_nodes_delimiter(input, "**", TextType.BOLD), expected, input
        )

    def test_split_nodes_delimiter_delim_at_end(self):
        input = [TextNode("Yabba dabba **doo**", TextType.TEXT)]
        expected = [
            TextNode("Yabba dabba ", TextType.TEXT),
            TextNode("doo", TextType.BOLD),
        ]
        self.assertListEqual(
            split_nodes_delimiter(input, "**", TextType.BOLD), expected, input
        )

    def test_split_nodes_delimiter_delim_at_all_sorts_of_places(self):
        input = [TextNode("**Yabba** **dabba** **doo**", TextType.TEXT)]
        expected = [
            TextNode("Yabba", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("dabba", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("doo", TextType.BOLD),
        ]
        self.assertListEqual(
            split_nodes_delimiter(input, "**", TextType.BOLD), expected, input
        )

    def test_split_nodes_delimiter_so_many_wrapping_delims(self):
        input = [TextNode("********aaaa*******************")]
        output = [TextNode("*" * 7), TextNode("aaaa"), TextNode("*" * 18)]
        self.assertListEqual(split_nodes_delimiter(input, "*", TextType.TEXT), output)

    def test_split_nodes_delimiter_oops_all_delims(self):
        input = [TextNode("_" * 10000)]
        output = [TextNode("_" * 10000)]
        self.assertListEqual(split_nodes_delimiter(input, "_", TextType.TEXT), output)

    def test_split_nodes_delimiter_chaining(self):
        input = [
            TextNode("_I am the root of **all** evil_. _I_. **AM**. _**PYTHON**_.")
        ]
        output = [
            # multi-delims are not supported
            TextNode("I am the root of **all** evil", TextType.ITALIC),
            TextNode(". ", TextType.TEXT),
            TextNode("I", TextType.ITALIC),
            TextNode(". ", TextType.TEXT),
            TextNode("AM", TextType.BOLD),
            TextNode(". ", TextType.TEXT),
            TextNode("**PYTHON**", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(
            split_nodes_delimiter(
                split_nodes_delimiter(input, "_", TextType.ITALIC), "**", TextType.BOLD
            ),
            output,
        )
