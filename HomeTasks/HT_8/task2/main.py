import re
import requests
import time
from bs4 import BeautifulSoup

import config as cfg
logger = cfg.logger


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

    return soup, r


def extract_name(soup_tr):
    name = soup_tr.select_one('td.field_domain > a')
    if name:
        return name.get('title')
    else:
        return None


def parser(url, data):
    base_url = "/".join(cfg.URL.split("/")[:3])
    next_url = cfg.URL[len(base_url):]
    count = 0
    continue_parsing = True
    while continue_parsing:
        soup, r = get_soup(base_url + next_url)
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

        count += 1
        logger.info("{} pages parsed ({} domains)".format(count, len(data)))
        if count % 5 == 0:
            # add sleep time for prevent hit the rate limiter
            time.sleep(10)
    return None

if __name__ == '__main__':
    logger.info("Program started")
    storage = []
    parser(cfg.URL, storage)
    logger.info("Parsing complete")
    logger.info("Program finished")
