from .textnode import TextNode, TextType

def main():
    text_node : TextNode = TextNode("Hello, World!", text_type=TextType.BOLD)
    print(text_node)


if __name__ == "__main__":
    main()
