import unittest


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def delete_from_bst_recursive(root, values_to_be_deleted):
    """
    Args:
     root(BinaryTreeNode)
     values_to_be_deleted(list)
    Returns:
     BinaryTreeNode
    """
    # Helper function to delete a node from the BST
    def delete_node(node, value):
        if not node:
            return None  # If the node is None, return None (base case)

        # Recursive case: traverse the tree to find the node to delete
        if value < node.value:
            node.left = delete_node(node.left, value)
        elif value > node.value:
            node.right = delete_node(node.right, value)
        else:
            # Node with the given value found, perform deletion
            if not node.left:
                return node.right  # If no left child, replace with right child
            elif not node.right:
                return node.left  # If no right child, replace with left child
            else:
                # Node has both left and right children
                # Find the in-order successor (minimum value in the right subtree)
                successor = find_min(node.right)
                node.value = successor.value  # Copy the successor's value
                # Delete the successor node
                node.right = delete_node(node.right, successor.value)
        return node

    # Helper function to find the minimum value node in a BST
    def find_min(node):
        while node.left:
            node = node.left
        return node

    # Iterate through the list of values to be deleted and delete them from the BST
    for value in values_to_be_deleted:
        root = delete_node(root, value)

    return root  # Return the root of the modified BST


def delete_from_bst(root, values_to_be_deleted):
    """
    Args:
     root(BinaryTreeNode_int32)
     values_to_be_deleted(list_int32)
    Returns:
     BinaryTreeNode_int32
    """

    for key in values_to_be_deleted:
        root = delete_from_bst_helper(root, key)
    return root


def delete_from_bst_helper(root: TreeNode, key: int):
    curr = root
    prev = None
    while curr:
        if key == curr.value:
            break
        elif key < curr.value:
            prev = curr
            curr = curr.left
        else:  # key > curr.value
            prev = curr
            curr = curr.right

    if curr is None:
        return root
    # case 1 - curr node is a leaf
    if curr.left is None and curr.right is None:
        if prev is None:  # one-node tree
            return None
        if curr is prev.left:
            prev.left = None
        else:  # curr is prev.right
            prev.right = None
        return root

    # case 2 - curr node has one child
    child = None
    if curr.left is None and curr.right is not None:
        child = curr.right
    if curr.right is None and curr.left is not None:
        child = curr.left
    if child is not None:
        if prev is None:
            root = child
            return root
        if curr is prev.left:
            prev.left = child
        else:  # curr is prev.right
            prev.right = child

        return root

    # case 3 - curr node has two child
    if curr.left is not None and curr.right is not None:
        succ = curr.right
        prev = curr
        while succ.left is not None:
            prev = succ
            succ = succ.left

        curr.value = succ.value
        if succ is prev.left:
            prev.left = succ.right
        else:  # succ is prev.right
            prev.right = succ.right
        return root


class TestDeleteFromBST(unittest.TestCase):
    def setUp(self):
        # Create a sample BST for testing
        self.root = TreeNode(5)
        self.root.left = TreeNode(3)
        self.root.right = TreeNode(8)
        self.root.left.left = TreeNode(2)
        self.root.left.right = TreeNode(4)
        self.root.right.left = TreeNode(7)
        self.root.right.right = TreeNode(9)

    def test_delete_leaf_node(self):
        # Delete a leaf node (2)
        values_to_delete = [2]
        delete_from_bst(self.root, values_to_delete)
        self.assertIsNone(self.root.left.left)

    def test_delete_node_with_one_child(self):
        # Delete a node (3) with one child
        values_to_delete = [3]
        delete_from_bst(self.root, values_to_delete)
        self.assertEqual(self.root.left.value, 4)

    def test_delete_node_with_two_children(self):
        # Delete a node (5) with two children
        values_to_delete = [5]
        delete_from_bst(self.root, values_to_delete)
        self.assertEqual(self.root.value, 7)

    def test_delete_nonexistent_value(self):
        # Attempt to delete a nonexistent value (6)
        values_to_delete = [6]
        delete_from_bst(self.root, values_to_delete)
        # The tree should remain unchanged
        self.assertEqual(self.root.value, 5)
        self.assertEqual(self.root.right.left.value, 7)

    def test_delete_multiple_values(self):
        # Delete multiple nodes (2, 3, 9)
        values_to_delete = [2, 3, 9]
        delete_from_bst(self.root, values_to_delete)
        self.assertIsNone(self.root.left.left)
        self.assertIsNone(self.root.left)
        self.assertIsNone(self.root.right.right)


if __name__ == '__main__':
    unittest.main()
