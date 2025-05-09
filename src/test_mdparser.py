from unittest import TestCase

from mdparser import extract_title, markdown_to_html, markdown_to_html_node


class TestMarkdownParser(TestCase):
    def test_extract_title(self):
        md = """
# hi
"""
        html = markdown_to_html_node(md)
        self.assertEqual(extract_title(html), "hi")

    def test_extract_title_raises(self):
        md = """
## hi
"""
        html = markdown_to_html_node(md)
        with self.assertRaises(Exception):
            extract_title(html)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        html = markdown_to_html(md)
        self.assertEqual(
            html,
            "<div><p>This is <strong>bolded</strong> paragraph text in a p tag here</p><p>This is another paragraph with <em>italic</em> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        html = markdown_to_html(md)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
