import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlnode = HTMLNode('a', 'Google', None, {'href': 'https://www.google.com'})
        htmlnode2 = HTMLNode('a', 'Google', None, {'href': 'https://www.google.com', 'target': '_blank'})
        self.assertEqual(htmlnode.props_to_html(), f' href="https://www.google.com"')
        self.assertEqual(htmlnode2.props_to_html(), f' href="https://www.google.com" target="_blank"')
    
