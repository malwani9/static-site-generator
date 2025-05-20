from htmlnode import HTMlNode, ParentNode, LeafNode
from textnode import TextNode, text_node_to_html_node, TextType
from markdown_parser import text_to_textnodes
from enum import Enum

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        if block != "":  
           block = block.strip() 
           final_blocks.append(block)
    return final_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.count("```") == 2:
        return BlockType.CODE
    if block.startswith(">"):
       block_lines = list(filter(None, block.split("\n")))
       if block.count(">") == len(block_lines):
           return BlockType.QUOTE
    if block.startswith("- "):
       block_lines = list(filter(None, block.split("\n")))
       if block.count("- ") == len(block_lines):
           return BlockType.UNORDERED_LIST
    if block[0].isdigit() and block.startswith(". ", 1):
       block_lines = list(filter(None, block.split("\n")))
       count = 0
       for line in block_lines:
           if block[0].isdigit() and block.startswith(". ", 1):
              count += 1
           if count == len(block_lines):   
              return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children_nodes.append(html_node)
    
    return ParentNode("div", children_nodes)

def block_to_html_node(block):

    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADING:
        return heading_to_html(block)
    elif block_type == BlockType.CODE:
        return code_to_html(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html(block)
    elif block_type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)


def heading_to_html(block):
    level = block.count("#")
    text = block[level+1:]
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    children_nodes = text_to_children(text)
    return ParentNode(f"h{level}", children_nodes)

def quote_to_html(block):
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        if not line.startswith(">"):
           raise ValueError("invalid quote block")
        quote_lines.append(line.lstrip(">").strip())
    content = " ".join(quote_lines)
    children_nodes = text_to_children(content)
    return ParentNode("blockquote", children_nodes)


def code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [child])
    return ParentNode("pre", [code_node])


def ordered_list_to_html(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line[3:]
        children_nodes = text_to_children(text)
        li_nodes.append(ParentNode("li", children_nodes))
    return ParentNode("ol", li_nodes)

def unordered_list_to_html(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line[2:]
        children_nodes = text_to_children(text)
        li_nodes.append(ParentNode("li", children_nodes))
    return ParentNode("ul", li_nodes)



def paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children_nodes  = text_to_children(paragraph)
    return ParentNode("p", children_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for text_node in text_nodes:
        child = text_node_to_html_node(text_node)
        children_nodes.append(child)
    return children_nodes