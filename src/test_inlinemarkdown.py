import unittest
from textnode import TextNode, TextType
from inlinemarkdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDlimiter(unittest.TestCase):
    def test_code(self):
        node  = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_bold_delimiter(self):
        # test bold delimiter
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_italic_delimiter(self):
        # test italic delimiter
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_code_delimiter(self):
        # test code delimiter
        node  = TextNode("This is text with `code` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_linkf(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) in it"
        )
        self.assertEqual([("link", "https://example.com")], matches)

class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # test two images
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),

            ],
            new_nodes,
        )

    def test_with_no_images(self):
        # test no images 
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual([TextNode("This is text with no images", TextType.TEXT),], new_nodes)

    def test_with_image_at_beginning(self):
        # test image at beginning
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) this is text with image at beginning",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" this is text with image at beginning", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_with_image_at_end(self):
        # test with image at end
        node = TextNode(
            "this is text with image at end ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            [
                TextNode("this is text with image at end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_with_empty_alt_text(self):
        # test with empty alt text
        node = TextNode(
            "this is text with empty alt text ![](https://i.imgur.com/zjjcJKZ.png) in it",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            [
                TextNode("this is text with empty alt text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes
        )

    def test_with_no_url(self):
        # test with no url
        node = TextNode("this is text with empty url ![image]()", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            [
                TextNode("this is text with empty url ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, ""),
            ],
            new_nodes
        )

class TestSplitLinks(unittest.TestCase):
    def test_with_link(self):
        # test with link
        node = TextNode(
            "this is text with a [link](https://example.com) in it",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("this is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes
        )

    def test_with_link_at_beginning(self):
        # test with link at beginning
        node = TextNode(
            "[link](https://example.com) this is text with link at beginning",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" this is text with link at beginning", TextType.TEXT),
            ],
            new_nodes
        )
        
   
    def test_with_multiple_links(self):
        # test with multiple links
        node = TextNode(
            "this is text with multiple links [link](https://example.com) in it [link2](https://example2.com)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("this is text with multiple links ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in it ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example2.com"),
            ],
            new_nodes
        )

    def test_with_empty_link_text(self):
        # test with empty link text
        node = TextNode(
            "this is text with empty link text [](https://example.com) in it", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("this is text with empty link text ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes
        )

    def test_with_empty_url(self):
        # test with empty url
        node = TextNode(
            "this is text with an empty url [link]() in it", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("this is text with an empty url ", TextType.TEXT),
                TextNode("link", TextType.LINK, ""),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_with_empty_text(self):
        nodes = text_to_textnodes("")

        self.assertEqual([TextNode("", TextType.TEXT)], nodes)

    def test_different_formatting_combos(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )

        self.assertEqual(
            [
                TextNode("This is ",TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_with_consecutive_delimiters(self):
        nodes = text_to_textnodes(
            "This is text with **consecutive** ![delimiters](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        self.assertEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("consecutive", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("delimiters", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            nodes
        )


if __name__ == "__main__":
    unittest.main()

