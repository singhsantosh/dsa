import unittest

"""
Asymptotic complexity in terms of size of 'arr' 'n':
* Time: O(n ^ 2).
* Auxiliary space: O(1).
* Total space: O(n).
"""


def merge_sort(arr):
    """
    Args:
     arr(list_int32)
    Returns:
     list_int32
    """
    n = len(arr) - 1
    if n < 0:
        return []
    helper(arr, 0, len(arr)-1)
    return arr


def helper(arr, start, end):
    # Leaf worker node
    if start == end:
        return

    # Internal worker node
    mid = (start + end) // 2
    helper(arr, start, mid)
    helper(arr, mid + 1, end)

    # merge sorted half
    i = start
    j = mid + 1
    aux = []
    while i <= mid and j <= end:
        if arr[i] <= arr[j]:
            aux.append(arr[i])
            i += 1
        else:  # arr[j] < arr[i]
            aux.append(arr[j])
            j += 1

    while i <= mid:
        aux.append(arr[i])
        i += 1

    while j <= end:
        aux.append(arr[j])
        j += 1

    arr = aux

    return


class TestInsertionSort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_element(self):
        self.assertEqual(merge_sort([5]), [5])

    def test_sorted_list(self):
        self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_list(self):
        self.assertEqual(merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_list(self):
        self.assertEqual(merge_sort(
            [5, 8, 3, 9, 4, 1, 7]), [1, 3, 4, 5, 7, 8, 9])

    def test_duplicate_elements(self):
        self.assertEqual(merge_sort([3, 5, 3, 4, 3]), [3, 3, 3, 4, 5])


if __name__ == "__main__":
    print("Testing merge sort")
    unittest.main()
