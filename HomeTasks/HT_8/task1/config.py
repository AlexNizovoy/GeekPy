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
    app_name = "Srapper"
    url = "http://quotes.toscrape.com/"

    out_dir = "results"
    storage_file = out_dir + os.sep + "storage.json"
    export_file = out_dir + os.sep + "result."  # runtime add file extension
    log_file = out_dir + os.sep + "scrapper.log"

    quote = Cfg_item("div", "class", "quote")
    text = Cfg_item("span", "itemprop", "text")
    author = Cfg_item("small", "itemprop", "author")
    tag = Cfg_item("div", "class", "tags")

    quote_sel = "div.quote"

    def __init__(self):
        if not os.path.isdir(self.out_dir):
            os.mkdir(self.out_dir)


cfg = Cfg()
# init logging
logger = logging.getLogger(cfg.app_name)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(cfg.log_file)
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
err = logging.FileHandler(cfg.log_file + '_errors.log')
err.setFormatter(fmt)
err.setLevel(logging.ERROR)
logger.addHandler(err)

if __name__ == '__main__':
    exit()
