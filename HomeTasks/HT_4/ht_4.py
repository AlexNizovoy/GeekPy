import sys
import os
import re
import csv
import time
# from datetime import datetime


def parse_single_log_line(text):
    """parse_single_log_line(text):

        Parsing single line of log-file and return dict with next fields:
        {
            "date_time"
            "marker"
            "description"
        }

        Like:
        parse_single_log_line("2017-11-10 11:29:47,177 11516 ERROR None openerp.http: Exception during JSON request handling.") -->
            {
                "date_time": "2017-11-10 11:29:47",
                "marker": "ERROR",
                "description": "openerp.http: Exception during JSON request handling."
            }
    """
    regex_date_time = r"^\d{4}-\d{2}-\d{2}\s\d{,2}:\d{2}:\d{2}"
    regex_marker = r"(WARNING|ERROR|CRITICAL)"
    regex_splitter = r"(WARNING|ERROR|CRITICAL)\s\S+\s"

    date_time = re.search(regex_date_time, text).group()
    # date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    marker = re.search(regex_marker, text).group()
    description = text[re.search(regex_splitter, text).end():]

    return {
        "date_time": date_time,
        "marker": marker,
        "description": description
    }


def parse_log(text):
    """parse_log(text):

        Return list with parsed log-text.
    """
    regex = r"^\d{4}-\d{2}-\d{2}\s\d{,2}:\d{2}:\d{2}[.,]\d{3}\s\d+\s(WARNING|ERROR|CRITICAL).+$"
    eol = r"\n"

    matches = re.finditer(regex, text, re.MULTILINE)
    line_numbers = tuple(item.start() for item in re.finditer(eol, text))

    result = []

    for match in matches:
        tmp = parse_single_log_line(match.group())
        result.append({
            "line_id": line_numbers.index(match.end()) + 1,
            "marker": tmp.get("marker"),
            "date_time": tmp.get("date_time"),
            "description": tmp.get("description")
            })

    return result


def unique_descriptions(lst):
    """unique_descriptions(lst):

        Get list with dict elements:
        {
            "line_id"
            "date_time"
            "marker"
            "description"
        }
        and return list with "description"-unique elements:
        {
            "count"
            "date_time"
            "marker"
            "description"
        }
        where "date_time" is the first available record
    """
    result = []
    for item in lst:
        is_unique = True
        for chk in result:
            if item["description"] == chk["description"]:
                chk["count"] += 1
                is_unique = False
                break
        if is_unique:
            tmp = {"count": 1}
            tmp.update(item)
            del tmp["line_id"]
            result.append(tmp)
    return result


def main():
    if len(sys.argv) >= 2:
        if os.path.isfile(sys.argv[1]):
            name = sys.argv[1]
        else:
            print("File {filename} not exist!".format(filename=sys.argv[1]))
            exit(1)
    else:
        name = input("Enter name of log-file (empty for default settings): ")
        if not name:
            name = "openerp-server.log"
        if not os.path.isfile(name):
            print("File {filename} not exist!".format(filename=name))
            exit(1)

    print("Open and parsing log-file...", end="")
    t0 = time.time()
    with open(name) as log_file:
        parsed = parse_log(log_file.read())
    t1 = time.time()
    print("Done. ({0} ms)".format((t1 - t0) * 1000))

    if not os.path.isdir("reports"):
        os.mkdir("reports")
        print("Make 'reports/' dir.")

    print("Extracting not INFO records... ", end="")
    t0 = time.time()
    with open("reports/all_data.csv", "w") as all_data:
        writer = csv.writer(all_data)
        for line in parsed:
            writer.writerow([line["line_id"], line["marker"], line["date_time"], line["description"]])
    t1 = time.time()
    print("Done. ({0} ms)".format((t1 - t0) * 1000))

    print("Combine unique records...", end="")
    t0 = time.time()
    with open("reports/unique.csv", "w") as unique:
        writer = csv.writer(unique)
        for line in unique_descriptions(parsed):
            writer.writerow([line["count"], line["marker"], line["date_time"], line["description"]])
    t1 = time.time()
    print("Done. ({0} ms)\nAll operations complete.".format((t1 - t0) * 1000))


if __name__ == '__main__':
    main()
