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
        return f"{key}=\"{value.replace('"', "&quot;")}\""

    def __repr__(self) -> str:
        props = ""
        if self.tag:
            props = self.tag
        if self.value:
            props += f", {self.value}"
        if self.children:
            props += f", {len(self.children)} child nodes"
        if self.props:
            props += f", {self.props}"

        return f"HTMLNode({props})"
