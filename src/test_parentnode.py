# test_parentnode.py
import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    # Provided examples (kept verbatim)
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # Additional edge cases & robustness

    def test_raises_when_tag_missing(self):
        with self.assertRaises(ValueError) as ctx:
            ParentNode(None, [LeafNode("span", "x")]).to_html()
        self.assertIn("must have a tag", str(ctx.exception))

    def test_raises_when_children_is_none(self):
        with self.assertRaises(ValueError) as ctx:
            ParentNode("div", None).to_html()
        self.assertIn("at least one child", str(ctx.exception))

    def test_raises_when_children_is_empty_list(self):
        with self.assertRaises(ValueError) as ctx:
            ParentNode("div", []).to_html()
        self.assertIn("at least one child", str(ctx.exception))

    def test_multiple_children_mixed_text_and_tags(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> and <i>italic</i> text</p>",
        )

    def test_nested_three_levels(self):
        n = ParentNode(
            "section",
            [
                ParentNode(
                    "article",
                    [
                        ParentNode(
                            "p",
                            [LeafNode(None, "deep")]
                        )
                    ],
                )
            ],
        )
        self.assertEqual(n.to_html(), "<section><article><p>deep</p></article></section>")

    def test_with_props(self):
        # Single prop to avoid dict order issues
        n = ParentNode("div", [LeafNode(None, "hi")], props={"class": "box"})
        self.assertEqual(n.to_html(), '<div class="box">hi</div>')

    def test_child_not_an_htmlnode_raises_attribute_error(self):
        # Spec says: iterate and call to_html on each child.
        # Passing a non-node should surface an AttributeError from that call.
        n = ParentNode("div", ["not-a-node"])
        with self.assertRaises(AttributeError):
            _ = n.to_html()

    def test_parent_does_not_accept_value_semantics(self):
        # ParentNode doesn't accept/emit 'value'; ensure children render, not a value
        n = ParentNode("ul", [LeafNode("li", "one"), LeafNode("li", "two")], props=None)
        self.assertEqual(n.to_html(), "<ul><li>one</li><li>two</li></ul>")

if __name__ == "__main__":
    unittest.main()
