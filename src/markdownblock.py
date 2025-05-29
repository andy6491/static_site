import re
from enum import Enum
from inlinemarkdown import *
from htmlnode import HTMLNode, ParentNode, LeafNode

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

def markdown_to_html_node(markdown):
    parent_div = HTMLNode("div", None, [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            paragraph_content = " ".join(block.strip().split("\n"))

            block_node = HTMLNode("p", None, [])

            # process text content of paragraph
            children = text_to_children(paragraph_content)
            if not children or len(children) == 0:
                block_node.value = paragraph_content
            else:
                block_node.children = children

            # add to parent div
            parent_div.children.append(block_node)

        elif block_type == BlockType.HEADING:
            # determine heading level (h1 - h3)
            level = 0 # default to level 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break

            # process heading text (without the # characters)
            heading_content = block[level:].strip()

            # create block node
            block_node = HTMLNode(f"h{level}", None, [])

            # check if heading_conyent is empty
            if not heading_content:
                # if heading is empty, use empty string
                block_node.value = ""
            else:
                # make sure getting children for heading
                children = text_to_children(heading_content)
        
                if not children or len(children) == 0:
                    block_node.value = heading_content
                else:
                    block_node.children = children

            # add to parent div
            parent_div.children.append(block_node)

        elif block_type == BlockType.CODE:
            pre_node = HTMLNode("pre", None, [])
            code_node = HTMLNode("code", None , [])

            # remove leading and trailing ``` and language identifier
            code_content = extract_code_block_content(block)

            # text node with code content
            code_text_node = TextNode(code_content, TextType.TEXT)

            # convert to HTML node and add to the structure
            code_html_node =text_node_to_html_node(code_text_node)
            code_node.children.append(code_html_node)
            pre_node.children.append(code_node)

            # add pre node (containing code node) to parent div
            parent_div.children.append(pre_node)

        elif block_type == BlockType.QUOTE:
            # remove '>' prefix from each line and join with spaces
            quote_lines = block.strip().split("\n")
            # remove '<' character from beginning of each line
            quote_lines = [line[1:].strip() if line.startswith(">") else line.strip() for line in quote_lines]
            # join lines with spaces
            quote_content = " ".join(quote_lines)

            # create blockquote node
            block_node = HTMLNode("blockquote", None, [])

            # process quote text
            children = text_to_children(quote_content)

            if not children or len(children) == 0:
                block_node.value = quote_content
            else:
                block_node.children = children

            # add to parent div
            parent_div.children.append(block_node)

        elif block_type == BlockType.UNORDERED_LIST:
            ul_node = HTMLNode("ul", None, [])
            # split block into list items
            lines = block.split("\n")
            # skip empty lines
            for line in lines:
                if not line.strip():
                    continue
                # remove list marker
                item_content = line.strip()
                if item_content.startswith("- "):
                    item_content = item_content[2:]
                elif item_content.startswith("* "):
                    item_content = item_content[2:]

                # create list item node
                li_node = HTMLNode("li", None, [])
                li_node.children = text_to_children(item_content)
                ul_node.children.append(li_node)

            parent_div.children.append(ul_node)

        elif block_type == BlockType.ORDERED_LIST:
            ol_node = HTMLNode("ol", None, [])

            # split block into list items
            lines = block.split("\n")
            for line in lines:
                # skip empty lines
                if not line.strip():
                    continue

                # remove list marker
                item_content = line.strip()
                
                # find where actual content starts
                for i, char in enumerate(item_content):
                    if i > 0 and char == '.' and item_content[:i].isdigit():
                        # found period after number
                        if i + 1 < len(item_content) and item_content[i+1] == ' ':
                            item_content = item_content[i+2:] # skip number, period
                        else:
                            item_content = item_content[i+1:] # skip number and period
                        break
                # create list item node
                li_node = HTMLNode("li", None, [])
                li_node.children = text_to_children(item_content)
                ol_node.children.append(li_node)

            parent_div.children.append(ol_node)

    return parent_div
    
        
def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = extract_markdown_images(nodes)
    nodes = extract_markdown_links(nodes)

    # process bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # process italic text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # process code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # convert TextNode to HTMLNode
    html_nodes = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    
    return html_nodes

def extract_code_block_content(block):
    # remove first line with ``` an doptional language
    lines = block.split("\n")
    # find lines with backticks
    start_index = -1
    end_index = -1
    for i, line in enumerate(lines):
        if "```" in line:
            if start_index == -1:
                start_index = i
            else:
                end_index = i
                break

    # extract content between backticks
    content_lines = lines[start_index + 1:end_index]

    # join remaining lines with newlines
    content = "\n".join(content_lines)

    # ensure trailing newline
    if not content.endswith("\n"):
        content += "\n"

    return content

    






    


