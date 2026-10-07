# 525. Contiguous Array (Medium)
# https://leetcode.com/problems/contiguous-array/description/

ENTRY = "findMaxLength"


class Solution:
    def findMaxLength(self, nums: list[int]) -> int:
        prefix_sum = {0: -1}
        current_sum = 0
        current_max = 0

        for ii, n in enumerate(nums):
            if n == 0:
                current_sum -= 1
            else:
                current_sum += 1

            if current_sum in prefix_sum:
                current_max = max(current_max, ii - prefix_sum[current_sum])
            else:
                prefix_sum[current_sum] = ii

        return current_max
