import unittest

from helpers import extract_markdown_images, extract_markdown_links,split_nodes_link,split_nodes_image, text_to_textnodes
from textnode import TextNode, TextType

class TestHelpers(unittest.TestCase):
    def test_extra_markdown_images(self):
        raw_text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(raw_text)
        self.assertListEqual([('image','https://i.imgur.com/zjjcJKZ.png')], matches)

    def test_extract_markdown_links(self):
        raw_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_answer =  [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        matches = extract_markdown_links(raw_text)
        self.assertListEqual(expected_answer, matches)


    def test_split_nodes_link(self):
        raw_text =  str("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        node = TextNode(text=raw_text, text_type=TextType.TEXT)
        new_nodes  = split_nodes_link([node])
        expected_result = [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('to boot dev', TextType.LINK, "https://www.boot.dev"),
            TextNode(' and ', TextType.TEXT),
            TextNode('to youtube', TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(len(expected_result), len(new_nodes))
        for i in range(len(new_nodes)):
            item = new_nodes[i]
            expected_item = expected_result[i]
            self.assertEqual(item.text, expected_item.text)
            self.assertEqual(item.text_type, expected_item.text_type)
            if item.text_type == TextType.LINK:
                self.assertEqual(item.url, expected_item.url)

    def test_split_nodes_image(self):
        raw_text =  str("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image2](https://i.imgur.com/zjjcJKZ.png)")
        node = TextNode(text=raw_text, text_type=TextType.TEXT)
        new_nodes  = split_nodes_image([node])
        expected_result = [
            TextNode('This is text with an ', TextType.TEXT),
            TextNode('image', TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(' and another ', TextType.TEXT),
            TextNode('image2', TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(len(expected_result), len(new_nodes))
        for i in range(len(new_nodes)):
            item = new_nodes[i]
            expected_item = expected_result[i]
            self.assertEqual(item.text, expected_item.text)
            self.assertEqual(item.text_type, expected_item.text_type)
            if item.text_type == TextType.IMAGE:
                self.assertEqual(item.url, expected_item.url)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        self.maxDiff = None
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual_output = text_to_textnodes(text)
  

        self.assertListEqual(expected_output, actual_output)





            


        

        

    