# 14. Write a script to generate and print a dictionary that contains a number (between 1 and n) in the form (x, x*x).
#         Sample Dictionary ( n = 5) :
#         Expected Output : {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

print("14. Write a script to generate and print a dictionary that contains a number (between 1 and n) in the form (x, x*x).")
n = input("Input integer n > 1: ")
try:
    n = int(n)
except:
    print("It's not integer!")
    exit(1)
if n <= 1:
    print("Inputed integer less or equal than 1!")
    exit(1)

result = {}
for i in range(1, n + 1):
    result[i] = i * i

print("{}".format(result))
