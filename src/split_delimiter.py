from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        # if not text node add it unchanged
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        # process text nodes
        text = old_node.text
        pieces = []

        # while we can find a delimiter pair
        while delimiter in text:
            start_index = text.find(delimiter)
            text_before = text[:start_index]

            # look for closing delimiter
            remaining_text = text[start_index + len(delimiter):]
            end_index = remaining_text.find(delimiter)

            if end_index == -1:
                # no closing delimiter found
                raise Exception(f"Missing closing delimiter: {delimiter}")
            
            # text before delimiters
            delimited_text = remaining_text[:end_index]

            # add nodes
            if text_before:
                pieces.append(TextNode(text_before, TextType.TEXT))
            pieces.append(TextNode(delimited_text, text_type))

            # update text to remaining portion
            text = remaining_text[end_index + len(delimiter):]

        # add any remaining text
        if text:
            pieces.append(TextNode(text, TextType.TEXT))

        # add processed pieces to result
        result.extend(pieces)

    return result



