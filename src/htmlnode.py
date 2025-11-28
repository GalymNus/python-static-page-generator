class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        inline_props = ""
        for prop in self.props:
            inline_props += f"{prop}={self.props[prop]} "
        return inline_props

    def __repr__(self):
        return f"{self.tag} | {self.value}"
