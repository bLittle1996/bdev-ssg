from typing import Callable
from enums import TextType
from funcs import pipe
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


##### utility functions #####


def text_to_nodes(text: str) -> list[TextNode]:
    return pipe(
        [TextNode(text)],
        split_nodes_images,
        split_nodes_links,
        split_delim("**", TextType.BOLD),
        split_delim("*", TextType.ITALIC),
        split_delim("_", TextType.ITALIC),
        split_delim("`", TextType.CODE),
    )


def split_delim(
    delimiter: str, node_type: TextType
) -> Callable[[list[TextNode]], list[TextNode]]:
    return lambda nodes: split_nodes_delimiter(nodes, delimiter, node_type)


# takes nodes, inspects their text, and if there is text surrounded by the delimiter turns it into a new set of nodes.
# chain 'em together to handle all the things
# i.e
# split_nodes_delimiter([TextNode(None, "I am **bold** and **cool**")], "**", TextType.BOLD)
# returns [TextNode(TextType.TEXT, "I am "), TextNode(TextType.BOLD, "bold"), TextNode(TextType.TEXT, " and "), TextNode(TextType.BOLD, "cool")]
def split_nodes_delimiter(
    nodes: list[TextNode], delimiter: str, node_type: TextType
) -> list[TextNode]:
    if len(delimiter) == 0:
        return nodes
    new_nodes: list[TextNode] = []
    for n in nodes:
        start_from = 0  # where in node text where begin to substr from
        i = 0
        if len(n.text) < len(delimiter) or n.type is not TextType.TEXT:
            new_nodes.append(n)
            continue
        while i <= len(n.text) - len(delimiter):
            # not enough occurrences or reached the end? let's skidaddle
            if n.text[start_from:].count(delimiter) <= 1 or i >= len(n.text) - len(
                delimiter
            ):
                new_nodes.append(TextNode(n.text[start_from:], n.type))
                break
            if (
                n.text[i : i + len(delimiter)] == delimiter
                # do not process adjacent delimiters
                and n.text[i : i + len(delimiter) * 2] != delimiter * 2
            ):
                split_start = i + len(delimiter)  # char right after delimeter
                split_end = (
                    n.text[split_start:].find(delimiter) + i + len(delimiter)
                )  # chars up delimeter
                # If possible, add any text before the delimiter (excluding it)
                if (split_start - len(delimiter)) - start_from > 0:
                    new_nodes.append(
                        TextNode(
                            n.text[start_from : split_start - len(delimiter)], n.type
                        )
                    )
                new_nodes.append(TextNode(n.text[split_start:split_end], node_type))
                # skip to the last delimiter
                start_from = split_end + len(delimiter)
                i = start_from
            else:
                i += 1
    return new_nodes


def split_nodes_links(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for n in nodes:
        if n.type is not TextType.TEXT:
            new_nodes.append(n)
            continue

        links = extract_markdown_links(n.text)
        remaining_text = n.text
        for label, link in links:
            markdown = f"[{label}]({link})"
            before, md, after = remaining_text.partition(markdown)
            new_nodes.append(TextNode(before))
            new_nodes.append(TextNode(label, TextType.LINK, link))
            remaining_text = after
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text))

    return new_nodes


def split_nodes_images(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for n in nodes:
        if n.type is not TextType.TEXT:
            new_nodes.append(n)
            continue

        images = extract_markdown_images(n.text)
        remaining_text = n.text
        for label, link in images:
            markdown = f"![{label}]({link})"
            before, md, after = remaining_text.partition(markdown)
            new_nodes.append(TextNode(before))
            new_nodes.append(TextNode(label, TextType.IMAGE, link))
            remaining_text = after
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text))

    return new_nodes


# note: not using regex because I do not have a [regex license](https://regexlicensing.org/) ;)


# returns a list of markdown images (i.e ![alt](link) )
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    extracted: list[tuple[str, str]] = []
    has_searched = False
    last_match: tuple[int, int, int, int] | None = None
    while not has_searched or last_match is not None:
        has_searched = True
        last_match = index_of_link(text, 0 if last_match is None else last_match[3])
        # no occurences of a link format? get outta here
        if last_match is None:
            break
        label_start, label_end, link_start, link_end = last_match
        # if the character before the beginning of the text label is not a !, it's a link!!!!
        if label_start > 0 and text[label_start - 1] != "!":
            continue
        label = text[label_start + 1 : label_end]
        link = text[link_start + 1 : link_end]
        extracted.append((label, link))

    return extracted


# returns a list of markdown links (i.e [alt](link) )
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    extracted: list[tuple[str, str]] = []
    has_searched = False
    last_match: tuple[int, int, int, int] | None = None
    while not has_searched or last_match is not None:
        has_searched = True
        last_match = index_of_link(text, 0 if last_match is None else last_match[3])
        # no occurences of a link format? get outta here
        if last_match is None:
            break
        label_start, label_end, link_start, link_end = last_match
        # if the character before the beginning of the text label is a !, it's not a link!!!!
        if label_start > 0 and text[label_start - 1] == "!":
            continue
        label = text[label_start + 1 : label_end]
        link = text[link_start + 1 : link_end]
        extracted.append((label, link))

    return extracted


# returns the index of the first occurrence of a markdown link [text](link), the indices are the position of the symbols.
# returns (text_start_index, text_end_index, link_start_index, link_end_index)
def index_of_link(text: str, start_from: int = 0) -> tuple[int, int, int, int] | None:
    # if there aren't even enough characters to have all the symbols plus text in between,
    # then we can't possibly have any links (i.e. [a](b) is the smallest possible valid format)
    if len(text) < len("[a](b)"):
        return None

    text_start_symbol, text_end_symbol = "[", "]"
    link_start_symbol, link_end_symbol = "(", ")"

    mid_link = False
    text_start_index, text_end_index, link_start_index, link_end_index = -1, -1, -1, -1
    for i, c in enumerate(text[start_from:]):
        i = i + start_from
        # look for text start symbol, while ensuring we aren't actually an image
        # and we don't have an empty text block
        if not mid_link and c == text_start_symbol:
            text_start_index = i
            mid_link = True

        # look for end of text symbol, ensuring the next one is the start of a link
        if (
            mid_link
            and c == text_end_symbol
            and i < len(text) - 1
            and text[i + 1] == link_start_symbol
            and not text_end_index > -1  # stop at first valid end symbol
        ):
            text_end_index = i
            link_start_index = i + 1

        # look for end of link symbol, and extract text and link.
        if (
            mid_link
            and c == link_end_symbol
            and (text[i - 1] != link_start_symbol)
            and link_start_index > -1
        ):
            link_end_index = i
            return (text_start_index, text_end_index, link_start_index, link_end_index)
    return None
