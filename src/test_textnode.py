import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_all_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_all_eq_two(self):
        node = TextNode("This is a text node", TextType.LINK, "https://url.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://url.com")
        self.assertEqual(node, node2)
    
    def test_not_eq_TextType(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_text(self):
        node = TextNode("This is a node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_all_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://urI.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://url.com")
        self.assertNotEqual(node, node2)
        

if __name__ == "__main__":
    unittest.main()