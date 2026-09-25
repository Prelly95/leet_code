class Solution:
    def longestPalindrome(self, s: str) -> str:
        # niaeve solution
        pal = ""
        str_len = len(s)
        if str_len == 1:
            return s

        step_left = 0
        step_right = 0
        for ii in range(1, str_len):
            left_cursor = ii - step_left
            right_cursor = ii + step_right
            while s[left_cursor] == s[right_cursor]:
                pal = self.set_pal(s[left_cursor: right_cursor + 1], pal)
                left_cursor -= 1
                right_cursor += 1

                if left_cursor < 0 or right_cursor >= len(s):
                    break

            left_cursor = ii - step_left - 1
            right_cursor = ii + step_right
            while s[left_cursor] == s[right_cursor]:
                pal = self.set_pal(s[left_cursor: right_cursor + 1], pal)
                left_cursor -= 1
                right_cursor += 1

                if left_cursor < 0 or right_cursor >= len(s):
                    break
        return pal

    def set_pal(self, suspect, current):
        return suspect if len(suspect) > len(current) else current
