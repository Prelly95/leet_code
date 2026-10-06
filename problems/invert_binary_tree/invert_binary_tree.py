# 226. Invert Binary Tree (Easy)
# https://leetcode.com/problems/invert-binary-tree/description/

from harness.structures import TreeNode


class Solution:
    def invertTree(self, root: TreeNode | None) -> TreeNode | None:
        if not root:
            return None

        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
