import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_no_title(self):
        md = """
    This text with no title
    """
        self.assertRaises(Exception, extract_title, md)

    def test_title(self):
        md = """
    # Text Title
    """
        self.assertEqual(extract_title(md), "Text Title")

    def test_extra_spacing(self):
        md = """
    #  Extra space title
    """
        self.assertEqual(extract_title(md), "Extra space title")

    def test_spacing_before_hash(self):
        md = """
     # Space before hash
    """
        self.assertRaises(Exception, extract_title, md)
    

if __name__ == "__main__":
    unittest.main()