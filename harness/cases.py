"""Load a problem's ``cases.json`` file.

A cases file is JSON. Either a bare list of cases::

    [
        {"input": {"nums": [2, 7, 11, 15], "target": 9}, "output": [0, 1]}
    ]

or an object with a ``cases`` list plus options::

    {
        "unordered": true,
        "cases": [
            {"input": {"nums": [3, 2, 4], "target": 6}, "output": [1, 2]}
        ]
    }

Each case has:

- ``input``: an object of keyword arguments (matched to your method's
  parameters), or an array for positional arguments.
- ``output`` (alias ``expected``): the value your solution should return.
- ``name`` (optional): a label for the case.
- ``unordered`` (optional): per-case override of the suite-level flag.

``unordered`` compares results ignoring order, nested lists included — handy
for problems like 3Sum or Group Anagrams. Any key starting with ``_`` (e.g.
``_comment``) is ignored, so you can leave notes in the file.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Case:
    """One test case: how to call the solution and what to expect back."""

    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    expected: object = None
    name: str = ""
    unordered: bool | None = None


@dataclass
class Suite:
    cases: list[Case] = field(default_factory=list)
    unordered: bool = False


def _build_case(raw: dict, index: int) -> Case:
    if "input" not in raw:
        raise ValueError(f"case {index} is missing an 'input' key")

    supplied = raw["input"]
    if isinstance(supplied, dict):
        args, kwargs = [], supplied
    elif isinstance(supplied, list):
        args, kwargs = supplied, {}
    else:
        # A single scalar input, e.g. "input": "babad".
        args, kwargs = [supplied], {}

    if "output" in raw:
        expected = raw["output"]
    elif "expected" in raw:
        expected = raw["expected"]
    else:
        raise ValueError(f"case {index} is missing an 'output' key")

    return Case(
        args=list(args),
        kwargs=dict(kwargs),
        expected=expected,
        name=str(raw.get("name", index)),
        unordered=raw.get("unordered"),
    )


def parse_cases(text: str) -> Suite:
    """Parse the contents of a ``cases.json`` file into a :class:`Suite`."""
    if not text.strip():
        return Suite()

    data = json.loads(text)

    if isinstance(data, list):
        raw_cases, unordered = data, False
    elif isinstance(data, dict):
        raw_cases = data.get("cases", [])
        unordered = bool(data.get("unordered", False))
    else:
        raise ValueError("cases file must be a JSON list or object")

    suite = Suite(unordered=unordered)
    for i, raw in enumerate(raw_cases):
        suite.cases.append(_build_case(raw, i))
    return suite


def load_cases(path: Path) -> Suite:
    return parse_cases(Path(path).read_text())
