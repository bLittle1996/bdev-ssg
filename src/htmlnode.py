from typing import Self


type Optional[T] = T | None


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: list[Self] = [],
        props: dict[str, str] = {},
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return " ".join(map(lambda v: self.__prop_to_html(*v), self.props.items()))

    def __prop_to_html(self, key: str, value: str) -> str:
        return f'{key}="{self._escape_special_chars(value)}"'

    # for text content or attribute content of a html node
    def _escape_special_chars(self, text: str) -> str:
        return text.replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

    def __repr__(self) -> str:
        props = ""
        if self.tag:
            props = self.tag
        if self.value:
            props += f', "{self.value}"'
        if self.children:
            props += f", {len(self.children)} child nodes"
        if self.props:
            props += f", {self.props}"

        if props.startswith(", "):
            props = props.replace(", ", "")

        return f"HTMLNode({props})"


class LeafNode(HTMLNode):
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
        if len(self.props) == 0:
            return f"<{self.tag}>{cleaned_value}</{self.tag}>"

        return f"<{self.tag} {self.props_to_html()}>{cleaned_value}</{self.tag}>"
