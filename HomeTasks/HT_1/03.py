# 3. Write a script to sum of the first n positive integers.

integers_list = input("#1 Enter a space-separated integers (leave it blank for default value): ")
if not len(integers_list):
    integers_list = "1 -1 1 1 -1 1 1 -1 1 1 -1 1 1 1".split(" ")
else:
    integers_list = integers_list.split(" ")
for i in range(len(integers_list)):
    try:
        # if used multiply spaces while entering a sequence, after split() will be some empty elements in list
        if len(integers_list[i]):
            integers_list[i] = int(integers_list[i])
    except Exception as e:
        print("You enter not integer!")
        # raise e
        exit(1)

n = input("#2 Enter a count of first positive integers (leave it blank for default value 5): ")
if not len(n):
    n = 5
else:
    try:
        n = int(n)
    except:
        print("You enter not integer!")
        exit(1)
    if n <= 0:
        print("'N' must be a positive!")
        exit(2)

result = 0
count = n
for i in integers_list:
    if i == "":
        # skip empty elements
        continue
    if i > 0:
        result += i
        count -= 1
        if count == 0:
            break

print("Sum of the first {} positive integers: {}".format(n, result))
