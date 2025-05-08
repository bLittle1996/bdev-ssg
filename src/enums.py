from enum import Enum
from functools import reduce
from typing import Callable, Sequence


class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMG"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    @staticmethod
    def from_text(text: str) -> "BlockType":
        lines = text.split("\n")
        num_lines = len(lines)
        last_line = num_lines - 1  # index

        if lines[0].startswith("```") and lines[last_line].endswith("```"):
            return BlockType.CODE
        if every(
            lambda l: l.startswith("- ") or l.startswith("* ") or l.startswith("+ "),
            lines,
        ):
            return BlockType.UNORDERED_LIST
        if is_ol(lines):
            return BlockType.ORDERED_LIST
        if every(lambda l: l.startswith("> ") or l == ">", lines):
            return BlockType.QUOTE
        if len(lines) == 1 and lines[0].startswith("#"):
            return BlockType.HEADING

        return BlockType.PARAGRAPH


def every[T](predicate: Callable[[T], bool], data: Sequence[T]) -> bool:
    return reduce(lambda acc, cur: acc and predicate(cur), data, True)


def is_ol(lines: list[str]) -> bool:
    # must start with digit(s) and then a .<space>
    def valid_line(l: str) -> bool:
        # 1.<space>to. do
        for i, c in enumerate(l):
            if c == "." and i + 1 < len(l) and l[i : i + 2] == ". ":
                return True
            if not c.isdigit():
                return False
        return False

    return every(valid_line, lines)
