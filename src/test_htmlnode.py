import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            props={"href": "https://example.com",
                   "target": "_blank"})
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

    def test_values(self):
        node = HTMLNode("div", "I wish I could read",)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
            )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


    # leafnode tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_leaf_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # parentnode tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_basic_parent_node(self):
        child = LeafNode("span", "Hello")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>Hello</span></div>")

    def test_multiple_children(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode("i", "Italic")
        parent = ParentNode("p", [child1, child2])
        self.assertEqual(parent.to_html(), "<p><b>Bold</b><i>Italic</i></p>")

    # error handling
    def test_tag_missing(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "test")]).to_html()

    def test_children_missing(self):
        with self.assertRaises(ValueError):
            node = HTMLNode("div", None, [])
            node.to_html()
        
    # property tests
    def test_with_single_property(self):
        node = ParentNode("div", [LeafNode("span", "text")], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span>text</span></div>')
    
    def test_with_multiple_properties(self):
        node = ParentNode("div", [LeafNode("span", "text")], {"class": "container", "id": "main"})
        result = node.to_html()
        self.assertTrue(
            result == '<div class="container" id="main"><span>text</span></div>' or
            result == '<div> id="main" class="container"><span>text</span></div>'
        )

    def test_nested_parents(self):
        innermost = LeafNode("span", "text")
        inner = ParentNode("div", [innermost])
        outer = ParentNode("section", [inner])
        self.assertEqual(outer.to_html(), "<section><div><span>text</span></div></section>")

    def test_complex_nesting(self):
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode("i", "Italic")
        inner1 = ParentNode("p", [leaf1, leaf2])
        leaf3 = LeafNode("a", "Link", {"href": "#"})
        inner2 = ParentNode("div", [leaf3])
        root = ParentNode("article", [inner1, inner2])
        self.assertEqual(
            root.to_html(),
            '<article><p><b>Bold</b><i>Italic</i></p><div><a href="#">Link</a></div></article>'
        )

    def test_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_mixed_leaf_and_parent_children(self):
        leaf1 = LeafNode("span", "text1")
        inner = ParentNode("div", [LeafNode("span", "nested")])
        leaf2 = LeafNode("span", "text2")
        parent = ParentNode("section", [leaf1, inner, leaf2])
        self.assertEqual(
            parent.to_html(),
            "<section><span>text1</span><div><span>nested</span></div><span>text2</span></section>"
        )
    def test_with_plain_text_nodes(self):
        bold = LeafNode("b", "Bold")
        text1 = LeafNode(None, "Plain text 1")
        italic = LeafNode("i", "Italic")
        text2 = LeafNode(None, "Plain text 2")
        parent = ParentNode("p", [bold, text1, italic, text2])
        self.assertEqual(
            parent.to_html(),
            "<p><b>Bold</b>Plain text 1<i>Italic</i>Plain text 2</p>"
        )


if __name__ == "__main__":
    unittest.main()




    
