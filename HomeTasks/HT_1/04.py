# 4. Write a script to concatenate N strings.

import sys


result = ""

# verify command line arguments for strings to concatenate
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        result += sys.argv[i]

while True:
    s = input("Input string to concatenate (leave it blank to finish): ")
    if not len(s):
        break
    result += s

print("\nResult of concatenate strings: ", result)
