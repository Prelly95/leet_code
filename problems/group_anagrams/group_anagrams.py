# 49. Group Anagrams (Medium)
# https://leetcode.com/problems/group-anagrams/description/

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        anagrams = {}
        for s in strs:
            alpha = "".join(sorted(s))
            if alpha in anagrams:
                anagrams[alpha].append(s)
            else:
                anagrams[alpha] = [s]
        return list(anagrams.values())