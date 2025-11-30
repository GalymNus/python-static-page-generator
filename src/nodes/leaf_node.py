from nodes.html_node import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        else:
            props = self.props_to_html()
            if self.tag != None:
                return f"<{self.tag}{props}>{self.value}</{self.tag}>"
            else:
                return f"{self.value}"

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        inline_props = ""
        for prop in self.props:
            inline_props += f' {prop}="{self.props[prop]}"'
        return inline_props

    def __repr__(self):
        return f"{self.tag} | {self.value}"
