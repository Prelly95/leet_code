"""Load a problem's ``Solution`` and run it against its ``cases.json``."""

from __future__ import annotations

import importlib.util
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path

from .cases import Suite, load_cases

GREEN = "\033[32m"
RED = "\033[31m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


@dataclass
class RunResult:
    problem: str
    passed: int = 0
    failed: int = 0
    errors: int = 0

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.errors

    @property
    def ok(self) -> bool:
        # A problem with no cases yet is not a failure — only real failed or
        # errored cases (or a missing solution file) count against a run.
        return self.failed == 0 and self.errors == 0


def to_camel(name: str) -> str:
    """``two_sum`` / ``two-sum`` -> ``twoSum``."""
    parts = [p for p in name.replace("-", "_").split("_") if p]
    if not parts:
        return name
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def _load_module(py_path: Path):
    # Namespaced module name avoids clashing with stdlib (e.g. a problem folder
    # named "queue"). Registering it in sys.modules lets debugpy attribute the
    # file so F5 breakpoints in the solution bind and are hit.
    mod_name = f"leet_solution_{py_path.stem}"
    spec = importlib.util.spec_from_file_location(mod_name, py_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {py_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def _find_entry(module, problem_name: str) -> str:
    """Work out which ``Solution`` method the cases should call.

    Order of preference: an explicit ``ENTRY`` in the module, then a method
    whose name is the camelCase of the problem folder, then the sole public
    method if there is exactly one.
    """
    explicit = getattr(module, "ENTRY", None)
    if explicit:
        return explicit

    solution = getattr(module, "Solution")
    methods = [
        n
        for n in vars(solution)
        if not n.startswith("_") and callable(getattr(solution, n))
    ]

    camel = to_camel(problem_name)
    if camel in methods:
        return camel
    if len(methods) == 1:
        return methods[0]
    raise ValueError(
        f"could not pick an entry method for {problem_name!r}; candidates: "
        f"{sorted(methods)}. Set ENTRY = \"methodName\" in the solution file."
    )


def _deep_sort(value):
    """Recursively sort lists so unordered results compare equal."""
    if isinstance(value, list):
        return sorted((_deep_sort(v) for v in value), key=repr)
    return value


def _matches(got, expected, unordered: bool) -> bool:
    if unordered:
        return _deep_sort(got) == _deep_sort(expected)
    return got == expected


def run_problem(problem_dir: Path, *, verbose: bool = True, catch: bool = True) -> RunResult:
    """Run every case for one problem folder and print the results.

    With ``catch=False`` exceptions from the solution are not swallowed, so a
    debugger attached via F5 stops at the line that raised.
    """
    problem_dir = Path(problem_dir)
    name = problem_dir.name
    result = RunResult(problem=name)

    solution_file = problem_dir / f"{name}.py"
    cases_file = problem_dir / "cases.json"

    if verbose:
        print(f"{BOLD}{name}{RESET}")

    if not solution_file.exists():
        print(f"  {RED}no solution file: {solution_file.name}{RESET}")
        result.errors += 1
        return result

    suite: Suite = load_cases(cases_file) if cases_file.exists() else Suite()
    if not suite.cases:
        print(f"  {DIM}no cases yet — add some to {cases_file.name}{RESET}")
        return result

    try:
        module = _load_module(solution_file)
        entry_name = _find_entry(module, name)
    except Exception as exc:  # import/entry problems fail the whole suite
        print(f"  {RED}failed to load solution: {exc}{RESET}")
        result.errors += len(suite.cases)
        return result

    for case in suite.cases:
        label = f"case {case.name}"
        if catch:
            try:
                method = getattr(module.Solution(), entry_name)
                got = method(*case.args, **case.kwargs)
            except Exception:
                result.errors += 1
                print(f"  {RED}✗ {label} raised{RESET}")
                if verbose:
                    print("      " + traceback.format_exc().replace("\n", "\n      ").rstrip())
                continue
        else:
            # Let the exception propagate so a debugger breaks at the throw.
            method = getattr(module.Solution(), entry_name)
            got = method(*case.args, **case.kwargs)

        unordered = suite.unordered if case.unordered is None else case.unordered
        if _matches(got, case.expected, unordered):
            result.passed += 1
            if verbose:
                print(f"  {GREEN}✓ {label}{RESET}")
        else:
            result.failed += 1
            print(f"  {RED}✗ {label}{RESET}")
            print(f"      expected: {case.expected!r}")
            print(f"      got:      {got!r}")

    return result


def discover_problems(problems_dir: Path) -> list[Path]:
    problems_dir = Path(problems_dir)
    if not problems_dir.exists():
        return []
    return sorted(p for p in problems_dir.iterdir() if p.is_dir() and not p.name.startswith("_"))
