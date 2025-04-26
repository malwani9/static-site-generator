import unittest
from htmlnode import HTMlNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
         node = LeafNode("p", "Hello, world!", None)
         self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
         node = LeafNode("a", "click here", {"href": "https://google.com", "target": "_blank"})
         self.assertEqual(node.to_html(), "<a href=\"https://google.com\" target=\"_blank\">click here</a>")
    
    def test_leaf_to_html_h1(self):
         node = LeafNode("h1", "Header", {"class": "header"})
         self.assertEqual(node.to_html(), "<h1 class=\"header\">Header</h1>") 
    
    def test_leaf_None(self):
        node = LeafNode(None, "Hello World")
        self.assertEqual(node.to_html(), "Hello World")

    def test_repr_leafNode(self):
        node = LeafNode("a", "click here", {"href": "https://google.com", "target": "_blank"})
        self.assertEqual(repr(node), "LeafNode: a, click here, {'href': 'https://google.com', 'target': '_blank'}")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_2(self):
        grandchild_node = LeafNode("b", "grandchild", {"class": "bold"})
        child_node = ParentNode("span", [grandchild_node],{"class": "span-text"})
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"container\"><span class=\"span-text\"><b class=\"bold\">grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_3(self):
        grandchild_node2 = LeafNode("i", "grandchild2", {"class": "italic"})
        grandchild_node = LeafNode("b", "grandchild", {"class": "bold"})
        child_node = ParentNode("span", [grandchild_node, grandchild_node2],{"class": "span-text"})
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"container\"><span class=\"span-text\"><b class=\"bold\">grandchild</b><i class=\"italic\">grandchild2</i></span></div>",
        )

    def test_to_html_with_grandchildren_4(self):
        anchor_child = grandchild_node = LeafNode("b", "click here", {"class": "bold"})
        grandchild_node2 = LeafNode("i", "grandchild2", {"class": "italic"})
        grandchild_node = LeafNode("b", "grandchild", {"class": "bold"})
        child_node = ParentNode("span", [grandchild_node, grandchild_node2],{"class": "span-text"})
        child_node2 = ParentNode("a", [anchor_child],{"href": "https://google.com", "target": "_blanck", "class": "link"})
        parent_node = ParentNode("div", [child_node2, child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"container\"><a href=\"https://google.com\" target=\"_blanck\" class=\"link\"><b class=\"bold\">click here</b></a><span class=\"span-text\"><b class=\"bold\">grandchild</b><i class=\"italic\">grandchild2</i></span></div>",
        )

    def test_to_html_with_grandchildren_5(self):
        grandchild_child_node= LeafNode("i", "click here", {"class": "italic"})
        grandchild_node = ParentNode("span", [grandchild_child_node], {"class": "span"})
        child_node_2 = ParentNode("a", [grandchild_node],{"href": "https://google.com", "target": "_blanck", "class": "link"})
        child_node = LeafNode("q", "It is not that we have a short time to live, but that we waste much of it.", {"class": "quote"})
        parent_node = ParentNode("div", [child_node, child_node_2], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"container\"><q class=\"quote\">It is not that we have a short time to live, but that we waste much of it.</q><a href=\"https://google.com\" target=\"_blanck\" class=\"link\"><span class=\"span\"><i class=\"italic\">click here</i></span></a></div>",
        )
        
    def test_to_html_with_notag_children(self):
        child_node_3 = LeafNode("a", "more here",{"href": "https://google.com", "target": "_blanck", "class": "link"})
        child_node_2 = LeafNode("a", "Seneca Quote",{"href": "https://google.com", "target": "_blanck", "class": "link"})
        child_node = LeafNode(None, "It is not that we have a short time to live, but that we waste much of it.")
        parent_node = ParentNode("div", [child_node, child_node_2, child_node_3], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"container\">It is not that we have a short time to live, but that we waste much of it.<a href=\"https://google.com\" target=\"_blanck\" class=\"link\">Seneca Quote</a><a href=\"https://google.com\" target=\"_blanck\" class=\"link\">more here</a></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [], {"class": "container"})
        self.assertRaises(
            ValueError,
            parent_node.to_html,
        )
    

if __name__ == "__main__":
    unittest.main()