from textnode import TextNode, TextType
import re
from typing import List, Tuple

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not delimiter:
        raise ValueError("Delimiter must be a non-empty string")

    new_nodes = []

    for node in old_nodes:
        # Only attempt to split plain text nodes
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        # No delimiter? keep as-is
        if delimiter not in text:
            new_nodes.append(node)
            continue

        parts = text.split(delimiter)

        # Valid markup produces an odd number of parts (outside/inside/outside/...)
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in: {text!r}"
            )

        # Build alternating TEXT / target-type nodes
        for i, part in enumerate(parts):
            if part == "":
                # Skip empty fragments to avoid zero-length nodes
                continue

            if i % 2 == 0:
                # outside delimiters -> plain text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # inside delimiters -> the given text_type
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Extracts Markdown image tuples: (alt_text, url)
    Example: '![alt](url)'
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Extracts Markdown link tuples: (anchor_text, url)
    Example: '[text](url)' but NOT images.
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
