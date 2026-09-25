# 442. Find All Duplicates in an Array (Medium)
# https://leetcode.com/problems/find-all-duplicates-in-an-array/

ENTRY = "findDuplicates"

class Solution:
    def findDuplicates(self, nums: list[int]) -> list[int]:

        res = []
        for n in nums:
            idx = abs(n) - 1
            if nums[idx] < 0:
                res.append(abs(n))
            nums[idx] = -1*nums[idx]
        return res