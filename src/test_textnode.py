import unittest 
from .textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode('This is text node', TextType.TEXT)
        node2 = TextNode('This is text node', TextType.TEXT)

        self.assertEqual(node1, node2)
    def test_neq(self):
        node1 = TextNode('This is link node', TextType.LINK, url='https://example.com')
        node2 = TextNode('This is image node', TextType.IMAGE, url='https://example.com/image.png')

        self.assertNotEqual(node1, node2)
    
    def test_text_node_to_html_node_with_plain_text(self):
        textnode = TextNode('This is a text node', TextType.TEXT)
        leafnode = text_node_to_html_node(text_node=textnode)
        self.assertEqual(leafnode.to_html(), 'This is a text node')
        self.assertEqual(leafnode.value, 'This is a text node')
        self.assertEqual(leafnode.tag, None)

    def test_text_node_to_html_node_with_img_tag(self):
        textnode = TextNode('Demo Image', TextType.IMAGE, 'http://www.google.com/public/some-image.png')
        leafnode = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.to_html(), '<img src="http://www.google.com/public/some-image.png" alt="Demo Image" />')

        

if __name__ == "__main__":
    unittest.main()