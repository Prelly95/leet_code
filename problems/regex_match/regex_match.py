# Two public methods, so tell the harness which one to call.
ENTRY = "isMatch"


class Solution:
    solved = {}

    def isMatch(self, s: str, p: str) -> bool:
        solved_key = (s, p)
        if solved_key in self.solved:
            return self.solved[solved_key]

        m, p = self.split_on_next_pattern(p)
        if len(m) == 2:
            if len(s) < 1:
                return self.isMatch(s, p)
            if m[0] == s[0] or m[0] == ".":
                take_one = self.isMatch(s[1:], m + p)
                take_none = self.isMatch(s, p)
                self.solved[solved_key] = take_none or take_one
                return self.solved[solved_key]
            else:
                return self.isMatch(s, p)

        if len(s) == 0:
            if len(m) == 0:
                return True
            elif len(m) == 1:
                self.solved[solved_key] = False
                return self.solved[solved_key]
            else:
                return self.isMatch(s, p)

        if len(m) < 1:
            return len(s) == 0
        if len(m) == 1:
            if m == s[0] or m == ".":
                return self.isMatch(s[1:], p)
            else:
                self.solved[solved_key] = False
                return self.solved[solved_key]

    def split_on_next_pattern(self, pattern) -> tuple[str, str]:
        start_of_new = 1
        if len(pattern) > 1:
            if pattern[1] == "*":
                start_of_new = 2

        return pattern[:start_of_new], pattern[start_of_new:]
