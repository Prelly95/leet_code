# 215. Kth Largest Element in an Array (Medium)
# https://leetcode.com/problems/kth-largest-element-in-an-array/description/

ENTRY = "findKthLargest"

class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:

        # iterate over the nums adding each element to a min-heap
        # limit the size of the heap to K
        # return the min value in the heap
        h = []
        for n in nums:
            self.heap_push(h, n)
            if len(h) > k:
                self.heap_pop(h)
        return self.heap_pop(h)


    def get_parent_index(self, child_index):
        return (child_index - 1) // 2

    def get_left_index(self, parent_index):
        return (parent_index * 2) + 1

    def get_right_index(self, parent_index):
        return (parent_index * 2) + 2

    def heap_push(self, heap, val):
        heap.append(val)
        child_index = len(heap) - 1
        parent_index = child_index # something to init to
        while parent_index > 0:
            parent_index = self.get_parent_index(child_index)
            if heap[child_index] < heap[parent_index]:
                self.swap_values(heap, parent_index, child_index)
                child_index = parent_index
            else:
                break

    def heap_pop(self, heap):
        smallest = heap[0]
        self.swap_values(heap, 0, len(heap) - 1)
        heap.pop()
        # bubble down
        parent_index = 0
        smaller_child = self.get_smaller_index(heap, parent_index)
        while smaller_child is not None:
            if heap[smaller_child] >= heap[parent_index]:
                break
            self.swap_values(heap, smaller_child, parent_index)
            parent_index = smaller_child
            smaller_child = self.get_smaller_index(heap, parent_index)

        return smallest

    def swap_values(self, heap, index_1, index_2):
        t = heap[index_1]
        heap[index_1] = heap[index_2]
        heap[index_2] = t

    def get_smaller_index(self, heap, parent_index):
        left_index = self.get_left_index(parent_index)
        right_index = self.get_right_index(parent_index)

        if left_index > len(heap) - 1:
            return None
        elif right_index > len(heap) - 1:
            return left_index

        if heap[left_index] < heap[right_index]:
            return left_index
        else:
            return right_index