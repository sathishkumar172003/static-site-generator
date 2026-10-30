from enum import Enum 
from .leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text:str, text_type:TextType=TextType.TEXT, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self,other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type.value}, url={self.url})"
    


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    # It returns the leaf node based on the type of text node
    tag = None
    value = "" if text_node.text_type == TextType.IMAGE else text_node.text
    props = {}
    match text_node.text_type:
        case TextType.TEXT:
            tag = None 
        case TextType.BOLD:
            tag = 'b'
        case TextType.CODE:
            tag = 'code'
        case TextType.IMAGE:
            tag = 'img'
            props = {'src': text_node.url, 'alt': text_node.text}
        case TextType.ITALIC:
            tag = 'i'
        case TextType.LINK:
            tag = 'a'
            props={'href': text_node.url}
        case _:
            raise ValueError('text type does not match')
    leafnode = LeafNode(tag, value, props)
    return leafnode
