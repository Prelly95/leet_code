# 10. Regular Expression Matching (Hard)
# https://leetcode.com/problems/regular-expression-matching/

ENTRY = "isMatch"

class Solution:
    def isMatch_old(self, s: str, p: str) -> bool:

        # Trivial Cases
        if p == ".*":
            return True

        m = p[0]
        ii = 0
        jj = 0

        while ii < len(s):
            if jj > len(p) - 1:
                return False

            m = p[jj]
            if m == "*":
                m_s = p[jj - 1]
                while s[ii] == m_s:
                    ii += 1
                    if ii >= len(s):
                        return True
                jj += 1

            elif m == ".":
                jj += 1
                ii += 1
            else:
                if jj + 1 < len(p) and (p[jj + 1] == "*"):
                    jj += 1
                elif s[ii] != m:
                    return False
                else:
                    jj += 1
                    # ii += 1

        return jj >= len(p)

    def isMatch(self, s: str, p: str) -> bool:

        # Trivial Cases
        if p == ".*":
            return True

        m = p[0]
        ii = 0
        jj = 0

        while jj < len(p):
            m = p[jj]
            if m == "*":
                m = p[jj - 1]
                if ii >= len(s):
                    return True
                while m == s[ii]:
                    ii += 1
                    if ii >= len(s):
                        return True
                jj += 1
            elif m == ".":
                ii += 1
                jj += 1
            else:
                if jj + 1 < len(p) and (p[jj + 1] == "*"):
                    jj += 1
                    if ii >= len(s):
                        continue
                    # elif s[ii] != p[jj - 1]:
                    #     return False
                elif ii >= len(s) or s[ii] != p[jj]:
                    return False
                else:
                    jj += 1
                    ii += 1

        return ii >= len(s)