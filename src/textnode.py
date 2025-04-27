from enum import Enum


class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMG"


class TextNode:
    def __init__(
        self, text: str, type: TextType = TextType.TEXT, url: str | None = None
    ) -> None:
        self.text = text
        self.type = type
        self.url = url

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, type(self)):
            return False

        return (
            self.type == value.type
            and self.text == value.text
            and self.url == value.url
        )

    def __repr__(self) -> str:
        if self.type in (TextType.IMAGE, TextType.LINK):
            return f'TextNode({self.type.value}, "{self.text}", "{self.url}")'
        return f'TextNode({self.type.value}, "{self.text}")'
