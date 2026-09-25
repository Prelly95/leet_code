"""Best-effort HTML -> Markdown conversion, standard library only.

Written for LeetCode problem descriptions, so it handles the tags they use:
paragraphs, bold/italic, inline code, ``<pre>`` example blocks, lists,
superscripts, links and images. Unknown tags are dropped but their text is
kept.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser


class _MarkdownWriter(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.list_stack: list[list] = []  # each entry: [kind, ordered_counter]
        self.in_pre = 0
        self.pre_buf: list[str] = []
        self._href = ""

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attrs = dict(attrs)
        if tag == "pre":
            self.in_pre += 1
            return
        if self.in_pre:
            return  # inside a code block, drop inline formatting
        if tag == "p":
            self.parts.append("\n\n")
        elif tag == "br":
            self.parts.append("\n")
        elif tag in ("strong", "b"):
            self.parts.append("**")
        elif tag in ("em", "i"):
            self.parts.append("*")
        elif tag == "code":
            self.parts.append("`")
        elif tag == "sup":
            self.parts.append("^")
        elif tag in ("ul", "ol"):
            self.list_stack.append([tag, 0])
            self.parts.append("\n")
        elif tag == "li":
            indent = "  " * max(0, len(self.list_stack) - 1)
            if self.list_stack and self.list_stack[-1][0] == "ol":
                self.list_stack[-1][1] += 1
                self.parts.append(f"\n{indent}{self.list_stack[-1][1]}. ")
            else:
                self.parts.append(f"\n{indent}- ")
        elif tag == "a":
            self._href = attrs.get("href", "")
            self.parts.append("[")
        elif tag == "img":
            self.parts.append(f"![{attrs.get('alt', '')}]({attrs.get('src', '')})")

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre":
            self.in_pre = max(0, self.in_pre - 1)
            if self.in_pre == 0:
                content = "".join(self.pre_buf).strip("\n")
                self.pre_buf = []
                self.parts.append(f"\n\n```\n{content}\n```\n")
            return
        if self.in_pre:
            return
        if tag in ("strong", "b"):
            self.parts.append("**")
        elif tag in ("em", "i"):
            self.parts.append("*")
        elif tag == "code":
            self.parts.append("`")
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self.parts.append("\n")
        elif tag == "a":
            self.parts.append(f"]({self._href})")

    def handle_data(self, data: str) -> None:
        if self.in_pre:
            self.pre_buf.append(data)
        else:
            self.parts.append(data.replace("\xa0", " "))


def html_to_markdown(source: str) -> str:
    """Convert a description's HTML into Markdown."""
    if not source:
        return ""
    writer = _MarkdownWriter()
    writer.feed(source)
    md = "".join(writer.parts)
    md = "\n".join(line.rstrip() for line in md.splitlines())
    md = re.sub(r"\n{3,}", "\n\n", md)  # collapse runs of blank lines
    return md.strip() + "\n"
