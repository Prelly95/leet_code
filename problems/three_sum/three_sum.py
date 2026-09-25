class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        sorted_list = sorted(nums)
        result = []
        ii = 0
        while ii < len(sorted_list):
            target = -sorted_list[ii]
            valid_triplets = self.twoSum(sorted_list[ii + 1 :], target)
            if len(valid_triplets) > 0:
                for t in valid_triplets:
                    result.append(t)
            while ii < len(sorted_list) - 1:
                if sorted_list[ii + 1] != sorted_list[ii]:
                    break
                ii += 1
            ii += 1
        return result

    def twoSum(self, nums, target):
        left = 0
        right = len(nums) - 1
        results = []
        while left < right:
            if (nums[left] + nums[right]) == target:
                results.append([-target, nums[left], nums[right]])
                right = self.count_repeats(right, nums, -1)
                left = self.count_repeats(left, nums, 1)

            elif (nums[left] + nums[right]) > target:
                # reduce the sum
                right = self.count_repeats(right, nums, -1)
            else:
                # increase the sum
                left = self.count_repeats(left, nums, 1)
        return results

    def count_repeats(
        self, start_index: int, in_array: list[int], direction: int
    ) -> int:
        ii = start_index
        if direction > 0:
            while ii < len(in_array) - 1:
                if in_array[ii + 1] == in_array[ii]:
                    ii += 1
                else:
                    break
            ii += 1
        else:
            while ii > 1:
                if in_array[ii - 1] == in_array[ii]:
                    ii -= 1
                else:
                    break
            ii -= 1
        return ii
