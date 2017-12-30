import os
import logging

if __name__ == '__main__':
    exit()

APP_NAME = "Srapper_Del_Domains"
URL = "https://www.expireddomains.net/deleted-info-domains/"
URL_IF_LOGGED_IN = "https://member.expireddomains.net/domains/expiredinfo/"

OUT_DIR = "results"
STORAGE_FILE = OUT_DIR + os.sep + "storage.json"
EXPORT_FILE = OUT_DIR + os.sep + "result."  # runtime add file extension
LOG_FILE = OUT_DIR + os.sep + "scrapper.log"

# During parsing title will be filled
title = ""

# Set it to True for load and export previous saved domains from storage
EXPORT_ONLY = False

if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0",
}
USER = "PPKzavod"
PASSWORD = "12345678"


# init logging
def create_logger():
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILE)
    fmt_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    fmt = logging.Formatter(fmt_str)
    fh.setFormatter(fmt)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    # create console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    # add error log
    err = logging.FileHandler(LOG_FILE + '_errors.log')
    err.setFormatter(fmt)
    err.setLevel(logging.ERROR)
    logger.addHandler(err)
    return logger

logger = create_logger()
