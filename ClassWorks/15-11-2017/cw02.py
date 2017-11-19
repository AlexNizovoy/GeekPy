import argparse
arg_parser = argparse.ArgumentParser(description='Great Description To Be Here')
arg_parser.add_argument("--day", "-d", type=int, required=True,  default=7, help="number of days")
arg_parser.add_argument("--dir", "-p", type=str, default='.', help="DIR name")
options = arg_parser.parse_args()
print(options.day)
