import re


def test1():
    regex = r"^\d{4}-\d{2}-\d{2}\s\d{,2}:\d{2}:\d{2}[.,]\d{3}\s\d+\s(WARNING|ERROR|CRITICAL).+$"
    eol = r"\n"

    test_str = open("test.log").read()

    matches = re.finditer(regex, test_str, re.MULTILINE)
    line_numbers = tuple(item.start() for item in re.finditer(eol, test_str))

    for match in matches:
        print("Match was found at line #{line} ({start}-{end}): {match}".format(line=line_numbers.index(match.end()) + 1, start=match.start(), end=match.end(), match=match.group()))
