def prnt_dots(n):
    for i in range(1, n + 1):
        print("." * i)
    for i in range(n - 1, 0, -1):
        print("." * i)


def prnt_2(n):
    i = 1
    x = 1
    while i:
        print("." * i)
        if i == n:
            x *= -1
        i += x


prnt_dots(5)

print("----")

prnt_2(5)
