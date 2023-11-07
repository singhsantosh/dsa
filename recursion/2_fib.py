def find_fibonacci(n):
    return helper(n, 0, 1)


def helper(n, a, b):
    if n == 0:
        return a
    else:
        return helper(n - 1, b, a + b)


print(find_fibonacci(3))
