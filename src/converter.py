from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINKS:
        if not text_node.url:
            raise ValueError("LINKS TextNode must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})

    elif text_node.text_type == TextType.IMAGES:
        if not text_node.url:
            raise ValueError("IMAGES TextNode must have a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    else:
        raise ValueError(f"Unknown TextType: {text_node.text_type}")
