# leetcode problem : https://leetcode.com/problems/valid-palindrome/description/
# 125. Valid Palindrome
# time  : O(n)
# space : O(1)
import unittest


class Solution:
    def is_palindrome(self, s: str) -> bool:
        s = s.lower()
        if len(s) == 0:
            return True
        l = 0
        r = len(s) - 1
        while l < r:
            while l < r and not self.isalphanum(s[l]):
                l += 1

            while l < r and not self.isalphanum(s[r]):
                r -= 1

            if s[l] != s[r]:
                return False
            l += 1
            r -= 1

        return True

    def isalphanum(self, c: str) -> bool:
        return ('a' <= c <= 'z' or '0' <= c <= '9')


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_is_palindrome(self):
        test_cases = [
            ("A man, a plan, a canal: Panama", True),
            ("race a car", False),
            ("", True),
            ("No 'x' in Nixon", True),
            ("Was it a car or a cat I saw?", True)
        ]

        for s, expected_output in test_cases:
            self.assertEqual(self.solution.is_palindrome(s), expected_output)


if __name__ == '__main__':
    unittest.main()
