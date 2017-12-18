# берете і парсите ось цей сайт - http://quotes.toscrape.com/
# 1. Фомар отримання даних наступний:
# text
# author:
#    url
#    author-title
#    born_date
#    born_place
#    about
# tags:
#    tag_name
#    tag_url
#    text
#    author
#    author_url
# вище зразок одного запису.
# Потрібно отримати всі таки записи з сайту
# Потрібно отримати список всіх авторів з даними про них з сайту
# Потрібно отримати список всіх тегів
# Це все записати в: JSON, XLS, TXT, CSV файли (для самих крутих в sqlite)
# Також повинен бути механізм отримання інформації лише про одного або список
# вказаних авторів по айдішнику автора(придумайте як це зробити)
# Використовувати requests+bs4
# Домашка рахується зарахованою якщо ви даєте посилання на репозиторій де є
# всі необходні скрипти, отримані данні + є інструкція як користуватись вашим
# парсером!
import pickle
import json
import requests
import os
import time
from bs4 import BeautifulSoup
from win32com.client import Dispatch
import sqlite3

from config import logger
from config import cfg


def concat_urls(base_url, add_url):
    if base_url[-1] == "/" and add_url[0] == "/":
        return "{}{}".format(base_url[:-1], add_url)
    else:
        return "{}{}".format(base_url, add_url)


class Quotes(object):
    """adding authors to temporary storage"""
    _quotes = []
    counter = 0

    def __init__(self):
        pass

    def add(self, text, author_id, author_title, author_url, tags, _id=None):
        args = locals().copy()
        args.pop("self")

        # Check for existing record
        quote = self.get(text)
        if quote and _id is None:
            return quote.get("_id")
        elif quote and _id:
            Quotes._quotes[quote.get("_id") - 1].update(args)
            return quote.get("_id")

        # create new record
        Quotes.counter += 1
        args["_id"] = Quotes.counter
        Quotes._quotes.append(args)
        return Quotes.counter

    def get(self, text):
        for quote in Quotes._quotes:
            if quote.get("text") == text:
                return quote
        return None

    def get_all(self):
        return Quotes._quotes


class Authors(object):
    """adding authors to temporary storage"""
    _authors = []
    counter = 0

    def __init__(self):
        pass

    def add(self, author_title, url, _id=None, born_date=None, born_place=None, about=None):
        args = locals().copy()
        # remove unneccessary and empty arguments
        args.pop("self")

        # Check for existing author
        author = self.get(author_title)
        if author and _id is None:
            return author.get("_id")
        # If author exist and exist updates for him - apply them
        elif author and _id:
            Authors._authors[author.get("_id") - 1].update(args)
            return author.get("_id")

        # or create new record
        Authors.counter += 1
        args["_id"] = Authors.counter
        Authors._authors.append(args)

        return Authors.counter

    def get(self, author_title=None, _id=None):
        if not author_title and not _id:
            return None
        for author in Authors._authors:
            if author_title and author.get("author_title") == author_title:
                return author
            elif _id and author.get("_id") == _id:
                return author
        return None

    def get_all(self):
        return Authors._authors


class Tags(object):
    """adding authors to temporary storage"""
    _tags = []
    counter = 0

    def __init__(self):
        pass

    def add(self, tag_name, url, _id=None, quotes=None):
        args = locals().copy()
        # remove unneccessary and empty arguments
        args.pop("self")

        # Check for existing record
        tag = self.get(tag_name)
        if tag and _id is None:
            return tag.get("_id")
        # If tag exist and exist updates for him - apply them
        elif tag and _id:
            Tags._tags[tag.get("_id") - 1].update(args)
            return tag.get("_id")

        # or create new record
        Tags.counter += 1
        args["_id"] = Tags.counter
        Tags._tags.append(args)
        return Tags.counter

    def get(self, tag_name):
        for tag in Tags._tags:
            if tag.get("tag_name") == tag_name:
                return tag
        return None

    def get_all(self):
        return Tags._tags


def get_soup(url, timeout=1, count=1):
    max_count = 4
    # Catch network problems
    try:
        r = requests.get(url=url, timeout=timeout)
    except requests.exceptions.Timeout:
        msg = "Timeout: {}. \
Try {} of {} (set timeout to {})".format(url, count, max_count, timeout)
        # print(msg)
        logger.error(msg)
        if count >= max_count:
            logger.error("TIMEOUT. Nothing to responce.")
            return None
        else:
            return get_soup(url, timeout=timeout + 10, count=count + 1)
    except requests.exceptions.ConnectionError:
        msg = "ConnectionError: {}. \
Try {} of {} (set timeout to {})".format(url, count, max_count, timeout)
        # print(msg)
        logger.error(msg)
        if count >= max_count:
            return None
        else:
            time.sleep(timeout)
            return get_soup(url, timeout=timeout + 10, count=count + 1)

    # Catch unsuccessful status codes
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # print(e.args[0])
        logger.error(e.args[0])
        return None

    soup = BeautifulSoup(r.text.encode(), "lxml")

    return soup


def save_storage(storage, branch):
    # if not branch:
    #     with open(cfg.storage_file, "wb") as f:
    #         data = {k: v.get_all() for (k, v) in storage.items()}
    #         pickle.dump(data, f)
    # else:
        fname = cfg.storage_file.split(".")
        fname[-2] = fname[-2] + '_' + branch
        fname = ".".join(fname)
        with open(fname, "wb") as f:
            data = {branch: storage.get(branch).get_all()}
            pickle.dump(data, f)


def load_storage(branches=None):
    data = {"quotes": Quotes(), "authors": Authors(), "tags": Tags()}
    if os.path.isdir(cfg.out_dir):
        # if os.path.isfile(cfg.storage_file):
        #     with open(cfg.storage_file, 'rb') as f:
        #         # Load storage like {"quotes": [list_of_quotes], etc.}
        #         tmp = pickle.load(f)
        #         logger.debug("Load from {}".format(cfg.storage_file))
        #         # Iterate over tmp items
        #         for branch, items in tmp.items():
        #             for item in items:
        #                 data.get(branch).add(**item)
        # else:
        #     logger.debug("{} not found. Load parts".format(cfg.storage_file))
        if branches is not None:
            for branch in branches:
                fname = cfg.storage_file.split(".")
                fname[-2] = fname[-2] + '_' + branch
                fname = ".".join(fname)
                if os.path.isfile(fname):
                    with open(fname, "rb") as f:
                        logger.debug("Load from {}".format(fname))
                        tmp = pickle.load(f)
                        for item in tmp.get(branch):
                            data.get(branch).add(**item)
                else:
                    logger.debug("{} not found".format(fname))
            return data
    logger.info("Storage loaded.")
    return data


def parse_authors(storage):
    data = storage.get("authors").get_all()
    count = 0
    for author in data:
        soup = get_soup(author.get("url"))
        if not soup:
            break

        b_date = soup.select_one("span.author-born-date")
        b_place = soup.select_one("span.author-born-location")
        about = soup.select_one("div.author-description")
        author.update({"born_date": b_date.text})
        author.update({"born_place": b_place.text[3:]})
        author.update({"about": about.text.strip()})

        storage["authors"].add(**author)
        count += 1
        if count % 5 == 0:
            msg = "{} of {} authors parsed.".format(count, len(data))
            logger.info(msg)
            save_storage(storage, "authors")

    logger.info("Authors parsing complete. {} authors parsed".format(count))


def parse_tags(storage):
    data = storage.get("tags").get_all()
    count = 0
    for tag in data:
        continue_parsing = True
        base_url = cfg.url
        next_page_url = ""
        # add slot for quotes with current tag
        tag["quotes"] = []
        while continue_parsing:
            t0 = time.time()
            soup = get_soup("{}{}".format(base_url, next_page_url))
            t1 = time.time()
            logger.debug("Get soup for {} sec".format(t1 - t0))
            if not soup:
                break
            t0 = time.time()
            quotes = soup.select(cfg.quote_sel)
            for quote in quotes:
                q_text = quote.select_one("span.text").text[1:-1]
                q_author_title = quote.select_one("small.author").text
                q_author_url = quote.select_one("span > a").get("href")
                q_author_url = concat_urls(cfg.url, q_author_url)
                item = {"text": q_text}
                item["author_title"] = q_author_title
                item["author_url"] = q_author_url
                # store quote in current tag
                tag["quotes"].append(item)
            t1 = time.time()
            logger.debug("Parse page for {} sec".format(t1 - t0))

            # Check for next page
            next_page = soup.select_one("li.next")
            if next_page:
                next_page_url = next_page.findNext("a").get("href")
                if next_page_url[0] == "/" and base_url[-1] == "/":
                    next_page_url = next_page_url[1:]
            else:
                continue_parsing = False

        # update tag in storage
        storage.get("tags").add(**tag)

        count += 1
        if count % 5 == 0:
            logger.info("{} of {} tags parsed.".format(count, len(data)))
            # Save parsed page
            save_storage(storage, "tags")

    logger.info("Tags parsing complete. {} tags parsed.".format(count))


def parse_quotes(url, storage):
    continue_parsing = True
    base_url = url
    next_page_url = ""
    count = 0
    while continue_parsing:
        soup = get_soup("{}{}".format(base_url, next_page_url))
        if not soup:
            break

        quotes = soup.findAll(cfg.quote.tag, {cfg.quote.case: cfg.quote.value})
        for q in quotes:
            item = {}
            # Get quote text
            text = q.find(cfg.text.tag, {cfg.text.case: cfg.text.value})
            item.update({"text": text.text[1:-1]})
            # Get quote author
            author = q.find(cfg.author.tag, {cfg.author.case: cfg.author.value})
            author_title = author.text
            author_url = author.findNext("a").get("href")
            author_url = concat_urls(url, author_url)
            # Add author to DB
            author_id = storage["authors"].add(author_title, author_url)
            item.update({"author_title": author_title})
            item.update({"author_url": author_url})
            item.update({"author_id": author_id})

            # Get tags
            tags = q.find(cfg.tag.tag, {cfg.tag.case: cfg.tag.value})
            tags = tags.findAll("a", {"class": "tag"})
            _tags = []
            for tag in tags:
                tag_name = tag.text
                tag_url = concat_urls(url, tag.get("href"))
                tag_id = storage["tags"].add(tag_name, tag_url)
                _tags.append({"_id": tag_id, "name": tag_name, "url": tag_url})

            item.update({"tags": _tags})
            # Save quote
            storage["quotes"].add(**item)
            count += 1
            if count % 5 == 0:
                logger.info("{} quotes parsed".format(count))

        # Check for next page
        next_page = soup.find("li", {"class": "next"})
        if next_page:
            next_page_url = next_page.findNext("a").get("href")
            if next_page_url[0] == "/" and url[-1] == "/":
                next_page_url = next_page_url[1:]
        else:
            continue_parsing = False

        # Save parsed page
        save_storage(storage, "quotes")

    logger.info("Quotes parsing complete. {} quotes parsed".format(count))
    return None


def export_json(storage):
    with open(cfg.export_file + "json", "w") as f:
        data = {k: v.get_all() for (k, v) in storage.items()}
        json.dump(data, f)
        logger.info("Export to {} complete.".format(f.name))


def export_xls(storage):
    # Works only with Excel installed
    def title_gen(ws, *args):
        # from data like:
        # ['ID', 'Tag', 'URL', ['Quotes','Text quote', 'Author', 'Author URL']]
        # make title like:
        # ID  |  Tag  |   URL   |   Quotes
        #     |       |         |   Text quote    |   Author   |   Author URL
        row = 1
        col = 1
        use_second_row = False
        for val in args:
            if isinstance(val, list):
                cell1 = ws.Cells(row, col)
                cell1.value = val[0]
                use_second_row = True
                for v in val[1:]:
                    ws.Cells(row + 1, col).value = v
                    col += 1
                cell2 = ws.Cells(row, col)
                ws.Range(cell1, cell2).Merge()
            else:
                ws.Cells(row, col).value = val
                col += 1
        if use_second_row:
            row += 1
        return row, col

    def write_row(ws, row, *args):
        col = 1
        for val in args:
            if isinstance(val, list):
                loop_col = col
                for v in val:
                    col = loop_col
                    for i in v:
                        ws.Cells(row, col).value = i
                        col += 1
                    row += 1
            else:
                ws.Cells(row, col).value = val
            col += 1
        return row

    excel = Dispatch("Excel.Application")
    wb = excel.Workbooks.Add()
    wsheets_count = wb.Sheets.Count
    # Check for enough worksheets
    while wsheets_count < len(storage.keys()):
        wb.Worksheets.Add()
        wsheets_count = wb.Sheets.Count

    # Store authors
    data = storage["authors"].get_all()
    ws = wb.Sheets(1)
    ws.Name = "Authors"
    # generate Title
    title_list = ["id", "Name", "Born date", "Born place", "About", "URL"]
    row, col = title_gen(ws, *title_list)
    for author in data:
        row += 1
        i = [author["_id"], author["author_title"], author["born_date"]]
        i.extend([author["born_place"], author["about"], author["url"]])
        row = write_row(ws, row, *i)

    # Store quotes
    data = storage["quotes"].get_all()
    ws = wb.Sheets(2)
    ws.Name = "Quotes"
    # generate Title
    title_list = ["id", "Text", "Author", "Author ID", "Author URL"]
    title_list.append(["Tags", "Tag ID", "Tag name", "Tag URL"])
    row, col = title_gen(ws, *title_list)
    for quote in data:
        row += 1
        i = [quote["_id"], quote["text"], quote["author_title"]]
        i.extend([quote["author_id"], quote["author_url"]])
        i.append([[i["_id"], i["name"], i["url"]] for i in quote["tags"]])
        row = write_row(ws, row, *i)

    # Store tags
    data = storage["tags"].get_all()
    ws = wb.Sheets(3)
    ws.Name = "Tags"
    # generate Title
    title_list = ["Tag ID", "Tag name", "Tag URL"]
    title_list.append(["Quotes", "Text", "Author", "Author URL"])
    row, col = title_gen(ws, *title_list)
    for tag in data:
        row += 1
        i = [tag["_id"], tag["tag_name"], tag["url"]]
        i.append([[i["text"], i["author_title"], i["author_url"]] for i in tag["quotes"]])
        row = write_row(ws, row, *i)

    wb.SaveAs(cfg.export_file + "xls")
    wb.Close()
    excel.Quit()
    logger.info("Export to {} complete.".format(cfg.export_file + "xls"))


def export_sqlite(data):
    conn = sqlite3.connect(cfg.export_file + '.sqlite')
    cursor = conn.cursor()

    pass
    conn.close()


if __name__ == '__main__':
    logger.info("Program started")
    # try to load previous storage
    data = load_storage(["quotes", "authors", "tags"])
    logger.info("Storage loaded")

    parse_quotes(cfg.url, data)
    parse_authors(data)
    parse_tags(data)
    export_json(data)
    # export_xls(data) - глючный экспорт, пробую sqlite
    logger.info("Program finished")
