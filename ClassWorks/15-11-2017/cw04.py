import random


lst = [5, 49, 20, 11, 4, 9, 3, 74, 90, 100]
for k in range(len(lst)):
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            lst[i], lst[i + 1] = lst[i + 1], lst[i]

print(lst)


def factorial(n):
    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))
