from blocknode import text_to_blocks
from htmlnode import ParentNode


def markdown_to_html(markdown: str) -> str:
    root = ParentNode("div")
    blocks = text_to_blocks(markdown)
    html_nodes = list(map(lambda b: b.to_html_node(), blocks))
    root.children = html_nodes
    return root.to_html()
