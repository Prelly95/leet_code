"""Shared LeetCode data structures and their list codecs.

Some problems take or return a linked list or a binary tree, but ``cases.json``
stores the raw values as plain lists (just like the LeetCode examples). The
runner bridges the gap automatically, driven by your solution method's type
annotations:

- annotate a parameter as ``ListNode`` / ``TreeNode`` and the harness *decodes*
  the raw list into that structure before calling you;
- annotate the return the same way and it *encodes* the returned structure back
  into a list before comparing against the case's ``output``.

So your solution file stays exactly what you'd paste into LeetCode — no wrapper
method, no ``ENTRY`` juggling. Just import the type and annotate:

    from harness.structures import ListNode

    class Solution:
        def mergeTwoLists(self, a: ListNode | None, b: ListNode | None) -> ListNode | None:
            ...

Adding a new structure (say LeetCode's graph ``Node``):

1. Define the class with two methods that match LeetCode's serialisation:
   ``from_list(values)`` (raw list -> structure, a classmethod) and
   ``to_list(obj)`` (structure -> raw list, a staticmethod that accepts None).
2. Register it: ``register(Node, decode=Node.from_list, encode=Node.to_list)``.

Annotate your solution with the new type and it just works. See the README's
"Special input types" section for the short version.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Codec:
    """How to turn a raw list into a structure and back again."""

    decode: Callable[[Any], Any]  # raw list -> structure
    encode: Callable[[Any], Any]  # structure -> raw list


# Maps a structure type to its codec. The runner looks types up here (including
# inside ``X | None`` annotations) to decide what to marshal.
CODECS: dict[type, Codec] = {}


def register(cls: type, *, decode: Callable[[Any], Any], encode: Callable[[Any], Any]) -> None:
    """Make ``cls`` marshalable: the runner will decode/encode it at the boundary."""
    CODECS[cls] = Codec(decode=decode, encode=encode)


class ListNode:
    """A singly-linked list node. Serialises as the list of its values."""

    def __init__(self, val: Any = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next

    @classmethod
    def from_list(cls, values: list | None) -> "ListNode | None":
        head: ListNode | None = None
        for v in reversed(values or []):
            head = cls(v, head)
        return head

    @staticmethod
    def to_list(node: "ListNode | None") -> list:
        out: list = []
        while node is not None:
            out.append(node.val)
            node = node.next
        return out


class TreeNode:
    """A binary tree node. Serialises as LeetCode's level-order list.

    LeetCode's format lists nodes breadth-first and omits the children of
    absent nodes, using ``null`` (JSON ``None``) for a missing child that still
    has a later sibling — e.g. ``[1, null, 2, 3]``.
    """

    def __init__(self, val: Any = 0, left: "TreeNode | None" = None, right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_list(cls, values: list | None) -> "TreeNode | None":
        values = list(values or [])
        if not values or values[0] is None:
            return None

        it = iter(values)
        root = cls(next(it))
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for side in ("left", "right"):
                v = next(it, _MISSING)
                if v is _MISSING:
                    return root
                if v is not None:
                    child = cls(v)
                    setattr(node, side, child)
                    queue.append(child)
        return root

    @staticmethod
    def to_list(root: "TreeNode | None") -> list:
        if root is None:
            return []
        out: list = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                out.append(None)
                continue
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        # LeetCode trims trailing nulls (children of leaf nodes).
        while out and out[-1] is None:
            out.pop()
        return out


_MISSING = object()  # sentinel so a genuine None value isn't mistaken for "ran out"


register(ListNode, decode=ListNode.from_list, encode=ListNode.to_list)
register(TreeNode, decode=TreeNode.from_list, encode=TreeNode.to_list)
