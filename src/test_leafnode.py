import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        leafnode = LeafNode('a', 'Google', {'href': 'http://www.google.com', 'target' : '_blank'})
        self.assertEqual(leafnode.to_html(), f'<a href="http://www.google.com" target="_blank">Google</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_tag(self):
        leafnode = LeafNode(tag=None, value='Hello World', props=None)
        self.assertEqual(leafnode.to_html(), 'Hello World')

    def test_value(self):
        leafnode = LeafNode('a', value=None, props=None)
        self.assertRaises(ValueError, leafnode.to_html)
    