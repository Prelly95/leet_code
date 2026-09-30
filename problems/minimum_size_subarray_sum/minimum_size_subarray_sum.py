# 209. Minimum Size Subarray Sum (Medium)
# https://leetcode.com/problems/minimum-size-subarray-sum/

ENTRY = "minSubArrayLen"

class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        left = 0
        right = 1
        current_sum = nums[left]
        MAX = len(nums) + 1
        min_len = MAX

        while right < len(nums) + 1:
            if current_sum < target:
                if not(right < len(nums)):
                    break
                current_sum += nums[right]
                right += 1
            else:
                min_len = min(min_len, right - left)
                current_sum -= nums[left]
                left += 1

        return min_len if min_len < MAX else 0