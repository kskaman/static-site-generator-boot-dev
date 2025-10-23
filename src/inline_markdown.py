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


def split_nodes_image(old_nodes):
    """
    Find Markdown images in TEXT nodes and split them into:
      - TEXT nodes for surrounding text
      - IMAGE nodes carrying alt text and url
    Leaves non-TEXT nodes unchanged.
    """
    new_nodes = []

    for node in old_nodes:
        # Only attempt to split plain text nodes
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        
        while True:
            images = extract_markdown_images(remaining)
            # If no images found, add the remaining text as a TEXT node and break
            if not images:
                if remaining:
                    new_nodes.append(TextNode(remaining, TextType.TEXT))
                break

            # Take the first image found
            alt_text, url = images[0]
            image_markup = f"![{alt_text}]({url})"
            
            # split around this exact image markup
            before, sep, after = remaining.partition(image_markup)

            # Sanity: sep should be the image markup
            # If not, something went wrong and we should break to avoid infinite loop
            if sep != image_markup:
                new_nodes.append(TextNode(remaining, TextType.TEXT))
                break

            # Add TEXT node for text before the image
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            # Add IMAGE node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Continue with the text after the image
            remaining = after
        
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Find Markdown links in TEXT nodes and split them into:
      - TEXT nodes for surrounding text
      - LINK nodes carrying anchor text and url
    Leaves non-TEXT nodes unchanged.
    """
    new_nodes = []

    for node in old_nodes:
        # Only attempt to split plain text nodes
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        
        while True:
            links = extract_markdown_links(remaining)
            # If no links found, add the remaining text as a TEXT node and break
            if not links:
                if remaining:
                    new_nodes.append(TextNode(remaining, TextType.TEXT))
                break

            # Take the first link found
            anchor_text, url = links[0]
            link_markup = f"[{anchor_text}]({url})"
            
            # split around this exact link markup
            before, sep, after = remaining.partition(link_markup)

            # Sanity: sep should be the link markup
            # If not, something went wrong and we should break to avoid infinite loop
            if sep != link_markup:
                new_nodes.append(TextNode(remaining, TextType.TEXT))
                break

            # Add TEXT node for text before the link
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            # Add LINK node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            # Continue with the text after the link
            remaining = after

    return new_nodes

def text_to_textnodes(text): 
    """Convert raw markdown-ish inline text into a flat list of TextNodes by
    progressively splitting on images, links, code, bold, and italic.

    Order matters:
      1) Images/Links first (they're stand-alone units)
      2) Code next (protects inline code from being parsed as bold/italic)
      3) Bold
      4) Italic

    Example:
      "This is **text** with an _italic_ word and a `code block` and an
       ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    """

    nodes = [TextNode(text, TextType.TEXT)]

    # 1) Images
    nodes = split_nodes_image(nodes)
    # 2) Links
    nodes = split_nodes_link(nodes)
    # 3) Code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # 4) Bold
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # 5) Italic
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    return nodes