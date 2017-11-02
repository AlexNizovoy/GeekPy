a = [1, 2, 3]
b = ["a", "b", "c"]
c = ["test", 20, 30]

# zip - iter with many syncro collections in one time
for (x, y, z) in zip(a, b, c):
    print(x, y, z)
