# 242. Valid Anagram (Easy)
# https://leetcode.com/problems/valid-anagram/

ENTRY = "isAnagram"

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        mismatches = 0
        c_count = {}
        for ii in range(len(s)):
            s_c = s[ii]
            t_c = t[ii]
            if s_c in c_count:
                temp = c_count[s_c]
                c_count[s_c] += 1
                if c_count[s_c] == 0:
                    mismatches -= 1
                elif temp == 0:
                    mismatches += 1
            else:
                c_count[s_c] = 1
                mismatches += 1

            if t_c in c_count:
                temp = c_count[t_c]
                c_count[t_c] -= 1
                if c_count[t_c] == 0:
                    mismatches -= 1
                elif temp == 0:
                    mismatches += 1
            else:
                c_count[t_c] = -1
                mismatches += 1

        return mismatches == 0