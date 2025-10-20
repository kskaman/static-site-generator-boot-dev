import unittest
from main import extract_markdown_images, extract_markdown_links

class TestMarkdownExtract(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_markdown_images_multiple(self):
        text = (
            "Look ![rick roll](https://i.imgur.com/aKaOqIh.gif) and "
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        self.assertListEqual([], extract_markdown_images("no images here"))

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        text = (
            "Links [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_links_do_not_capture_images(self):
        text = "![img](https://i.imgur.com/x.png) and [link](https://example.com)"
        self.assertListEqual(
            [("link", "https://example.com")],
            extract_markdown_links(text)
        )

    def test_images_do_not_capture_links(self):
        text = "![img](https://i.imgur.com/x.png) and [link](https://example.com)"
        self.assertListEqual(
            [("img", "https://i.imgur.com/x.png")],
            extract_markdown_images(text)
        )

if __name__ == "__main__":
    unittest.main()
