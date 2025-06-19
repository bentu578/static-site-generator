import unittest
from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_multiple_children(self):
        children = [
            LeafNode("b", "Bold"),
            LeafNode(None, " plain "),
            LeafNode("i", "Italic"),
        ]
        parent = ParentNode("p", children)
        self.assertEqual(parent.to_html(), "<p><b>Bold</b> plain <i>Italic</i></p>")

    def test_missing_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")])

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

if __name__ == "__main__":
    unittest.main()
