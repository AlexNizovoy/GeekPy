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
import os
from bs4 import BeautifulSoup

import config

cfg = config.Cfg()


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

        # Check for existing record
        quote = self.get(text)
        if quote:
            return quote.get("_id")

        # create new record
        Quotes.counter += 1
        item = {"_id": Quotes.counter}
        item.update(kwargs)
        Quotes._quotes.append(item)
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

    def add(self, author_title, url, **kwargs):
        args = locals().copy()
        # remove unneccessary and empty arguments
        args.pop("self")
        if not kwargs:
            args.pop("kwargs")

        # Check for existing author
        author = self.get(author_title)
        if author and not kwargs:
            return author.get("_id")
        # If author exist and exist updates for him - apply them
        elif author and kwargs:
            Authors._authors[author.get("_id") - 1].update(kwargs)
            return author.get("_id")

        # or create new record
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

        # Check for existing record
        tag = self.get(tag_name)
        if tag and not kwargs:
            return tag.get("_id")
        # If tag exist and exist updates for him - apply them
        elif tag and kwargs:
            Tags._tags[tag.get("_id") - 1].update(kwargs)
            return tag.get("_id")

        # or create new record
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

    # TODO: Make safe (check for resp.code, catch exceptions etc.)
    return soup


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


def load_storage(branches=None):
    if os.path.isdir(cfg.out_dir) and os.path.isfile(cfg.storage_file):
        with open(cfg.storage_file, 'rb') as f:
            data = pickle.load(f)
    elif os.path.isdir(cfg.out_dir):
        data = {"quotes": Quotes(), "authors": Authors(), "tags": Tags()}
        for branch in branches:
            fname = cfg.storage_file.split(".")
            fname[-2] = fname[-2] + '_' + branch
            fname = ".".join(fname)
            if os.path.isfile(fname):
                with open(fname, "rb") as f:
                    tmp = pickle.load(f)
                    for item in tmp:
                        data.get(branch).add(**item)
        return data
    return {"quotes": Quotes(), "authors": Authors(), "tags": Tags()}


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
            print("{} of {} authors parsed.".format(count, len(data)))
            save_storage(storage, "authors")

    print("{} autors parsed".format(count))
    save_storage(storage)


def parse_tags(storage):
    data = storage.get("tags").get_all()
    count = 0
    for tag in data:
        continue_parsing = True

        # Make pure base_url for correct pagination
        base_url = tag.get("url").split("/")
        if "page" in base_url:
            idx = base_url.index("page")
            base_url = base_url[:idx]
        base_url = "/".join(base_url)

        next_page_url = ""
        # add slot for quotes with current tag
        tag["quotes"] = []
        while continue_parsing:
            soup = get_soup("{}{}".format(base_url, next_page_url))
            if not soup:
                break

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

            # Check for next page
            next_page = soup.select_one("li.next")
            if next_page:
                next_page_url = next_page.findNext("a").get("href")
                if next_page_url[0] == "/" and base_url[-1] == "/":
                    next_page_url = next_page_url[1:]
            else:
                continue_parsing = False

        count += 1
        if count % 5 == 0:
            print("{} of {} tags parsed.".format(count, len(data)))
            # Save parsed page
            save_storage(storage, "tags")

    print("{} tags parsed.".format(count))
    save_storage(storage)


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
                print("{} quotes parsed".format(count))

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

    print("{} quotes parsed".format(count))
    save_storage(storage)
    return None


if __name__ == '__main__':
    # try to load previous storage
    data = load_storage(["quotes", "authors", "tags"])

    parse_quotes(cfg.url, data)
    parse_authors(data)
    parse_tags(data)
