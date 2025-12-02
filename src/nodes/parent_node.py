from nodes.html_node import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required!")
        if self.children is None:
            raise ValueError("Parent node should have at least 1 child node!")
        props = self.props_to_html()
        children = ""
        for child in self.children:
            if child != None:
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
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
