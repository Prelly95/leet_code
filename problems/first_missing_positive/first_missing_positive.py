class Solution(object):
    def firstMissingPositive(self, nums):
        # return self.firstMissingPositive_cycle_sort(nums)
        return self.firstMissingPositive_sign_signaling(nums)


    def firstMissingPositive_cycle_sort(self, nums):
        N = len(nums)

        for n in nums:
            print(nums)
            corrected_index = n-1
            if (corrected_index) < 0 or corrected_index > N - 1:
                continue
            this_n = n
            while nums[corrected_index] != this_n:
                temp_n = nums[corrected_index]
                nums[corrected_index] = this_n
                corrected_index = temp_n-1
                if (corrected_index) < 0 or corrected_index > N - 1:
                    break
                this_n = temp_n

        ii = 0
        for n in nums:
            if n - 1 != ii:
                return ii + 1
            ii += 1
        return ii + 1


    def firstMissingPositive_sign_signaling(self, nums):
        N = len(nums)
        for ii, n in enumerate(nums):
            if n < 1:
                # shift any invalid numbers to above the max possible value
                nums[ii] = N + 1

        for n in nums:
            idx = abs(n) - 1
            if idx < N-1:
                nums[idx] = -abs(nums[idx])

        for ii, n in enumerate(nums):
            if n > -1:
                return ii + 1

        return N + 1