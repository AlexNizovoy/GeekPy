import os


class Cfg_item(object):
    """docstring for Cfg_item"""
    def __init__(self, tag, case, value):
        self.tag = tag
        self.case = case
        self.value = value


class Cfg(object):
    """Config generator for dot-notation access to settings"""
    url = "http://quotes.toscrape.com/"

    out_dir = "results"
    storage_file = out_dir + os.sep + "storage.dat"
    quote = Cfg_item("div", "class", "quote")
    text = Cfg_item("span", "itemprop", "text")
    author = Cfg_item("small", "itemprop", "author")
    tag = Cfg_item("div", "class", "tags")

    quote_sel = "div.quote"

    def __init__(self):
        if not os.path.isdir(self.out_dir):
            os.mkdir(self.out_dir)


if __name__ == '__main__':
    exit()
