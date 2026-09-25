class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        m = len(matrix)
        n = len(matrix[0])

        top_index = 0
        left_index = 0
        bottom_index = m - 1
        right_index = n - 1
        res = []
        vector = 0
        cell_index = 0
        while cell_index < m * n:
            if vector == 0:
                for col in range(left_index, right_index + 1):
                    res.append(matrix[top_index][col])
                    cell_index += 1
                top_index += 1
                vector = 1
            elif vector == 1:
                for row in range(top_index, bottom_index + 1):
                    res.append(matrix[row][right_index])
                    cell_index += 1
                right_index -= 1
                vector = 2
            elif vector == 2:
                for col in range(right_index, left_index - 1, -1):
                    res.append(matrix[bottom_index][col])
                    cell_index += 1
                bottom_index -= 1
                vector = 3
            elif vector == 3:
                for row in range(bottom_index, top_index - 1, -1):
                    res.append(matrix[row][left_index])
                    cell_index += 1
                left_index += 1
                vector = 0

        return res
