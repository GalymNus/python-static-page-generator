from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold_text"
    CODE = "code_text"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, two):
        if self.text == two.text and self.text_type == two.text_type and self.url == two.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
