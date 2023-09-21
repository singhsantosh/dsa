import unittest


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def preorder(root):
    """
    Args:
     root(BinaryTreeNode_int32)
    Returns:
     list_int32
    """

    result = []
    preorder_helper(root, result)
    return result


def preorder_helper(root, result):
    if not root:
        return

    result.append(root.value)
    preorder_helper(root.left, result)
    preorder_helper(root.right, result)


class TestBinaryTreePreorder(unittest.TestCase):
    def test_empty_tree(self):
        root = None
        self.assertEqual(preorder(root), [])

    def test_single_node_tree(self):
        root = BinaryTreeNode(5)
        self.assertEqual(preorder(root), [5])

    def test_full_tree(self):
        # Create a binary tree with the following structure:
        #        1
        #       / \
        #      2   3
        #     / \ / \
        #    4  5 6  7
        root = BinaryTreeNode(1)
        root.left = BinaryTreeNode(2)
        root.right = BinaryTreeNode(3)
        root.left.left = BinaryTreeNode(4)
        root.left.right = BinaryTreeNode(5)
        root.right.left = BinaryTreeNode(6)
        root.right.right = BinaryTreeNode(7)
        self.assertEqual(preorder(root), [1, 2, 4, 5, 3, 6, 7])


if __name__ == '__main__':
    unittest.main()
