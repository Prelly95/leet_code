# 518. Coin Change II (Medium)
# https://leetcode.com/problems/coin-change-ii/

ENTRY = "change"

class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        self.MAX = amount + 1
        return self.dfs(coins,amount, 0)

    def dfs(self, coins, amount , start):

        if amount == 0:
            return 1
        elif amount < 0:
            return 0

        success = 0
        for ii in range(start, len(coins)):
            target = amount - coins[ii]
            success += self.dfs(coins, target, ii)
        return success




if __name__ == "__main__":
    s = Solution().change(4, [1, 2, 5])
    print(s)