import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    # case 1 : <div>  <p>  Hello world  </p>  </div> -> asset equal
    def test_to_html_with_children(self):
        leafnode = LeafNode('p', 'Hello world')
        parentnode = ParentNode('div', [leafnode])
        expected_output = "<div><p>Hello world</p></div>"
        self.assertEqual(parentnode.to_html(), expected_output)

    # case 2 : <p>  <a href="http://www.google.com"> Google </a> </p>  
    def test_to_html_with_props(self):
        leafnode = LeafNode('a', 'Google', {'href': 'http://www.google.com'})
        parentnode = ParentNode('p', [leafnode])
        exp_str = '<p><a href="http://www.google.com">Google</a></p>'
        self.assertEqual(parentnode.to_html(), exp_str )

    # case 3: <div> <p> <b> Hello </b> <i> World </i>  </p> </div>
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
