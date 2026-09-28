# 226. Invert Binary Tree (Easy)
# https://leetcode.com/problems/invert-binary-tree/description/

ENTRY = "marshal_input"

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_level_order_list(cls, val_list, i=0):
        # Base case: if index is out of bounds or element is None
        if i >= len(val_list) or val_list[i] is None:
            return None
        
        # Create the root node for the current subtree
        root = TreeNode(val_list[i])
        
        # Recursively build the left and right subtrees
        root.left = cls.from_level_order_list(val_list, 2 * i + 1)
        root.right = cls.from_level_order_list(val_list, 2 * i + 2)
        
        return root

    def to_list(self) -> list:
        """Converts the tree into a level-ordered list."""
        if not self:
            return []

        result = []
        # Use a queue to track nodes as we visit level by level
        queue: TreeNode = [self]
        while queue:
            current = queue[0]
            queue = queue[1:]

            if current:
                result.append(current.val)
                # Queue children regardless of whether they are None
                queue.append(current.left)
                queue.append(current.right)
            else:
                result.append(None)

        # Trim trailing None values from the end of the list
        while result and result[-1] is None:
            result.pop()

        return result
    
class Solution:
    def marshal_input(self, root):
        tree = TreeNode.from_level_order_list(root)
        res = self.invertTree(tree)
        if res:
            return res.to_list()
        else:
            return []

    def invertTree(self, root: TreeNode | None) -> TreeNode | None:
        if not root:
            return None

        left_temp = root.left
        root.left = root.right
        root.right = left_temp

        root.left = self.invertTree(root.left)
        root.right = self.invertTree(root.right)
        return root

