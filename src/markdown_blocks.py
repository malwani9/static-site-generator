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
    if block[0].isdigit() and block.startswith("# ", 1):
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