# 121. Best Time to Buy and Sell Stock (Easy)
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

from typing import List

ENTRY = "maxProfit"


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        buy = prices[0]
        sell = prices[0]
        profit = 0
        for v in prices:
            if v <= buy:
                # reset
                buy = v
                sell = v
            elif v > sell:
                sell = v
                temp_p = sell - buy
                profit = max(temp_p, profit)
        return profit
