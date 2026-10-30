from .htmlnode import HTMLNode

VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value : str, props : dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value and self.tag not in VOID_ELEMENTS:
            raise ValueError('Every Leaf Node should have a value')
        if not self.tag:
            return self.value
        if self.tag in VOID_ELEMENTS:
            return f"<{self.tag}{self.props_to_html()} />"
        formatted_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return formatted_str
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props_to_html()})"


    
