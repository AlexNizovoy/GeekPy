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
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create console handler
ch = logging.StreamHandler()
ch.setFormatter(fmt)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


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

    def _init_db(self):
        try:
            conn = psycopg2.connect(database=cfg.DB_NAME, user=cfg.DB_USER,
                                    password=cfg.DB_PASS, host=cfg.DB_HOST,
                                    port=cfg.DB_HOST_PORT)
            curs = conn.cursor()
        except:
            # Error connect to DB. Try connect to default DB and create user-DB
            try:
                msg = "Error connect to DB '{}'. \
Try connect to default DB and create user-DB".format(cfg.DB_NAME)
                print(msg)
                logger.error(msg)
                conn = psycopg2.connect(database="postgres", user=cfg.DB_USER,
                                        password=cfg.DB_PASS, host=cfg.DB_HOST,
                                        port=cfg.DB_HOST_PORT)
                conn.autocommit = True
                curs = conn.cursor()
                curs.execute("CREATE DATABASE {}".format(cfg.DB_NAME))
                curs.close()
                conn.close()
                # Reconnect to new DB
                conn = psycopg2.connect(database=cfg.DB_NAME, user=cfg.DB_USER,
                                        password=cfg.DB_PASS, host=cfg.DB_HOST,
                                        port=cfg.DB_HOST_PORT)
                curs = conn.cursor()
                logger.info("DB '{}'' create".format(cfg.DB_NAME))
            except:
                logger.error("Unable connect to DB. Check for settings!")
                print("Unable connect to DB. Check for settings!")
                return None, None

        return conn, curs

    def __init__(self, category):
        if category.lower() == "all":
            self.categories = cfg.CATEGORIES
        elif category.lower() in cfg.CATEGORIES:
            self.categories.append(category)
        else:
            logger.error("{} is not valid category!".format(category))
            self.categories = []

        self._conn, self._curs = self._init_db()
        if self._conn is None or self._curs is None:
            return None

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

    def _db_writer(self, tablename, data, title=None):
        """Check for 'tablename' table in DB, create it (need for 'title' list)
        and write 'data' list in one row of table

        Format of 'title':
        [("name1", "type1"), ("name2", "type2") ...]
        [("id", "INTEGER"), ("time", "INTEGER")]
        """
        # Check for table in DB
        try:
            self._curs.execute("""SELECT * FROM {}""".format(tablename))
        except Exception:
            # Reset connection for clear transaction with error
            self._conn.reset()
            # Generate columns names and types
            if title is None:
                logger.error("Need for title for create table \
'{}'!".format(tablename))
                logger.error("Program terminated!")
                exit(1)
            title_str = ""
            for i in title:
                title_str += i[0] + " " + i[1] + ", "
            title_str = title_str[:-2]

            self._curs.execute("""CREATE TABLE {} ({})""".format(tablename,
                                                                 title_str))
            self._conn.commit()

        # Check for existing record
        query = """SELECT * FROM {tn} WHERE id = {id}"""
        query = query.format(tn=tablename, id=data.get("id"))
        self._curs.execute(query)
        record = self._curs.fetchone()
        if record is None:
            record_exist = False
        else:
            record_exist = True

        # Check for new columns in record. If have one - add them to table
        query = """SELECT column_name FROM information_schema.columns
                   WHERE table_name='{}'""".format(tablename)
        self._curs.execute(query)
        columns = self._curs.fetchall()
        columns = [i[0] for i in columns]
        query = """ALTER TABLE {} ADD COLUMN {} text"""
        for col_name in data.keys():
            if col_name not in columns:
                self._curs.execute(query.format(tablename, col_name))
                self._conn.commit()

        # TODO: add escaping writed value
        if record_exist:
            # Update record
            query = """UPDATE {tn}
                       SET {set_str}
                       WHERE id = {id};"""
            set_str = ""
            for key, value in data.items():
                set_str += """ "{}"='{}', """
                set_str = set_str.format(key, str(value).replace("'", "''"))
            set_str = set_str[:-2]
            query = query.format(tn=tablename, set_str=set_str,
                                 id=data.get("id"))
        else:
            # Insert new record
            query = """INSERT INTO {tn}({keys})
                       VALUES ({values});"""
            keys, values = "", ""
            for key, value in data.items():
                keys += """ "{}", """.format(key)
                values += """ '{}', """.format(str(value).replace("'", "''"))
            keys = keys[:-2]
            values = values[:-2]
            query = query.format(tn=tablename, keys=keys, values=values)
        self._curs.execute(query)
        self._conn.commit()

    def _make_title(self, data):
        """Get iterable 'data' with name of fields and return list with
        elements ['id', 'type', 'score', 'time', 'by', 'title', 'text', 'url',
        and rest]. If some of listed elements not present in 'data' - they
        skipped.
        """
        result = []
        fields = [("id", "integer"), ("type", "varchar(10)"),
                  ("score", "integer"), ("time", "integer"), ("by", "text"),
                  ("title", "text"), ("text", "text"), ("url", "text")]
        for i in [i[0] for i in fields]:
            if i in data:
                for tmp in fields:
                    if tmp[0] == i:
                        result.append(tmp)
        return result

    @property
    def count(self):
        """Return count of records"""
        count = 0

        # Get all names of tables
        query = """SELECT table_name
                   FROM information_schema.tables
                   WHERE table_schema = 'public'"""
        self._curs.execute(query)
        tables = self._curs.fetchall()
        tables = [i[0] for i in tables]
        for tablename in tables:
            query = """SELECT COUNT(*) FROM {}""".format(tablename)
            self._curs.execute(query)
            count += self._curs.fetchone()[0]

        return count

    def get_records(self):
        """Return records in format like:
        [
            {
                "name": "jobstories",
                "title": ["list", "of", "column", "names"],
                "data": [
                    ["values", "in", "record"],
                    ...
                    [ ... ]
                ]
            },
            {
                ...
            }
        ]
        """
        result = []
        # Get all names of tables
        query = """SELECT table_name
                   FROM information_schema.tables
                   WHERE table_schema = 'public'"""
        self._curs.execute(query)
        tables = self._curs.fetchall()
        tables = [i[0] for i in tables]
        for tablename in tables:
            # Get column names of table
            query = """SELECT column_name FROM information_schema.columns
                       WHERE table_name='{}'""".format(tablename)
            self._curs.execute(query)
            columns = self._curs.fetchall()
            columns = [i[0] for i in columns]
            query = """SELECT * FROM {}""".format(tablename)
            self._curs.execute(query)
            data = self._curs.fetchall()
            result.append({
                "name": tablename,
                "title": columns,
                "data": data
                })

        return result

    def renew_records(self):
        from_dt = datetime.strptime(cfg.from_date, "%Y-%m-%d").timestamp()
        for cat in self.categories:
            count = 0
            cat_records = self.get_category(cat)
            title = []

            for record in cat_records:
                rec_data = self.get_item(record)
                # Check for title.
                if not len(title):
                    title = self._make_title(rec_data.keys())
                if rec_data.get("score") < cfg.score or \
                   rec_data.get("time") < from_dt:
                    continue
                text = rec_data.get("text")
                if text and len(cfg.tag):
                    rec_data["text"] = remove_tag(text)

                self._db_writer(tablename=cat, data=rec_data, title=title)
                count += 1

                if count % 10 == 0:
                    print("In category '{}' get {} records from {}". format(
                        cat, count, len(cat_records)))
            msg = "In category '{}' get {} records"
            msg = msg.format(cat, count)
            logger.info(msg)
            print(msg)

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

    def export(self, data, raw=False):
        """If 'raw == True' write 'data' to output file without
        """
        output = templates.base
        style = templates.style
        script = templates.script
        if not raw:
            result = []
            for category in data:
                # generate title from existing keys of all items in category
                title = category.get("title")
                name = category.get("name")
                cat_html = templates.category
                thead = self.item(title=title)
                data_html = []
                for record in category.get("data"):
                    data_html.append(self.item(record, title))
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

    def item(self, data=None, title=None):
        """Get 'data' like ["val1", "val2"] and
        'title' like ["name1", "name2"]
        return HTML-text like
        <tr>
            <td>val1</td>
            <td>val2</td>
        </tr>
        """
        # TODO: Поправить метод
        if data is None and title is None:
            return "\n"
        result = ["<tr>"]
        if data is None:
            for i in title:
                result.append("<th>{}</th>".format(i.upper()))
        else:
            for key, val in zip(title, data):
                if key == "time":
                    unix_time = val
                    str_unix_time = str(datetime.fromtimestamp(unix_time))
                    result.append("<td>{}</td>".format(str_unix_time))
                else:
                    result.append("<td>{}</td>".format(val))
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

    arg_parser.add_argument("-exp_only", action="store_true",
                            help="use it for export to HTML only (no get new)")
    cat_name = arg_parser.parse_args().category
    exp_only = arg_parser.parse_args().exp_only

    # TODO: Добавить возможность бэкапа базы

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
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # logging all options for the possibility of changing their quantity
    logger.info("Program started with next options: {opt}".format(
        opt=arg_parser.parse_args()))
    if create_dir:
        logger.info("Create output directory '{dir_name}'.".format(
            dir_name=cfg.OUT_DIR))
    if create_log_file:
        logger.info("Create log-file '{log_file}'.".format(
            log_file=cfg.LOG_FILE))

    parser = Parser(cat_name)
    if parser is None:
        logger.error("Error of creating parser. Program terminated!")
        exit(1)

    # Check for export to HTML only, without renew data from server
    if not exp_only:
        parser.renew_records()

    data = parser.get_records()
    count = parser.count

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
