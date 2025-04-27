import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        cases = [
                (TextNode("hello world"), TextNode("hello world"), True ),
                (TextNode("hello world"), TextNode("HELLO WORLD"), False ),
                (TextNode("hello world", TextType.BOLD), TextNode("hello world"), False ),
                (TextNode("hello world", TextType.LINK, "stub"), TextNode("hello world", TextType.LINK, "stub"), True ),
                (TextNode("hello world", TextType.LINK, "stub"), TextNode("hello world", TextType.LINK, "awef"), False ),
                (TextNode("hello world", TextType.IMAGE, "stub"), TextNode("hello world", TextType.LINK, "stub"), False ),
        ]

        for a, b, expected in cases:
            if expected == True:
                self.assertEqual(a, b)
            else:
                self.assertNotEqual(a, b)
            

if __name__ == "__main__":
    unittest.main()
