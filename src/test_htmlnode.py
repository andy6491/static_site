import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
        assert node.props_to_html() == ' href="https://example.com" target="_blank"'

    def test_defaults(self):
        node = HTMLNode()
        assert node.tag is None
        assert node.value is None
        assert node.children is None
        assert node.props is None

    def test_invalid_props(self):
        node = HTMLNode(tag="div", props=None)
        assert node.props_to_html() == "" 
