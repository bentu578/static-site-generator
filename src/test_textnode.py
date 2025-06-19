import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.LINKS, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINKS, "https://example.com")
        self.assertEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.LINKS, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINKS, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_default_url(self):
        node = TextNode("This is a test node", TextType.NORMAL)
        self.assertIsNone(node.url)

if __name__ == "__main__":
    unittest.main()