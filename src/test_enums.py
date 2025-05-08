import unittest

from enums import BlockType


class TestEnums(unittest.TestCase):
    def test_block_type_from_text(self):
        cases: list[tuple[str, BlockType]] = [
            ("# Yeah I'm a heading", BlockType.HEADING),
            ("## Yeah I'm a heading", BlockType.HEADING),
            ("### Yeah I'm a heading", BlockType.HEADING),
            ("#### Yeah I'm a heading", BlockType.HEADING),
            ("##### Yeah I'm a heading", BlockType.HEADING),
            ("###### Yeah I'm a heading", BlockType.HEADING),
            (
                "################## Yeah I'm a heading",
                BlockType.HEADING,
            ),  # who cares how many, we'll just limit it to an h6
            (
                "###### Yeah\nI'm a heading, jkjk",
                BlockType.PARAGRAPH,
            ),  # no multi-line headings, I don't wanna deal with that and neither do you!
            ("- todo", BlockType.UNORDERED_LIST),
            ("* todo", BlockType.UNORDERED_LIST),
            ("+ todo", BlockType.UNORDERED_LIST),
            ("- todo\n- teehee", BlockType.UNORDERED_LIST),
            ("* todo\n* teehee", BlockType.UNORDERED_LIST),
            ("+ todo\n+ teehee", BlockType.UNORDERED_LIST),
            ("+ todo\n- teehee\n* hohoho", BlockType.UNORDERED_LIST),
            ("+ todo\n- teehee\n1. ohnono", BlockType.PARAGRAPH),
            ("1. todo", BlockType.ORDERED_LIST),
            ("2. todo", BlockType.ORDERED_LIST),
            ("2000000. todo", BlockType.ORDERED_LIST),
            ("1. todo\n2. yargggg", BlockType.ORDERED_LIST),
            ("1. todo\n1. yargggg", BlockType.ORDERED_LIST),
            ("1. todo\n2.yargggg", BlockType.PARAGRAPH),
            ("1. todo\nyargggg", BlockType.PARAGRAPH),
            ("> Grapes are good - Albert Einstein", BlockType.QUOTE),
            (
                "> Grapes are good - Albert Einstein\n> We're all alberto",
                BlockType.QUOTE,
            ),
            (
                "> Grapes are good - Albert Einstein\n>\n> multi line drifting",
                BlockType.QUOTE,
            ),
            ("```python sucks lmao```", BlockType.CODE),
            ("```python sucks lmao\nand here's\nWHY!!!!```", BlockType.CODE),
            ("```python sucks lmao\nand here's```\nWHY????", BlockType.PARAGRAPH),
            ("```python sucks lmao", BlockType.PARAGRAPH),
            ("It's just text", BlockType.PARAGRAPH),
            ("It's just text\nno really", BlockType.PARAGRAPH),
            ("It's just text\nno really\n# I mean it!!!", BlockType.PARAGRAPH),
        ]

        for input, expected in cases:
            self.assertEqual(BlockType.from_text(input), expected, f"\nGiven: {input}")
