# 21. Merge Two Sorted Lists (Easy)
# https://leetcode.com/problems/merge-two-sorted-lists/description/

from harness.structures import ListNode

ENTRY = "mergeTwoLists"


class Solution:
    def mergeTwoLists(
        self, list1: ListNode | None, list2: ListNode | None
    ) -> ListNode | None:
        if not list1:
            return list2

        if not list2:
            return list1

        if list1.val <= list2.val:
            current_node = list1
            other_node = list2
        else:
            current_node = list2
            other_node = list1

        start = current_node

        while current_node:
            if not current_node.next:
                current_node.next = other_node
                break
            if current_node.next.val > other_node.val:
                t = current_node.next
                current_node.next = other_node
                other_node = t

            current_node = current_node.next
        return start

    def reverseList(self, head: ListNode | None) -> ListNode | None:
        prev_node = None
        current_node = head

        while current_node:
            if not current_node.next:
                current_node.next = prev_node
                break
            next_node = current_node.next
            current_node.next = prev_node
            prev_node = current_node
            current_node = next_node

        return current_node
