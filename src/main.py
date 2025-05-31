from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode
from markdownblock import markdown_to_html_node
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
        if line.startswith("# "):
            title = line[2:]
            strip_title = title.strip()
            return strip_title
    raise Exception("No title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_read = f.read()
    with open(template_path, "r") as f:
        template_read = f.read()
    markdown_conversion = markdown_to_html_node(from_read).to_html()
    title = extract_title(from_read)
    replace_title = template_read.replace("{{ Title }}", title)
    replace_content = replace_title.replace("{{ Content }}", markdown_conversion)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        dest_write = f.write(replace_content)

def copy_public(static, public):
    if os.path.exists(public):
        shutil.rmtree(public)
        if os.path.exists(static):
            shutil.copytree(static, public)


  



def main():
    node = TextNode("this is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    copy_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")




main()
