import markdown
from markdown_include_snippets.include import MarkdownInclude

sourceRemote = """
# Heading Level 1 of main file

{!https://file-examples-com.github.io/uploads/2017/02/file_example_JSON_1kb.json!}
"""

sourceLocal = """
# Heading Level 1 of main file

{!test_file.txt!tag=doc}
"""

print(markdown.markdown(sourceLocal, extensions=[MarkdownInclude()]))
