class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        count_to_sum = {v: 1 for v in coins}
        count_to_sum[0] = 0
        coins = sorted(coins)
        coins.reverse()
        self.dfs(coins, amount, 0, count_to_sum, 0)
        if amount in count_to_sum:
            return count_to_sum[amount]
        else:
            return -1

    def dfs(self, coins, amount, current_sum, depth_to_sum, depth):
        depth += 1
        for coin in coins:
            current_sum += coin
            target = amount - current_sum

            if target in depth_to_sum:
                depth_to_target = depth + depth_to_sum[target]
                if amount in depth_to_sum:
                    depth_to_sum[amount] = min(depth_to_target, depth_to_sum[amount])
                else:
                    depth_to_sum[amount] = depth_to_target
                    break

            if current_sum in depth_to_sum:
                depth_to_sum[current_sum] = min(depth, depth_to_sum[current_sum])
            else:
                depth_to_sum[current_sum] = depth

            if target == 0:
                break
            if target < 0:
                current_sum -= coin
                break

            self.dfs(coins, amount, current_sum, depth_to_sum, depth)
            current_sum -= coin
