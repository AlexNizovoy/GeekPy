# 8. Write a script to replace last value of tuples in a list.
#         Sample list: [(10, 20, 40), (40, 50, 60), (70, 80, 90)]
#         Expected Output: [(10, 20, 100), (40, 50, 100), (70, 80, 100)]

import json


def err_usage(msg="", e=None):
    print('ERROR: {}'.format(msg))
    if e:
        raise e
    exit(1)


def parse_list(lst):
    """Parsing string like [(1, 2, 3), (4, 5, 6, 7), (10, 3, 66)] - because json.loads() don't convert tuples"""
    result = []
    lst = lst.replace(" ", "").replace("[", "").replace("]", "")
    lst = lst.replace("(", "[").replace(")", "]").replace("],[", "], [")
    lst = lst.split(", ")
    for i in lst:
        result.append(tuple(json.loads(i)))
    return result

strings_list = input("Input a list with tuples (JSON) \nor leave it blank for default value [(10, 20, 40), (40, 50, 60), (70, 80, 90)]: ")
if not len(strings_list):
    strings_list = "[(10, 20, 40), (40, 50, 60), (70, 80, 90)]"
try:
    strings_list = parse_list(strings_list.replace("\'", "\""))
except:
    err_usage("Invalid input list! Try again.")

n = input("Input a value to replace last value (JSON): ")
try:
    replace_val = []
    n = json.loads(n.replace("\'", "\""))
    replace_val.append(n)
    replace_val = tuple(replace_val)
except Exception as e:
    err_usage("Invalid input value! Try again.", e)

result = []
for i in strings_list:
    result.append(i[:-1] + replace_val)

print("\nResult of replacing:", result)
