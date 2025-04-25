import unittest
from htmlnode import HTMlNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.node = HTMlNode(tag="a", value="this is a link", props={"href":"https://nodistenation.com", "target": "_blank"})

    def test_to_HTML_props(self):
        result = self.node.to_HTML_props()
        self.assertEqual(result, " href=\"https://nodistenation.com\" target=\"_blank\"")

    def test_to_HTML_props_2(self):
        node = HTMlNode(tag="a", value="this is a link", props= None)
        result = node.to_HTML_props()
        self.assertEqual(result, "")
    
    def test_to_html_raise_error(self):
        self.assertRaises(NotImplementedError, self.node.to_html)

    def test_repr(self):
        self.assertEqual(repr(self.node), "HTMLNode: a, this is a link, children: None, {'href': 'https://nodistenation.com', 'target': '_blank'}")

    def test_repr_2(self):
        self.assertNotEqual(repr(self.node), "HTMLNode: a, this is a link, children: None, {'href': 'https://nodistenation.com'}")


    def test_node_values(self):
        node = HTMlNode("p", "Hello World")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

if __name__ == "__main__":
    unittest.main()