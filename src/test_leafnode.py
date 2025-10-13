import unittest

from leafnode import LeafNode;

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_anchor_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_raw_text_when_tag_none(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_raises_when_value_none(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_raises_when_value_empty_string(self):
        node = LeafNode("em", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_has_no_children(self):
        node = LeafNode("strong", "bold")
        self.assertIsNone(node.children)

    def test_props_multiple_attributes(self):
        node = LeafNode("img", "alt text", {"src": "/x.png", "alt": "logo"})
        # Note: dict preserves insertion order in modern Python; adjust if needed.
        self.assertEqual(node.to_html(), '<img src="/x.png" alt="logo">alt text</img>')

if __name__ == "__main__":
    unittest.main()
