# 525. Contiguous Array (Medium)
# https://leetcode.com/problems/contiguous-array/description/

ENTRY = "findMaxLength"

class Solution:
    def findMaxLength(self, nums: list[int]) -> int:
        sum = 0
        current_max = 0
        first_index_seen = {0: -1}

        for ii, n in enumerate(nums[::2]):
            if n:
                sum += 1
            else:
                sum -= 1

            if sum not in first_index_seen:
                first_index_seen[sum] = ii

            if sum in first_index_seen:
                current_max = max(current_max, ii - first_index_seen[sum])

        return current_max
