# 10. Write a script to concatenate following dictionaries to create a new one.
#         Sample Dictionary :
#         dic1={1:10, 2:20}
#         dic2={3:30, 4:40}
#         dic3={5:50,6:60}
#         Expected Result : {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}


def dict_concatenate(*args):
    result = {}
    for i in args:
        for key, val in i.items():
            result[key] = val
    return result


dic1 = {1: 10, 2: 20}
dic2 = {3: 30, 4: 40}
dic3 = {5: 50, 6: 60}

print("10. Write a script to concatenate following dictionaries to create a new one.")
print("""Sample Dictionary :
dic1 = {1: 10, 2: 20}
dic2 = {3: 30, 4: 40}
dic3 = {5: 50, 6: 60}""")
result = dict_concatenate(dic1, dic2, dic3)
print("\nResult of concatenate: {}".format(result))
