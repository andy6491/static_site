import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("First text", TextType.BOLD)
        node2 = TextNode("different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("text", TextType.BOLD, "https://example.com")
        node2 = TextNode("text", TextType.BOLD, "https://different.com")
        self.assertNotEqual(node, node2)
    
    def test_one_url_none(self):
        node = TextNode("text", TextType.LINK, "https://example.com")
        node2 = TextNode("text", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_same_url(self):
        node = TextNode("text", TextType.ITALIC, "https://example.com")
        node2 = TextNode("text", TextType.ITALIC, "https://example.com")
        self.assertEqual(node, node2)



if __name__ == "__main__":
    unittest.main()