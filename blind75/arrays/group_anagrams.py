# https://leetcode.com/problems/group-anagrams/description/
# 49. Group Anagrams

import unittest
import collections
from typing import List

# time  : O(m * n) where m is the number of strings in the input and
# n is the average length of strings.
# space : O(m)


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # dict with key as count frequency and value as the string.
        key_freq_map = collections.defaultdict(list)

        for s in strs:
            count = [0] * 26

            for c in s:
                count[ord(c) - ord("a")] += 1

            key_freq_map[tuple(count)].append(s)

        return key_freq_map.values()


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_groupAnagrams(self):
        input_strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
        expected_output = [
            ["eat", "tea", "ate"],
            ["tan", "nat"],
            ["bat"]
        ]
        self.assertCountEqual(self.solution.groupAnagrams(
            input_strs), expected_output)


if __name__ == '__main__':
    unittest.main()
