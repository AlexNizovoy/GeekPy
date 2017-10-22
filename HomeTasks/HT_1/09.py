# 9. Write a script to remove an empty tuple(s) from a list of tuples.
#         Sample data: [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]
#         Expected output: [('',), ('a', 'b'), ('a', 'b', 'c'), 'd']


sample_data = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]
print("9. Write a script to remove an empty tuple(s) from a list of tuples.")
print("Sample data: {}".format(sample_data))
for i in range(len(sample_data) - 1, -1, -1):
    if not len(sample_data[i]):
        del sample_data[i]
print("Result of replacing: {}".format(sample_data))
