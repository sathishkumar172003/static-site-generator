from enum import Enum
from textwrap import dedent
import os 
import re

from .helpers import text_to_textnodes
from .htmlnode import HTMLNode
from .textnode import text_node_to_html_node

def markdown_to_blocks(md: str)->list[str]:
    # It takes a markdown string and returns a list of blocks
    # A block is a string that is separated by two new lines
    blocks = md.split("\n\n")
    result = [dedent(block).strip() for block in blocks if block.strip() != ""]
    return result

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(single_line_of_md: str):
    txt = single_line_of_md
    if not txt:
        return BlockType.PARAGRAPH
    if re.match(r"^#{1,6}\s", txt):
        return BlockType.HEADING
    elif txt.startswith("```\n") and txt.endswith("\n```"):
        return BlockType.CODE
    elif txt.startswith(">"):
        lines = txt.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH 
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in txt.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d+\. ", line) for line in txt.split("\n")):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(text):
    # text_to_textnodes
    # text_node_to_html_node

    textnodes = text_to_textnodes(text)
    children = []
    for textnode in textnodes:
        leafnode = text_node_to_html_node(textnode)
        children.append(leafnode)
    return children

def markdown_to_htmlnode(md: str):
    blocks = markdown_to_blocks(md)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = None 
        content = block
        match block_type:
            case BlockType.PARAGRAPH:
                tag = 'p'
            case BlockType.HEADING:
                heading_match = re.match(r"^(#{1,6})\s+(.*)$", block, re.DOTALL)
                tag = f"h{len(heading_match.group(1))}"
                content = heading_match.group(2)
            case BlockType.CODE:
                tag = 'pre'
            case BlockType.QUOTE:
                tag = 'blockquote'
            case BlockType.UNORDERED_LIST:
                tag = 'ul'
            case BlockType.ORDERED_LIST:
                tag = 'ol'
            
        block_node  = HTMLNode(tag, '', [], {})
        if block_type == BlockType.CODE:
            code = block[4:-4] + "\n"
            block_node.children = [HTMLNode("code", code, [], {})]
        elif block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            marker = r"^- " if block_type == BlockType.UNORDERED_LIST else r"^\d+\. "
            block_node.children = [
                HTMLNode("li", "", text_to_children(re.sub(marker, "", line)), {})
                for line in block.split("\n")
            ]
        elif block_type == BlockType.QUOTE:
            quote_lines = (line[1:].strip() for line in block.split("\n"))
            content = " ".join(line for line in quote_lines if line)
            block_node.children = text_to_children(content)
        else:
            block_node.children = text_to_children(content)
        block_nodes.append(block_node)
        

    root_node = HTMLNode('div', '', block_nodes, {})
    return root_node


def extract_title(markdown: str) -> str:
    # It takes a markdown string and returns the title of the markdown
    # The title is the first line that starts with a # and is followed by a space
    lines = markdown.split("\n")
    try:
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip()
    except Exception as e:
        raise Exception("No title found in markdown")

def generate_page(from_path: str, template_path, dest_path, basepath="/"):
    print('Generating page from {} to {}'.format(from_path, dest_path))
    if not os.path.exists(from_path):
        raise Exception("Source file does not exist: {}".format(from_path))
    if not os.path.exists(template_path):
        raise Exception("Template file does not exist: {}".format(template_path))
    with open(from_path, 'r') as f:
        print('Reading markdown from {}'.format(from_path))
        markdown = f.read()
    with open(template_path, 'r') as f:
        print('Reading template from {}'.format(template_path))
        template = f.read()
    html_node = markdown_to_htmlnode(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Content }}", html)
    html = html.replace("{{ Title }}", title)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, 'w') as f:
        print('Writing HTML to {}'.format(dest_path))
        f.write(html)
    

    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    # crawl every entry in content dir
    # For each markdown file found, generate new .html file using the same template.html file
    # the generated pages should be written to the public directory in the same directory structure
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, relative_path[:-3] + ".html")
                generate_page(from_path, template_path, dest_path, basepath)
    