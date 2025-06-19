from enum import Enum, auto
import re

from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        split_parts = node.text.split(delimiter)

        if len(split_parts) % 2 == 0:
            raise Exception(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        for i, part in enumerate(split_parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = node.text
        for alt_text, url in matches:
            split_text = text.split(f"![{alt_text}]({url})", 1)
            before, after = split_text if len(split_text) == 2 else (split_text[0], "")

            if before:
                new_nodes.append(TextNode(before, TextType.NORMAL))
            new_nodes.append(TextNode(alt_text, TextType.IMAGES, url))
            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = node.text
        for link_text, url in matches:
            split_text = text.split(f"[{link_text}]({url})", 1)
            before, after = split_text if len(split_text) == 2 else (split_text[0], "")

            if before:
                new_nodes.append(TextNode(before, TextType.NORMAL))
            new_nodes.append(TextNode(link_text, TextType.LINKS, url))
            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    raw_blocks = markdown.strip().split("\n\n")
    blocks = [block.strip() for block in raw_blocks if block.strip()]
    return blocks


def block_to_block_type(block):
    lines = block.strip().split('\n')

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if len(lines) == 1 and lines[0].startswith("#"):
        if lines[0].lstrip("#").startswith(" ") and 1 <= lines[0].count("#") <= 6:
            return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(r"^\d+\. ", line) for line in lines):
        expected = 1
        for line in lines:
            num = int(line.split(". ")[0])
            if num != expected:
                break
            expected += 1
        else:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            collapsed = " ".join(line.strip() for line in block.splitlines())
            children.append(ParentNode("p", children=text_to_children(collapsed)))



        elif block_type == BlockType.HEADING:
            heading_level = block.count("#", 0, block.find(" "))
            content = block[heading_level + 1:].strip()
            children.append(ParentNode(f"h{heading_level}", children=text_to_children(content)))

        elif block_type == BlockType.CODE:
            code_content = block.strip("`").strip()
            code_node = LeafNode("code", code_content)
            children.append(ParentNode("pre", children=[code_node]))

        elif block_type == BlockType.QUOTE:
            cleaned = "\n".join(line[1:].strip() for line in block.splitlines())
            children.append(ParentNode("blockquote", children=text_to_children(cleaned)))

        elif block_type == BlockType.UNORDERED_LIST:
            items = [ParentNode("li", children=text_to_children(line[2:])) for line in block.splitlines()]
            children.append(ParentNode("ul", children=items))

        elif block_type == BlockType.ORDERED_LIST:
            items = [ParentNode("li", children=text_to_children(line.split(". ", 1)[1])) for line in block.splitlines()]
            children.append(ParentNode("ol", children=items))

        else:
            raise Exception(f"Unknown block type: {block_type}")

    return ParentNode("div", children=children)
