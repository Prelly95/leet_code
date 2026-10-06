# LeetCode practice harness

A tiny harness for grinding LeetCode problems. Scaffold a problem, drop the
examples into a JSON file, and run.

## Workflow

With [`just`](https://github.com/casey/just):

```bash
just init two_sum        # scaffold an empty problems/two_sum/
just add <leetcode_url>  # import a problem from LeetCode (stub + examples)
just run two_sum         # run one problem
just run                 # run everything
just list                # list scaffolded problems
just edit two_sum        # open the solution in $EDITOR
just                     # show all recipes
```

Or call the CLI directly:

```bash
uv run leet.py init two_sum
uv run leet.py run two_sum
uv run leet.py run
uv run leet.py list
```

`init` creates a folder under `problems/` with two files:

- `<name>.py` — a `Solution` class stub (LeetCode style).
- `cases.json` — where you add the examples.

## Importing from a URL

`add` pulls a problem straight from LeetCode via its public GraphQL API:

```bash
uv run leet.py add https://leetcode.com/problems/two-sum/
# or: just add https://leetcode.com/problems/two-sum/
```

It fills in the folder for you:

- `<name>.py` — the real Python3 signature (`def twoSum(self, nums: list[int],
  target: int) -> list[int]:`), with `ENTRY` set automatically when the method
  name isn't the camelCase of the folder.
- `cases.json` — populated with the problem's own examples, and
  `"unordered": true` when the statement says the answer may be in any order.
- `README.md` — the problem description, converted from HTML to Markdown.

Notes:

- Uses the standard library only — no extra dependencies.
- It's an unofficial endpoint; heavy use may be rate-limited.
- Premium problems need a session cookie: `export LEETCODE_SESSION=<cookie>`.
- Examples that don't parse cleanly (e.g. some tree/linked-list formats) leave
  `cases.json` for you to finish by hand.

## Debugging (F5)

Open a problem's `<name>.py`, set breakpoints, and press **F5** — the
"Debug current problem" launch config runs that problem's `cases.json` through
the harness under the debugger. It reads your cases (no `__main__` block or
retyped inputs needed), and it doesn't swallow exceptions, so a crash drops you
at the failing line. From the terminal it's `just debug <problem>` (or
`uv run leet.py debug <problem>`).

## Tab completion

Complete problem names for `just run` / `just edit` — `just run <TAB>` cycles
through the problem set. Add this to `~/.bashrc`:

```bash
source /home/patrick/Projects/python_playground/leet_code/completions/just-leet.bash
```

## cases.json format

JSON — either a bare list of cases, or an object with a `cases` list plus
options:

```json
{
  "unordered": false,
  "cases": [
    {"input": {"nums": [2, 7, 11, 15], "target": 9}, "output": [0, 1]},
    {"input": {"nums": [3, 2, 4], "target": 6}, "output": [1, 2]}
  ]
}
```

Each case:

- `input` — an object of keyword args (matched to your method's parameters),
  or an array for positional args (e.g. `"input": [[1, 0]]` passes one list).
- `output` (alias `expected`) — the value your solution should return.
- `name` (optional) — a label for the case.
- `unordered` (optional) — per-case override of the suite-level flag.

`unordered` compares results ignoring order, nested lists included — handy for
problems like 3Sum or Group Anagrams. Any key starting with `_` (e.g.
`_comment`) is ignored, so you can leave notes in the file.

## How the entry method is chosen

The runner calls one method on your `Solution`. It picks, in order:

1. `ENTRY = "methodName"` if defined at module level in the solution file.
2. The method whose name is the camelCase of the folder (`two_sum` → `twoSum`).
3. The only public method, if there's exactly one.

If your file has several public methods and none matches the folder name, set
`ENTRY` explicitly (see `problems/regex_match/regex_match.py`).

## Special input types (ListNode / TreeNode)

Some problems take or return a linked list or a binary tree, but `cases.json`
stores the raw values as plain lists (exactly like the LeetCode examples). You
don't write any conversion code — import the type and annotate your method, and
the harness decodes each list argument into the structure before calling you,
then encodes a structure result back to a list to compare against `output`:

```python
from harness.structures import ListNode

class Solution:
    def mergeTwoLists(self, list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
        ...
```

`cases.json` stays plain lists — `{"input": {"list1": [1, 2, 4], "list2": [1, 3, 4]}, "output": [1, 1, 2, 3, 4, 4]}`.
`TreeNode` works the same way, using LeetCode's level-order format (e.g.
`[3, 9, 20, null, null, 15, 7]`). The conversion is driven purely by the type
annotation, so it also sees types inside `X | None`.

### Adding a new type

To support another LeetCode structure (say the graph `Node`), edit
`harness/structures.py`:

1. Define the class with a `from_list(values)` classmethod (raw list →
   structure) and a `to_list(obj)` staticmethod (structure → raw list, must
   accept `None`), matching how LeetCode serialises it.
2. Register it: `register(Node, decode=Node.from_list, encode=Node.to_list)`.

Then annotate your solution with `Node` and it just works — no runner changes.

## Layout

```
justfile                CLI shortcuts (run / init / list / edit)
leet.py                 the harness CLI
harness/
  cases.py              parses cases.json
  runner.py             loads a Solution and runs its cases
  structures.py         ListNode / TreeNode and their list codecs
  leetcode.py           imports a problem from its LeetCode URL
completions/
  just-leet.bash        bash tab-completion for problem names
problems/
  <name>/<name>.py      your solution
  <name>/cases.json     the examples
```
