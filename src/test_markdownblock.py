import unittest
from markdownblock import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = """"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_multiple_consecutive_newline(self):
        md = """
    This is _text_

    with multiple consecutive newlines
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is _text_",
                "with multiple consecutive newlines"
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        md = """ This is text with leading and trailing whitespace """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is text with leading and trailing whitespace"
            ],
        )

    def test_single_block(self):
        md = """This is text with a single block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is text with a single block"
            ]
        )

    def test_internal_newlines(self):
        md = """This is text with
            internal newlines"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is text with\ninternal newlines"

            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "this is a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_headings(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### hrading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### heading 6"), BlockType.HEADING)

        # test invalid headings
        self.assertEqual(block_to_block_type("########### too many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#no space"), BlockType.PARAGRAPH)

    def test_code(self):
        block = "```this is a code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> this is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line 1\nline 2"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- unordered list"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item 1\n2. item 2\n3. item 3"), BlockType.ORDERED_LIST)
        # invalid ordered list
        self.assertEqual(block_to_block_type("1.no space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. item 2\n3. item 3"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. item 1\n3. item 3"), BlockType.PARAGRAPH)

    def test_mixed_content(self):
        self.assertEqual(
            block_to_block_type("this is a paragraph\n# with a heading"),
            BlockType.PARAGRAPH
        )

    def test_empty(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
    
if __name__ == "__main__":
    unittest.main()
