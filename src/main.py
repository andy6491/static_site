from textnode import TextNode, TextType
print("hello world")

def main():
    node = TextNode("this is some anchor text", TextType.LINKS, "https://www.boot.dev")
    print(node)



main()
