from functools import reduce
from enums import BlockType
from htmlnode import ParentNode
from textnode import TextNode, text_to_nodes

type BlockChildren = list[list[TextNode]]


class BlockNode:
    def __init__(self, text: str) -> None:
        self.type = BlockType.from_text(text)
        self.text = text
        self.cleaned_text = self.__strip_markdown(text)
        self.children: BlockChildren = []
        self.__init_children()

    def __init_children(self):
        # new lines will be turned into a space instead!
        lines = [self.cleaned_text.replace("\n", " ")]
        # only lists should actually create seperate lines from their new lines
        # as each - is a discrete <li> parent node
        if self.type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            lines = self.cleaned_text.splitlines()
        # quoutes should keep new lines, for multi-line quoutes
        if self.type in (BlockType.QUOTE, BlockType.CODE):
            lines = [self.cleaned_text]

        # some types cannot have markdown parsed inside of them, like code blocks.
        # we'll just use raw text nodes in that case
        if self.type == BlockType.CODE:
            self.children = list(map(lambda l: [TextNode(l.strip("\n"))], lines))
        else:
            self.children = list(map(text_to_nodes, lines))

    def to_html_node(self) -> ParentNode:
        node = ParentNode(self.get_tag(), self.__get_child_html_nodes())
        if self.type == BlockType.CODE:
            node = ParentNode("pre", [node])
        return node

    def __get_child_html_nodes(self):
        lines_as_html_nodes = list(
            map(
                lambda node_list: list(
                    map(lambda node: node.to_html_node(), node_list)
                ),
                self.children,
            )
        )
        if self.type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            # wrap each line in an <li>
            list_items = list(map(lambda l: ParentNode("li", l), lines_as_html_nodes))
            return list_items

        # for everything else, we just smoosh it all together
        flattened_list = reduce(
            lambda flattened, cur_list: flattened + cur_list, lines_as_html_nodes
        )
        return flattened_list

    def get_tag(self) -> str:
        match self.type:
            case BlockType.PARAGRAPH:
                return "p"
            case BlockType.QUOTE:
                return "blockquote"
            case BlockType.CODE:
                return "code"
            case BlockType.HEADING:
                return self.__get_heading_level()
            case BlockType.ORDERED_LIST:
                return "ol"
            case BlockType.UNORDERED_LIST:
                return "ul"
            case _:
                return "div"

    def __get_heading_level(self):
        if self.type is not BlockType.HEADING:
            raise ValueError(
                "__get_heading_level must be called on HEADING block types"
            )
        count = 0
        for c in self.text:
            if c != "#":
                break
            # h6 is the smallest heading
            count = min(6, count + 1)
        return f"h{count}"

    def __eq__(self, target: object, /) -> bool:
        if not isinstance(target, BlockNode):
            return False
        # no need to compare children, as it is constructed from self.text
        return self.type == target.type and self.text == target.text

    def __strip_markdown(self, md: str) -> str:
        match self.type:
            case BlockType.UNORDERED_LIST:
                return "\n".join(map(lambda l: l[l.index(" ") + 1 :], md.split("\n")))
            case BlockType.ORDERED_LIST:
                return "\n".join(map(lambda l: l[l.index(" ") + 1 :], md.split("\n")))
            case BlockType.CODE:
                return md.strip("```")
            case BlockType.QUOTE:
                return "\n".join(
                    # strip the newline and space variants
                    map(
                        lambda l: (
                            l.lstrip("> ") if l.startswith("> ") else l.lstrip(">")
                        ),
                        md.split("\n"),
                    )
                )
            case BlockType.HEADING:
                return md[md.index(" ") + 1 :]
            case _:
                return md


# turns the whole md document into a list of strings. Deletes extra whitespace, sorry
def text_to_blocks(md: str) -> list[BlockNode]:
    # looks awful
    return list(
        filter(
            # gotta have some lines
            lambda b: len(b.children) > 0
            # and those lines better not be empty
            and len(b.children[0]) > 0,
            list(map(lambda s: BlockNode(s.strip()), md.split("\n\n"))),
        )
    )
