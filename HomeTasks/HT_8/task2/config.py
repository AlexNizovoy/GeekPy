import os
import logging

if __name__ == '__main__':
    exit()

APP_NAME = "Srapper_Del_Domains"
URL = "https://www.expireddomains.net/deleted-info-domains/"

OUT_DIR = "results"
STORAGE_FILE = OUT_DIR + os.sep + "storage.json"
EXPORT_FILE = OUT_DIR + os.sep + "result."  # runtime add file extension
LOG_FILE = OUT_DIR + os.sep + "scrapper.log"

if not os.path.isdir(OUT_DIR):
    os.mkdir(OUT_DIR)


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
