import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.example.com"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=a, value=Click here, children=[], props={'href': 'https://www.example.com'})"

        )

if __name__=="__main__":
    unittest.main()