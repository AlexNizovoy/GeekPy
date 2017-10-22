# 7. Write a script to concatenate all elements in a list into a string and print it.

import sys
import json


def err_usage(msg=""):
    print('Use program: python 07.py "[\'list\', \'of\', \'strings\', \'to\', \'concatenate\']"', '\n{}'.format(msg))
    print("\n(JSON-like notation in double-quotas. Strings in single-quotas)")
    exit(1)

# verify command line arguments for strings to concatenate
if len(sys.argv) != 2:
    err_usage("err_args")
try:
    strings_list = json.loads(sys.argv[1].replace("\'", "\""))
except:
    err_usage("err_json")

print("\nResult of concatenate strings:", "".join(strings_list))
