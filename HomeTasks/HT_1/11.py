# 11. Write a script to remove duplicates from Dictionary.


def dict_count_values(d=None, value=None):
    if not d or not value:
        return None
    return list(d.values()).count(value)


sample = {1: 10, 2: 20, 3: 30, 4: 40, 5: 10, 6: 60, 7: 30, 8: 80}
result = sample.copy()

print("11. Write a script to remove duplicates from Dictionary.")
print("Sample Dictionary : {}".format(sample))
for key, value in sample.items():
    if dict_count_values(result, value) > 1:
        result.pop(key)

print("\nResult of removing: {}".format(result))
