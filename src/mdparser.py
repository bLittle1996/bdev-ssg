from textnode import TextNode, TextType

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
        if len(n.text) < len(delimiter):
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
