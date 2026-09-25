"""Import a problem from its LeetCode URL via the public GraphQL API.

The problem page is a client-rendered app, so fetching the URL's HTML only
yields a JS shell. Instead we query ``https://leetcode.com/graphql`` with the
slug from the URL, which returns structured data: the Python3 method stub, the
metadata (method name + params), and the description HTML with the examples.

From that we build a signature-correct solution stub and a ``cases.json``
populated with the problem's own examples. Uses only the standard library.
"""

from __future__ import annotations

import ast
import html
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from .markdown import html_to_markdown
from .runner import to_camel

GRAPHQL_URL = "https://leetcode.com/graphql"

_QUERY = """
query q($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    difficulty
    metaData
    content
    codeSnippets { langSlug code }
  }
}
"""

# ``name =`` but not ``==``, used to split an example's Input into arguments.
_ASSIGN = re.compile(r"([A-Za-z_]\w*)\s*=(?!=)")


@dataclass
class Problem:
    slug: str
    frontend_id: str
    title: str
    difficulty: str
    method: str
    params: list[str] = field(default_factory=list)
    python_stub: str = ""
    content_html: str = ""
    url: str = ""


def slug_from_url(url: str) -> str:
    """Pull the ``two-sum`` slug out of a problem URL (or accept a bare slug)."""
    match = re.search(r"/problems/([A-Za-z0-9-]+)", url)
    if match:
        return match.group(1)
    bare = url.strip().strip("/")
    if re.fullmatch(r"[a-z0-9-]+", bare):
        return bare
    raise ValueError(f"could not find a problem slug in {url!r}")


def fetch_problem(url: str, *, session: str | None = None, timeout: int = 20) -> Problem:
    """Fetch a problem's data from the LeetCode GraphQL API."""
    slug = slug_from_url(url)
    payload = json.dumps({"query": _QUERY, "variables": {"titleSlug": slug}}).encode()
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (leet-code practice harness)",
        "Referer": f"https://leetcode.com/problems/{slug}/",
    }
    if session:
        headers["Cookie"] = f"LEETCODE_SESSION={session}"

    request = urllib.request.Request(GRAPHQL_URL, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read())
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"could not reach LeetCode ({exc})") from exc

    question = (body.get("data") or {}).get("question")
    if not question:
        raise RuntimeError(
            f"no data for {slug!r} — it may be premium-only "
            "(set LEETCODE_SESSION), or the URL is wrong"
        )

    meta = json.loads(question.get("metaData") or "{}")
    python_stub = ""
    for snippet in question.get("codeSnippets") or []:
        if snippet.get("langSlug") == "python3":
            python_stub = snippet.get("code", "")
            break

    return Problem(
        slug=slug,
        frontend_id=question.get("questionFrontendId", ""),
        title=question.get("title", ""),
        difficulty=question.get("difficulty", ""),
        method=meta.get("name", ""),
        params=[p["name"] for p in meta.get("params", [])],
        python_stub=python_stub,
        content_html=question.get("content") or "",
        url=url if url.startswith("http") else f"https://leetcode.com/problems/{slug}/",
    )


def _html_to_text(source: str) -> str:
    text = re.sub(r"<sup>(.*?)</sup>", r"^\1", source)  # 10<sup>4</sup> -> 10^4
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text)


def _parse_value(raw: str):
    raw = raw.strip()
    for loader in (json.loads, ast.literal_eval):
        try:
            return loader(raw)
        except Exception:
            continue
    return raw  # leave anything exotic as a string for the user to fix


def _parse_input(raw: str) -> tuple[list, dict]:
    matches = list(_ASSIGN.finditer(raw))
    if not matches:
        return [_parse_value(raw)], {}
    kwargs: dict = {}
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        value = raw[start:end].strip().rstrip(",").strip()
        kwargs[m.group(1)] = _parse_value(value)
    return [], kwargs


def parse_examples(content_html: str) -> list[dict]:
    """Turn the description's Input/Output examples into case dicts."""
    lines = [ln.strip() for ln in _html_to_text(content_html).splitlines()]
    cases: list[dict] = []
    pending: str | None = None
    for line in lines:
        low = line.lower()
        if low.startswith("input:"):
            pending = line[len("input:"):].strip()
        elif low.startswith("output:") and pending is not None:
            args, kwargs = _parse_input(pending)
            cases.append(
                {
                    "input": kwargs if kwargs else args,
                    "output": _parse_value(line[len("output:"):].strip()),
                }
            )
            pending = None
    return cases


def _solution_text(problem: Problem) -> str:
    header = f"# {problem.frontend_id}. {problem.title} ({problem.difficulty})\n# {problem.url}\n"

    folder = problem.slug.replace("-", "_")
    entry = ""
    if problem.method and problem.method != to_camel(folder):
        entry = f'\nENTRY = "{problem.method}"\n'

    code = problem.python_stub.rstrip()
    if not code:
        code = f"class Solution:\n    def {problem.method or to_camel(folder)}(self):\n        ..."
    else:
        # LeetCode stubs end at the (empty) method body; give it a real one.
        body_indent = "        "
        for line in code.splitlines():
            stripped = line.lstrip()
            if problem.method and stripped.startswith(f"def {problem.method}"):
                body_indent = line[: len(line) - len(stripped)] + "    "
                break
        code += f"\n{body_indent}# TODO: implement\n{body_indent}pass"

    return f"{header}{entry}\n{code}\n"


def _cases_text(problem: Problem, cases: list[dict]) -> str:
    text = _html_to_text(problem.content_html)
    unordered = bool(re.search(r"in any order", text, re.IGNORECASE))

    comment = (
        f"LeetCode {problem.frontend_id} — {problem.title} "
        f"({problem.difficulty}). {problem.url}"
    )
    lines = [
        "{",
        f'  "_comment": {json.dumps(comment, ensure_ascii=False)},',
        f'  "unordered": {"true" if unordered else "false"},',
        '  "cases": [',
    ]
    rendered = ["    " + json.dumps(c, ensure_ascii=False) for c in cases]
    lines.append(",\n".join(rendered))
    lines.append("  ]")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _description_md(problem: Problem) -> str:
    title = f"# {problem.frontend_id}. {problem.title}".rstrip()
    meta = " · ".join(filter(None, [problem.difficulty, f"[Problem]({problem.url})"]))
    body = html_to_markdown(problem.content_html)
    return f"{title}\n\n{meta}\n\n{body}"


def build_files(problem: Problem) -> tuple[str, str, str, int]:
    """Return ``(solution_text, cases_text, description_md, n_cases)``."""
    cases = parse_examples(problem.content_html)
    return (
        _solution_text(problem),
        _cases_text(problem, cases),
        _description_md(problem),
        len(cases),
    )
