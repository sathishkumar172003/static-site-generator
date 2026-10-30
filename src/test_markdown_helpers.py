import unittest
import os
import tempfile

from src.markdown_helpers import (
    BlockType,
    block_to_block_type,
    extract_title,
    generate_pages_recursive,
    markdown_to_blocks,
    markdown_to_htmlnode,
)

class TestMarkdownHelpers(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
     
        self.assertEqual(blocks, [
             "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ])

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> Quote line 1\n> Quote line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item 1\n- List item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Ordered item 1\n2. Ordered item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_markdown_to_blocks_and_to_block_type(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(block_types, [
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.UNORDERED_LIST,
        ])
        
    def test_markdown_to_htmlnode(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_blocks_are_rendered_as_html_elements(self):
        md = """# Title

## Section

> First quote line
> Second quote line

- one **bold**
- two

1. first
2. second
"""
        html = markdown_to_htmlnode(md).to_html()

        self.assertEqual(
            html,
            "<div><h1>Title</h1><h2>Section</h2>"
            "<blockquote>First quote line Second quote line</blockquote>"
            "<ul><li>one <b>bold</b></li><li>two</li></ul>"
            "<ol><li>first</li><li>second</li></ol></div>",
        )

    def test_extract_title(self):
        md = """
# My Title
"""
        title = extract_title(md)
        self.assertEqual(title, "My Title")

    def test_generate_pages_recursive_preserves_content_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            content_dir = os.path.join(temp_dir, "content")
            output_dir = os.path.join(temp_dir, "public")
            blog_dir = os.path.join(content_dir, "blog", "post")
            os.makedirs(blog_dir)

            with open(os.path.join(content_dir, "index.md"), "w") as file:
                file.write("# Home\n\n[Post](/blog/post)\n\n![Image](/images/example.png)\n")
            with open(os.path.join(blog_dir, "index.md"), "w") as file:
                file.write("# Blog post\n\n[Back home](/)\n")
            template_path = os.path.join(temp_dir, "template.html")
            with open(template_path, "w") as file:
                file.write(
                    '<link href="{{ Basepath }}index.css">'
                    "<title>{{ Title }}</title>{{ Content }}"
                )

            generate_pages_recursive(content_dir, template_path, output_dir)

            self.assertTrue(os.path.isfile(os.path.join(output_dir, "index.html")))
            self.assertTrue(
                os.path.isfile(os.path.join(output_dir, "blog", "post", "index.html"))
            )
            with open(os.path.join(output_dir, "index.html")) as file:
                home_html = file.read()
            with open(os.path.join(output_dir, "blog", "post", "index.html")) as file:
                post_html = file.read()
            self.assertIn('href="blog/post/index.html"', home_html)
            self.assertIn('src="images/example.png"', home_html)
            self.assertIn('href="../../index.html"', post_html)
            self.assertIn('href="../../index.css"', post_html)
            self.assertFalse(
                os.path.exists(os.path.join(output_dir, "index.html", "blog"))
            )