import html_to_markdown as markdown
from readability import Document as ReadableDocument  # pyright: ignore[reportMissingTypeStubs]
from langchain_core.documents import Document
from typing import cast


def clean_html_doc(doc: Document) -> Document:
    readable = ReadableDocument(doc.page_content)
    title = readable.title()
    html_content = cast(str, readable.summary())
    markdowned = markdown.convert(html_content)
    return Document(
        page_content=markdowned,
        metadata=cast(dict[str, object], doc.metadata | {"title": title}),
    )
