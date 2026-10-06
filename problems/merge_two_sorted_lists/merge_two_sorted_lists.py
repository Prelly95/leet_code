# 21. Merge Two Sorted Lists (Easy)
# https://leetcode.com/problems/merge-two-sorted-lists/description/

ENTRY = "martial_inputs"

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def to_list(self):
        res = [self.val]
        linked_list = self.next
        while linked_list:
            res.append(linked_list.val)
            linked_list = linked_list.next
        return res

    @staticmethod
    def new_linked_list(arr=None) -> "ListNode" | None:
        start = None
        if arr is not None and len(arr) > 0:
            start = ListNode(arr[0])
            current_node = start
            for v in arr[1:]:
                current_node.next = ListNode(v)
                current_node = current_node.next
        return start


class Solution:
    def martial_inputs(
        self, list1: list[int] | None, list2: list[int] | None
    ):

        output = self.mergeTwoLists(ListNode.new_linked_list(list1), ListNode.new_linked_list(list2))
        if output:
            return output.to_list()
        else:
            return []

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