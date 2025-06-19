
import unittest
from utils import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_normal(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_with_whitespace(self):
        md = "#   My Blog   "
        self.assertEqual(extract_title(md), "My Blog")

    def test_extract_title_missing(self):
        md = "## Subheading\nSome content here."
        with self.assertRaises(Exception):
            extract_title(md)
