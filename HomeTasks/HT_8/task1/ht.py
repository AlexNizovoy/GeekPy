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

    def add(self, text, author_id, author_title, author_url, _tags):
        Quotes.counter += 1
        Quotes._quotes.append({"_id": Quotes.counter, "text": text, "author_id": author_id, "author_title": author_title, "author_url": author_url, "tags": _tags})
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

    def add(self, name, url):
        author = self.get(name)
        if author:
            return author.get("_id")
        Authors.counter += 1
        Authors._authors.append({"_id": Authors.counter, "name": name, "url": url})
        return Authors.counter

    def get(self, name):
        for author in Authors._authors:
            if author.get("name") == name:
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

    def add(self, name, url):
        tag = self.get(name)
        if tag:
            return tag.get("_id")
        Tags.counter += 1
        Tags._tags.append({"_id": Tags.counter, "name": name, "url": url})
        return Tags.counter

    def get(self, name):
        for tag in Tags._tags:
            if tag.get("name") == name:
                return tag
        return None

    def get_all(self):
        return Tags._tags


def parse_author(url, storage):
    return {"url": url, "author_title": None, "born_date": None,
            "born_place": None, "about": None}


def parse_tag(url, storage):
    return {"tag_name": None, "tag_url": None, "text": None,
            "author": None, "author_url": None}


def save_storage(storage):
    with open(cfg.storage_file, "wb") as f:
        data = {"quotes": storage["quotes"].get_all(), "authors": storage["authors"].get_all(), "tags": storage["tags"].get_all()}
        pickle.dump(data, f)


def parse_quotes(url, storage):
    continue_parsing = True
    base_url = cfg.url
    next_page_url = ""
    while continue_parsing:
        r = requests.get("{}{}".format(base_url, next_page_url))
        soup = BeautifulSoup(r.text.encode(), "html.parser")

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
                print(storage["quotes"].counter)

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


if __name__ == '__main__':
    data = {"quotes": Quotes(), "authors": Authors(), "tags": Tags()}
    parse_quotes(cfg.url, data)
