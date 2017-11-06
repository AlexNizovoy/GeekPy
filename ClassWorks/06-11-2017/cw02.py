import re

pattern = r"[0-9]+"

number_re = re.compile(pattern)

print(number_re.findall("122 234 65487"))

# regex.com
# regex101.com
