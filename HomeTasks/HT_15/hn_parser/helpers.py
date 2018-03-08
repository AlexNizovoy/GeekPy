from django.core.cache import cache
from datetime import datetime
import logging
import os
import re
import requests
import time

from stories.models import Story, StoryType, StoryCategory
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
            self.ready = True
        else:
            logger.error("{} is not valid category!".format(category))
            self.category = ""
            self.ready = False

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


def parse_stories(category_name, token=None):
    from_dt = datetime.strptime(cfg.from_date, "%Y-%m-%d").timestamp()
    count = 0
    getter = Getter(category_name)
    if not getter.ready:
        return None

    cat_records = getter.get_category()
    result = []

    for record in cat_records:
        rec_data = getter.get_item(record)
        if rec_data is None:
            continue
        if rec_data.get("score") < cfg.score or \
           rec_data.get("time") < from_dt:
            continue
        text = rec_data.get("text")
        rec_data["time"] = str(datetime.fromtimestamp(rec_data.get("time")))
        rec_data["story_category"] = category_name
        if text and len(cfg.tag):
            rec_data["text"] = remove_tag(text)
        # rename unsupported field-names
        # if rec_data.get('type'):
        #     rec_data['rec_type'] = rec_data.get('type')
        #     del rec_data['type']
        # if rec_data.get('id'):
        #     rec_data['rec_id'] = rec_data.get('id')
        #     del rec_data['id']

        result.append(rec_data)
        count += 1

        msg = "In category '{}' get {} records from {}". format(
                category_name, count, len(cat_records))
        if token:
            # store value in cache for 100 seconds
            cache.set(token, msg, 100)

        if count % 10 == 0:
            print(msg)

    msg = "In category '{}' get {} records"
    msg = msg.format(category_name, count)
    logger.info(msg)
    print(msg)
    return result


def write_records(data, token=None):
    rename_fields = [('story_id', 'id'), ('story_type', 'type')]
    count = 0
    all_count = len(data)
    for story in data:
        # rename fields in received records to fields in Models
        for (i, k) in rename_fields:
            if not story.get(i):
                # write new field only if it not present
                story[i] = story.get(k)
            if k in story.keys():
                del story[k]
        # get or create StoryType from DB
        story_type = StoryType.objects.get_or_create(name=story['story_type'])[0]
        # add foreign key
        story['story_type'] = story_type
        # get or create StoryCategory from DB
        story_category = StoryCategory.objects.get_or_create(name=story['story_category'])[0]
        # add foreign key
        story['story_category'] = story_category
        Story.objects.update_or_create(story_id=story['story_id'], defaults=story)
        count += 1
        if count % 5 == 0:
            msg = "In DB write {} records from {}".format(count, all_count)
            if token:
                # store value in cache for 100 seconds
                cache.set(token, msg, 100)

    return count
