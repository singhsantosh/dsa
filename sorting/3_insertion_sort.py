import unittest

"""
Asymptotic complexity in terms of size of 'arr' 'n':
* Time: O(n ^ 2).
* Auxiliary space: O(1).
* Total space: O(n).
"""


def insertion_sort(arr):
    """
    Args:
     arr(list_int32)
    Returns:
     list_int32
    """
    n = len(arr)

    for i in range(n):
        temp = arr[i]
        red = i - 1
        while red >= 0 and arr[red] > temp:
            arr[red + 1] = arr[red]
            red -= 1
        arr[red + 1] = temp

    return arr


class TestInsertionSort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(insertion_sort([]), [])

    def test_single_element(self):
        self.assertEqual(insertion_sort([5]), [5])

    def test_sorted_list(self):
        self.assertEqual(insertion_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_list(self):
        self.assertEqual(insertion_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_list(self):
        self.assertEqual(insertion_sort(
            [5, 8, 3, 9, 4, 1, 7]), [1, 3, 4, 5, 7, 8, 9])

    def test_duplicate_elements(self):
        self.assertEqual(insertion_sort([3, 5, 3, 4, 3]), [3, 3, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
