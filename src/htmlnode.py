from typing import Sequence


type Optional[T] = T | None


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Sequence["HTMLNode"] = [],
        props: dict[str, str] = {},
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # overriden by implementing classes
    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return " ".join(map(lambda v: self.__prop_to_html(*v), self.props.items()))

    def __prop_to_html(self, key: str, value: str) -> str:
        if self.tag == "img" and key == "href":
            key = "src"
        return f'{key}="{self._escape_special_chars(value)}"'

    # for text content or attribute content of a html node, not intended for external use
    def _escape_special_chars(self, text: str) -> str:
        return text.replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

    # DFS for tag
    def find(self, tag: str) -> "HTMLNode | None":
        if self.tag == tag:
            return self
        for c in self.children:
            found = c.find(tag)
            if found:
                return found
        return None

    def __eq__(self, rhs: object, /) -> bool:
        if not isinstance(rhs, type(self)):
            return False

        tag_eq = self.tag == rhs.tag
        value_eq = self.value == rhs.value
        children_eq = len(self.children) == len(rhs.children)
        prop_eq = len(self.props) == len(rhs.props)
        if children_eq:
            for i, node in enumerate(self.children):
                children_eq = children_eq and node == rhs.children[i]
        if prop_eq:
            for k, v in self.props.items():
                prop_eq = prop_eq and k in rhs.props and v == rhs.props[k]

        return tag_eq and value_eq and children_eq and prop_eq

    def __repr__(self) -> str:
        props = ""
        if self.tag:
            props = self.tag
        props += f', {f"\"{self.value}\"" if self.value else None}'
        if self.children:
            props += f", {len(self.children)} child nodes"
        if self.props:
            props += f", {self.props}"

        if props.startswith(", "):
            props = props.replace(", ", "")

        return f"{type(self).__name__}({props})"


class LeafNode(HTMLNode):
    self_closing_tags = ("img",)

    def __init__(
        self,
        tag: Optional[str],
        value: str,
        props: dict[str, str] = {},
    ):
        super().__init__(tag, value, [], props)
        self.value = value  # for type system

    def to_html(self) -> str:
        cleaned_value = self._escape_special_chars(self.value)
        if not self.tag:
            return cleaned_value
        html = f"<{self.tag} {self.props_to_html()}>{cleaned_value}</{self.tag}>"
        if len(self.props) == 0:
            html = html.replace(" >", ">", 1)
        if self.tag in self.self_closing_tags:
            # self closing tags should not have children, so remove the value and closing tag
            html = html.replace(f"</{self.tag}>", "").replace(cleaned_value, "")

        return html


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: Sequence[HTMLNode] = [], props: dict[str, str] = {}
    ):
        super().__init__(tag, None, children, props)
        self.tag = tag

    def to_html(self):
        child_html = "".join(map(lambda n: n.to_html(), self.children))
        if len(self.props) == 0:
            return f"<{self.tag}>{child_html}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{child_html}</{self.tag}>"
