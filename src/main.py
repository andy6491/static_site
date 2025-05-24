from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode

print("hello world")

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

def main():
    node = TextNode("this is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)



main()
