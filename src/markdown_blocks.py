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
        return paragraph_to_html_node(block)


def heading_to_html(block):
    level = block.count("#")
    text = block[level+1:]
    children_nodes = text_to_children(text)
    return ParentNode(f"h{level}", children_nodes)

def quote_to_html(block):
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        text = line[2:]
        line_children = text_to_children(text)
        children_nodes.extend(line_children)
    return ParentNode("blockquote", children_nodes)


def code_to_html(block):
    text = block.replace("```", "")
    text_node = TextNode(text, TextType.CODE, None)
    return text_node_to_html_node(text_node)


def ordered_list_to_html(block):
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        text = line[2:]
        line_children = text_to_children(text)
        children_nodes.extend(line_children)
    return line_children

def unordered_list_to_html(block):
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        text = line[2:]
        line_children = text_to_children(text)
        children_nodes.extend(line_children)
    return line_children



def paragraph_to_html_node(block):
    children_nodes  = text_to_children(block)
    return ParentNode("p", children_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for text_node in text_nodes:
        child = text_node_to_html_node(text_node)
        children_nodes.append(child)
    return children_nodes