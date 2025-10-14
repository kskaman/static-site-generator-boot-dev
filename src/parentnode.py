# parentnode.py
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # tag and children are required; value is not accepted for ParentNode
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("ParentNode must have a tag")
        # Treat 'missing children' and empty list as invalid for a parent node
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child")

        inner_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>"
