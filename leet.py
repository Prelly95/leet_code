#!/usr/bin/env python3
"""LeetCode practice harness.

Usage:
    uv run leet.py init <problem_name>   scaffold a new problem folder
    uv run leet.py add <leetcode_url>    import a problem from its LeetCode URL
    uv run leet.py run [problem_name]    run one problem, or all of them
    uv run leet.py debug <problem_name>  run one problem without catching errors (for F5)
    uv run leet.py list                  list scaffolded problems

Scaffolding a problem creates ``problems/<problem_name>/`` containing a
``<problem_name>.py`` solution stub and a ``cases.json`` to fill with the
LeetCode examples. See harness/cases.py for the cases.json format.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from harness.runner import discover_problems, run_problem, to_camel

ROOT = Path(__file__).resolve().parent
PROBLEMS = ROOT / "problems"


SOLUTION_TEMPLATE = '''\
class Solution:
    def {method}(self):
        # TODO: fill in the signature (its parameter names must match the
        # keys in each cases.json "input") and implement the solution.
        ...


# If the harness can't find the entry method automatically (e.g. the method
# name isn't the camelCase of the folder and there's more than one public
# method), name it explicitly:
# ENTRY = "{method}"

# For linked-list / tree problems, import the shared type and annotate your
# parameters/return with it — the harness marshals the raw lists in cases.json
# to and from the structure for you:
#   from harness.structures import ListNode, TreeNode
'''

CASES_TEMPLATE = '''\
{
  "_comment": "'input' is an object of keyword args (or an array for positional args); 'output' is the expected return. Set 'unordered': true to compare ignoring order. Replace the example below.",
  "unordered": false,
  "cases": [
    {"input": {"nums": [2, 7, 11, 15], "target": 9}, "output": [0, 1]}
  ]
}
'''


def slugify(name: str) -> str:
    slug = re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_").lower()
    if not slug:
        raise SystemExit(f"cannot make a folder name from {name!r}")
    return slug


def cmd_init(name: str) -> int:
    slug = slugify(name)
    problem_dir = PROBLEMS / slug
    if problem_dir.exists():
        print(f"problem already exists: {problem_dir.relative_to(ROOT)}")
        return 1

    problem_dir.mkdir(parents=True)
    (problem_dir / f"{slug}.py").write_text(
        SOLUTION_TEMPLATE.format(method=to_camel(slug))
    )
    (problem_dir / "cases.json").write_text(CASES_TEMPLATE)

    rel = problem_dir.relative_to(ROOT)
    print(f"created {rel}/")
    print(f"  edit {rel}/{slug}.py   and add examples to {rel}/cases.json")
    print(f"  then: uv run leet.py run {slug}")
    return 0


def cmd_add(url: str) -> int:
    from harness.leetcode import build_files, fetch_problem

    try:
        problem = fetch_problem(url, session=os.environ.get("LEETCODE_SESSION"))
    except Exception as exc:
        print(f"import failed: {exc}")
        return 1

    slug = problem.slug.replace("-", "_")
    problem_dir = PROBLEMS / slug
    if problem_dir.exists():
        print(f"problem already exists: {problem_dir.relative_to(ROOT)}")
        return 1

    solution_text, cases_text, description_md, n_cases = build_files(problem)
    problem_dir.mkdir(parents=True)
    (problem_dir / f"{slug}.py").write_text(solution_text)
    (problem_dir / "cases.json").write_text(cases_text)
    (problem_dir / "README.md").write_text(description_md)

    rel = problem_dir.relative_to(ROOT)
    print(f"added {rel}/  ({problem.difficulty}, {n_cases} example case(s))")
    if n_cases == 0:
        print("  couldn't parse examples — add cases to cases.json by hand")
    print(f"  implement {rel}/{slug}.py, then: uv run leet.py run {slug}")
    return 0


def cmd_run(name: str | None) -> int:
    if name:
        dirs = [PROBLEMS / slugify(name)]
        if not dirs[0].exists():
            print(f"no such problem: {name}")
            return 1
    else:
        dirs = discover_problems(PROBLEMS)
        if not dirs:
            print("no problems yet — scaffold one with: uv run leet.py init <name>")
            return 1

    results = [run_problem(d) for d in dirs]
    if len(results) > 1:
        passed = sum(r.passed for r in results)
        failed = sum(r.failed for r in results)
        errors = sum(r.errors for r in results)
        print(f"\ntotal: {passed} passed, {failed} failed, {errors} errored")
    return 0 if all(r.ok for r in results) else 1


def cmd_debug(name: str) -> int:
    problem_dir = PROBLEMS / slugify(name)
    if not problem_dir.exists():
        print(f"no such problem: {name}")
        return 1
    # catch=False lets a solution's exception reach the F5 debugger.
    result = run_problem(problem_dir, catch=False)
    return 0 if result.ok else 1


def cmd_list() -> int:
    dirs = discover_problems(PROBLEMS)
    if not dirs:
        print("no problems yet — scaffold one with: uv run leet.py init <name>")
        return 0
    for d in dirs:
        print(d.name)
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1

    command, *rest = argv
    if command == "init":
        if not rest:
            print("usage: leet.py init <problem_name>")
            return 1
        return cmd_init(rest[0])
    if command == "add":
        if not rest:
            print("usage: leet.py add <leetcode_url>")
            return 1
        return cmd_add(rest[0])
    if command == "run":
        return cmd_run(rest[0] if rest else None)
    if command == "debug":
        if not rest:
            print("usage: leet.py debug <problem_name>")
            return 1
        return cmd_debug(rest[0])
    if command == "list":
        return cmd_list()

    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
