from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """
    A leaf HTML node (no children).
    - `value` is required (must be non-empty when rendered).
    - `tag` is required as a parameter but may be None to emit raw text.
    - `props` is optional.
    """

    def __init__(self, tag, value, props=None):
        # children are not allowed for a LeafNode
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        # All leaf nodes must have a value
        if self.value is None or (isinstance(self.value, str) and self.value == ""):
            raise ValueError("LeafNode must have a non-empty value")

        # No tag? Return raw text
        if self.tag is None:
            return str(self.value)

        # Otherwise render as a tag with optional props
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
