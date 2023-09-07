import unittest
import random

"""
Asymptotic complexity in terms of size of 'arr' 'n':
* Time: O(n * log n).
* Auxiliary space: O(n).
* Total space: O(n).
"""


def quick_sort(arr):
    """
    Args:
     arr(list_int32)
    Returns:
     list_int32
    """
    helper(arr, 0, len(arr) - 1)
    return arr


def helper(arr, start, end):
    # Leaf worker node
    if start >= end:
        return

    # Internal worker node
    pivot_index = random.randint(start, end)
    # swap element in pivot_index with that at start index.
    arr[start], arr[pivot_index] = arr[pivot_index], arr[start]

    # Lomuto's partitioning
    smaller = start
    for bigger in range(start + 1, end + 1):
        if arr[bigger] < arr[start]:
            smaller += 1
            arr[smaller], arr[bigger] = arr[bigger], arr[smaller]
    arr[start], arr[smaller] = arr[smaller], arr[start]

    helper(arr, start, smaller - 1)
    helper(arr, smaller + 1, end)


class TestInsertionSort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(quick_sort([]), [])

    def test_single_element(self):
        self.assertEqual(quick_sort([5]), [5])

    def test_sorted_list(self):
        self.assertEqual(quick_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_list(self):
        self.assertEqual(quick_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_list(self):
        self.assertEqual(quick_sort(
            [5, 8, 3, 9, 4, 1, 7]), [1, 3, 4, 5, 7, 8, 9])

    def test_duplicate_elements(self):
        self.assertEqual(quick_sort([3, 5, 3, 4, 3]), [3, 3, 3, 4, 5])


if __name__ == "__main__":
    print("Testing merge sort")
    unittest.main()
