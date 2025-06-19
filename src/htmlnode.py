class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError

    
    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        
        return(
            f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={self.children}, props={self.props})"
        )
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if tag is None and value is None:
            raise ValueError("LeafNode must have a tag or value")
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("ParentNode must have a tag")
        if not children:
            raise ValueError("ParentNode must have children")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
from textnode import TextType, TextNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return ParentNode("b", [LeafNode(None, text_node.text)])
    elif text_node.text_type == TextType.ITALIC:
        return ParentNode("i", [LeafNode(None, text_node.text)])
    elif text_node.text_type == TextType.CODE:
        return ParentNode("code", [LeafNode(None, text_node.text)])
    elif text_node.text_type == TextType.LINKS:
        return ParentNode("a", [LeafNode(None, text_node.text)], props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")

