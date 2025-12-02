import re
import os
from nodes.leaf_node import LeafNode
from nodes.text_node import TextType, TextNode
from nodes.parent_node import ParentNode
from nodes.html_node import HTMLNode
from enum import Enum
from pathlib import Path

PUBLIC_DIRECTORY = "docs"
STATIC_DIRECTORY = "static"
CONTENT_DIRECTORY = "content"
TEMPLATE_PATH = "template.html"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UN_LIST = "unordered_list"
    OR_LIST = "ordered_list"


def text_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text.replace("\n", " "))
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.LINK:
            props = {"href": text_node.url}
            return LeafNode("a", text_node.text, props)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            props = {"src": f"{text_node.url}", "alt": text_node.text}
            return LeafNode("img", "", props)
        case _:
            raise Exception("Node is not text_node")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


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
    new_node = [TextNode(text, TextType.TEXT)]
    result = split_nodes_delimiter(new_node, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result


def markdown_to_blocks(markdown):
    return markdown.strip().split("\n\n")


def get_block_type(block):
    if re.match("^#{1,9}", block):
        return BlockType.HEADING
    if re.match("^```", block):
        return BlockType.CODE
    if re.match("^>{1,2}", block):
        return BlockType.QUOTE
    if re.match("^-", block):
        return BlockType.UN_LIST
    if re.match("^\d{1,3}\. ", block):
        return BlockType.OR_LIST
    return BlockType.PARAGRAPH


def handle_unordered_list(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        child = None
        if not line.startswith("- "):
            raise Exception("Invalid unordered list")
        children.append(ParentNode("li", text_to_children(
            line.replace("- ", ""))))
    return children


def handle_ordered_list(block):
    children = []
    lines = block.split("\n")
    count = 1
    for line in lines:
        child = None
        if not line.startswith(f"{count}. "):
            raise Exception("Invalid ordered list")
        children.append(ParentNode("li", text_to_children(
            line.replace(f"{count}. ", ""))))
        count += 1
    return children


def handle_backquote(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        child = None
        if not line.startswith(">"):
            raise Exception("Invalid quote block")
        children.append(line.lstrip(">").strip())
    return text_to_children(" ".join(children))


def handle_text_to_html(block_type, block):
    match (block_type):
        case BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            if level + 1 >= len(block):
                raise ValueError(f"invalid heading level: {level}")
                text = block[level + 1:]
            clear_text = block.replace("#", "", level).replace(" ", "", 1)
            children = text_to_children(clear_text)
            return ParentNode(tag=f"h{level}", children=children)
        case BlockType.CODE:
            code_block = text_to_html_node(
                TextNode(block.replace("```", "").replace("\n", "", 1), TextType.CODE))
            pre_block = ParentNode(tag="pre", children=[code_block])
            return LeafNode(tag=f"code", value=pre_block)
        case BlockType.QUOTE:
            children = handle_backquote(block)
            return ParentNode(tag="blockquote", children=children)
        case BlockType.UN_LIST:
            children = handle_unordered_list(block)
            return ParentNode(tag="ul", children=children)
        case BlockType.OR_LIST:
            children = handle_ordered_list(block)
            return ParentNode(tag="ol", children=children)
        case _:
            children = text_to_children(block)
            return ParentNode(tag="p", children=children)


def text_to_children(text):
    children_text = text_to_textnodes(text)
    children = []
    for child in children_text:
        tag = text_to_html_node(child)
        children.append(tag)
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_tags = []
    for block in blocks:
        block_type = get_block_type(block)
        html_tags.append(handle_text_to_html(block_type, block))
    return ParentNode(tag="div", children=html_tags)


def extract_title(markdown):
    if "#" in markdown:
        text = re.search("(?<=(#{1}) )\w*", markdown)
        return text.group().strip()
    else:
        raise Exception("ERROR: # expected in markdown")


def generate_page(from_path, template_path, dest_path, base_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as content_file:
        content = content_file.read()
        with open(template_path) as template_file:
            html = markdown_to_html_node(content).to_html()
            title = extract_title(content)
            template_file_content = template_file.read()
            template_file_content = template_file_content.replace(
                "{{ Title }}", title)
            template_file_content = template_file_content.replace(
                "{{ Content }}", html)
            template_file_content = template_file_content.replace(
                'href="/', f'href="{base_path}')
            template_file_content = template_file_content.replace(
                'src="/', f'src="{base_path}')
            with open(dest_path, "w") as page:
                page.write(template_file_content)


def remove_dir(dir=PUBLIC_DIRECTORY):
    try:
        directory = Path(dir)
        for item in directory.iterdir():
            if item.is_dir():
                remove_dir(item)
            else:
                item.unlink()
        directory.rmdir()
    except Exception as error:
        print(f"Error: {error}")


def copy_static_files_to_static():
    source_dir = os.path.abspath(STATIC_DIRECTORY)
    destination_dir = os.path.abspath(PUBLIC_DIRECTORY)

    for root, dirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        dest_path = os.path.join(destination_dir, rel_path)

        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            print(f"Created directory: '{dest_path}'")

        for file_name in files:
            src_file_path = os.path.join(root, file_name)
            dest_file_path = os.path.join(dest_path, file_name)

            try:
                with open(src_file_path, 'rb') as fsrc:
                    with open(dest_file_path, 'wb') as fdst:
                        fdst.write(fsrc.read())
                print(f"Copied file: '{file_name}' to '{dest_path}'")
            except Exception as e:
                print(f"Error copying file '{src_file_path}': {e}")


def generate_pages_recursive(base_path):
    source_dir = os.path.abspath(CONTENT_DIRECTORY)
    destination_dir = os.path.abspath(PUBLIC_DIRECTORY)
    for root, dirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        dest_path = os.path.join(destination_dir, rel_path)

        for file_name in files:
            if file_name.endswith(".md"):
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                src_file_path = os.path.join(root, file_name)
                dest_file_path = os.path.join(
                    dest_path, file_name.replace(".md", ".html"))
                generate_page(src_file_path, TEMPLATE_PATH,
                              dest_file_path, base_path)
