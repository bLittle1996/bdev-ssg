from blocknode import text_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode


def markdown_to_html(markdown: str) -> str:
    return markdown_to_html_node(markdown).to_html()


def markdown_to_html_node(markdown: str) -> HTMLNode:
    root = ParentNode("div")
    blocks = text_to_blocks(markdown)
    html_nodes = list(map(lambda b: b.to_html_node(), blocks))
    root.children = html_nodes
    return root


def extract_title(html: HTMLNode) -> str:
    h1 = html.find("h1")
    title = None
    if h1 is None:
        raise Exception("no h1 in html node")
    if isinstance(h1, ParentNode) and len(h1.children) == 1:
        title = h1.children[0].value
    else:
        title = h1.value
    if title is None:
        raise ValueError(
            "invalid h1 node, must be LeafNode with value or ParentNode with one LeafNode child"
        )

    return title
