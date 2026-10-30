class HTMLNode:
    def __init__(self, tag: str | None, value: str | None , children: list["HTMLNode"] | None, props: dict | None ):
        self.tag = tag
        self.value = value 
        self.children = children 
        self.props = props 


    def to_html(self):
        if not self.value and not self.children:
            raise ValueError('Every HTML Node should have a value or children')
        if not self.tag:
            return self.value
        formatted_str = f"<{self.tag}{self.props_to_html()}>"
        if self.value:
            formatted_str += f"{self.value}"
        if self.children:
            for child in self.children:
                formatted_str += child.to_html()
        formatted_str += f"</{self.tag}>"
        return formatted_str

    def props_to_html(self):
        # This method returns the formatted string representing the html attributes of the node. 
        s = ''
        data = self.props if self.props else {}
        for key,value in data.items():
            s += f' {key}="{value}"'
        return s
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props_to_html()})'
    

