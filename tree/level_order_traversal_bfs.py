import unittest

from collections import deque


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def level_order_traversal(root):
    """
    Args:
     root(BinaryTreeNode_int32)
    Returns:
     list_list_int32
    """

    if not root:
        return []

    result = []
    q = deque()
    q.append(root)  # Enque

    while q:
        level_values = []
        level_size = len(q)

        for _ in range(level_size):
            node = q.popleft()  # Deque
            level_values.append(node.value)

            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        result.append(level_values)

    return result


class TestLevelOrderTraversal(unittest.TestCase):

    def test_empty_tree(self):
        # Test when the tree is empty
        root = None
        result = level_order_traversal(root)
        self.assertEqual(result, [])

    def test_single_node(self):
        # Test when the tree has only one node
        root = BinaryTreeNode(5)
        result = level_order_traversal(root)
        self.assertEqual(result, [[5]])

    def test_full_binary_tree(self):
        # Test a full binary tree
        root = BinaryTreeNode(1)
        root.left = BinaryTreeNode(2)
        root.right = BinaryTreeNode(3)
        root.left.left = BinaryTreeNode(4)
        root.left.right = BinaryTreeNode(5)
        root.right.left = BinaryTreeNode(6)
        root.right.right = BinaryTreeNode(7)
        result = level_order_traversal(root)
        self.assertEqual(result, [[1], [2, 3], [4, 5, 6, 7]])

    def test_unbalanced_tree(self):
        # Test an unbalanced tree
        root = BinaryTreeNode(1)
        root.left = BinaryTreeNode(2)
        root.left.left = BinaryTreeNode(3)
        result = level_order_traversal(root)
        self.assertEqual(result, [[1], [2], [3]])


if __name__ == '__main__':
    unittest.main()
