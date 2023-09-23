import unittest


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def postorder(root):
    """
    Args:
     root(BinaryTreeNode_int32)
    Returns:
     list_int32
    """
    result = []
    postorder_helper(root, result)
    return result


def postorder_helper(root, result):
    if not root:
        return

    postorder_helper(root.left, result)
    postorder_helper(root.right, result)

    result.append(root.value)


class TestBinaryTreePostorder(unittest.TestCase):
    def test_empty_tree(self):
        root = None
        self.assertEqual(postorder(root), [])

    def test_single_node_tree(self):
        root = BinaryTreeNode(5)
        self.assertEqual(postorder(root), [5])

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
        self.assertEqual(postorder(root), [1, 3, 2, 5, 7, 6, 4])


if __name__ == '__main__':
    unittest.main()
