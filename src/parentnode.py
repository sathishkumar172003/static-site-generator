from .htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag : str, children : list["HTMLNode"], props : dict | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('Tag is required')
        if not self.children:
            raise ValueError('Children are required')
        #
        inner_html_str = ""
        for child in self.children:
            inner_html_str += child.to_html()
        formatted_str = f'<{self.tag}{self.props_to_html()}>{inner_html_str}</{self.tag}>'
        return formatted_str 

    