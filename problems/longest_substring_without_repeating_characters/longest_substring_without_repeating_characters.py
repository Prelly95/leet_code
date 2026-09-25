class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        repeated = {}
        left = 0
        right = 0
        longest = 0
        while right < len(s):
            if s[right] in repeated:
                if repeated[s[right]] > 0:
                    repeated[s[left]] = 0
                    left += 1
                else:
                    repeated[s[right]] = 1
                    right += 1
            else:
                repeated[s[right]] = 1
                right += 1

            current = right - left
            if current > longest:
                longest = current

        return longest
