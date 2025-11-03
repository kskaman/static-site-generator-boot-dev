from enum import Enum
from htmlnode import LeafNode, ParentNode
import re

from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    """
    Convert a markdown string into a list of block elements.

    Args:
        markdown (str): The markdown content to be converted.

    Returns:
        list: A list of block elements representing the markdown content.
    """
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    
    return blocks


def block_to_block_type(block):
    """
    Determine the block type of a given markdown block.

    Args:
        block (str): The markdown block.

    Returns:
        BlockType: The type of the block.
    """
    if block.startswith('#'):
        return BlockType.HEADING
    elif block.startswith('>'):
        return BlockType.QUOTE
    elif block.startswith('- ') or block.startswith('* '):
        return BlockType.ULIST
    elif block[0].isdigit() and block[1:3] == '. ':
        return BlockType.OLIST
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH
    
# ==== Inline conversion hook ====
def text_to_children(text: str):
    """
    Shared function that converts inline Markdown to a list of HTMLNodes.
    Replace this with your project's TextNode -> HTMLNode pipeline.
    For now, we keep it simple: one raw text leaf (no inline parsing).
    """
    # If you have text nodes and converters, wire them in here:
    nodes =  text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in nodes]


# ==== Block builders ====
def _build_heading(block: str) -> ParentNode:
    m = re.match(r"^(#{1,6})\s+(.*)$", block, flags=re.DOTALL)
    if not m:
        # Fallback to paragraph if malformed
        return _build_paragraph(block)
    level = min(len(m.group(1)), 6)
    text = m.group(2).strip()
    return ParentNode(f"h{level}", text_to_children(text))


def _strip_quote_markers(block: str) -> str:
    lines = []
    for ln in block.splitlines():
        # Remove one leading '>' and an optional space following it
        ln = re.sub(r"^\s*>\s?", "", ln)
        lines.append(ln)
    return "\n".join(lines).strip()


def _build_quote(block: str) -> ParentNode:
    inner = _strip_quote_markers(block)
    # Common HTML is <blockquote><p>…</p></blockquote>, but
    # we allow multiple paragraphs inside a single quote.
    paragraphs = [seg for seg in inner.split("\n\n") if seg.strip()]
    p_children = []
    for seg in paragraphs:
        p_children.append(ParentNode("p", text_to_children(" ".join(seg.splitlines()))))
    return ParentNode("blockquote", p_children if p_children else [ParentNode("p", text_to_children(""))])


def _build_ulist(block: str) -> ParentNode:
    items = []
    for ln in block.splitlines():
        m = re.match(r"^\s*[-*]\s+(.*)$", ln)
        if not m:
            # Skip malformed lines in a UL block
            continue
        txt = m.group(1).strip()
        items.append(ParentNode("li", text_to_children(txt)))
    return ParentNode("ul", items)


def _build_olist(block: str) -> ParentNode:
    items = []
    for ln in block.splitlines():
        m = re.match(r"^\s*\d+\.\s+(.*)$", ln)
        if not m:
            continue
        txt = m.group(1).strip()
        items.append(ParentNode("li", text_to_children(txt)))
    return ParentNode("ol", items)


def _build_code(block: str) -> ParentNode:
    """
    Parse fenced code block:
    ```lang
    code...
    ```
    No inline parsing inside code.
    """
    lines = block.splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].startswith("```"):
        fence_open = lines[0]
        lang = fence_open[3:].strip() or None
        code_text = "\n".join(lines[1:-1])
        if not code_text.endswith("\n"):
            code_text += "\n"
    else:
        # Not a proper fence; treat as paragraph fallback
        return _build_paragraph(block)

    code_props = {"class": f"language-{lang}"} if lang else None
    code_node = LeafNode("code", code_text, code_props)
    return ParentNode("pre", [code_node])


def _build_paragraph(block: str) -> ParentNode:
    # Collapse internal newlines to spaces (typical Markdown paragraph behavior)
    text = " ".join(block.splitlines())
    return ParentNode("p", text_to_children(text))


# ==== Public: markdown_to_html_node ====
def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Convert a full Markdown string to a single parent HTML node (a <div>)
    whose children are the per-block HTML trees.
    """
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            node = _build_heading(block)
        elif btype == BlockType.QUOTE:
            node = _build_quote(block)
        elif btype == BlockType.ULIST:
            node = _build_ulist(block)
        elif btype == BlockType.OLIST:
            node = _build_olist(block)
        elif btype == BlockType.CODE:
            node = _build_code(block)  # special: no inline parsing
        else:
            node = _build_paragraph(block)

        children.append(node)

    return ParentNode("div", children)
