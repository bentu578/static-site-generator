import unittest
from inline_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node 
from textnode import TextNode, TextType




class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a 'code block' word", TextType.NORMAL)
        result = split_nodes_delimiter([node], "'", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_split_bold(self):
        node = TextNode("A **bold** word", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("A ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_no_split_non_normal(self):
        node = TextNode("Just a link", TextType.LINKS, "https://example.com")
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [node])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("Unmatched `codeblock", TextType.NORMAL)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Here is ![img1](https://img.com/1.png) and ![img2](https://img.com/2.jpg)"
        expected = [
            ("img1", "https://img.com/1.png"),
            ("img2", "https://img.com/2.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "A link [to Google](https://google.com) and [to Boot.dev](https://boot.dev)"
        expected = [
            ("to Google", "https://google.com"),
            ("to Boot.dev", "https://boot.dev"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_ignore_image_links_in_link_match(self):
        text = "Mixed ![img](https://img.com/x.png) and [real link](https://real.com)"
        expected = [("real link", "https://real.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_matches(self):
        text = "No links or images here"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Link to [Boot.dev](https://boot.dev) and [YouTube](https://youtube.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link to ", TextType.NORMAL),
                TextNode("Boot.dev", TextType.LINKS, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("YouTube", TextType.LINKS, "https://youtube.com"),
            ],
            new_nodes,
        )

    def test_no_links_or_images(self):
        node = TextNode("Just plain text.", TextType.NORMAL)
        self.assertEqual(split_nodes_link([node]), [node])
        self.assertEqual(split_nodes_image([node]), [node])

    def test_text_to_textnodes_full(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINKS, "https://boot.dev"),

        ]
        self.assertEqual(result, expected)

    


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ndef hello():\n    return 'hi'\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> still quoted"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is just a paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_ordered_list(self):
        block = "1. First\n3. Skipped"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)




class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

        def test_codeblock(self):
            md = """```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
            )




# ✅ Correct indentation
if __name__ == "__main__":
    unittest.main()
