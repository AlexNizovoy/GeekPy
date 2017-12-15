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
import requests
from bs4 import BeautifulSoup

import config

cfg = config.Cfg()

_tags = []


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

    def add(self, text, author_id, author_title, author_url, tags):
        kwargs = locals().copy()
        kwargs.pop("self")
        Quotes.counter += 1
        item = {"_id": Quotes.counter}
        item.update(kwargs)
        Quotes._quotes.append(item)
        return Quotes.counter

    def get(self, name):
        for quote in Quotes._quotes:
            if quote.get("name") == name:
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

    def add(self, author_title, url, **kwargs):
        args = locals().copy()
        # remove unneccessary and empty arguments
        args.pop("self")
        if not kwargs:
            args.pop("kwargs")

        author = self.get(author_title)
        # Check for existing author
        if author and not kwargs:
            return author.get("_id")
        # If author exist and exist updates for him - apply them
        elif author and kwargs:
            Authors._authors[author.get("_id") - 1].update(kwargs)
            return author.get("_id")
        Authors.counter += 1
        item = {"_id": Authors.counter}
        item.update(args)
        Authors._authors.append(item)

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

    def add(self, tag_name, url, **kwargs):
        args = locals().copy()
        # remove unneccessary and empty arguments
        args.pop("self")
        if not kwargs:
            args.pop("kwargs")

        tag = self.get(tag_name)
        if tag and not kwargs:
            return tag.get("_id")
        # If tag exist and exist updates for him - apply them
        elif tag and kwargs:
            Tags._tags[tag.get("_id") - 1].update(kwargs)
            return tag.get("_id")
        Tags.counter += 1
        item = {"_id": Tags.counter}
        item.update(args)
        Tags._tags.append(item)
        return Tags.counter

    def get(self, tag_name):
        for tag in Tags._tags:
            if tag.get("tag_name") == tag_name:
                return tag
        return None

    def get_all(self):
        return Tags._tags


def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode(), "html.parser")

    return soup


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
        if count % 10 == 0:
            print("{} of {} authors parsed.".format(count, len(data)))

        save_storage(storage, "authors")


def parse_tags(url, storage):
    return {"tag_name": None, "tag_url": None, "text": None,
            "author": None, "author_url": None}


def save_storage(storage, branch=None):
    if not branch:
        with open(cfg.storage_file, "wb") as f:
            data = {k: v.get_all() for (k, v) in storage.items()}
            pickle.dump(data, f)
    else:
        fname = cfg.storage_file.split(".")
        fname[-2] = fname[-2] + '_' + branch
        fname = ".".join(fname)
        with open(fname, "wb") as f:
            data = {branch: storage.get(branch).get_all()}
            pickle.dump(data, f)


def parse_quotes(url, storage):
    continue_parsing = True
    base_url = cfg.url
    next_page_url = ""
    while continue_parsing:
        soup = get_soup("{}{}".format(base_url, next_page_url))
        if not soup:
            break

        quotes = soup.findAll(cfg.quote.tag, {cfg.quote.case: cfg.quote.value})
        for q in quotes:
            # Get quote text
            text = q.find(cfg.text.tag, {cfg.text.case: cfg.text.value}).text[1:-1]
            # Get quote author
            author = q.find(cfg.author.tag, {cfg.author.case: cfg.author.value})
            author_title = author.text
            author_url = author.findNext("a").get("href")
            author_url = concat_urls(cfg.url, author_url)
            # Add author to DB
            author_id = storage["authors"].add(author_title, author_url)

            # Get tags
            tags = q.find(cfg.tag.tag, {cfg.tag.case: cfg.tag.value}).findAll("a", {"class": "tag"})
            _tags = []
            for tag in tags:
                tag_name = tag.text
                tag_url = concat_urls(cfg.url, tag.get("href"))
                tag_id = storage["tags"].add(tag_name, tag_url)
                _tags.append({"_id": tag_id, "name": tag_name, "url": tag_url})

            # Save quote
            count = storage["quotes"].add(text, author_id, author_title, author_url, _tags)
            if count % 10 == 0:
                print("{} quotes parsed".format(count))

        # Check for next page
        next_page = soup.find("li", {"class": "next"})
        if next_page:
            next_page_url = next_page.findNext("a").get("href")
            if next_page_url[0] == "/" and cfg.url[-1] == "/":
                next_page_url = next_page_url[1:]
        else:
            continue_parsing = False

        # Save parsed page
        save_storage(storage)
    return None


if __name__ == '__main__':
    data = {"quotes": Quotes(), "authors": Authors(), "tags": Tags()}
    parse_quotes(cfg.url, data)
    parse_authors(data)
    parse_tags(data)
