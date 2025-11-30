import re
from nodes.leaf_node import LeafNode
from nodes.text_node import TextType, TextNode


def text_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, text_node.props)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            return LeafNode("img", "", text_node.props)
        case _:
            raise Exception("Node is not text_node")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimeter_found = False
    for old_node in old_nodes:
        if delimiter in old_node.text:
            delimeter_found = True
    if delimeter_found:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
            else:
                if (delimiter in old_node.text):
                    strings = old_node.text.split(delimiter)
                    if len(strings) <= 2:
                        raise Exception("No matching delimiter found")
                    else:
                        left = TextNode(strings[0], TextType.TEXT)
                        new_node = TextNode(strings[1], text_type)
                        right = TextNode(strings[2], TextType.TEXT)
                        new_nodes.extend([left, new_node, right])
                else:
                    new_nodes.append(old_node)
        return new_nodes
    else:
        raise Exception("No delimeter found")
        parts = old_nodes.split(delimiter)


def extract_markdown_images(text):
    imgs = re.findall(r"[\!]\[(.*?)\]\((.*?)\)", text)
    result = []
    for img in imgs:
        result.append((img[0], img[1]))
    return result


def extract_markdown_links(text):
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    result = []
    for link in links:
        result.append((link[0], link[1]))
    return result


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            old_note_text = old_node.text
            if "![" in old_note_text:
                for image in extract_markdown_images(old_node.text):
                    sections = old_note_text.split(
                        f"![{image[0]}]({image[1]})", 1)
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(
                        TextNode(image[0], TextType.IMAGE, image[1]))
                    old_note_text = sections[1]
                    if old_note_text != "" and "![" not in old_note_text:
                        new_nodes.append(
                            TextNode(old_note_text, TextType.TEXT))
            else:
                new_nodes.append(old_node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            old_note_text = old_node.text
            if "[" in old_node.text:
                for link in extract_markdown_links(old_node.text):
                    sections = old_note_text.split(
                        f"[{link[0]}]({link[1]})", 1)
                    section = sections[0]
                    new_nodes.append(TextNode(section, TextType.TEXT))
                    new_nodes.append(
                        TextNode(link[0], TextType.LINK, link[1]))
                    old_note_text = sections[1]
            else:
                new_nodes.append(old_node)
    return new_nodes


def text_to_textnodes(text):
    new_node = TextNode(text, TextType.TEXT)
    result = split_nodes_delimiter([new_node], "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result
