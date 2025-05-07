import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_parser import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links

class TestMardownParser(unittest.TestCase):
    def test_equal_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT, None)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("bolded phrase", TextType.BOLD),
    TextNode(" in the middle", TextType.TEXT),
])
    def test_equal_italic(self):
        node = TextNode("This is text with a _italic phrase_ in the middle", TextType.TEXT, None)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("italic phrase", TextType.ITALIC),
    TextNode(" in the middle", TextType.TEXT),
])
        
    def test_equal_code(self):
        node = TextNode("This is text with a `code block` in the middle", TextType.TEXT, None)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" in the middle", TextType.TEXT),
])
        
    def test_equal_code_2(self):
        node = TextNode("code block", TextType.CODE, None)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
    TextNode("code block", TextType.CODE),
])
    
        
    def test_missing_colsing_delimeter(self):
        node = TextNode("This is text with a _italic phrase in the middle", TextType.TEXT, None)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "_", TextType.ITALIC)

    
    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )
       
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_linkss(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://google.com)"
        )
        self.assertListEqual([("link", "https://google.com")], matches)

    def test_extract_markdown_linkss(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and ![third image](https://i.imgur.com/4elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/4elNhQu.png"
                ),

            ],
            new_nodes,
        )
    
    def test_split_images_3(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) ![third image](https://i.imgur.com/4elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" ", TextType.TEXT),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/4elNhQu.png"
                ),

            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://google.com) and another [second link](https://google.com/images)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://google.com/images"
                ),
            ],
            new_nodes,
        )

    def test_split_links_2(self):
        node = TextNode(
            "This is text with an [link](https://google.com) and another [second link](https://google.com/images) and [third link](https://google.com/@what)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://google.com/images"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "third link", TextType.LINK, "https://google.com/@what"
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()