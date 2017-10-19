from math import pi


radius = input("Input radius of a circle:")
try:
    radius = float(radius)
except:
    print("Your input must be float!")
    exit(1)
square = pi * radius ** 2

print("Square of a circle:", square)