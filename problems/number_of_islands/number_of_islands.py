# 200. Number of Islands (Medium)
# https://leetcode.com/problems/number-of-islands/

ENTRY = "numIslands"

class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        searched = set()
        islands = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                coordinates = f"{row}, {col}"
                if coordinates not in searched:
                    searched.add(coordinates)
                    if grid[row][col] == "1":
                        islands += 1
                        self.explore_island(grid, row+1, col, searched)
                        self.explore_island(grid, row-1, col, searched)
                        self.explore_island(grid, row, col+1, searched)
                        self.explore_island(grid, row, col-1, searched)
        return islands

    def explore_island(self, grid, row, col, searched):
        if row > len(grid)-1 or row < 0 or col > len(grid[0])-1 or col < 0:
            return
        if grid[row][col] == "0":
            return

        coordinates = f"{row}, {col}"
        if coordinates in searched:
            return
        searched.add(coordinates)

        self.explore_island(grid, row+1, col, searched)
        self.explore_island(grid, row-1, col, searched)
        self.explore_island(grid, row, col+1, searched)
        self.explore_island(grid, row, col-1, searched)