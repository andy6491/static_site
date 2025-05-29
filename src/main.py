from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode
import os, shutil


print("hello world")

def copy_content(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    items = os.listdir(source)
    for item in items:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copying file: {source_path}")
        else:
            os.mkdir(destination_path)
            copy_content(source_path, destination_path)
            print(f"Creating directory: {destination_path}")


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line == "# ":
            return line



def main():
    node = TextNode("this is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    copy_content("static", "public")




main()
