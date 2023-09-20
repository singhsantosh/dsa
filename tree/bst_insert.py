

class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def build_a_bst(values):
    """
    Args:
     values(list_int32)
    Returns:
     BinaryTreeNode_int32
    """
    root = None

    for value in values:
        root = insert(root, value)

    return root


def insert(root, value):

    newNode = BinaryTreeNode(value)
    if not root:
        return newNode

    prev = None
    curr = root
    while curr:
        if value == curr.value:
            return root
        elif value < curr.value:
            prev = curr
            curr = curr.left
        else:
            prev = curr
            curr = curr.right

    if value < prev.value:
        prev.left = newNode
    else:
        prev.right = newNode

    return root


root = build_a_bst([7, 5, 9])
print(f"root = {root.value}")
print(f"left = {root.left.value}")
print(f"left = {root.right.value}")
