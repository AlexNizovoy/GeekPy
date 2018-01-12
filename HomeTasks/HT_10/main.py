import argparse
from datetime import datetime
import logging
import os
import psycopg2
import pickle
import re
import requests
import time

import config as cfg
import templates

# init logging on top for logging inside class
logger = logging.getLogger(cfg.APP_NAME)
logger.setLevel(logging.INFO)


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


class Parser(object):
    """Parser for web-site"""
    categories = []
    processed_id = []

    def __init__(self, category, clear_storage=True):
        if category.lower() == "all":
            self.categories = cfg.CATEGORIES
        elif category.lower() in cfg.CATEGORIES:
            self.categories.append(category)
        else:
            logger.error("{} is not valid category!".format(category))
            self.categories = []
        if not clear_storage:
            self._load_storage()

    def _load_storage(self):
        if os.path.isdir(cfg.OUT_DIR) and os.path.isfile(cfg.STORAGE_FILE):
            with open(cfg.STORAGE_FILE, "rb") as f:
                self.processed_id = pickle.load(f)
        elif not os.path.isdir(cfg.OUT_DIR):
            os.mkdir(cfg.OUT_DIR)

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

    def get_records(self):
        data = {}
        from_dt = datetime.strptime(cfg.from_date, "%Y-%m-%d").timestamp()
        for cat in self.categories:
            count = 0
            skipped = 0
            cat_records = self.get_category(cat)
            records = []
            for record in cat_records:
                if record in self.processed_id:
                    skipped += 1
                    continue
                rec_data = self.get_item(record)
                if rec_data.get("score") < cfg.score or \
                   rec_data.get("time") < from_dt:
                    skipped += 1
                    continue
                text = rec_data.get("text")
                if text and len(cfg.tag):
                    rec_data["text"] = remove_tag(text)
                records.append(rec_data)
                count += 1
                if count % 10 == 0:
                    print("In category '{}' get {} records from {}". format(
                        cat, count, len(cat_records)))
            msg = "In category '{}' get {} records ({} records skipped)"
            msg = msg.format(cat, count, skipped)
            logger.info(msg)
            print(msg)
            data[cat] = records

        # Save storge
        with open(cfg.STORAGE_FILE, "wb") as f:
            pickle.dump(self.processed_id, f)

        return data

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
        self.processed_id.append(item_id)
        return data

    def get_category(self, category):
        if category.lower() not in cfg.CATEGORIES:
            return None
        url = cfg.url_category.format(category)
        logger.info("Get category '{}'...".format(category))
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


class HTML_Export(object):
    """Class for export in HTML"""
    def __init__(self):
        pass

    def _make_title(self, data):
        """Get iterable 'data' with name of fields and return list with
        elements ['id', 'type', 'score', 'time', 'by', 'title', 'text', 'url',
        and rest]. If some of listed elements not present in 'data' - they
        skipped.
        """
        tmp = list(data)
        count = 0
        for i in ["id", "type", "score", "time", "by", "title", "text", "url"]:
            if i in tmp:
                idx = tmp.index(i)
                tmp[count], tmp[idx] = tmp[idx], tmp[count]
                count += 1
        return tmp

    def export(self, data, raw=False):
        """If 'raw == True' write 'data' to output file without
        """
        output = templates.base
        style = templates.style
        script = templates.script
        if not raw:
            result = []
            for name, category in data.items():
                # generate title from existing keys of all items in category
                sequence = []
                for i in category:
                    sequence.extend(i.keys())
                sequence = list(set(sequence))
                sequence = self._make_title(sequence)
                cat_html = templates.category
                thead = self.item(sequence=sequence)
                data_html = []
                for record in category:
                    data_html.append(self.item(record, sequence))
                data_html = "\n".join(data_html)
                cat_html = cat_html.format(name=name.capitalize(),
                                           table_head=thead, data=data_html)
                result.append(cat_html)
            output = output.format(style=style, categories="\n".join(result),
                                   script=script)
        else:
            output = output.format(style=style, categories=data, script=script)

        datestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = cfg.OUT_FILE.format(datestamp=datestamp)
        with open(fname, "w", encoding="utf-8") as f:
            f.write(output)
        return fname

    def item(self, data=None, sequence=None):
        """Get 'data' like {"name2": "val2", "name1": "val1"} and
        'sequence' like ["name1", "name2"] (for ordered output values)
        return HTML-text like
        If record in 'data' not contains item from 'sequence' - put None
        <tr>
            <td>val1</td>
            <td>val2</td>
        </tr>
        """
        if data is None and sequence is None:
            return "\n"
        result = ["<tr>"]
        for i in sequence:
            if data is None:
                result.append("<th>{}</th>".format(i.upper()))
            elif i == "time":
                unix_time = data.get(i)
                str_unix_time = str(datetime.fromtimestamp(unix_time))
                result.append("<td>{}</td>".format(str_unix_time))
            else:
                result.append("<td>{}</td>".format(data.get(i)))
        result.append("</tr>")
        return "\n".join(result)


def main():
    # get command-line args
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c", "--category", type=str,
                            default=cfg.DEFAULT_CATEGORY,
                            choices=["all"] + cfg.CATEGORIES,
                            help="name of category. Use '-c all' for process \
over all categories.")
    arg_parser.add_argument("-clr", action="store_true",
                            help="use it for clear storage of processed items")
    cat_name = arg_parser.parse_args().category
    clear_storage = arg_parser.parse_args().clr

    create_dir = False
    create_log_file = False

    # Check for existing directory and log-file
    if not os.path.isdir(cfg.OUT_DIR):
        os.mkdir(cfg.OUT_DIR)
        create_dir = True

    if not os.path.isfile(cfg.LOG_FILE):
        create_log_file = True

    # add handlers to logger
    fh = logging.FileHandler(cfg.LOG_FILE)
    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    # create console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # logging all options for the possibility of changing their quantity
    logger.info("Program started with next options: {opt}".format(
        opt=arg_parser.parse_args()))
    if create_dir:
        logger.info("Create output directory '{dir_name}'.".format(
            dir_name=cfg.OUT_DIR))
    if create_log_file:
        logger.info("Create log-file '{log_file}'.".format(
            log_file=cfg.LOG_FILE))

    parser = Parser(cat_name, clear_storage=clear_storage)
    data = parser.get_records()
    count = 0
    for i in data.values():
        count += len(i)
    logger.info("TOTAL get {} records.".format(count))
    exporter = HTML_Export()
    if count == 0:
        msg = templates.err_msg
        fname = exporter.export(msg, raw=True)
    else:
        fname = exporter.export(data)
    logger.info("Output file '{}' generated".format(fname))
    logger.info("Program finished.")

if __name__ == '__main__':
    main()
