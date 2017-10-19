n = input("Input a integer: ")
try:
    n = int(n)
except:
    print("Your input must be integer!")
    exit(1)

result = n + int(str(n)*2) + int(str(n)*3)

print("Result is ", result)