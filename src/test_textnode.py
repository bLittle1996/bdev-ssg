import unittest

from htmlnode import LeafNode
from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_nodes,
)


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

    def test_text_to_nodes(self):
        cases: list[tuple[str, list[TextNode]]] = [
            ("I am nothing special.", [TextNode("I am nothing special.")]),
            (
                "**I am nothing special.**",
                [TextNode("I am nothing special.", TextType.BOLD)],
            ),
            (
                "*I am nothing special.*",
                [TextNode("I am nothing special.", TextType.ITALIC)],
            ),
            (
                "_I am nothing special._",
                [TextNode("I am nothing special.", TextType.ITALIC)],
            ),
            (
                "`I am nothing special.`",
                [TextNode("I am nothing special.", TextType.CODE)],
            ),
            (
                "**I am getting** a *little* `bit more involved` _now_!",
                [
                    TextNode("I am getting", TextType.BOLD),
                    TextNode(" a "),
                    TextNode("little", TextType.ITALIC),
                    TextNode(" "),
                    TextNode("bit more involved", TextType.CODE),
                    TextNode(" "),
                    TextNode("now", TextType.ITALIC),
                    TextNode("!"),
                ],
            ),
            (
                "Hey! [Check this out](rickroll). `:)`",
                [
                    TextNode("Hey! "),
                    TextNode("Check this out", TextType.LINK, "rickroll"),
                    TextNode(". "),
                    TextNode(":)", TextType.CODE),
                ],
            ),
            (
                "Hey! [Check this out](rickroll). `:)` ![Also a cute cat](cute cat for sure)!!! <3",
                [
                    TextNode("Hey! "),
                    TextNode("Check this out", TextType.LINK, "rickroll"),
                    TextNode(". "),
                    TextNode(":)", TextType.CODE),
                    TextNode(" "),
                    TextNode("Also a cute cat", TextType.IMAGE, "cute cat for sure"),
                    TextNode("!!! <3"),
                ],
            ),
            ("![just image](see?)", [TextNode("just image", TextType.IMAGE, "see?")]),
        ]

        for input, expected in cases:
            self.assertListEqual(text_to_nodes(input), expected)

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

    def split_nodes_links_happy_path(self):
        cases: list[tuple[list[TextNode], list[TextNode]]] = [
            (
                [TextNode("I should ![not](split it up)")],
                [TextNode("I should ![not](split it up)")],
            ),
            (
                [TextNode("I should [definitely](split it up)")],
                [
                    TextNode("I should "),
                    TextNode("definitely", TextType.LINK, "split it up"),
                ],
            ),
            (
                [
                    TextNode(
                        "I should [really](split it up) and have extra text to boot!"
                    )
                ],
                [
                    TextNode("I should "),
                    TextNode("really", TextType.LINK, "split it up"),
                    TextNode(" and have extra text to boot!"),
                ],
            ),
            (
                [TextNode("[I](start) have [one](one) or [two](two) links myself")],
                [
                    TextNode("I", TextType.LINK, "start"),
                    TextNode(" have "),
                    TextNode("one", TextType.LINK, "one"),
                    TextNode(" or "),
                    TextNode("two", TextType.LINK, "two"),
                    TextNode(" myself"),
                ],
            ),
            (
                [TextNode("![Mix](image) and [match!](link)")],
                [
                    TextNode("![Mix](image) and "),
                    TextNode("match!", TextType.LINK, "link"),
                ],
            ),
        ]

        for input, expected in cases:
            self.assertListEqual(split_nodes_links(input), expected)

    def split_nodes_images_happy_path(self):
        cases: list[tuple[list[TextNode], list[TextNode]]] = [
            (
                [TextNode("I should [not](split it up)")],
                [TextNode("I should [not](split it up)")],
            ),
            (
                [TextNode("I should ![definitely](split it up)")],
                [
                    TextNode("I should "),
                    TextNode("definitely", TextType.IMAGE, "split it up"),
                ],
            ),
            (
                [
                    TextNode(
                        "I should ![really](split it up) and have extra text to boot!"
                    )
                ],
                [
                    TextNode("I should "),
                    TextNode("really", TextType.IMAGE, "split it up"),
                    TextNode(" and have extra text to boot!"),
                ],
            ),
            (
                [TextNode("![I](start) have ![one](one) or ![two](two) links myself")],
                [
                    TextNode("I", TextType.IMAGE, "start"),
                    TextNode(" have "),
                    TextNode("one", TextType.IMAGE, "one"),
                    TextNode(" or "),
                    TextNode("two", TextType.IMAGE, "two"),
                    TextNode(" myself"),
                ],
            ),
            (
                [TextNode("![Mix](image) and [match!](link)")],
                [
                    TextNode("Mix", TextType.IMAGE, "image"),
                    TextNode(" and [match!](link)"),
                ],
            ),
        ]

        for input, expected in cases:
            self.assertListEqual(split_nodes_images(input), expected)

    def test_extract_markdown_links_happy_path(self):
        happy_sunshine_cases: list[tuple[str, list[tuple[str, str]]]] = [
            ("I don't even have a link", []),
            ("I almost [have](a link", []),
            ("I almost [have] (a link)", []),
            ("I almost [have(a link)", []),
            ("I almost (have)[a link]", []),
            ("I have ![have](an image) and a [link](link)", [("link", "link")]),
            ("I do [have](a link)", [("have", "a link")]),
            (
                "I do [have](a link) and [another one](winky face)",
                [("have", "a link"), ("another one", "winky face")],
            ),
            ("I do ![have an](image ackchually)", []),
        ]

        for input, output in happy_sunshine_cases:
            self.assertListEqual(extract_markdown_links(input), output)

    def test_extract_markdown_links_edge_cases(self):
        edgy_cases: list[tuple[str, list[tuple[str, str]]]] = [
            ("My soul lays [forgotten]() in the shadows", []),
            (
                "I am the [darkness]([within](metal guitar riff))",
                [("darkness", "[within](metal guitar riff")],
            ),
        ]

        for input, output in edgy_cases:
            self.assertListEqual(extract_markdown_links(input), output)

    def test_extract_markdown_images_happy_path(self):
        happy_sunshine_cases: list[tuple[str, list[tuple[str, str]]]] = [
            ("I don't even have an image", []),
            ("I almost ![have](an image", []),
            ("I almost ![have(an image)", []),
            ("I almost ! [have](an image)", []),
            ("I almost ![have] (an image)", []),
            ("I almost !(have)[an image]", []),
            ("I have ![have](an image) and a [link](link)", [("have", "an image")]),
            ("I do ![have](an image)", [("have", "an image")]),
            (
                "I do ![have](an image) and ![another one](winky face)",
                [("have", "an image"), ("another one", "winky face")],
            ),
            ("I do [have a](link ackchually)", []),
        ]

        for input, output in happy_sunshine_cases:
            self.assertListEqual(extract_markdown_images(input), output)

    def test_extract_markdown_images_edge_cases(self):
        edgy_cases: list[tuple[str, list[tuple[str, str]]]] = [
            ("Cloaked in shadows, I remain concealed from mortal eyes", []),
            (
                "The ![darkness](link![haha](gotem)) is my only mistress",
                [("darkness", "link![haha](gotem")],
            ),
            ("! [My bleeding heart bleeds blood for you](link_actually)", []),
        ]

        for input, output in edgy_cases:
            self.assertListEqual(extract_markdown_images(input), output)
