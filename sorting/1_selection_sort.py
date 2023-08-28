import unittest

"""
Asymptotic complexity in terms of size of `arr` `n`:
* Time: O(n ^ 2).
* Auxiliary space: O(1).
* Total space: O(n).
"""


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # Assume the smallest element is the current element
        min_index = i
        # Iterate through the unsorted part of the list
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                # Update the min_index if a smaller element is found
                min_index = j
        # Swap the found minimum element with the first element of the unsorted part
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


class TestSelectionSort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(selection_sort([]), [])

    def test_single_element(self):
        self.assertEqual(selection_sort([5]), [5])

    def test_sorted_list(self):
        self.assertEqual(selection_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_list(self):
        self.assertEqual(selection_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_list(self):
        self.assertEqual(selection_sort([3, 5, 2, 4, 1]), [1, 2, 3, 4, 5])

    def test_duplicate_elements(self):
        self.assertEqual(selection_sort([3, 5, 3, 4, 3]), [3, 3, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
