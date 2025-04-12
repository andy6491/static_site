import re
from textnode import TextNode, TextType

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


        

        
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches