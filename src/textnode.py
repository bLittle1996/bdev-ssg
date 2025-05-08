from enums import TextType
from htmlnode import LeafNode


class TextNode:
    def __init__(
        self, text: str, type: TextType = TextType.TEXT, url: str | None = None
    ) -> None:
        self.text = text
        self.type = type
        self.url = url
        self.__ensure_valid()  # raises if not valid

    def to_html_node(self) -> LeafNode:
        tag = None
        text = self.text
        props: dict[str, str] = {}

        if self.type == TextType.TEXT:
            tag = None
        if self.type == TextType.BOLD:
            tag = "strong"
        if self.type == TextType.ITALIC:
            tag = "em"
        if self.type == TextType.CODE:
            tag = "code"
        if self.type == TextType.LINK and self.url:  # and is for pyright only
            tag = "a"
            props = {"href": self.url}
        if self.type == TextType.IMAGE and self.url:
            tag = "img"
            props = {"href": self.url, "alt": self.text}
            text = ""  # imgs cant have text children, so use an empty string

        return LeafNode(tag, text, props)

    def __ensure_valid(self) -> None:
        if self.type in (TextType.LINK, TextType.IMAGE) and self.url == None:
            raise ValueError("must provide url for image and link types")

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
