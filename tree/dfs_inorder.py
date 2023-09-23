import unittest


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def inorder(root):
    """
    Args:
     root(BinaryTreeNode_int32)
    Returns:
     list_int32
    """
    result = []
    inorder_helper(root, result)
    return result


def inorder_helper(root, result):
    if not root:
        return

    inorder_helper(root.left, result)
    result.append(root.value)
    inorder_helper(root.right, result)


class TestBinaryTreeInorder(unittest.TestCase):
    def test_empty_tree(self):
        root = None
        self.assertEqual(inorder(root), [])

    def test_single_node_tree(self):
        root = BinaryTreeNode(5)
        self.assertEqual(inorder(root), [5])

    def test_full_tree(self):
        # Create a binary tree with the following structure:
        #        4
        #       / \
        #      2   6
        #     / \ / \
        #    1  3 5  7
        root = BinaryTreeNode(4)
        root.left = BinaryTreeNode(2)
        root.right = BinaryTreeNode(6)
        root.left.left = BinaryTreeNode(1)
        root.left.right = BinaryTreeNode(3)
        root.right.left = BinaryTreeNode(5)
        root.right.right = BinaryTreeNode(7)
        self.assertEqual(inorder(root), [1, 2, 3, 4, 5, 6, 7])


if __name__ == '__main__':
    unittest.main()
