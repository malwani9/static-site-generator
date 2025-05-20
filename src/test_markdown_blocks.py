import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):
      def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

      def test_markdown_to_blocks_2(self):
            md = """

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

      def test_markdown_to_blocks_3(self):
            md = """

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items

            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )


      def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
      

      def test_block_to_block_type_heading(self):
            block = """# This is heading"""
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.HEADING)
      
      def test_block_to_block_type_code(self):
            block = """```This is code blcok```"""
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.CODE)

      def test_block_to_block_type_quote(self):
            block = """> How strange and foolish is man.
> He loses his health in gaining wealth. Then to regain health he wastes his wealth. 
> He ruins his present while worrying about his future but weeps in the future by recalling his past. 
> He lives as though death shall never come to him but dies in a way as if he were never born."""
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.QUOTE)
      
      def test_block_to_block_type_unordered_list(self):
            block = """- How strange and foolish is man.
- He loses his health in gaining wealth. Then to regain health he wastes his wealth. 
- He ruins his present while worrying about his future but weeps in the future by recalling his past. 
- He lives as though death shall never come to him but dies in a way as if he were never born."""
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.UNORDERED_LIST)

      def test_block_to_block_type_ordered_list(self):
            block = """1. How strange and foolish is man.
2. He loses his health in gaining wealth. Then to regain health he wastes his wealth. 
3. He ruins his present while worrying about his future but weeps in the future by recalling his past. 
4. He lives as though death shall never come to him but dies in a way as if he were never born."""
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.ORDERED_LIST)
     
      def test_block_to_block_type_paragraph(self):
            block = """How strange and foolish is man.
He loses his health in gaining wealth. Then to regain health he wastes his wealth. 
He ruins his present while worrying about his future but weeps in the future by recalling his past. 
He lives as though death shall never come to him but dies in a way as if he were never born."""
            block_type = block_to_block_type(block)
            self.assertEqual(block_type, BlockType.PARAGRAPH)



      def test_headingblock(self):
          md = """## this is **bold** heading"""

          node = markdown_to_html_node(md)
          html = node.to_html()
          self.assertEqual(
                html,
                "<div><h2>this is <b>bold</b> heading</h2></div>",
            )
      
      def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )
          
      def test_paragraphblock(self):
          md = """This is another paragraph with _italic_ text and `code` here"""

          node = markdown_to_html_node(md)
          html = node.to_html()
          self.assertEqual(
                html,
                "<div><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            ) 
          
      def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
          
      def test_quoteblock(self):
          md = """> quote"""

          node = markdown_to_html_node(md)
          html = node.to_html()
          self.assertEqual(
                html,
                "<div><blockquote>quote</blockquote></div>",
            ) 
          
      def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

      def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

      def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )