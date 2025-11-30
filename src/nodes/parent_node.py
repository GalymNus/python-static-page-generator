from nodes.html_node import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required!")
        elif self.children == None:
            raise ValueError("Parent node should have at least 1 child node!")
        else:
            props = self.props_to_html()
            children = ""
            for child in self.children:
                children += child.to_html()
            return f"<{self.tag}{props}>{children}</{self.tag}>"

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        inline_props = ""
        for prop in self.props:
            inline_props += f' {prop}="{self.props[prop]}"'
        return inline_props

    def __repr__(self):
        return f"{self.tag} | {self.value}"
