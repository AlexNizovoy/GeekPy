import json
import os
import random
import re
import requests
import time
from bs4 import BeautifulSoup
import xlwt

import config as cfg
logger = cfg.logger


def login():
    data = {"login": cfg.USER, "password": cfg.PASSWORD}
    url_login = "https://member.expireddomains.net/login/"
    session = requests.Session()
    r = session.post(url_login, data=data, headers=cfg.HEADERS)
    if r.request.url.find("member") > 0:
        # run logged in scrapping
        logger.info("Log in as {} success!".format(cfg.USER))
        return session
    else:
        # run not-logged in scrapping
        logger.info("Log in unsuccessful! Scrapping as anonimous.")
        return None


def get_soup(url, timeout=1, count=1, session=None):
    MAX_COUNT = 4
    # Catch network problems
    try:
        if session is None:
            r = requests.get(url=url, timeout=timeout)
        else:
            r = session.get(url=url, timeout=timeout)
    except requests.exceptions.Timeout:
        msg = "Timeout: {}. \
Try {} of {} (set timeout to {})".format(url, count, MAX_COUNT, timeout)
        logger.error(msg)
        if count >= MAX_COUNT:
            logger.error("TIMEOUT. Nothing to responce.")
            return None
        else:
            return get_soup(url, timeout=timeout + 10, count=count + 1, session=session)
    except requests.exceptions.ConnectionError:
        msg = "ConnectionError: {}. \
Try {} of {} (set timeout to {})".format(url, count, MAX_COUNT, timeout)
        logger.error(msg)
        if count >= MAX_COUNT:
            return None
        else:
            time.sleep(timeout)
            return get_soup(url, timeout=timeout + 10, count=count + 1, session=session)

    # Catch unsuccessful status codes
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(e.args[0])
        return None

    soup = BeautifulSoup(r.text.encode(), "lxml")

    return soup, r


def extract_name(soup_tr):
    name = soup_tr.select_one('td.field_domain > a')
    if name:
        return name.get('title')
    else:
        return None


def load_storage():
    if os.path.isdir(cfg.OUT_DIR):
        if os.path.isfile(cfg.STORAGE_FILE):
            with open(cfg.STORAGE_FILE, 'r') as f:
                return json.load(f)
    return {"data": [], "last_url": None, "title": ""}


def save_storage(data, last_url=None):
    storage = {"data": data, "last_url": last_url}
    with open(cfg.STORAGE_FILE, 'w') as f:
        json.dump(storage, f)
    return None


def parser(storage, last_url=None):
    data = storage["data"]
    session = login()
    if session is None:
        url = cfg.URL
    else:
        url = cfg.URL_IF_LOGGED_IN

    base_url = "/".join(url.split("/")[:3])
    next_url = storage.get("last_url") or url[len(base_url):]

    # Get page title
    soup, r = get_soup(base_url + next_url, session=session)
    storage["title"] = soup.select_one("title").text
    time.sleep(5)

    count = 0
    continue_parsing = True
    while continue_parsing:
        t0 = time.time()
        soup, r = get_soup(base_url + next_url, session=session)
        if soup is None:
            logger.debug("Soup is None!")
            logger.debug("requests = {}".format(r))
            break
        tr_list = soup.select("table.base1 > tbody > tr")
        name_list = [extract_name(i) for i in tr_list]
        data.extend(name_list)
        next_url_tag = soup.select_one("div.pagescode a.next")
        if next_url_tag:
            next_url = next_url_tag.get("href")
            logger.debug("Next_url = {}".format(next_url))
        else:
            continue_parsing = False
            logger.debug("next_url not found")
            hit_limit_tag = soup.select_one('body > p')
            if hit_limit_tag:
                logger.debug("found hit_limit_tag!")
                text = hit_limit_tag.text
                r = re.search(r"(\d+)( secon)", text)
                if r:
                    wait = int(r.groups()[0])
                    wait += 1
                    logger.debug("sleep for {} seconds".format(wait))
                    time.sleep(wait)
                    continue_parsing = True
        if not continue_parsing:
            with open("last_page.html", 'w') as f:
                    f.write(soup.decode())
            next_url = None

        # add sleep time
        wait = time.time() - t0
        wait += wait * random.random() * 5
        time.sleep(wait)

        count += 1
        logger.info("{} pages parsed ({} domains)".format(count, len(data)))
        save_storage(data, next_url)
        if count % 5 == 0:
            # add sleep time for prevent hit the rate limiter
            wait = random.randint(20, 50)
            logger.debug("sleep for {} seconds".format(wait))
            time.sleep(wait)
    return None


def export_storage(data):
    data = storage["data"]
    # Export to JSON
    with open(cfg.EXPORT_FILE + "json", "w") as f:
        json.dump(data, f)
        logger.info("JSON Export to {} complete.".format(f.name))

    # Export to TXT
    with open(cfg.EXPORT_FILE + "txt", "w") as f:
        f.write(storage["title"] + "\n"*2)
        f.write("\n".join(data))
    logger.info("TXT Export to {} complete.".format(f.name))

    # Export to XLS
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Deleted domains")
    ws.write(0, 0, storage["title"])
    row = 2
    for i in data:
        ws.write(row, 0, i)
        row += 1
    fname = cfg.EXPORT_FILE + "xls"
    wb.save(fname)
    logger.info("XLS Export to {} complete.".format(fname))


if __name__ == '__main__':
    logger.info("Program started")
    storage = load_storage()
    if not cfg.EXPORT_ONLY:
        try:
            parser(storage)
        except KeyboardInterrupt:
            logger.info("Parsing canceled!")
        logger.info("Parsing complete")
    storage["data"] = list(set(storage["data"]))
    storage["data"].sort()
    export_storage(storage)
    logger.info("Program finished")
