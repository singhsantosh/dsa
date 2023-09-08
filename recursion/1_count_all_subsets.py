import unittest


def count_all_subsets(n):
    if n == 0:
        return 1
    else:
        return 2 * count_all_subsets(n - 1)


class TestCoutAllSubsets(unittest.TestCase):

    def test_empty_set(self):
        self.assertEqual(count_all_subsets(0), 1)

    def test_set_with_one_element(self):
        self.assertEqual(count_all_subsets(1), 2)

    def test_set_with_two_element(self):
        self.assertEqual(count_all_subsets(2), 4)

    def test_set_with_ten_element(self):
        self.assertEqual(count_all_subsets(10), 1024)


if __name__ == "__main__":
    unittest.main()
