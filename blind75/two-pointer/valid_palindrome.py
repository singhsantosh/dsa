# leetcode problem : https://leetcode.com/problems/valid-palindrome/description/
# time  : O(n)
# space : O(1)
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


def main():
    s = Solution()
    test_cases = ["RACEACAR", "A", "ABCDEFGFEDCBA",
                  "ABC", "ABCBA", "ABBA", "RACEACAR"]
    for i in range(len(test_cases)):
        print("Test Case #", i + 1)
        print("-" * 100)
        print("The input string is '", test_cases[i], "' and the length of the string is ", len(
            test_cases[i]), ".", sep='')
        print("Is it a palindrome?.....", s.is_palindrome(test_cases[i]))
        print("-" * 100)


if __name__ == '__main__':
    main()
