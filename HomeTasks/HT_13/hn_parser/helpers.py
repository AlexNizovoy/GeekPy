from django.core.cache import cache
from datetime import datetime
import logging
import os
import re
import requests
import time

import hn_parser.config as cfg


# init logging on top for logging inside class
if not os.path.isdir(cfg.LOG_DIR):
    os.mkdir(cfg.LOG_DIR)

logger = logging.getLogger(cfg.APP_NAME)
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create console handler
ch = logging.StreamHandler()
ch.setFormatter(fmt)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
# add handlers to logger
fh = logging.FileHandler(cfg.LOG_FILE)
fh.setFormatter(fmt)
logger.addHandler(fh)


class Getter(object):
    """Parser for web-site"""
    category = ""

    def __init__(self, category):
        if category.lower() in cfg.CATEGORIES:
            self.category = category
        else:
            logger.error("{} is not valid category!".format(category))
            self.category = ""

    def _rq(self, url, timeout=1, count=1):
        MAX_COUNT = 4
        try:
            r = requests.get(url=url, timeout=timeout)
        except requests.exceptions.Timeout:
            msg = "Timeout: {}. \
Try {} of {} (set timeout to {})".format(url, count, MAX_COUNT, timeout)
            logger.error(msg)
            if count >= MAX_COUNT:
                logger.error("TIMEOUT. Nothing to responce.")
                return None
            else:
                return self._rq(url, timeout=timeout + 10, count=count + 1)
        except requests.exceptions.ConnectionError:
            msg = "ConnectionError: {}. \
Try {} of {} (set timeout to {})".format(url, count, MAX_COUNT, timeout)
            logger.error(msg)
            if count >= MAX_COUNT:
                return None
            else:
                time.sleep(timeout)
                return self._rq(url, timeout=timeout + 10, count=count + 1)

        # Catch unsuccessful status codes
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(e.args[0])
            return None

        return r

    def get_item(self, item_id):
        url = cfg.url_item.format(item_id)
        logger.info("Get item #{}...".format(item_id))
        r = self._rq(url)
        if r is None:
            logger.error("Request return None!")
            return None
        try:
            data = r.json()
        except Exception:
            logger.error("Request return not-JSON data!")
            return None
        return data

    def get_category(self):
        url = cfg.url_category.format(self.category)
        logger.info("Get category '{}'...".format(self.category))
        r = self._rq(url)
        if r is None:
            logger.error("Request return None!")
            return None
        try:
            data = r.json()
        except Exception:
            logger.error("Request return not-JSON data!")
            return None
        return data


def remove_tag(text):
    result = text
    indexes = []
    regex = r"<(" + cfg.tag + r").*?>(.|\n)+?</(" + cfg.tag + r")>"
    matches = re.finditer(regex, text)
    for match in matches:
        indexes.append((match.start(), match.end()))
    for i in range(len(indexes) - 1, -1, -1):
        result = result[:indexes[i][0]] + result[indexes[i][1]:]
    return result


def parse_stories(category_name, token):
    from_dt = datetime.strptime(cfg.from_date, "%Y-%m-%d").timestamp()
    count = 0
    getter = Getter(category_name)
    cat_records = getter.get_category()
    result = []

    for record in cat_records:
        rec_data = getter.get_item(record)
        if rec_data.get("score") < cfg.score or \
           rec_data.get("time") < from_dt:
            continue
        text = rec_data.get("text")
        rec_data["time"] = str(datetime.fromtimestamp(rec_data.get("time")))
        if text and len(cfg.tag):
            rec_data["text"] = remove_tag(text)
        # rename unsupported field-names
        if rec_data.get('type'):
            rec_data['rec_type'] = rec_data.get('type')
            del rec_data['type']
        if rec_data.get('id'):
            rec_data['rec_id'] = rec_data.get('id')
            del rec_data['id']

        result.append(rec_data)
        count += 1

        msg = "In category '{}' get {} records from {}". format(
                category_name, count, len(cat_records))
        # store value in cache for 100 seconds
        cache.set(token, msg, 100)
        print(token, cache.get(token))

        if count % 10 == 0:
            print(msg)

    msg = "In category '{}' get {} records"
    msg = msg.format(category_name, count)
    logger.info(msg)
    print(msg)
    return result


def write_records(data):
    for story in data:
        pass
    return None
