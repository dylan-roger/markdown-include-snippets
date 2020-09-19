import markdown
from markdown_include_snippets.include import MarkdownInclude

source = """
# Heading Level 1 of main file

{!https://file-examples-com.github.io/uploads/2017/02/file_example_JSON_1kb.json!}
"""

print(markdown.markdown(source, extensions=[MarkdownInclude()]))
