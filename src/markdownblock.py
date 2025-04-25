import re
from enum import Enum
from inlinemarkdown import *
from main import text_node_to_html_node

def markdown_to_blocks(markdown):
    block_list = []
    split_blocks = markdown.split("\n\n")
    for block in split_blocks:
        strip_block = block.strip()
        if strip_block != "":
            lines = strip_block.split("\n")
            processed_lines = [line.strip() for line in lines]
            processed_block = "\n".join(processed_lines)
            block_list.append(processed_block)

    return block_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    # check for heading
    if block.startswith("#"):
        if re.match(r'^#{1,6} ', block):
            return BlockType.HEADING
    
    # check for code
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # check for quote
    all_quotes = True
    for line in lines:
        if not line.startswith(">"):
            all_quotes = False
            break
    if all_quotes and lines:
        return BlockType.QUOTE
        
    # check for unordered list
    all_unordered = True
    for line in lines:
        if not line.startswith("- "):
            all_unordered = False
            break
    if all_unordered and lines:
        return BlockType.UNORDERED_LIST
        
    # check for ordered list
    all_ordered = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            all_ordered = False
            break
    if all_ordered and lines:
        return BlockType.ORDERED_LIST

    # if none of the above it's a paragraph
    return BlockType.PARAGRAPH
    






    


