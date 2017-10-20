# 6. Write a script to check whether a specified value is contained in a group of values.
#         Test Data :
#         3 -> [1, 5, 8, 3] : True
#         -1 -> (1, 5, 8, 3) : False

values_list = input("#1 Enter a space-separated group of values (leave it blank for default value): ")
if not len(values_list):
    values_list = "1 5 8 3".split(" ")
else:
    values_list = values_list.split(" ")

# run down for values_list, delete empty elements, try convert first into int, then into float. If fail - keep str.
for i in range(len(values_list)-1, -1, -1):
    if values_list[i] == "":
        del values_list[i]
    else:
        try:
            values_list[i] = int(values_list[i])
        except:
            try:
                values_list[i] = float(values_list[i])
            except:
                pass

chk = input("Enter a value to find in group: ")
if not len(chk):
    chk = 0
else:
    try:
        chk = int(chk)
    except:
        try:
            chk = float(chk)
        except:
            pass

print("{0} --> {1} : {2}".format(chk, values_list, chk in values_list))
