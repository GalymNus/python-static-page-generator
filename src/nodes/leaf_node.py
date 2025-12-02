from nodes.html_node import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        inline_props = ""
        for prop in self.props:
            inline_props += f' {prop}="{self.props[prop]}"'
        return inline_props

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
