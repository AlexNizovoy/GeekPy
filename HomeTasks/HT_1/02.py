# 2. Write a script to print out a set containing all the colours from color_list_1 which are not present in color_list_2.
#         Test Data :
#         color_list_1 = set(["White", "Black", "Red"])
#         color_list_2 = set(["Red", "Green"])
#         Expected Output :
#         {'Black', 'White'}

color_list_1 = input("#1 Enter a comma-and-space-separated items (leave it blank for default value): ")
if not len(color_list_1):
    color_list_1 = set(["White", "Black", "Red"])
else:
    color_list_1 = set(color_list_1.split(", "))
color_list_2 = input("#2 Enter a comma-and-space-separated items (leave it blank for default value): ")
if not len(color_list_2):
    color_list_2 = set(["Red", "Green"])
else:
    color_list_2 = set(color_list_2.split(", "))
print(color_list_1.difference(color_list_2))
