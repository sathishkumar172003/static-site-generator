
from .textnode import TextNode, TextType
import re 

IMAGE_RE = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINKS_RE = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


# This function can handle -> Bold, Italic, Code, 
def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:

    new_nodes = []

    for old_node in old_nodes:
        # Preserve nodes that are not normal text
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # If the delimiter does not exist, preserve the node
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue

        # Split the text using the delimiter
        text_parts = old_node.text.split(delimiter)

        # An even number of parts means unmatched delimiters
        if len(text_parts) % 2 == 0:
            raise ValueError("Invalid Markdown: missing closing delimiter")

        # Alternate between normal text and formatted text
        for i, part in enumerate(text_parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
# This can handle Links 
def split_nodes_link(old_nodes: list[TextNode])->list[TextNode]:
    # It Takes a Text Node with text type and return list of text nodes:
    # for each node, i will use a regex to to split my text into chunks, and chunk at even index is my link node
    node_list = []
    
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            node_list.append(node)
        else:
            items = re.split(r"(\[.*?\]\(.*?\))",node.text)
           
            for i,a in enumerate(items):
                if a == '':
                    continue 
                if i % 2 == 0:
                    text_node = TextNode(a,TextType.TEXT)
                    node_list.append(text_node)
                else:
                    text,link = extract_markdown_links(a)[0] # the function returns a list with a tuple, where each tuple contains (text,link)
                    link_node = TextNode(text, TextType.LINK, link)
                    node_list.append(link_node)
    return node_list
# This can handle images 
def split_nodes_image(old_nodes: list[TextNode])->list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
        else:
            items = re.split(r"(!\[.*?\]\(.*?\))",node.text)
            for i,a in enumerate(items):
                if a == '':
                    continue 
                if i % 2 == 0:
                    text_node = TextNode(a,TextType.TEXT)
                    new_nodes.append(text_node)
                else:
                    alt_text,image_link = extract_markdown_images(a)[0] # the function returns a list with a tuple, where each tuple contains (alt_text,image_link)
                    image_node = TextNode(alt_text, TextType.IMAGE, image_link)
                    new_nodes.append(image_node)
    return new_nodes

def extract_markdown_images(text)->list[tuple[str]]:
    return re.findall(IMAGE_RE,text)

def extract_markdown_links(text)->list[tuple[str]]:
    return re.findall(LINKS_RE, text)


def text_to_textnodes(text: str) -> list[TextNode]:
    # text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
    txt = text.replace("\n"," ")
    nodes = [TextNode(txt, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
