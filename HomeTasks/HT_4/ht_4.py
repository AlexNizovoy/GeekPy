import sys


def main():
    if sys.argv >= 1:
        try:
            log_file = open(sys.argv[1])
        except OSError as e:
            print("{0}: {1}".format(e.filename, e.strerror))
            exit(1)
        else:
            print("Unexpected error!")
            exit(2)
    else:
        name = input("Enter name of log-file (empty for default settings): ")
        if not name:
            name = "openerp-server.log"
        try:
            log_file = open(name)
        except OSError as e:
            print("{0}: {1}".format(e.filename, e.strerror))
            exit(1)
        else:
            print("Unexpected error!")
            exit(2)

    # datetime.datetime.strptime("2017-11-10 12:29:13,413", "%Y-%m-%d %H:%M:%S.%f")
