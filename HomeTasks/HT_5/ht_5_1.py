import argparse
import csv
from datetime import datetime as dt
import json
import logging
import os
import time
import urllib.request
from urllib.error import URLError, HTTPError

import config as cfg


def finish(logger=None, err_code=0, err_msg=None):
    """Helper for program terminate"""
    if err_msg and logger:
        logger.error(err_msg)
    if err_msg:
        print(err_msg)
    if logger:
        logger.info("Program finished with error-code {err_code}".format(
            err_code=err_code))
    print("Program finished with error-code {err_code}".format(
        err_code=err_code))

    exit(err_code)


def req_wrapper(url, logger=None, log_msg=None):
    """Wrap request in try...except with necessary logging"""
    data = None
    try:
        if logger:
            logger.info(log_msg)
        response = urllib.request.urlopen(url, timeout=5)
    except HTTPError as e:
        finish(logger, 1, "The server couldn't fulfill the request. \
Error code: {err_code}".format(err_code=e.code))
    except URLError as e:
        finish(logger, 2,
               "We failed to reach a server. Reason: {reason}".format(
                   reason=e.reason))
    else:
        data = json.loads(response.read().decode("utf-8"))
        if logger:
            logger.info("Get responce from url='{url}'".format(url=url))
        response.close()
    return data


def get_item(item_id, logger=None):
    url = cfg.url_item.replace("{{placeholder}}", str(item_id))

    return req_wrapper(url, logger, "Send request for Get item #'{id}' with \
url='{url}'".format(id=item_id, url=url))


def main():
    # get command-line args
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c", "--category", type=str,
                            default=cfg.default_category,
                            choices=cfg.categories, help="name of category")
    cat_name = arg_parser.parse_args().category

    create_dir = False
    create_log_file = False

    # Check for existing directory and log-file
    if not os.path.isdir(cfg.out_dir):
        os.mkdir(cfg.out_dir)
        create_dir = True

    if not os.path.isfile(cfg.out_dir + os.sep + cfg.log_file):
        create_log_file = True

    # init logging
    logger = logging.getLogger(cfg.app_name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(cfg.out_dir + os.sep + cfg.log_file)
    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    # logging all options for the possibility of changing their quantity
    logger.info("Program started with next options: {opt}".format(
        opt=arg_parser.parse_args()))
    if create_dir:
        logger.info("Create output directory '{dir_name}'.".format(
            dir_name=cfg.out_dir))
    if create_log_file:
        logger.info("Create log-file '{log_file}'.".format(
            log_file=cfg.out_dir + os.sep + cfg.log_file))

    # get list of item's numbers in selected category
    url = cfg.url_category.replace("{{placeholder}}", cat_name)
    log_msg = "Send request for Get '{0}' category with url='{1}'".format(
        cat_name, url)
    t0 = time.time()
    data = req_wrapper(url, logger, log_msg)
    t1 = time.time()
    logger.info("Received {count} items by request for get '{cat_name}' \
category with url='{url}' by {time} ms".format(count=len(data),
                                               cat_name=cat_name, url=url,
                                               time=t1 - t0))
    print("From category {0} received {1} items by {2} sec.".format(cat_name,
                                                                    len(data),
                                                                    t1 - t0))

    # Check for items in data
    if not len(data):
        finish(logger, 3,
               "There is no items receive from '{cat_name}' category!".format(
                   cat_name=cat_name))
    csv_file = cfg.out_dir + os.sep + cfg.out_file

    t0 = time.time()
    with open(csv_file, "w", newline="", encoding="utf-8") as result:
        from_dt = dt.strptime(cfg.from_date, "%Y-%m-%d").timestamp()
        writer = csv.writer(result)
        title_writed = False
        count = 0
        count_all = len(data)
        percent_prev = (count / count_all)
        out = []
        print("Processed: 0%", end="")
        for item_id in data:
            item = get_item(item_id, logger)
            # check percents of processed records
            count += 1
            percent_cur = (count / count_all) * 100
            if percent_cur - percent_prev >= 1:
                print("\rProcessed: {:4.4}%   ".format(percent_cur), end="")
                percent_prev = percent_cur
            # write title line in csv-file
            if not title_writed:
                writer.writerow(list(item.keys()))
                title_writed = True
            # apply filters
            if item.get("score") >= cfg.score and item.get("time") >= from_dt:
                out.append(list(item.values()))
        print()
        writer.writerows(out)
    t1 = time.time()
    print("Write output file {0} by {1} sec.".format(csv_file, t1 - t0))
    logger.info("Write output file {0} by {1} sec.".format(csv_file, t1 - t0))

    # End of program
    finish(logger)


if __name__ == '__main__':
    main()