# 1 .Write a script which accepts a sequence of comma-separated numbers from user and generate a list and a tuple with those numbers.
# 		Sample data : 1, 5, 7, 23
# 		Output :
# 		List : [‘1', ' 5', ' 7', ' 23']
# 		Tuple : (‘1', ' 5', ' 7', ' 23')
sequence = input("Enter a comma-separated numbers: ")
lst = sequence.split(",")
tpl = tuple(lst)
print("List:", lst)
print("Tuple:", tpl)
