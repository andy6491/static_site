import re
from htmlnode import HTMLNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case (TextType.TEXT):
            return HTMLNode(None, text_node.text)
        case (TextType.BOLD):
            return HTMLNode("b", text_node.text)
        case (TextType.ITALIC):
            return HTMLNode("i", text_node.text)
        case (TextType.CODE):
            return HTMLNode("code", text_node.text)
        case (TextType.LINK):
            return HTMLNode("a", text_node.text, None, {"href": text_node.url})
        case (TextType.IMAGE):
            return HTMLNode("img", "", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # if not text node add it unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # process text nodes
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invlaid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
        
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # process text nodes only
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # extract images
        images = extract_markdown_images(old_node.text)

        if not images:
            new_nodes.append(old_node)
            continue
        
        # process images
        current_text = old_node.text
        current_nodes = []

        for alt_text, url in images:
            # split around image markdown
            image_markdown = f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)

            # add text before image if not empty
            if parts[0]:
                current_nodes.append(TextNode(parts[0], TextType.TEXT))

            # add image node
            current_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # update current_text to remaining text
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        # add any remaining text
        if current_text:
            current_nodes.append(TextNode(current_text, TextType.TEXT))

        new_nodes.extend(current_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # extract links
        links = extract_markdown_links(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        current_nodes = []

        for anchor_text, url in links:
            link_markdown = f"[{anchor_text}]({url})"
            parts = current_text.split(link_markdown, 1)

            # add text
            if parts[0]:
                current_nodes.append(TextNode(parts[0], TextType.TEXT))

            # add link node
            current_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            # update current_text to remaining text
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

            # add remaining text
        if current_text:
            current_nodes.append(TextNode(current_text, TextType.TEXT))

        new_nodes.extend(current_nodes)
    return new_nodes 

def text_to_textnodes(text):
    # special case for empty string
    if text == "":
        return [TextNode("", TextType.TEXT)]
    
    nodes = [TextNode(text, TextType.TEXT)]
    # process images
    nodes = split_nodes_image(nodes)
    # process links
    nodes = split_nodes_link(nodes)

    # process other delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes



        
def extract_markdown_images(input_text):
    # if imput is string
    if isinstance(input_text, str):
        matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", input_text)
        return matches
    
    # if input is list of TextNodes
    result = []
    for text_node in input_text:
        if text_node.text_type != TextType.TEXT:
            result.append(text_node)
            continue

        text = text_node.text
        matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

        # split text by image markdown syntax and create new nodes
        curr_idx = 0
        for alt_text, url in matches:
            image_md = f"![{alt_text}]({url})"
            start_idx = text.find(image_md, curr_idx)

            # add text before the image as a TEXT node
            if start_idx > curr_idx:
                result.append(TextNode(text[curr_idx:start_idx], TextType.TEXT))

            # add image as an IMAGE node
            result.append(TextNode(alt_text, TextType.IMAGE, url))

            # update current index to after the image markdown
            curr_idx = start_idx + len(image_md)

        # add any remaining text
        if curr_idx < len(text):
            result.append(TextNode(text[curr_idx:], TextType.TEXT)) 

    return result

def extract_markdown_links(input_data):
    # if input is a string
    if isinstance(input_data, str):
        matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", input_data)
        return matches

    # if input is a list ofTextNodes
    result = []
    for text_node in input_data:
        if text_node.text_type != TextType.TEXT:
            result.append(text_node)
            continue
        text = text_node.text
        matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

        if not matches:
            result.append(text_node)
            continue
        # process matches abd build new nodes
        curr_idx = 0
        for link_text, url in matches:
            link_md = f"[{link_text}]({url})"
            start_idx = text.find(link_md, curr_idx)

            # add text befor link as a Text node
            if start_idx > curr_idx:
                result.append(TextNode(text[curr_idx:start_idx], TextType.TEXT))

            # add link as a LINK node
            result.append(TextNode(link_text, TextType.LINK, url))

            # update current index to after the link markdown
            curr_idx = start_idx + len(link_md)
        
        # add any remaining text
        if curr_idx < len(text):
            result.append(TextNode(text[curr_idx:], TextType.TEXT))
    return result