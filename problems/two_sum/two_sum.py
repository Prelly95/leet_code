# 1. Two Sum (Easy)
# https://leetcode.com/problems/two-sum/description/

class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        hist = {}
        for ii, n in enumerate(nums):
            t = target - n

            if t in hist:
                return [hist[t], ii]
            else:
                hist[n] = ii