import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

if __name__ == "__main__":
    unittest.main()
