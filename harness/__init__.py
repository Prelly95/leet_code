"""A tiny LeetCode practice harness.

Scaffold a problem, then paste the examples straight off the problem page
into ``cases.txt`` and run the harness to test your ``Solution``.

See ``leet.py`` for the command line interface.
"""

from .cases import Case, parse_cases
from .runner import RunResult, run_problem

__all__ = ["Case", "parse_cases", "RunResult", "run_problem"]
