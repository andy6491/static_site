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
        f.write(replace_content)

def copy_public(static, public):
    if os.path.exists(public):
        shutil.rmtree(public)
        if os.path.exists(static):
            shutil.copytree(static, public)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)
    for item in items:
        source_path = os.path.join(dir_path_content, item)
        content_relative_path = source_path[len(dir_path_content):]
        if content_relative_path.startswith("/"):
            content_relative_path = content_relative_path[1:]
        html_relative_path = content_relative_path.replace(".md", ".html")
        dest_path = os.path.join(dest_dir_path, html_relative_path)
        if os.path.isfile(source_path) and source_path.endswith(".md"):
            create_dir = os.path.dirname(dest_path)
            os.makedirs(create_dir, exist_ok=True)
            with open(source_path, "r") as f:
                source_read = f.read()
            with open(template_path, "r") as f:
                template_read = f.read()
            markdown_conversion = markdown_to_html_node(source_read).to_html()
            replace_content = template_read.replace("{{ Content }}", markdown_conversion)
            with open(dest_path, "w") as f:
                f.write(replace_content)
        elif os.path.isdir(source_path):
            os.makedirs(os.path.join(dest_dir_path, item), exist_ok=True)
            generate_pages_recursive(source_path, template_path, os.path.join(dest_dir_path, item))



def main():
    node = TextNode("this is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    copy_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")




main()
