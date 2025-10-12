import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_returns_empty_when_no_props(self):
        node1 = HTMLNode(tag="p", value="Hello", props=None)
        node2 = HTMLNode(tag="a", value="Click", props={})
        self.assertEqual(node1.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), "")

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        result = node.props_to_html()
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith(" "))
        self.assertIn(" target=", result)

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode(tag="div", value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_displays_all_fields(self):
        child = HTMLNode(tag="span", value="Child")
        node = HTMLNode(tag="div", value=None, children=[child], props={"class": "container"})
        text = repr(node)
        self.assertIn("HTMLNode(", text)
        self.assertTrue("tag=div" in text or "tag='div'" in text)
        self.assertIn("children", text)
        self.assertIn("props", text)

    def test_all_fields_optional(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


if __name__ == "__main__":
    unittest.main()
