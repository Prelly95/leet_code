ENTRY = "subarraySum"


class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        count = 0
        current_sum = 0
        prefix_list = {0: 1}
        for n in nums:
            current_sum = current_sum + n
            target = current_sum - k

            if target in prefix_list:
                count += prefix_list[target]

            if current_sum in prefix_list:
                prefix_list[current_sum] += 1
            else:
                prefix_list[current_sum] = 1
        return count

    def subarraySumSlow(self, nums: list[int], k: int) -> int:
        count = 0
        current_sum = 0
        prefix_list = [0]
        for n in nums:
            current_sum = n + current_sum
            target = current_sum - k
            for p in prefix_list:
                if p == target:
                    count += 1

            prefix_list.append(current_sum)
        return count
