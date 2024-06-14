from typing import List, Optional
from collections import deque
import re

# Definition for a binary tree node.
class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.val} {self.left} {self.right})"

class Tree:
    def splitDfsOutput(self, traversal: str) -> List[str]:
        return re.findall(r'(-*)(\d+)', traversal)

    def Recover(self, traversal: str) -> Optional[Node]:
        if not traversal:
            return None

        stack = []
        root = None
        for depth, val_str in self.splitDfsOutput(traversal):
            val = int(val_str)
            node = Node(val)

            if not stack:
                root = node
            else:
                while len(stack) > len(depth):
                    stack.pop()
                if stack:
                    parent = stack[-1]
                    if not parent.left:
                        parent.left = node
                    else:
                        parent.right = node

            stack.append(node)

        return root

    def level_order_traversal(self,root):
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val if node else None)

                if node and node.left!=None:
                    queue.append(node.left)
                    queue.append(node.right)

            result.extend(current_level)

        return result

inp = input()
tree = Tree()
r = tree.Recover(inp)

# Perform level-order traversal
result = tree.level_order_traversal(r)
if result[-1] == None:
    result = result[:-1]

print(str(result).replace("None","null"))
