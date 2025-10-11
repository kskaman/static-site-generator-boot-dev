import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same_values(self):
        n1 = TextNode("Hello", TextType.BOLD_TEXT)
        n2 = TextNode("Hello", TextType.BOLD_TEXT)
        self.assertEqual(n1, n2)

    def test_not_eq_different_text(self):
        n1 = TextNode("Hello", TextType.BOLD_TEXT)
        n2 = TextNode("Hi", TextType.BOLD_TEXT)
        self.assertNotEqual(n1, n2)

    def test_not_eq_different_text_type(self):
        n1 = TextNode("Hello", TextType.BOLD_TEXT)
        n2 = TextNode("Hello", TextType.ITALIC_TEXT)
        self.assertNotEqual(n1, n2)

    def test_eq_with_same_url(self):
        n1 = TextNode("Click here", TextType.LINK_TEXT, "https://example.com")
        n2 = TextNode("Click here", TextType.LINK_TEXT, "https://example.com")
        self.assertEqual(n1, n2)

    def test_not_eq_one_url_none(self):
        n1 = TextNode("Click here", TextType.LINK_TEXT)
        n2 = TextNode("Click here", TextType.LINK_TEXT, "https://example.com")
        self.assertNotEqual(n1, n2)

    def test_not_eq_different_url(self):
        n1 = TextNode("Click here", TextType.LINK_TEXT, "https://a.com")
        n2 = TextNode("Click here", TextType.LINK_TEXT, "https://b.com")
        self.assertNotEqual(n1, n2)


if __name__ == "__main__":
    unittest.main()
