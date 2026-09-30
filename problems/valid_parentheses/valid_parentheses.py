# 20. Valid Parentheses (Easy)
# https://leetcode.com/problems/valid-parentheses/

ENTRY = "isValid"

class Solution:
    def isValid(self, s: str) -> bool:
        bracket_match_map = {
            ")":"(",
            "}":"{",
            "]":"[",
        }
        bracket_stack = []
        
        for c in s:
            if c in bracket_match_map:
                if len(bracket_stack) < 1:
                    return False
                
                o = bracket_stack.pop()
                if o != bracket_match_map[c]:
                    return False
            else:
                bracket_stack.append(c)

        return len(bracket_stack) == 0