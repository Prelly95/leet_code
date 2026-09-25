# 217. Contains Duplicate (Easy)
# https://leetcode.com/problems/contains-duplicate/

class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        # TODO: implement
        seen = set()
        for n in nums:
            if n in seen:
                return True
            else:
                seen.add(n)

        return False
