import unittest
from content_generator import extract_title

class TestContentGenerator(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        header = extract_title(markdown)
        self.assertEqual(header, "Tolkien Fan Club")