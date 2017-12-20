import os
import logging


class Cfg_item(object):
    """docstring for Cfg_item"""
    def __init__(self, tag, case, value):
        self.tag = tag
        self.case = case
        self.value = value


class Cfg(object):
    """Config generator for dot-notation access to settings"""
    APP_NAME = "Srapper"
    URL = "http://quotes.toscrape.com/"

    OUT_DIR = "results"
    STORAGE_FILE = OUT_DIR + os.sep + "storage.json"
    EXPORT_FILE = OUT_DIR + os.sep + "result."  # runtime add file extension
    LOG_FILE = OUT_DIR + os.sep + "scrapper.log"

    quote = Cfg_item("div", "class", "quote")
    text = Cfg_item("span", "itemprop", "text")
    author = Cfg_item("small", "itemprop", "author")
    tag = Cfg_item("div", "class", "tags")

    quote_sel = "div.quote"

    def __init__(self):
        if not os.path.isdir(self.OUT_DIR):
            os.mkdir(self.OUT_DIR)


cfg = Cfg()
# init logging
logger = logging.getLogger(cfg.APP_NAME)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(cfg.LOG_FILE)
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(fmt)
fh.setLevel(logging.INFO)
logger.addHandler(fh)
# create console handler
ch = logging.StreamHandler()
ch.setFormatter(fmt)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
# add error log
err = logging.FileHandler(cfg.LOG_FILE + '_errors.log')
err.setFormatter(fmt)
err.setLevel(logging.ERROR)
logger.addHandler(err)

if __name__ == '__main__':
    exit()
